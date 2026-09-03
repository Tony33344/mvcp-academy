import { useEffect, useMemo, useState } from 'react'
import { flashcards as allCards, topics } from '../lib/data'
import { gradeCard, dueCards, srsStats } from '../lib/srs'
import ConfidenceBadge from '../components/ConfidenceBadge'
import type { Grade } from 'ts-fsrs'

export default function Flashcards() {
  const [topicFilter, setTopicFilter] = useState<string>('all')
  const [queue, setQueue] = useState<string[]>([])
  const [idx, setIdx] = useState(0)
  const [revealed, setRevealed] = useState(false)
  const [sessionDone, setSessionDone] = useState(0)
  const [stats, setStats] = useState({ total: 0, due: 0 })

  const filtered = useMemo(() =>
    topicFilter === 'all' ? allCards : allCards.filter(c => c.topics.includes(topicFilter)), [topicFilter])

  async function loadQueue() {
    const ids = filtered.map(c => c.id)
    const due = await dueCards(ids)
    const shuffled = [...due].sort((a, b) => ((a.charCodeAt(0) * 31 + a.length) % 97) - ((b.charCodeAt(0) * 31 + b.length) % 97))
    setQueue(shuffled.slice(0, 30))
    setIdx(0); setRevealed(false)
    setStats(await srsStats(ids))
  }
  useEffect(() => { loadQueue() }, [topicFilter])

  const card = allCards.find(c => c.id === queue[idx])

  async function grade(g: Grade) {
    if (!card) return
    await gradeCard(card.id, g)
    setSessionDone(s => s + 1)
    setRevealed(false)
    if (idx + 1 >= queue.length) { await loadQueue() } else { setIdx(i => i + 1) }
  }

  if (!card) {
    return (
      <div className="space-y-4 max-w-2xl mx-auto">
        <div className="flex items-center justify-between">
          <h1 className="font-display text-2xl font-semibold">Flashcards</h1>
          <select className="input max-w-[220px] text-xs" value={topicFilter} onChange={e => setTopicFilter(e.target.value)} aria-label="Filter teme">
            <option value="all">Vse teme</option>
            {topics.map(t => <option key={t.id} value={t.id}>{t.n}. {t.title}</option>)}
          </select>
        </div>
        <div className="flashcard text-center py-16 px-6">
          <div className="font-display text-5xl text-stone-200 mb-4">✓</div>
          <p className="font-display text-xl">Vse ponovljeno.</p>
          <p className="text-sm text-stone-600 mt-2">Skupaj {stats.total} kartic · {stats.due} zapadlih · seja: {sessionDone}</p>
          <button onClick={loadQueue} className="btn mt-6">Osveži vrsto</button>
        </div>
      </div>
    )
  }

  const grades: { g: Grade; label: string; cls: string }[] = [
    { g: 1, label: 'Ponovi', cls: 'bg-red-700 hover:bg-red-600' },
    { g: 2, label: 'Težko', cls: 'bg-stone-700 hover:bg-stone-600' },
    { g: 3, label: 'Dobro', cls: 'bg-stone-900 hover:bg-stone-600' },
    { g: 4, label: 'Znam', cls: 'bg-emerald-700 hover:bg-emerald-600' },
  ]

  return (
    <div className="space-y-4 max-w-2xl mx-auto">
      <div className="flex items-center justify-between gap-3">
        <h1 className="font-display text-2xl font-semibold">Flashcards</h1>
        <select className="input max-w-[200px] text-xs" value={topicFilter} onChange={e => setTopicFilter(e.target.value)} aria-label="Filter tem">
          <option value="all">Vse teme</option>
          {topics.map(t => <option key={t.id} value={t.id}>{t.n}. {t.title}</option>)}
        </select>
      </div>
      <div className="flex justify-between text-xs text-stone-600 tracking-wide">
        <span>{idx + 1} / {queue.length}</span>
        <span>SEJA {sessionDone} · ZAPADLIH {stats.due}</span>
      </div>

      <div className="flashcard min-h-[260px] flex flex-col justify-center px-8 py-10">
        <div className="kicker mb-4">{card.kind}{card.topics.length ? ` · ${card.topics.join(' · ')}` : ''}</div>
        <p className="font-display text-xl leading-snug">{card.prompt}</p>
        {revealed ? (
          <div className="mt-6 pt-6 border-t border-stone-100">
            <p className="text-[15px] leading-relaxed text-stone-700">{card.answer}</p>
            <div className="mt-3"><ConfidenceBadge authority={card.authority} verification={card.source} /></div>
          </div>
        ) : (
          <button onClick={() => setRevealed(true)} className="btn mt-8 self-start">Pokaži odgovor</button>
        )}
      </div>

      {revealed && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {grades.map(g => (
            <button key={g.g} onClick={() => grade(g.g)} className={`${g.cls} text-white rounded-xl py-3.5 text-sm font-medium min-h-[48px] transition-colors`}>
              {g.label}
            </button>
          ))}
        </div>
      )}
      <p className="text-[11px] text-stone-600 text-center tracking-wide">1 PONOVI KMALU · 4 ZNAM — FSRS RAZPOREDE NASLEDNJI TERMIN</p>
    </div>
  )
}
