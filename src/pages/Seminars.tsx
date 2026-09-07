import { Link, useParams } from 'react-router-dom'
import { seminars, topics } from '../lib/data'

const SECTIONS = [
  { key: "convention", icon: "⚖️", label: "Pravna podlaga — pogodba in točni členi" },
  { key: "definition", icon: "📖", label: "Definicija (iz študentskega pasporta)" },
  { key: "omejitve", icon: "🚧", label: "Omejitve" },
  { key: "pomembnost", icon: "💡", label: "Pomembnost" },
  { key: "izzivi", icon: "⚠️", label: "Izzivi v implementaciji" },
  { key: "primeri", icon: "🌍", label: "Primeri iz prakse" },
] as const

function Content({ text }: { text: string }) {
  const lines = text.split("\n").map(l => l.trim()).filter(Boolean)
  const bulletish = lines.filter(l => /^[-•*·]/.test(l)).length
  if (bulletish >= 2) {
    return (
      <ul className="space-y-1.5">
        {lines.map((l, i) => (
          <li key={i} className="text-sm leading-relaxed text-stone-800 flex gap-2">
            <span className="text-stone-400 shrink-0">—</span>
            <span>{l.replace(/^[-•*·]\s*/, "")}</span>
          </li>
        ))}
      </ul>
    )
  }
  return <p className="text-sm leading-relaxed text-stone-800 whitespace-pre-line">{text}</p>
}

export default function Seminars() {
  return (
    <div className="space-y-8">
      <div>
        <div className="kicker mb-2">VIR IZPITNIH VPRAŠANJ</div>
        <h1 className="font-display text-3xl font-semibold tracking-tight">Seminarji & skupinske raziskave</h1>
        <p className="text-sm text-stone-600 mt-2 leading-relaxed max-w-2xl">
          Vseh 16 seminarskih nalog iz mape <em>clankiseminarske naloge</em> v enem mestu: pogodba in točni členi,
          definicija, omejitve, izzivi v implementaciji, primeri iz prakse, študentski pisni izdelki (pasporti)
          in povezava na izpitna vprašanja. <strong>Izpitna vprašanja prihajajo tudi od tu!</strong>
        </p>
      </div>

      <div className="grid sm:grid-cols-2 gap-2">
        {seminars.map(s => {
          const t = topics.find(x => x.id === s.topicIds[0])
          const hasPassport = !!s.convention
          return (
            <Link key={s.n} to={`/learn/seminars/${s.n}`} className="card card-hover !p-0 overflow-hidden block">
              <div className="flex items-center">
                <div className="w-14 shrink-0 text-center py-4 border-r border-stone-200 font-display text-stone-400 font-semibold">
                  {String(s.n).padStart(2, "0")}
                </div>
                <div className="px-4 py-3 flex-1">
                  <div className="font-medium text-sm leading-snug">{t ? t.title : s.title.replace(/^\d+\.\s*/, "")}</div>
                  <div className="text-[11px] text-stone-500 mt-0.5">
                    {hasPassport ? `📋 pasport · ${s.files.length} datotek` : `📄 seminarska naloga · ${s.files.length} datotek`}
                  </div>
                </div>
              </div>
            </Link>
          )
        })}
      </div>
    </div>
  )
}

