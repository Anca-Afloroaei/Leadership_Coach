import inspect  # for signature inspection - see generate_development_plan_from_ai - LOOK INTO IT!!
import json
import logging
import re
from html import escape as html_escape
from typing import Any, Callable, Optional, Tuple
from urllib import request as urlrequest
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from fastapi import HTTPException, status
from openai import OpenAI
from pydantic import AnyUrl, BaseModel
from sqlmodel import Session, select

from config import settings

# from sqlalchemy.exc import IntegrityError
from entities.development_plans import DevelopmentPlan
from entities.questionnaires import Questionnaire
from entities.user_answers import UserAnswer
from entities.users import User
from features.results.service import get_user_results_by_record_id

from .models import (
    DevelopmentPlanCreate,
    DevelopmentPlanRead,
    DevelopmentPlanSummaryRead,
    GeneratedPlanPayload,
    GeneratePlanRequest,
    GeneratePlanResponse,
)

try:
    from markdown import markdown as _md_render
except ImportError:  # pragma: no cover - optional dependency
    _md_render = None  # type: ignore[assignment]

try:
    from weasyprint import HTML as _weasy_html
except ImportError:  # pragma: no cover - optional dependency
    _weasy_html = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

# def create_assessment(assessment: DevelopmentPlanCreate, session: Session, current_user: User) -> DevelopmentPlanRead:
def create_development_plan(development_plan: DevelopmentPlanCreate, session: Session) -> DevelopmentPlanRead:
    """
    Create a new Development Plan in the database.
    """
    new_development_plan = DevelopmentPlan(
        user_id=development_plan.user_id,
        user_answers_record_id=development_plan.user_answers_record_id,
        goal=development_plan.goal,
        description=development_plan.description,
        start_date=development_plan.start_date,
        end_date=development_plan.end_date,
        status=development_plan.status,
        progress=development_plan.progress,
        resources=development_plan.resources,
        challenges=development_plan.challenges,
        next_steps=development_plan.next_steps,
        action_items=development_plan.action_items,
        target_date=development_plan.target_date,
        plan_markdown=development_plan.plan_markdown,
    )
    session.add(new_development_plan)
    session.commit()
    session.refresh(new_development_plan)
    logger.info(f"Develpment Plan: {new_development_plan.id}")
    # return new_development_plan
    return DevelopmentPlanRead.model_validate(new_development_plan)


def get_development_plan_by_id(development_plan_id: str, session: Session) -> DevelopmentPlanRead:
    """
    Retrieve a Development Plan by its ID.
    """
    statement = select(DevelopmentPlan).where(DevelopmentPlan.id == development_plan_id)
    development_plan = session.exec(statement).first()
    if not development_plan:
        logger.error(f"Development Plan with ID {development_plan_id} not found")
        raise HTTPException(status_code=404, detail="Development Plan not found")
    logger.info(f"Development Plan retrieved: {development_plan.id}")
    return DevelopmentPlanRead.model_validate(development_plan)  # Assuming DevelopmentPlanRead has a model_validate method to convert the model 


def delete_development_plan(development_plan_id: str, session: Session) -> None:
    """
    Delete a Development Plan by its ID.
    """
    statement = select(DevelopmentPlan).where(DevelopmentPlan.id == development_plan_id)
    development_plan = session.exec(statement).first()
    if not development_plan:
        logger.error(f"Development Plan with ID {development_plan_id} not found")
        raise HTTPException(status_code=404, detail="Development Plan not found")
    session.delete(development_plan)
    session.commit()
    logger.info(f"Development Plan with ID {development_plan_id} deleted successfully")
    return None


def _format_list(items: list[str]) -> str:
    if not items:
        return ""
    return "\n".join(f"- {it}" for it in items)


