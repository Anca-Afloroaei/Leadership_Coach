from fastapi import FastAPI
from features.users.controller import router as users_router
from features.leadership_assessments.controller import router as assessments_router
from features.development_plans.controller import router as development_plans_router
from features.user_module_progress.controller import router as user_module_progress_router
from features.leadership_modules.controller import router as leadership_modules_router
from features.questionnaires.controller import router as questionnaires_router
from features.answers.controller import router as answers_router
from features.questions.controller import router as questions_router
from features.question_and_answers.controller import router as question_and_answers_router
from features.auth.controller import router as auth_router
from features.user_answers.controller import router as user_answers_router


def register_routers(app: FastAPI):
    """
    Register all routers with the FastAPI application.
    This function should be called after creating the FastAPI app instance.
    """
    app.include_router(users_router)
    app.include_router(assessments_router)
    app.include_router(development_plans_router)
    app.include_router(user_module_progress_router)
    app.include_router(leadership_modules_router)
    app.include_router(answers_router)
    app.include_router(questions_router)
    app.include_router(question_and_answers_router)
    app.include_router(questionnaires_router)
    app.include_router(auth_router)
    app.include_router(user_answers_router)