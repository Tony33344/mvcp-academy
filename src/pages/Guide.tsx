import { Link, useParams } from 'react-router-dom'
import { topics, flashcards } from '../lib/data'
import Md from '../components/Md'
import ConfidenceBadge from '../components/ConfidenceBadge'

export default function Guide() {
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">📖 Vodnik — jedro + 16 tem</h1>
      <p className="text-sm text-slate-500 dark:text-slate-400">
        Vsak pasport: pravna podlaga → nadzor → težave/primeri → model odgovora. Klikni temo za podrobnosti.
      </p>
      <div className="grid sm:grid-cols-2 gap-3">
        {topics.map(t => (
          <Link key={t.id} to={`/exam/guide/${t.id}`} className="card hover:border-blue-400 transition-colors block">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-sm">{t.n}. {t.title}</span>
              {t.status.includes('jedro') && <span className="badge bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-200">jedro</span>}
            </div>
            <div className="text-xs text-slate-500 mt-1">{t.titleEn}</div>
            <div className="text-xs mt-2 text-slate-600 dark:text-slate-300 line-clamp-2">{t.legal.slice(0, 120)}…</div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export function TopicDetail() {
  const { topicId } = useParams()
  const t = topics.find(x => x.id === topicId)
  if (!t) return <p>Tema ni najdena.</p>
  const related = flashcards.filter(c => c.topics.includes(t.id))

  return (
    <article className="space-y-4">
      <div>
        <Link to="/exam/guide" className="text-sm text-blue-600 dark:text-blue-400">← Vse teme</Link>
        <h1 className="text-xl font-bold mt-2">{t.n}. {t.title}</h1>
        <p className="text-sm text-slate-500">{t.titleEn} · status: {t.status}</p>
      </div>

      <section className="card">
        <h2 className="font-semibold text-sm mb-2">① Pravna podlaga (vir + člen)</h2>
        <Md>{t.legal}</Md>
      </section>
      <section className="card">
        <h2 className="font-semibold text-sm mb-2">② Nadzor / postopek</h2>
        <Md>{t.monitoring}</Md>
      </section>
      <section className="card">
        <h2 className="font-semibold text-sm mb-2">③ Težave v praksi / primeri</h2>
        <Md>{t.problems}</Md>
      </section>
      <section className="card border-blue-300 dark:border-blue-800">
        <h2 className="font-semibold text-sm mb-2">④ Model odgovora (shema)</h2>
        <Md>{t.model}</Md>
      </section>

      <section className="card">
        <h2 className="font-semibold text-sm mb-2">Gradiva v korpusu</h2>
        <ul className="text-sm list-disc pl-5 space-y-1">
          {t.materials.map(m => <li key={m} className="text-slate-600 dark:text-slate-300">{m}</li>)}
        </ul>
      </section>

      {related.length > 0 && (
        <section className="card">
          <h2 className="font-semibold text-sm mb-2">Povezane kartice ({related.length})</h2>
          <ul className="text-sm space-y-2">
            {related.slice(0, 8).map(c => (
              <li key={c.id} className="border-l-2 border-slate-200 dark:border-slate-700 pl-3">
                <div className="font-medium">{c.prompt}</div>
                <div className="text-slate-500 text-xs mt-0.5">{c.answer}</div>
                {c.source && <ConfidenceBadge authority={c.authority} verification={c.source} />}
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="no-print flex gap-2">
        <Link to="/practice/flashcards" className="btn-secondary">⚡ Vadba teme</Link>
        <Link to="/exam/simulator" className="btn">⏱️ Simulator</Link>
      </div>
    </article>
  )
}