def generate_development_plan_from_ai(
    payload: GeneratePlanRequest,
    current_user: User,
    session: Session,
) -> GeneratePlanResponse:
    """
    Generate a development plan using OpenAI, persist a DevelopmentPlan record, and
    return the saved plan together with a nicely formatted markdown version.

    Falls back gracefully with 503 if the OpenAI SDK is missing or the API key is not configured.
    """
    # Authorization: must be the same user
    if payload.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")

    # Get results for context (competency -> percentage)
    results = get_user_results_by_record_id(
        payload.user_answers_record_id, current_user, session
    )

    # Prepare AI call
    if not settings.OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY not configured")
    try:
        # Import lazily to avoid hard dependency at startup
        from openai import OpenAI
    except Exception:
        raise HTTPException(status_code=503, detail="OpenAI SDK not installed. Please install 'openai'.")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Build structured system/user prompt
    system_prompt = (
        "You are a Top Leadership Development Expert and coach. Create a practical, time-bound "
        "leadership development plan that is specific, measurable, and aligned to the user's "
        "focus areas, role, industry, and experience level. Include a concrete timeline with "
        "measurable milestones and concrete, actionable steps they need to take. Create several "
        "progressive modules. \n"
        "Invoke web search to find authoritative resources (books, courses, articles, videos, podcasts, tools). "
        "Only include high-quality, relevant resources from reputable sources. **DO NOT HALLUCINATE**"
        # "Provide numerous resources they can access and learn from. "
        "Respond ONLY with valid JSON matching the schema. For the plan_markdown, format a readable "
        "plan with clear sections and bullet lists.\n\n"
        "RESOURCES REQUIREMENTS (plan_markdown):\n"
        "- Include a 'Resources' section as a bulleted list.\n"
        "- Use this exact pattern per item: '- {Type}: [Title](https://url) — one sentence on what it is and why it's relevant'.\n"
        "- {Type} must be one of: Book, Course, Workshop, Webinar, Article, Podcast, Video, Toolkit.\n"
        "- The link must be to an authoritative/official source (publisher, creator, provider). Avoid homepages and SEO blogs.\n"
        "- HTTPS only; avoid link shorteners and tracking parameters. Use canonical URLs.\n"
        "- The URL must be a deep link to the specific resource (path length >= 1), not just the site root.\n"
        "- Do NOT output search engine links or aggregators (e.g., google.com, bing.com, duckduckgo.com, yahoo.com).\n"
        "- The link must be the canonical page hosted by the original publisher/creator/provider; if unavailable, prefer well-known distributors (e.g., amazon.com for books, coursera.org/edx.org for courses, youtube.com/ted.com for videos) — never a search results page.\n"
        "- If a credible url cannot be found, output the item without a link: '- {Type}: Title — description'.\n"
        "- Do NOT add an extra '-' inside the link text (no '[- Title]').\n"
        "- Provide at most 6 high-quality resources.\n"
        "- Do NOT add any follow-up questions or sugestions after the JSON output. Refrain from any additional commentary whatsoever.\n"
        "- At the end of the plan, add a motivaing closing statement to encourage the user to follow through on their development plan. Make it concise and impactful.\n"
    )

    user_context = {
        "role": payload.role,
        "industry": payload.industry,
        "years_experience": payload.years_experience,
        "duration_days": payload.duration_days,
        "focus_areas": payload.focus_areas,
        "baseline_results": results.results,
    }

    # We ask the model for structured fields + a plan_markdown for display
    json_schema_hint = {
        "type": "object",
        "properties": {
            "goal": {"type": "string"},
            "description": {"type": "string"},
            "action_items": {"type": "array", "items": {"type": "string"}},
            "next_steps": {"type": "array", "items": {"type": "string"}},
            "resources": {"type": "array", "items": {"type": "string"}},
            "challenges": {"type": "array", "items": {"type": "string"}},
            "milestones": {"type": "array", "items": {"type": "object"}},
            "plan_markdown": {"type": "string"},
        },
        "required": [
            "goal",
            "description",
            "action_items",
            "next_steps",
            "resources",
            "challenges",
            "milestones",
            "plan_markdown",
        ],
    }

    # Prefer Responses API with typed parsing; fall back to Chat Completions if unavailable
    
    input=(
            "Generate a leadership development plan using the provided context.\n"
            "Context (JSON):\n" + json.dumps(user_context)
        )
    

    # Responses API with typed parsing; FOR GPT-5 MINI
    response = client.responses.parse(
        model="gpt-5-mini",
        input=[{"role": "system", "content": system_prompt}, {"role": "user", "content": input}],
        text_format=GeneratedPlanPayload,
        # temperature=0.0,
        tools=[{"type": "web_search"}],
        # tool_choice="auto"
        max_output_tokens=50000,
        reasoning={"effort": "low"}
    )
    generated = response.output_parsed  # type: ignore[attr-defined]

    # ------------------------------------------------------------------------------
    # ALTERNATIVE: Use GPT-4o Mini with typed parsing if available, else fallback to
    # Chat Completions with manual JSON parsing. This is more complex but works
    # around SDK versions and model availability.
    # ------------------------------------------------------------------------------

    # try:     # Use Responses API with typed parsing if available
    #     # Inspect signature to determine if text_format or response_format is supported
    #     # (added in openai-python v0.27.0 and v0.28.0 respectively)
    #     parse_params = inspect.signature(client.responses.parse).parameters
    #     if "text_format" in parse_params:
    #         response = client.responses.parse(text_format=GeneratedPlanPayload, **common_args)
    #         generated = response.output_parsed  # type: ignore[attr-defined]
    #     elif "response_format" in parse_params:
    #         response = client.responses.parse(response_format=GeneratedPlanPayload, **common_args)
    #         generated = response.output_parsed  # type: ignore[attr-defined]
    #     else:
    #         raise RuntimeError("OpenAI client does not support typed parsing")
    # except Exception as err:  # noqa: BLE001 - we want to capture the concrete error for diagnostics
    #     primary_err = err
    #     generated = None
    # if generated is None:
    #     # Fallback to Chat Completions with manual JSON parsing
    #     try:
    #         completion = client.chat.completions.create(


    # FOR GPT-4o MINI

    # common_args = dict(
    #     model="gpt-4o-mini",
    #     input=[{"role": "system", "content": system_prompt}, {"role": "user", "content": input}],
    #     temperature=0.0,
    #     tools=[{"type": "web_search"}],
    # )

    # generated: Optional[GeneratedPlanPayload] = None
    # primary_err: Optional[Exception] = None

    # ------------------------------------------------------------------------------
    # NOTE: The below logic is somewhat complex to handle various SDK versions and

    # try:
    #     parse_params = inspect.signature(client.responses.parse).parameters
    #     if "text_format" in parse_params:
    #         response = client.responses.parse(text_format=GeneratedPlanPayload, **common_args)
    #         generated = response.output_parsed  # type: ignore[attr-defined]
    #     elif "response_format" in parse_params:
    #         response = client.responses.parse(response_format=GeneratedPlanPayload, **common_args)
    #         generated = response.output_parsed  # type: ignore[attr-defined]
    #     else:
    #         primary_err = RuntimeError("OpenAI client does not support typed parsing")
    # except Exception as err:  # noqa: BLE001 - we want to capture the concrete error for diagnostics
    #     primary_err = err

    # if generated is None:
    #     try:
    #         completion = client.chat.completions.create(
    #             model="gpt-4o-mini",
    #             messages=[
    #                 {"role": "system", "content": system_prompt},
    #                 {
    #                     "role": "user",
    #                     "content": (
    #                         "Generate a leadership development plan as strict JSON matching this schema: "
    #                         f"{json.dumps(json_schema_hint)}\n\n"
    #                         "Context (JSON):\n" + json.dumps(user_context) + "\n\n"
    #                         "In plan_markdown, include a 'Resources' section. For each resource, follow this pattern exactly: "
    #                         "'- {Type}: [Title](https://url) — one sentence description'. Use authoritative links only; if none found, output without a link. "
    #                         "Do not include an extra '-' inside the link text. Provide at most 6 items. HTTPS only; avoid shorteners and tracking params; "
    #                         "link to the specific resource, not the site root. Do NOT output search engine links (google/bing/duckduckgo/yahoo) or generic directory pages; "
    #                         "use the canonical page by the original publisher/creator/provider, or a well-known distributor. If a suitable direct URL cannot be found, output the item without a link."
    #                     ),
    #                 },
    #             ],
    #             temperature=0.0,
    #             response_format={"type": "json_object"},
    #         )
    #         text = completion.choices[0].message.content or "{}"
    #         data = json.loads(text)
    #         generated = GeneratedPlanPayload.model_validate(data)
    #     except Exception as fallback_err:
    #         raise HTTPException(
    #             status_code=502,
    #             detail=f"Model parsing failed: {primary_err} | Fallback: {fallback_err}",
    #         ) from fallback_err
        
    # ------------------------------------------------------------------------------



    # Map to DevelopmentPlan fields
    from datetime import datetime, timedelta, timezone
    start_date = datetime.now(timezone.utc)
    end_date = start_date + timedelta(days=payload.duration_days)

    dp_create = DevelopmentPlanCreate(
        user_id=current_user.id,
        user_answers_record_id=payload.user_answers_record_id,
        goal=generated.goal,
        description=generated.description,
        start_date=start_date,
        end_date=end_date,
        status="In Progress",
        progress=0,
        resources=_format_list(generated.resources),
        challenges=_format_list(generated.challenges),
        next_steps=_format_list(generated.next_steps),
        action_items=_format_list(generated.action_items),
        target_date=end_date,
        plan_markdown=generated.plan_markdown,
    )

    # Return model-generated markdown as-is to avoid replacing links with search pages
    saved = create_development_plan(dp_create, session)
    # return GeneratePlanResponse(plan=saved, plan_markdown=generated.plan_markdown)
    return GeneratePlanResponse(plan=saved, plan_markdown=saved.plan_markdown)


