import { Link } from 'react-router-dom'
import { topics, core } from '../lib/data'
import Md from '../components/Md'

export default function ExamDashboard() {
  return (
    <div className="space-y-8">
      <div>
        <div className="kicker mb-2">FDV · prof. dr. Petra Roter</div>
        <h1 className="font-display text-3xl font-semibold tracking-tight">Izpitni način</h1>
        <p className="text-sm text-stone-500 dark:text-stone-400 mt-2 leading-relaxed">
          75 minut, na papir · dovoljena knjiga <em>Dokumenti človekovih pravic</em> ·
          minimum 35/60 točk · odgovori v jedrnatih alinejah s točnimi členi in avtorji.
        </p>
      </div>

      <div className="grid sm:grid-cols-3 gap-3">
        <Link to="/exam/guide" className="card card-hover !p-5">
          <div className="kicker mb-2">01</div>
          <div className="font-medium text-sm">Vodnik — jedro + 16 tem</div>
          <div className="text-xs text-stone-400 mt-1">Pasporti s 4 sidri in modeli odgovorov</div>
        </Link>
        <Link to="/exam/green-book" className="card card-hover !p-5">
          <div className="kicker mb-2">02</div>
          <div className="font-medium text-sm">Zeleni priročnik — kazipot</div>
          <div className="text-xs text-stone-400 mt-1">Tema → točni členi → hitro iskanje</div>
        </Link>
        <Link to="/exam/simulator" className="card card-hover !p-5">
          <div className="kicker mb-2">03</div>
          <div className="font-medium text-sm">Simulator izpita</div>
          <div className="text-xs text-stone-400 mt-1">75 minut, samopreverjanje po točkah</div>
        </Link>
      </div>

      <section>
        <h2 className="kicker mb-4">Jedro snovi — na vsakem izpitu</h2>
        <div className="space-y-2">
          {core.map((c, i) => (
            <details key={c.id} className="card !py-0">
              <summary className="cursor-pointer text-sm py-4 flex items-center gap-4 list-none">
                <span className="font-display text-stone-300 dark:text-stone-600 font-semibold">{String(i + 1).padStart(2, '0')}</span>
                <span className="flex-1">{c.title}</span>
                <span className="text-xs text-stone-400">{c.points}T</span>
              </summary>
              <div className="mt-2 pt-4 border-t border-stone-100 dark:border-stone-800"><Md>{c.body}</Md></div>
            </details>
          ))}
        </div>
      </section>

      <section>
        <h2 className="kicker mb-4">Seminarski bazen — 6 tem, izberi 4</h2>
        <div className="grid sm:grid-cols-2 gap-2">
          {topics.map(t => (
            <Link key={t.id} to={`/exam/guide/${t.id}`} className="card card-hover !p-0 overflow-hidden block">
              <div className="flex items-center">
                <div className="w-14 shrink-0 text-center py-4 border-r border-stone-100 dark:border-stone-800 font-display text-stone-300 dark:text-stone-600">
                  {String(t.n).padStart(2, '0')}
                </div>
                <div className="px-4 py-3.5">
                  <div className="font-medium text-sm leading-snug">{t.title}</div>
                  <div className="text-[11px] text-stone-400 mt-0.5">{t.titleEn}</div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
