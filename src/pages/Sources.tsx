import { sources, docsManifest } from '../lib/data'

export default function Sources() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold">🔗 Viri</h1>
        <p className="text-sm text-stone-600 mt-1">
          Uradni viri: OHCHR, UN, Svet Evrope. Povezave odprejo žive baze; PDF-ji so za offline branje.
        </p>
      </div>

      <section>
        <h2 className="font-semibold mb-3">Baze in vodniki</h2>
        <div className="grid sm:grid-cols-2 gap-3">
          {sources.map(s => (
            <a key={s.id} href={s.url} target="_blank" rel="noopener noreferrer" className="card hover:border-blue-400 block">
              <div className="font-medium text-sm">{s.title} <span aria-hidden>↗</span></div>
              <div className="text-xs text-stone-600 mt-1">{s.body}</div>
            </a>
          ))}
        </div>
      </section>

      <section>
        <h2 className="font-semibold mb-3">Ključni dokumenti (offline)</h2>
        <p className="text-xs text-stone-600 mb-3">
          Prenesi PDF v brskalnik (shranjeno v predpomnilnik service workerja). Viri: OHCHR/UN — javni dokumenti.
        </p>
        <div className="space-y-2">
          {docsManifest.map(d => (
            <div key={d.id} className="card flex items-center justify-between gap-3 !py-3">
              <div>
                <div className="text-sm font-medium">{d.title}</div>
                <div className="text-xs text-stone-600">avtoriteta {d.authority} · {d.topics.join(', ') || 'splošno'}</div>
              </div>
              <a href={`/docs/${d.file}`} target="_blank" rel="noopener noreferrer" className="btn-secondary !py-1.5 !px-3 text-xs shrink-0">
                Odpri/Prenesi
              </a>
            </div>
          ))}
        </div>
        <p className="text-xs text-stone-600 mt-2">
          Če PDF ni prenesen, uporabi povezavo na uradni vir zgoraj (OHCHR → pogodbeno telo → splošni komentarji).
        </p>
      </section>
    </div>
  )
}