def get_development_plan_for_user_answers(
    user_answers_record_id: str,
    current_user: User,
    session: Session,
) -> GeneratePlanResponse:
    stmt = (
        select(DevelopmentPlan)
        .where(
            (DevelopmentPlan.user_answers_record_id == user_answers_record_id)
            & (DevelopmentPlan.user_id == current_user.id)
        )
        .order_by(DevelopmentPlan.created_at.desc())
    )
    plan = session.exec(stmt).first()
    if not plan:
        # logger.error(
        #     "Development plan not found for user_answers_record_id %s", user_answers_record_id
        legacy_stmt = (
            select(DevelopmentPlan)
            .where(
                (DevelopmentPlan.user_id == current_user.id)
                & (DevelopmentPlan.user_answers_record_id.is_(None))
            )
            .order_by(DevelopmentPlan.created_at.desc())
        )
        plan = session.exec(legacy_stmt).first()
        if not plan:
            logger.info(
                "Development plan not found for user_answers_record_id %s", user_answers_record_id
            )
            raise HTTPException(status_code=404, detail="Development Plan not found")
    plan_read = DevelopmentPlanRead.model_validate(plan)
    return GeneratePlanResponse(plan=plan_read, plan_markdown=plan.plan_markdown)


def _require_pdf_dependencies() -> Tuple[Callable[[str], str], Callable[..., Any]]:
    missing: list[str] = []
    if _md_render is None:
        missing.append("'markdown'")
    if _weasy_html is None:
        missing.append("'weasyprint'")
    if missing:
        detail = (
            "PDF generation is not available. Please install "
            + " and ".join(missing)
            + " packages and any system dependencies."
        )
        raise HTTPException(status_code=503, detail=detail)
    return _md_render, _weasy_html


