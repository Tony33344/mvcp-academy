import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { flashcards, quiz } from '../lib/data'
import { srsStats } from '../lib/srs'

export default function Practice() {
  const [stats, setStats] = useState({ total: 0, new: 0, learning: 0, review: 0, due: 0 })
  useEffect(() => { srsStats(flashcards.map(c => c.id)).then(setStats) }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold">⚡ Vadba</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Retrieval practice — najučinkovitejša tehnika (Dunlosky 2013). Ponovi pred branjem.
        </p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { l: 'Skupaj', v: stats.total }, { l: 'Nove', v: stats.new },
          { l: 'V učenju', v: stats.learning }, { l: 'Za ponovitev', v: stats.due },
        ].map(s => (
          <div key={s.l} className="card text-center">
            <div className="text-xl font-bold text-blue-600 dark:text-blue-400">{s.v}</div>
            <div className="text-xs text-slate-500">{s.l}</div>
          </div>
        ))}
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        <Link to="/practice/flashcards" className="card hover:border-blue-400">
          <div className="text-2xl mb-1">🃏</div>
          <div className="font-semibold text-sm">Flashcards (SRS)</div>
          <div className="text-xs text-slate-500 mt-1">{flashcards.length} kartic · FSRS razporejanje · {stats.due} zapadlih</div>
        </Link>
        <Link to="/practice/quiz" className="card hover:border-blue-400">
          <div className="text-2xl mb-1">📝</div>
          <div className="font-semibold text-sm">Vprašanja</div>
          <div className="text-xs text-slate-500 mt-1">{quiz.length} vprašanj · MCQ + odprti odgovori + scenariji</div>
        </Link>
      </div>

      <div className="card bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-900">
        <h2 className="font-semibold text-sm mb-1">Kako vaditi učinkovito</h2>
        <ul className="text-sm list-disc pl-5 space-y-1 text-slate-700 dark:text-slate-300">
          <li><strong>Zapri zvezke</strong> — odgovori iz glave, ne beri.</li>
          <li><strong>Mešaj teme</strong> (interleaving) — lažje ločiš podobne pojme (Odbor/Svet/Komisija).</li>
          <li><strong>Oceni iskreno</strong> — nizko zaupanje = kartica se vrne prej.</li>
          <li><strong>Preveri vir</strong> — vsak odgovor ima navedbo (A–E).</li>
        </ul>
      </div>
    </div>
  )
}
