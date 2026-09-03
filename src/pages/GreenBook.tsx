import { useState, useMemo } from 'react'
import { greenbook } from '../lib/data'

export default function GreenBook() {
  const [search, setSearch] = useState('')
  const [drillActive, setDrillActive] = useState(false)
  const [drillIdx, setDrillIdx] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)
  const [drillScore, setDrillScore] = useState({ correct: 0, total: 0 })

  const filtered = useMemo(() => {
    if (!search.trim()) return greenbook
    const q = search.toLowerCase()
    return greenbook.filter(g =>
      g.topic.toLowerCase().includes(q) || g.articles.toLowerCase().includes(q)
    )
  }, [search])

  const drillItem = greenbook[drillIdx % greenbook.length]

  function nextDrill(hit: boolean) {
    setDrillScore(s => ({ correct: s.correct + (hit ? 1 : 0), total: s.total + 1 }))
    setShowAnswer(false)
    setDrillIdx(i => i + 1)
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="kicker mb-2">DOVOLJENO NA IZPITU</div>
        <h1 className="font-display text-3xl font-semibold">📗 Zeleni priročnik — kazipot členov</h1>
        <p className="text-sm text-stone-600 mt-2 leading-relaxed">
          <em>Dokumenti človekovih pravic z uvodnimi pojasnili</em> (Cerar, Jamnikar, Smrkolj).
          Uporabi jo <strong>izključno za točne navedbe členov</strong> med pisanjem, ne za učenje.
        </p>
      </div>

      {/* Drill toggle / Search banner */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="relative flex-1 min-w-[240px]">
          <input
            type="text"
            className="input pl-9"
            placeholder="Išči pravico, člen, pogodbo (npr. 'mučenje', '10', 'CAT')..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <span className="absolute left-3 top-3 text-stone-600 text-sm">🔍</span>
          {search && (
            <button
              onClick={() => setSearch('')}
              className="absolute right-3 top-2.5 text-xs text-stone-600 hover:text-stone-600 p-1"
            >
              ✕
            </button>
          )}
        </div>
        <button
          onClick={() => { setDrillActive(!drillActive); setShowAnswer(false) }}
          className={drillActive ? "btn-ghost" : "btn"}
        >
          {drillActive ? "Zapri Speed Drill" : "⚡ Zaženi Speed-Drill členov"}
        </button>
      </div>

      {/* Speed Drill Box */}
      {drillActive && (
        <div className="card !p-6 border-blue-300 bg-blue-50/50">
          <div className="flex justify-between items-center mb-3">
            <span className="kicker text-blue-700">SPEED DRILL — KATERI ČLENI VELJAJO?</span>
            <span className="text-xs text-stone-500">Točnost: {drillScore.total ? Math.round((drillScore.correct / drillScore.total) * 100) : 0}% ({drillScore.correct}/{drillScore.total})</span>
          </div>
          <div className="text-xl font-display font-semibold mb-3">
            Tema: <span className="text-blue-700">{drillItem.topic}</span>
          </div>
          <p className="text-xs text-stone-500 mb-4">V glavi si povej: katera pogodba in kateri člen?</p>

          {showAnswer ? (
            <div className="space-y-4 pt-4 border-t border-blue-200">
              <div className="font-mono text-sm bg-white p-3 rounded-lg border border-stone-200 text-stone-800">
                {drillItem.articles}
              </div>
              <div className="flex gap-2">
                <button onClick={() => nextDrill(false)} className="btn-ghost !text-red-600 flex-1">Sem se zmotil / nisem vedel</button>
                <button onClick={() => nextDrill(true)} className="btn !bg-emerald-700 hover:!bg-emerald-600 flex-1">Točno sem vedel ✓</button>
              </div>
            </div>
          ) : (
            <button onClick={() => setShowAnswer(true)} className="btn">Preveri rešitev</button>
          )}
        </div>
      )}

      {/* Table */}
      <div className="card !p-0 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-stone-200 bg-stone-50 text-left text-xs uppercase tracking-wider text-stone-500">
              <th className="py-3 px-4 w-1/3">Tema / Pravica</th>
              <th className="py-3 px-4">Ključni členi in viri</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-stone-100">
            {filtered.map(g => (
              <tr key={g.topic} className="hover:bg-stone-50/50 transition-colors">
                <td className="py-3 px-4 font-medium align-top">{g.topic}</td>
                <td className="py-3 px-4 text-stone-700 font-mono text-xs leading-relaxed">{g.articles}</td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={2} className="py-6 text-center text-stone-600 text-sm">
                  Ni zadetkov za "{search}".
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Tactial instructions */}
      <div className="card !p-5 border-amber-200 bg-amber-50/40">
        <h2 className="font-semibold text-sm mb-2 text-amber-900">💡 4 pravila za zeleni priročnik na izpitu:</h2>
        <ul className="text-xs space-y-2 text-stone-700">
          <li><strong>1. Ne listaj v prazno:</strong> Uporabi kazipot zgoraj preden odpreš knjigo. Vsaka izgubljena minuta listanja je ena manj za pisanje odgovorov.</li>
          <li><strong>2. Citiraj natančno z oznako člena:</strong> Npr. <em>»po čl. 1A(2) Konvencije o statusu beguncev«</em> ali <em>»čl. 10(2) EKČP«</em>, ne <em>»po paktu o človekovih pravicah«</em>.</li>
          <li><strong>3. Česa NI v knjigi:</strong> ICPED (prisilna izginotja), ICRMW (delavci migranti), fakultativni protokoli (1. OP, OP-CEDAW, OP-CRC). Te si zapomni na pamet z našimi karticami!</li>
          <li><strong>4. Nalepi si 7 barvnih zavihkov:</strong> SDČP, MPDPP, MPESKP, EKČP, CAT, CRC, CEDAW.</li>
        </ul>
      </div>
    </div>
  )
}