def _format_iso_date(value: Optional[str]) -> str:
    if not value:
        return "—"
    try:
        dt = value
        from datetime import datetime

        parsed = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        return parsed.strftime("%B %d, %Y")
    except Exception:
        return "—"


def _build_plan_pdf_html(
    plan: DevelopmentPlanRead,
    plan_markdown: str,
    user_display_name: Optional[str] = None,
) -> str:
    markdown_renderer, _ = _require_pdf_dependencies()
    markdown_html = markdown_renderer(plan_markdown or "")
    metadata_rows = []
    metadata = [
        ("Goal", plan.goal or "—"),
        ("Status", plan.status or "—"),
        ("Target Date", plan.target_date.isoformat() if plan.target_date else None),
        # ("Progress", f"{plan.progress}%" if plan.progress is not None else "—"),
    ]
    for label, value in metadata:
        display = _format_iso_date(value) if label == "Target Date" else (value or "—")
        metadata_rows.append(
            f"<tr><th>{html_escape(label)}</th><td>{html_escape(str(display))}</td></tr>"
        )

    display_name = user_display_name or f"user ID: {plan.user_id}"

    return f"""
    <!DOCTYPE html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\" />
        <style>
          @page {{
            size: A4;
            margin: 24px;
            @bottom-right {{
              content: "Page " counter(page) " of " counter(pages);
              font-size: 12px;
              color: #555;
            }}
          }}
          body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 24px; color: #111; }}
          h1 {{ margin-bottom: 8px; }}
          h2 {{ margin-top: 32px; margin-bottom: 12px; }}
          table {{ border-collapse: collapse; margin-top: 16px; width: 100%; }}
          th {{ text-align: left; font-weight: 600; padding: 8px 12px; width: 160px; background: #f5f5f5; }}
          td {{ padding: 8px 12px; border-bottom: 1px solid #e0e0e0; }}
          .markdown-body {{ margin-top: 32px; line-height: 1.6; }}
          .markdown-body ul {{ padding-left: 20px; }}
          .markdown-body a {{ color: #0d47a1; text-decoration: none; }}
          .markdown-body a:hover {{ text-decoration: underline; }}
        </style>
      </head>
      <body>
        <header>
          <h1>Leadership Development Plan</h1>
          <div>Generated for {html_escape(display_name)}</div>
          <table>{''.join(metadata_rows)}</table>
        </header>
        <section class=\"markdown-body\">{markdown_html}</section>
      </body>
    </html>
    """


