import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { topics, flashcards, quiz } from '../lib/data'
import { srsStats } from '../lib/srs'
import { getSetting, setSetting } from '../db/db'

export default function Home() {
  const [examDate, setExamDate] = useState<string>('')
  const [stats, setStats] = useState({ total: 0, new: 0, learning: 0, review: 0, due: 0 })
  const [daysLeft, setDaysLeft] = useState<number | null>(null)

  useEffect(() => {
    getSetting<string>('examDate', '').then((d: string) => { setExamDate(d); if (d) {
      const diff = Math.ceil((new Date(d).getTime() - Date.now()) / 86400000)
      setDaysLeft(diff >= 0 ? diff : null)
    }})
    srsStats(flashcards.map(c => c.id)).then(setStats)
  }, [])

  return (
    <div className="space-y-10">
      {/* Hero */}
      <section className="pt-6 pb-2">
        <p className="kicker">Mednarodno varstvo človekovih pravic</p>
        <h1 className="font-display text-4xl sm:text-5xl font-semibold leading-[1.08] tracking-tight mt-2 mb-3">
          Nauči se človekovih pravic<br />
          <span className="text-stone-600">kot pravnik, ne kot papiga.</span>
        </h1>
        <p className="text-stone-500 text-sm leading-relaxed max-w-lg">
          Retrieval practice, razpršeno ponavljanje, preverjeni viri. Zgrajeno okoli izpita prof. dr. Petre Roter — uporabno za vsakogar.
        </p>
      </section>

      <hr className="rule" />

      {/* exam countdown */}
      <section className="flex flex-wrap items-center gap-4">
        <div className="flex items-baseline gap-3">
          <span className="kicker">Izpit</span>
          <input type="date" aria-label="Izpitni datum" className="input !w-auto !min-h-0 py-1.5 text-sm"
            value={examDate}
            onChange={e => { setExamDate(e.target.value); setSetting('examDate', e.target.value) }} />
        </div>
        {daysLeft !== null && daysLeft >= 0 && (
          <div className="flex items-baseline gap-2">
            <span className="font-display text-3xl font-semibold">{daysLeft}</span>
            <span className="text-sm text-stone-500">dni</span>
          </div>
        )}
      </section>

      <hr className="rule" />

      {/* two doors */}
      <section className="grid sm:grid-cols-2 gap-4">
        <Link to="/exam" className="card card-hover group !p-6">
          <div className="kicker text-red-700 mb-3">Način A</div>
          <h2 className="font-display text-2xl font-semibold mb-2">Izpit</h2>
          <p className="text-sm text-stone-600 leading-relaxed">
            Jedro snovi, 16 seminarskih tem, zeleni priročnik, simulator 75 min. Vse označeno po viru in letu.
          </p>
          <span className="inline-block mt-4 text-sm text-stone-600 group-hover:translate-x-1 transition-transform">→</span>
        </Link>
        <Link to="/learn" className="card card-hover group !p-6">
          <div className="kicker text-stone-600 mb-3">ZA VSE</div>
          <h2 className="font-display text-2xl font-semibold group-hover:underline decoration-stone-300 underline-offset-4">Kurikulum</h2>
          <p className="text-sm text-stone-500 mt-2 leading-relaxed">
            Od koncepta do aktualnih dogodkov — 8 modulov, 15 primerjalnih tabel, graf znanja.
          </p>
        </Link>
      </section>

      <section className="grid grid-cols-3 gap-px bg-stone-200 rounded-xl overflow-hidden border border-stone-200">
        {[
          { v: flashcards.length, l: 'kartic' },
          { v: quiz.length, l: 'vprašanj' },
          { v: topics.length, l: 'tem' },
        ].map(s => (
          <div key={s.l} className="bg-white px-4 py-5 text-center">
            <div className="font-display text-3xl font-semibold">{s.v}</div>
            <div className="text-[11px] uppercase tracking-wider text-stone-600 mt-1">{s.l}</div>
          </div>
        ))}
      </section>

      <section className="grid sm:grid-cols-2 gap-3">
        <Link to="/practice/flashcards" className="card card-hover !p-5 flex items-center justify-between">
          <div>
            <div className="kicker mb-1">Danes</div>
            <div className="font-medium text-sm">Flashcards — retrieval practice</div>
          </div>
          <span className="text-stone-500 group-hover:translate-x-1 transition-transform">→</span>
        </Link>
        <Link to="/sources" className="card card-hover group !p-6">
          <div className="kicker mb-1">VIRI</div>
          <div className="font-medium text-sm">OHCHR · UPR · HUDOC · pogodbe</div>
          <span className="text-stone-500">↗</span>
        </Link>
      </section>
    </div>
  )
}
