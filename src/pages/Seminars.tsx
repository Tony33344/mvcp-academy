import { useState, useMemo } from 'react'
import { seminars, topicById } from '../lib/data'
import Md from '../components/Md'

export default function Seminars() {
  const [open, setOpen] = useState<string | null>(null)
  const [search, setSearch] = useState('')

  const filtered = useMemo(() => {
    if (!search.trim()) return seminars
    const q = search.toLowerCase()
    return seminars.filter(s =>
      s.title.toLowerCase().includes(q) ||
      s.convention.toLowerCase().includes(q) ||
      s.definition.toLowerCase().includes(q) ||
      s.primeri.toLowerCase().includes(q)
    )
  }, [search])

  return (
    <div className="space-y-6">
      <div>
        <div className="kicker mb-2">SEMINARJI &amp; SKUPINSKE RAZISKAVE — VIR IZPITNIH VPRAŠANJ</div>
        <h1 className="font-display text-3xl font-semibold tracking-tight">📄 16 seminarskih nalog — integrirano</h1>
        <p className="text-sm text-stone-600 dark:text-stone-400 mt-2 leading-relaxed">
          Vsaka seminarska naloga iz mape <em>clankiseminarsk enaloge</em> v enem mestu: pogodba in točni členi,
          definicija, omejitve, izzivi v implementaciji, primeri iz prakse, študentski pisni izdelki (pasporti)
          in povezava na izpitna vprašanja. Izpitna vprašanja prihajajo tudi od tu!
        </p>
      </div>

      <input
        type="text"
        className="input"
        placeholder="Išči po vseh 16 nalogah (npr. 'CAT', 'dolus specialis', 'Aarhuška')…"
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      <div className="space-y-2.5">
        {filtered.map(s => {
          const topic = topicById[s.id]
          const isOpen = open === s.id
          return (
            <div key={s.id} className="card !p-0 overflow-hidden">
              <button
                onClick={() => setOpen(isOpen ? null : s.id)}
                className="w-full text-left px-4 py-3.5 flex items-center justify-between gap-3 hover:bg-stone-50 dark:hover:bg-stone-900/40 transition-colors"
              >
                <span className="flex items-baseline gap-3 min-w-0">
                  <span className="font-mono text-xs text-stone-400 shrink-0 w-6">{s.n}.</span>
                  <span className="text-sm font-semibold leading-snug">{s.title}</span>
                </span>
                <span className="text-stone-400 text-xs shrink-0">{isOpen ? '▲' : '▼'}</span>
              </button>

              {isOpen && (
                <div className="px-4 pb-5 pt-1 space-y-4 border-t border-stone-100 dark:border-stone-800">
                  {topic && (
                    <div className="pt-3">
                      <span className="text-[10px] uppercase tracking-wider text-stone-400 font-semibold">Povezani pasport (izpitni bazen)</span>
                      <p className="text-xs text-stone-600 dark:text-stone-300 mt-1">{topic.legal}</p>
                    </div>
                  )}

                  <div>
                    <span className="text-[10px] uppercase tracking-wider text-stone-400 font-semibold">⚖️ Pravna podlaga — pogodba in točni členi</span>
                    <div className="mt-1 text-xs leading-relaxed bg-stone-50 dark:bg-stone-900/50 p-3 rounded border border-stone-200 dark:border-stone-800">
                      <Md>{s.convention}</Md>
                    </div>
                  </div>

                  <div>
                    <span className="text-[10px] uppercase tracking-wider text-stone-400 font-semibold">📖 Definicija (iz študentskega pasporta)</span>
                    <p className="text-xs leading-relaxed mt-1 text-stone-800 dark:text-stone-200">{s.definition}</p>
                  </div>

                  <div className="grid sm:grid-cols-2 gap-3">
                    <div>
                      <span className="text-[10px] uppercase tracking-wider text-stone-400 font-semibold">🚧 Omejitve</span>
                      <p className="text-xs leading-relaxed mt-1 text-stone-700 dark:text-stone-300">{s.omejitve}</p>
                    </div>
                    <div>
                      <span className="text-[10px] uppercase tracking-wider text-stone-400 font-semibold">💡 Pomembnost</span>
                      <p className="text-xs leading-relaxed mt-1 text-stone-700 dark:text-stone-300">{s.pomembnost}</p>
                    </div>
                  </div>

                  <div>
                    <span className="text-[10px] uppercase tracking-wider text-stone-400 font-semibold">⚠️ Izzivi v implementaciji</span>
                    <p className="text-xs leading-relaxed mt-1 text-stone-700 dark:text-stone-300">{s.izzivi}</p>
                  </div>

                  <div>
                    <span className="text-[10px] uppercase tracking-wider text-stone-400 font-semibold">🌍 Primeri iz prakse</span>
                    <p className="text-xs leading-relaxed mt-1 text-stone-700 dark:text-stone-300">{s.primeri}</p>
                  </div>

                  <div>
                    <span className="text-[10px] uppercase tracking-wider text-stone-400 font-semibold">📚 Študentski pisni izdelki (mapa seminarskih nalog)</span>
                    <ul className="text-xs mt-1 space-y-1">
                      {s.studentWork.map((w, i) => (
                        <li key={i} className="text-stone-600 dark:text-stone-400 font-mono">— {w}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="p-3 bg-red-50/60 dark:bg-red-950/20 rounded border border-red-200 dark:border-red-900/40">
                    <span className="text-[10px] uppercase tracking-wider text-red-700 dark:text-red-300 font-semibold">🎯 Povezava na izpitna vprašanja</span>
                    <ul className="text-xs mt-1.5 space-y-1">
                      {s.examQuestions.map((q, i) => (
                        <li key={i} className="text-red-800 dark:text-red-200 leading-relaxed">→ {q}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          )
        })}
        {filtered.length === 0 && (
          <div className="card text-center text-stone-400 text-sm py-8">Ni zadetkov za "{search}".</div>
        )}
      </div>
    </div>
  )
}
