import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { exams, quizById, topics } from '../lib/data'
import { db, type QuizAttempt } from '../db/db'
import Md from '../components/Md'

type Phase = 'select' | 'running' | 'review'

export default function Simulator() {
  const nav = useNavigate()
  const [phase, setPhase] = useState<Phase>('select')
  const [examId, setExamId] = useState<string>('rok1-2026')
  const [remaining, setRemaining] = useState(75 * 60)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [scores, setScores] = useState<Record<string, number>>({})
  const [confidences, setConfidences] = useState<Record<string, number>>({})
  const [attemptId, setAttemptId] = useState<number | null>(null)

  const exam = exams.find(e => e.id === examId)!
  const questions = useMemo(() => exam.questionIds.map(id => quizById[id]).filter(Boolean), [exam])

  useEffect(() => {
    if (phase !== 'running') return
    const t = setInterval(() => setRemaining(r => {
      if (r <= 1) { clearInterval(t); finish(); return 0 }
      return r - 1
    }), 1000)
    return () => clearInterval(t)
  }, [phase])

  function start(id: string) {
    setExamId(id); setPhase('running'); setRemaining(75 * 60); setAnswers({}); setScores({}); setConfidences({})
  }

  async function finish() {
    setPhase('review')
    const ids = exam.questionIds
    const attempts = ids.map(qid => ({
      questionId: qid, score: scores[qid] ?? 0, points: quizById[qid]?.points ?? 2,
      confidence: (confidences[qid] ?? 2) as 1 | 2 | 3 | 4, at: Date.now(), mode: 'exam' as const,
    }))
    await db.quizAttempts.bulkAdd(attempts)
  }

  const totalPoints = questions.reduce((s, q) => s + q.points, 0)
  const earned = questions.reduce((s, q) => s + (scores[q.id] ?? 0), 0)
  const pct = totalPoints ? Math.round((earned / totalPoints) * 100) : 0

  if (phase === 'select') {
    return (
      <div className="space-y-4">
        <h1 className="text-xl font-bold">⏱️ Simulator izpita</h1>
        <p className="text-sm text-stone-600">75 minut · napiši odgovore na papir ali v polja · nato se oceni po rubriki (model odgovor = alineje).</p>
        <div className="grid sm:grid-cols-3 gap-3">
          {exams.map(e => (
            <button key={e.id} onClick={() => start(e.id)} className="card text-left hover:border-blue-400">
              <div className="font-semibold text-sm">{e.title}</div>
              <div className="text-xs text-stone-600 mt-1">{e.questionIds.length} vprašanj · {e.durationMin} min</div>
              <div className="text-xs text-amber-600 mt-1">{e.formatNote}</div>
            </button>
          ))}
        </div>
        <div className="card bg-slate-50 text-xs text-stone-600">
          Namig: piši jedrnate alineje s točnimi členi. Po času se oceni iskreno — rezultat hrani šibke teme.
        </div>
      </div>
    )
  }

  if (phase === 'running') {
    const mm = String(Math.floor(remaining / 60)).padStart(2, '0')
    const ss = String(remaining % 60).padStart(2, '0')
    return (
      <div className="space-y-4">
        <div className="sticky top-14 z-30 card flex items-center justify-between !py-2">
          <span className="font-mono text-lg font-bold">{mm}:{ss}</span>
          <span className="text-xs text-stone-600">{exam.title} · {questions.length} vprašanj</span>
          <button onClick={finish} className="btn !py-1.5 !px-3 text-xs">Zaključi</button>
        </div>
        {questions.map((q, i) => (
          <div key={q.id} className="card">
            <div className="flex justify-between items-start gap-2 mb-2">
              <span className="font-medium text-sm">{i + 1}. {q.prompt}</span>
              <span className="badge bg-stone-100 shrink-0">{q.points}T</span>
            </div>
            <textarea className="input min-h-[90px] font-mono text-xs" placeholder="Tvoje alineje (vir + člen + primer)…"
              value={answers[q.id] ?? ''} onChange={e => setAnswers(a => ({ ...a, [q.id]: e.target.value }))} />
          </div>
        ))}
        <button onClick={finish} className="btn w-full">Zaključi in oceni</button>
      </div>
    )
  }

  // review
  return (
    <div className="space-y-4">
      <div className="card text-center">
        <div className="text-3xl font-bold">{earned}/{totalPoints} točk ({pct} %)</div>
        <p className="text-sm text-stone-600 mt-1">
          {pct >= 58 ? '✅ Nad pragom (35/60 ≈ 58 %)' : '⚠️ Pod pragom — osredotoči se na šibke teme'}
        </p>
      </div>
      {questions.map((q, i) => {
        const sc = scores[q.id] ?? 0
        return (
          <div key={q.id} className="card">
            <div className="flex justify-between items-start gap-2">
              <span className="font-medium text-sm">{i + 1}. {q.prompt}</span>
              <span className={`badge shrink-0 ${sc / q.points >= 0.6 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-700'}`}>
                {sc}/{q.points}
              </span>
            </div>
            {answers[q.id] && <div className="mt-2 text-xs text-stone-600 border-l-2 border-stone-300 pl-2">Tvoj odgovor: {answers[q.id].slice(0, 200)}…</div>}
            <details className="mt-2" open>
              <summary className="cursor-pointer text-xs font-semibold text-blue-700 dark:text-blue-400">Model odgovor (alineje, ki prinašajo točke):</summary>
              <ul className="text-xs list-disc pl-5 mt-1 space-y-1 bg-stone-50 dark:bg-stone-900/50 p-2.5 rounded border border-stone-200 dark:border-stone-800 text-stone-800 dark:text-stone-200">
                {q.answerOutline.map((a, j) => <li key={j}>{a}</li>)}
              </ul>
            </details>
            <div className="mt-3 flex flex-wrap items-center gap-2 text-xs">
              <span>Oceni svoj odgovor:</span>
              {[0, Math.round(q.points * 0.5), q.points].map((v, j) => (
                <button key={j} onClick={() => setScores(s => ({ ...s, [q.id]: v }))}
                  className={`px-2.5 py-1 rounded border text-xs ${sc === v ? 'bg-blue-600 text-white border-blue-600' : 'border-stone-300'}`}>
                  {v}T
                </button>
              ))}
              <span className="ml-2">Zaupanje:</span>
              {[1, 2, 3, 4].map(c => (
                <button key={c} onClick={() => setConfidences(cf => ({ ...cf, [q.id]: c }))}
                  className={`px-2 py-1 rounded border text-xs ${(confidences[q.id] ?? 0) === c ? 'bg-slate-900 text-white' : 'border-stone-300'}`}>
                  {c}
                </button>
              ))}
            </div>
          </div>
        )
      })}
      <button onClick={() => setPhase('select')} className="btn-secondary w-full">← Drug izpit</button>
    </div>
  )
}
