import { AUTHORITY_LABELS } from '../lib/data'

export default function ConfidenceBadge({ authority, verification }: { authority: string; verification?: string }) {
  const color = authority === 'A' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    : authority === 'B' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
    : authority === 'C' ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
    : authority === 'E' ? 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200'
    : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300'
  return (
    <span className={`badge ${color}`} title={verification ?? AUTHORITY_LABELS[authority] ?? authority}>
      {authority === 'A' ? '✅' : authority === 'E' ? '⚠️' : '🎓'} {AUTHORITY_LABELS[authority]?.slice(0, 1)} {AUTHORITY_LABELS[authority]?.split('—')[1]?.trim() ?? ''}
    </span>
  )
}