export function SeminarDetail() {
  const { folder } = useParams()
  const s = seminars.find(x => x.n === Number(folder))
  if (!s) return <p>Seminar ni najden.</p>
  const t = topics.find(x => x.id === s.topicIds[0])
  const mainSections = SECTIONS.filter(sec => s[sec.key])
  const extras = Object.entries(s.extraSections ?? {})

  return (
    <article className="space-y-6">
      <div>
        <Link to="/learn/seminars" className="text-xs text-stone-500 hover:text-stone-900">← Vsi seminarji</Link>
        <div className="kicker mt-3 mb-1">SEMINARSKA NALOGA {String(s.n).padStart(2, "0")}</div>
        <h1 className="font-display text-3xl font-semibold tracking-tight leading-tight">
          {t ? t.title : s.title.replace(/^\d+\.\s*/, "")}
        </h1>
        <p className="text-xs text-stone-500 mt-1">Mapa: {s.folderName}</p>
      </div>

      {s.studentWorkSummary && (
        <section className="card !p-5 border-l-4 border-l-blue-600">
          <h2 className="font-semibold text-sm mb-2">📚 Povzetek študentskega dela</h2>
          <p className="text-sm leading-relaxed text-stone-800">{s.studentWorkSummary}</p>
        </section>
      )}

      {s.articleSummary && (
        <section className="card !p-5 border-l-4 border-l-purple-600">
          <h2 className="font-semibold text-sm mb-2">📄 Povzetek znanstvenega članka</h2>
          <p className="text-sm leading-relaxed text-stone-800">{s.articleSummary}</p>
        </section>
      )}

      {mainSections.length > 0 && (
        <div className="space-y-4">
          {mainSections.map(sec => (
            <section key={sec.key} className="card !p-5">
              <h2 className="font-semibold text-sm mb-2">{sec.icon} {sec.label}</h2>
              <Content text={s[sec.key]} />
            </section>
          ))}
          {extras.map(([k, v]) => (
            <section key={k} className="card !p-5">
              <h2 className="font-semibold text-sm mb-2">📌 {k}</h2>
              <Content text={v} />
            </section>
          ))}
        </div>
      )}

      {s.essay && (
        <section className="card !p-6">
          <h2 className="font-semibold text-sm mb-3">📄 Študentska seminarska naloga{s.studentWorkFile ? ` (${s.studentWorkFile})` : ""}</h2>
          <p className="text-sm leading-relaxed text-stone-800 whitespace-pre-line">{s.essay}</p>
          <p className="text-xs text-stone-400 mt-3">⚠️ Izvleček — celotno delo v mapi seminarskih nalog.</p>
        </section>
      )}

      {mainSections.length === 0 && !s.essay && (
        <div className="card !p-5 border-amber-300 bg-amber-50/50">
          <p className="text-sm text-stone-700">⚠️ Pasport za to temo ni bil mogoče avtomatsko izlužiti — uporabi datoteke iz korpusa spodaj.</p>
        </div>
      )}

      <section className="card !p-5">
        <h2 className="font-semibold text-sm mb-3">📚 Študentski pisni izdelki in gradiva ({s.files.length})</h2>
        <ul className="text-xs space-y-1.5">
          {s.files.map(f => (
            <li key={f} className="flex items-center gap-2 text-stone-700">
              <span className="text-stone-400">{f.endsWith(".docx") ? "📝" : /članek|clanek|article|Declaration|Schrijver|Klabbers|Castellino|walz/i.test(f) ? "📄" : "📕"}</span>
              <span className="font-mono">{f}</span>
              {s.studentWorkFile === f && <span className="badge bg-blue-100 text-blue-800 text-[10px]">izluženo zgoraj</span>}
            </li>
          ))}
        </ul>
      </section>

      <section className="card !p-5 border-blue-300 bg-blue-50/40">
        <h2 className="font-semibold text-sm mb-2">🎯 Povezava na izpitna vprašanja</h2>
        <p className="text-xs text-stone-600 mb-3">Izpitna vprašanja prihajajo tudi iz te seminarske naloge. Vadba za to temo:</p>
        <div className="flex flex-wrap gap-2">
          <Link to="/practice/quiz" className="btn !py-2 !px-3 text-xs">📝 Vprašanja</Link>
          <Link to="/practice/flashcards" className="btn-ghost !py-2 !px-3 text-xs">⚡ Flashcards</Link>
          {t && <Link to={`/exam/guide/${t.id}`} className="btn-ghost !py-2 !px-3 text-xs">📖 Pasport v vodniku</Link>}
        </div>
      </section>
    </article>
  )
}
