import { AUTHORITY_LABELS } from '../lib/data'

export default function ConfidenceBadge({ authority, verification }: { authority: string; verification?: string }) {
  const color = authority === 'A' ? 'bg-green-100 text-green-800'
    : authority === 'B' ? 'bg-blue-100 text-blue-800'
    : authority === 'C' ? 'bg-purple-100 text-purple-800'
    : authority === 'E' ? 'bg-amber-100 text-amber-800'
    : 'bg-stone-100 text-stone-800'
  return (
    <span className={`badge ${color}`} title={verification ?? AUTHORITY_LABELS[authority] ?? authority}>
      {authority === 'A' ? '✅' : authority === 'E' ? '⚠️' : '🎓'} {AUTHORITY_LABELS[authority]?.slice(0, 1)} {AUTHORITY_LABELS[authority]?.split('—')[1]?.trim() ?? ''}
    </span>
  )
}