def get_development_plan_pdf_for_user_answers(
    user_answers_record_id: str,
    current_user: User,
    session: Session,
) -> Tuple[bytes, str]:
    _, weasy_html = _require_pdf_dependencies()
    response = get_development_plan_for_user_answers(user_answers_record_id, current_user, session)
    plan = response.plan
    plan_markdown = response.plan_markdown or plan.plan_markdown or ""

    user_display_name = " ".join(
        part for part in [current_user.first_name, current_user.last_name] if part
    ).strip()

    html = _build_plan_pdf_html(plan, plan_markdown, user_display_name)
    pdf_bytes = weasy_html(string=html).write_pdf()
    filename = f"development-plan-{plan.id}.pdf"

    return pdf_bytes, filename


def list_development_plans_for_user(
    current_user: User,
    session: Session,
) -> list[DevelopmentPlanSummaryRead]:
    stmt = (
        select(DevelopmentPlan, UserAnswer, Questionnaire)
        .join(UserAnswer, UserAnswer.id == DevelopmentPlan.user_answers_record_id)
        .join(Questionnaire, Questionnaire.id == UserAnswer.questionnaire_id)
        .where(DevelopmentPlan.user_id == current_user.id)
        .order_by(DevelopmentPlan.created_at.desc())
    )
    rows = session.exec(stmt).all()

    summaries: list[DevelopmentPlanSummaryRead] = []
    for plan, ua, questionnaire in rows:
        if not plan.user_answers_record_id:
            continue
        title = getattr(questionnaire, "title", "") or questionnaire.id
        summaries.append(
            DevelopmentPlanSummaryRead(
                plan_id=plan.id,
                user_answers_record_id=plan.user_answers_record_id,
                questionnaire_id=ua.questionnaire_id,
                questionnaire_title=title,
                created_at=plan.created_at,
            )
        )
    return summaries


def _verify_url(url: str, timeout: float = 5.0) -> tuple[bool, Optional[str]]:
    """Return (is_valid, final_url). Consider valid for 2xx/3xx HTTP responses.
    Be non-destructive: failures upstream should not cause us to strip links.
    """
    try:
        req = urlrequest.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible)"})
        with urlrequest.urlopen(req, timeout=timeout) as resp:
            code = getattr(resp, 'status', None) or getattr(resp, 'code', None) or 0
            final_url = getattr(resp, 'geturl', lambda: url)()
            if 200 <= int(code) < 400:
                return True, final_url
            return False, final_url
    except Exception:
        return False, None

