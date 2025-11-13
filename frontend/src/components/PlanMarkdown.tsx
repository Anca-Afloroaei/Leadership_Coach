'use client';

import clsx from 'clsx';
import { useMemo } from 'react';

interface PlanMarkdownProps {
  content: string;
  className?: string;
}

/**
 * Lightweight markdown renderer tailored for the AI-generated leadership plans.
 * Supports headings, paragraphs, lists, and inline links without pulling additional deps.
 */
export function PlanMarkdown({ content, className }: PlanMarkdownProps) {
  const elements = useMemo(() => {
    const parseInline = (text: string): (string | JSX.Element)[] => {
      const parts: (string | JSX.Element)[] = [];
      const linkRe = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g;
      let lastIndex = 0;
      let match: RegExpExecArray | null;
      while ((match = linkRe.exec(text)) !== null) {
        const [full, label, href] = match;
        const start = match.index;
        if (start > lastIndex) {
          parts.push(text.slice(lastIndex, start));
        }
        parts.push(
          <a
            key={`lnk-${lastIndex}`}
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="underline text-primary hover:opacity-80"
          >
            {label}
          </a>
        );
        lastIndex = start + full.length;
      }
      if (lastIndex < text.length) {
        parts.push(text.slice(lastIndex));
      }
      return parts.length ? parts : [text];
    };

    const lines = content.split(/\r?\n/);
    const nodes: JSX.Element[] = [];
    let listBuffer: string[] = [];
    let key = 0;

    const flushList = () => {
      if (!listBuffer.length) return;
      nodes.push(
        <ul key={`ul-${key++}`} className="list-disc pl-5 space-y-1">
          {listBuffer.map((item, idx) => (
            <li key={`li-${key}-${idx}`} className="text-sm">
              {parseInline(item)}
            </li>
          ))}
        </ul>
      );
      listBuffer = [];
    };

    for (const raw of lines) {
      const line = raw.trimEnd();
      if (line.startsWith('# ')) {
        flushList();
        nodes.push(
          <h1 key={`h1-${key++}`} className="text-xl font-bold mt-4">
            {line.slice(2)}
          </h1>
        );
      } else if (line.startsWith('## ')) {
        flushList();
        nodes.push(
          <h2 key={`h2-${key++}`} className="text-lg font-semibold mt-3">
            {line.slice(3)}
          </h2>
        );
      } else if (line.startsWith('### ')) {
        flushList();
        nodes.push(
          <h3 key={`h3-${key++}`} className="font-semibold mt-2">
            {line.slice(4)}
          </h3>
        );
      } else if (/^[-*]\s+/.test(line)) {
        listBuffer.push(line.replace(/^[-*]\s+/, ''));
      } else if (line === '') {
        flushList();
        nodes.push(<div key={`sp-${key++}`} className="h-2" />);
      } else {
        flushList();
        nodes.push(
          <p key={`p-${key++}`} className="text-sm text-foreground">
            {parseInline(line)}
          </p>
        );
      }
    }

    flushList();
    return nodes;
  }, [content]);

  return <div className={clsx('space-y-1', className)}>{elements}</div>;
}
