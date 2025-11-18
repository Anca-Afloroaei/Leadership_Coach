'use client';

import clsx from 'clsx';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { Components } from 'react-markdown';

interface PlanMarkdownProps {
  content: string;
  className?: string;
}

/**
 * Markdown renderer for AI-generated leadership plans.
 * Uses react-markdown to support full markdown syntax including bold, italic, code, etc.
 */
export function PlanMarkdown({ content, className }: PlanMarkdownProps) {
  // Custom component overrides for consistent styling
  const components: Components = {
    // Links: open in new tab with custom styling
    a: ({ href, children }) => (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="underline text-primary hover:opacity-80"
      >
        {children}
      </a>
    ),
    // Headings with custom Tailwind classes
    h1: ({ children }) => (
      <h1 className="text-xl font-bold mt-4">{children}</h1>
    ),
    h2: ({ children }) => (
      <h2 className="text-lg font-semibold mt-3">{children}</h2>
    ),
    h3: ({ children }) => (
      <h3 className="font-semibold mt-2">{children}</h3>
    ),
    h4: ({ children }) => (
      <h4 className="font-semibold text-sm mt-2">{children}</h4>
    ),
    // Lists with spacing
    ul: ({ children }) => (
      <ul className="list-disc pl-5 space-y-1">{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal pl-5 space-y-1">{children}</ol>
    ),
    li: ({ children }) => <li className="text-sm">{children}</li>,
    // Paragraphs
    p: ({ children }) => (
      <p className="text-sm text-foreground">{children}</p>
    ),
    // Code blocks - note: inline prop is passed via node metadata
    code: ({ children, className: codeClassName, ...props }) => {
      // Check if this is inline code by looking at the className or parent context
      const isInline = !codeClassName?.includes('language-');

      if (isInline) {
        return (
          <code className="bg-muted px-1.5 py-0.5 rounded text-xs font-mono">
            {children}
          </code>
        );
      }
      return (
        <code className="block bg-muted p-3 rounded text-xs font-mono overflow-x-auto">
          {children}
        </code>
      );
    },
    // Strong (bold) text
    strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
    // Emphasis (italic) text
    em: ({ children }) => <em className="italic">{children}</em>,
  };

  return (
    <div className={clsx('space-y-1', className)}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={components}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}