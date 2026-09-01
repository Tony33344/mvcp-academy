import { useEffect, useMemo, useState } from 'react'
import { quiz, topics, quizById } from '../lib/data'
import { db, type QuizAttempt } from '../db/db'
import Md from '../components/Md'
import ConfidenceBadge from '../components/ConfidenceBadge'

export default function Quiz() {
  const [topicFilter, setTopicFilter] = useState('all')
  const [mode, setMode] = useState<'select' | 'open'>('select')
  const [current, setCurrent] = useState<string | null>(null)
  const [answer, setAnswer] = useState('')
  const [confidence, setConfidence] = useState(2)
  const [scored, setScored] = useState<number | null>(null)
  const [revealed, setRevealed] = useState(false)
  const [history, setHistory] = useState<QuizAttempt[]>([])

  const pool = useMemo(() => topicFilter === 'all' ? quiz : quiz.filter(q => q.topics.includes(topicFilter)), [topicFilter])

  useEffect(() => {
    db.quizAttempts.orderBy('at').reverse().limit(20).toArray().then(setHistory)
  }, [scored])

  function start(qid: string) {
    setCurrent(qid); setAnswer(''); setConfidence(2); setScored(null); setRevealed(false); setMode('open')
  }

  async function save(score: number) {
    if (!current) return
    const q = quizById[current]
    await db.quizAttempts.add({ questionId: current, score, points: q.points, confidence: confidence as 1|2|3|4, at: Date.now(), mode: 'quiz' })
    setScored(score)
  }

  if (mode === 'select') {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <h1 className="text-xl font-bold">📝 Vprašanja</h1>
          <select className="input max-w-[220px] text-sm" value={topicFilter} onChange={e => setTopicFilter(e.target.value)}>
            <option value="all">Vse teme</option>
            {topics.map(t => <option key={t.id} value={t.id}>{t.n}. {t.title}</option>)}
          </select>
        </div>
        <div className="space-y-3">
          {pool.map(q => (
            <button key={q.id} onClick={() => start(q.id)} className="card w-full text-left hover:border-blue-400">
              <div className="flex justify-between items-start gap-2">
                <span className="text-sm font-medium">{q.prompt}</span>
                <span className="badge bg-slate-100 dark:bg-slate-800 shrink-0">{q.points}T</span>
              </div>
              <div className="text-xs text-slate-500 mt-1">
                {q.type} · {q.provenance} {q.officialStatus === 'generatedVariant' && '· ⚠️ generirana variant'}
              </div>
            </button>
          ))}
        </div>
        {history.length > 0 && (
          <div className="card">
            <h2 className="font-semibold text-sm mb-2">Zadnji poskusi</h2>
            <ul className="text-xs space-y-1">
              {history.slice(0, 8).map(h => (
                <li key={h.id} className="flex justify-between">
                  <span className="truncate pr-2">{quizById[h.questionId]?.prompt.slice(0, 60) ?? h.questionId}…</span>
                  <span className={h.score / h.points >= 0.6 ? 'text-green-600' : 'text-red-500'}>{h.score}/{h.points}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    )
  }

  const q = quizById[current!]
  return (
    <div className="space-y-4 max-w-2xl">
      <button onClick={() => setMode('select')} className="text-sm text-blue-600 dark:text-blue-400">← Vsa vprašanja</button>
      <div className="card">
        <div className="flex justify-between items-start gap-2 mb-3">
          <p className="font-medium">{q.prompt}</p>
          <span className="badge bg-slate-100 dark:bg-slate-800 shrink-0">{q.points}T</span>
        </div>
        <textarea className="input min-h-[120px] font-mono text-xs" placeholder="Alineje: vir + člen + primer…"
          value={answer} onChange={e => setAnswer(e.target.value)} disabled={scored !== null} />
        {!revealed ? (
          <button onClick={() => setRevealed(true)} className="btn mt-3" disabled={!answer.trim()}>Razkrij model odgovor</button>
        ) : (
          <>
            <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-700">
              <h3 className="text-xs font-semibold uppercase text-slate-400 mb-2">Model odgovor (alineje)</h3>
              <ul className="text-sm list-disc pl-5 space-y-1.5">
                {q.answerOutline.map((a, i) => <li key={i}>{a}</li>)}
              </ul>
            </div>
            {scored === null ? (
              <div className="mt-4 space-y-2">
                <p className="text-xs text-slate-500">Oceni svoj odgovor iskreno (točke):</p>
                <div className="flex flex-wrap gap-2">
                  {Array.from({ length: q.points + 1 }, (_, v) => (
                    <button key={v} onClick={() => save(v)}
                      className={`px-3 py-2 rounded-lg border text-sm min-h-[44px] ${scored === v ? 'bg-blue-600 text-white border-blue-600' : 'border-slate-300 dark:border-slate-600'}`}>
                      {v}T
                    </button>
                  ))}
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs text-slate-500">Zaupanje pred odgovorom:</span>
                  {[1, 2, 3, 4].map(c => (
                    <button key={c} onClick={() => setConfidence(c)}
                      className={`px-2.5 py-1.5 rounded border text-xs ${confidence === c ? 'bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900' : 'border-slate-300 dark:border-slate-600'}`}>
                      {c}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="mt-3 flex items-center gap-2">
                <span className={`badge ${scored / q.points >= 0.6 ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-200'}`}>
                  {scored}/{q.points}
                </span>
                <button onClick={() => start(pool[(pool.findIndex(x => x.id === current) + 1) % pool.length].id)} className="btn-secondary !py-1.5 text-xs">
                  Naslednje vprašanje →
                </button>
              </div>
            )}
          </>
        )}
      </div>
      <div className="text-xs text-slate-400">Vir: {q.provenance} · status: {q.officialStatus}</div>
    </div>
  )
}