DENY_DOMAINS = {
    "bit.ly", "t.co", "goo.gl", "tinyurl.com", "ow.ly", "t.ly", "shorturl.at", "rb.gy",
}

TRACKING_PARAMS_PREFIXES = ("utm_", "gclid", "fbclid", "mc_cid", "mc_eid")

def _sanitize_url(url: str) -> Optional[str]:
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https"):
            return None
        scheme = "https"
        netloc = p.netloc.lower()
        if any(netloc.endswith(d) for d in DENY_DOMAINS):
            return None
        # strip tracking params
        q = [(k, v) for (k, v) in parse_qsl(p.query, keep_blank_values=True) if not any(k.lower().startswith(pref) for pref in TRACKING_PARAMS_PREFIXES)]
        query = urlencode(q)
        return urlunparse((scheme, netloc, p.path or "/", p.params, query, p.fragment))
    except Exception:
        return None

def _build_search_url(title: str, rtype: str) -> str:
    # Use DuckDuckGo with type keyword and "official" bias
    q = f"{title.strip()} {rtype.strip()} official"
    return f"https://duckduckgo.com/?{urlencode({'q': q})}"


class _SingleUrl(BaseModel):
    url: AnyUrl


def _find_authoritative_url(title: str, rtype: str) -> Optional[str]:
    """Ask the model (with WebSearch) for one authoritative URL for the given resource.
    Returns a single URL string or None.
    """
    client = OpenAI()
    try:
        resp = client.responses.parse(
            model="gpt-4o-mini",
            instructions=(
                "You are assisting with link validation. Find ONE authoritative, working URL (HTTP 200) "
                "for the given resource (type and title), preferably the official source. Return JSON {\"url\": \"...\"}."
            ),
            input=json.dumps({"title": title, "type": rtype}),
            response_format=_SingleUrl,
            temperature=0.0,
            tools=[{"type": "web_search"}],
            tool_choice="auto",
        )
        return str(resp.output_parsed.url)
    except Exception:
        return None


_RES_LINE_RE = re.compile(
    r"^\-\s*(?P<type>Book|Course|Workshop|Webinar|Article|Podcast|Video|Toolkit)\s*:\s*"
    r"(?:(?P<link>\[(?P<title>[^\]]+)\]\((?P<url>https?://[^)]+)\))|(?P<title_nolink>[^—\n]+))\s*—\s*(?P<desc>.+)$"
)


def _repair_resources_in_markdown(md: str) -> str:
    """Walk through markdown lines and for recognized resource bullets ensure links are valid.
    - If a link exists and is invalid, attempt to replace with an authoritative link via WebSearch.
    - If no link exists, attempt to find one. Keep the display format unchanged otherwise.
    """
    lines = md.splitlines()
    fixed: list[str] = []
    # Limit processing to avoid long latency
    processed = 0
    max_to_check = 10
    for line in lines:
        stripped = line.strip()
        m = _RES_LINE_RE.match(stripped)
        if not m or processed >= max_to_check:
            fixed.append(line)
            continue
        processed += 1
        rtype = m.group('type') or ''
        title = (m.group('title') or m.group('title_nolink') or '').strip()
        desc = (m.group('desc') or '').strip()
        url = (m.group('url') or '').strip() or None

        # Default to building a safe link or a search link
        if url:
            sanitized = _sanitize_url(url)
            if sanitized is None:
                search = _build_search_url(title, rtype)
                fixed.append(f"- {rtype}: [{title}]({search}) — {desc}")
            else:
                ok, final = _verify_url(sanitized)
                # Treat homepage (root path) as insufficiently specific
                p = urlparse(final or sanitized)
                is_root = (p.path or "/") in ("", "/")
                if not ok or is_root:
                    search = _build_search_url(title, rtype)
                    fixed.append(f"- {rtype}: [{title}]({search}) — {desc}")
                else:
                    fixed.append(f"- {rtype}: [{title}]({final or sanitized}) — {desc}")
        else:
            search = _build_search_url(title, rtype)
            fixed.append(f"- {rtype}: [{title}]({search}) — {desc}")

    return "\n".join(fixed)
