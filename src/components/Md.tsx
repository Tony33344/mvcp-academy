import ReactMarkdown from 'react-markdown'

export default function Md({ children }: { children: string }) {
  return <div className="prose-mvcp text-sm"><ReactMarkdown>{children}</ReactMarkdown></div>
}
