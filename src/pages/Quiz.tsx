import { useEffect, useMemo, useState } from 'react'
import { quiz, topics, quizById } from '../lib/data'
import { db, type QuizAttempt } from '../db/db'

export default function Quiz() {
  const [topicFilter, setTopicFilter] = useState('all')
  const [mode, setMode] = useState<'select' | 'open'>('select')
  const [current, setCurrent] = useState<string | null>(null)
  const [answer, setAnswer] = useState('')
  const [confidence, setConfidence] = useState(2)
  const [scored, setScored] = useState<number | null>(null)
  const [revealed, setRevealed] = useState(false)
  const [history, setHistory] = useState<QuizAttempt[]>([])

  // Checklist state for active recall
  const [checks, setChecks] = useState({
    articleCited: false,
    bodyMentioned: false,
    authorOrCase: false,
    clearBullets: false,
  })

  const pool = useMemo(() => topicFilter === 'all' ? quiz : quiz.filter(q => q.topics.includes(topicFilter)), [topicFilter])

  useEffect(() => {
    db.quizAttempts.orderBy('at').reverse().limit(20).toArray().then(setHistory)
  }, [scored])

  function start(qid: string) {
    setCurrent(qid)
    setAnswer('')
    setConfidence(2)
    setScored(null)
    setRevealed(false)
    setChecks({ articleCited: false, bodyMentioned: false, authorOrCase: false, clearBullets: false })
    setMode('open')
  }

  async function save(score: number) {
    if (!current) return
    const q = quizById[current]
    await db.quizAttempts.add({ questionId: current, score, points: q.points, confidence: confidence as 1|2|3|4, at: Date.now(), mode: 'quiz' })
    setScored(score)
  }

  if (mode === 'select') {
    return (
      <div className="space-y-6">
        <div>
          <div className="kicker mb-2">AKTIVNI RECALL & RUBRIKE</div>
          <h1 className="font-display text-3xl font-semibold tracking-tight">📝 Vprašanja z izpitov & banke</h1>
          <p className="text-sm text-stone-600 mt-2">
            37 vprašanj z modelnimi odgovori, točkovnimi rubrikami in preverbo alinej po navodilih prof. Roter.
          </p>
        </div>

        {/* Formula summary banner */}
        <div className="card !p-5 border-stone-200 bg-stone-50/50">
          <div className="kicker mb-2 text-stone-600">💡 FORMULA ZA TOČKE PO PROF. ROTER:</div>
          <div className="grid sm:grid-cols-3 gap-3 text-xs leading-relaxed">
            <div className="p-3 bg-white rounded-lg border border-stone-200">
              <span className="font-bold text-stone-900 block mb-1">2 TOČKI</span>
              Točen vir + člen + 1 jedrnata poved bistva (npr. ICJ 38(1)(b) običaj + state practice/opinio juris).
            </div>
            <div className="p-3 bg-white rounded-lg border border-stone-200">
              <span className="font-bold text-stone-900 block mb-1">4 TOČKE</span>
              3–4 alineje: Člen + pristojno telo + postopek + avtor/primer (npr. Lemkin, Tate, Osman).
            </div>
            <div className="p-3 bg-white rounded-lg border border-stone-200">
              <span className="font-bold text-stone-900 block mb-1">6 TOČK (Vincent)</span>
              Vseh 5 elementov (subjekt, objekt, uveljavljanje, dolžnost/Shue, utemeljitev) + primer.
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between flex-wrap gap-2">
          <div className="text-xs text-stone-500 font-medium">Bazen vprašanj ({pool.length})</div>
          <select className="input max-w-[220px] text-xs" value={topicFilter} onChange={e => setTopicFilter(e.target.value)} aria-label="Filter po temi">
            <option value="all">Vse teme ({quiz.length})</option>
            {topics.map(t => <option key={t.id} value={t.id}>{t.n}. {t.title}</option>)}
          </select>
        </div>

        <div className="space-y-2.5">
          {pool.map((q, idx) => (
            <button key={q.id} onClick={() => start(q.id)} className="card card-hover w-full text-left !p-4 block">
              <div className="flex justify-between items-start gap-3">
                <span className="text-sm font-medium leading-snug">
                  <span className="text-stone-600 mr-2 font-mono text-xs">{idx + 1}.</span>
                  {q.prompt}
                </span>
                <span className="badge bg-stone-100 text-stone-700 shrink-0 font-mono text-xs">
                  {q.points}T
                </span>
              </div>
              <div className="text-[11px] text-stone-600 mt-2 flex flex-wrap items-center gap-2">
                <span>{q.provenance}</span>
                <span>•</span>
                <span className="capitalize">{q.type}</span>
                {q.officialStatus === 'generatedVariant' && <span className="text-amber-600 font-medium">⚠️ Varianta</span>}
              </div>
            </button>
          ))}
        </div>

        {history.length > 0 && (
          <div className="card !p-5">
            <h2 className="font-semibold text-sm mb-3">Zadnji poskusi</h2>
            <ul className="text-xs space-y-2 divide-y divide-stone-100">
              {history.slice(0, 6).map(h => (
                <li key={h.id} className="pt-2 flex justify-between items-center">
                  <span className="truncate pr-3 text-stone-600">{quizById[h.questionId]?.prompt ?? h.questionId}</span>
                  <span className={`font-mono font-medium shrink-0 ${h.score / h.points >= 0.6 ? 'text-emerald-600' : 'text-red-500'}`}>
                    {h.score} / {h.points}T
                  </span>
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
    <div className="space-y-6 max-w-2xl">
      <button onClick={() => setMode('select')} className="text-xs text-stone-500 hover:text-stone-900 flex items-center gap-1">
        ← Vsa vprašanja
      </button>

      <div className="card !p-6 space-y-4">
        <div className="flex justify-between items-start gap-3">
          <div>
            <div className="kicker mb-1">{q.provenance} • {q.type.toUpperCase()}</div>
            <h2 className="font-display text-xl font-semibold leading-snug">{q.prompt}</h2>
          </div>
          <span className="badge bg-stone-100 text-stone-800 shrink-0 text-xs px-2.5 py-1">
            {q.points} TOČK{q.points === 2 ? 'I' : q.points === 4 ? 'E' : ''}
          </span>
        </div>

        {/* Answer area */}
        <div>
          <label className="text-xs text-stone-500 font-medium block mb-1.5">
            Tvoj odgovor (piši v jedrnatih alinejah, kot na izpitu):
          </label>
          <textarea
            className="input min-h-[140px] font-mono text-xs leading-relaxed"
            placeholder="• Vir in člen: ...&#10;• Pristojno telo in narava: ...&#10;• Težava / avtor / primer: ..."
            value={answer}
            onChange={e => setAnswer(e.target.value)}
            disabled={scored !== null}
          />
        </div>

        {/* Rubric Self-Checklist */}
        <div className="p-3 bg-stone-50 rounded-lg border border-stone-200 text-xs space-y-2">
          <div className="font-semibold text-stone-600">HITRA SAMOPREVERBA ALINEJ:</div>
          <div className="grid sm:grid-cols-2 gap-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" checked={checks.articleCited} onChange={e => setChecks({ ...checks, articleCited: e.target.checked })} />
              <span>Naveden točen člen / pogodba</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" checked={checks.bodyMentioned} onChange={e => setChecks({ ...checks, bodyMentioned: e.target.checked })} />
              <span>Omenjeno nadzorno telo / postopek</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" checked={checks.authorOrCase} onChange={e => setChecks({ ...checks, authorOrCase: e.target.checked })} />
              <span>Omenjen avtor ali konkreten primer</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" checked={checks.clearBullets} onChange={e => setChecks({ ...checks, clearBullets: e.target.checked })} />
              <span>Odgovor je v jasnih alinejah</span>
            </label>
          </div>
        </div>

        {!revealed ? (
          <button onClick={() => setRevealed(true)} className="btn w-full" disabled={!answer.trim()}>
            Razkrij uradni model odgovora
          </button>
        ) : (
          <div className="space-y-4 pt-3 border-t border-stone-200">
            <div>
              <h3 className="kicker mb-2 text-stone-500">MODEL ODGOVORA (ALINEJE ZA MAKSIMALNE TOČKE)</h3>
              <ul className="text-xs space-y-2 bg-stone-50 p-4 rounded-xl border border-stone-200">
                {q.answerOutline.map((a, i) => (
                  <li key={i} className="flex gap-2">
                    <span className="text-blue-600 font-bold">•</span>
                    <span className="text-stone-800 leading-relaxed">{a}</span>
                  </li>
                ))}
              </ul>
            </div>

            {scored === null ? (
              <div className="space-y-3 pt-2">
                <p className="text-xs text-stone-600 font-medium">
                  Koliko točk bi si prisodil glede na model zgoraj?
                </p>
                <div className="flex flex-wrap gap-2">
                  {Array.from({ length: q.points + 1 }, (_, v) => (
                    <button
                      key={v}
                      onClick={() => save(v)}
                      className="px-4 py-2.5 rounded-lg border text-sm font-medium border-stone-300 hover:bg-stone-100 transition-colors"
                    >
                      {v} T
                    </button>
                  ))}
                </div>
                <div className="flex items-center gap-2 pt-2 text-xs text-stone-600">
                  <span>Zaupanje pred preverbo:</span>
                  {[1, 2, 3, 4].map(c => (
                    <button
                      key={c}
                      onClick={() => setConfidence(c)}
                      className={`px-2 py-1 rounded text-xs border ${confidence === c ? 'bg-stone-900 text-white' : 'border-stone-300'}`}
                    >
                      {c === 1 ? 'Nizko' : c === 4 ? 'Gotovo' : c}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-stone-100 flex items-center justify-between">
                <div>
                  <span className="text-xs text-stone-500">Tvoja ocena: </span>
                  <span className="font-display font-semibold text-base">{scored} / {q.points}T</span>
                </div>
                <button
                  onClick={() => start(pool[(pool.findIndex(x => x.id === current) + 1) % pool.length].id)}
                  className="btn !py-2 !px-3 text-xs"
                >
                  Naslednje vprašanje →
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
