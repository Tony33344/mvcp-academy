import { glossary, AUTHORITY_LABELS } from '../lib/data'

export default function About() {
  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-xl font-bold">ℹ️ O aplikaciji</h1>
        <p className="text-sm text-stone-600 mt-1">
          MVČP Academy je izobraževalno orodje za mednarodno varstvo človekovih pravic (FDV UL, prof. dr. Petra Roter).
        </p>
      </div>

      <section className="card">
        <h2 className="font-semibold text-sm mb-2">Metoda učenja (zakaj tako?)</h2>
        <ul className="text-sm list-disc pl-5 space-y-1.5 text-stone-800">
          <li><strong>Retrieval practice</strong> — vadba z odgovarjanjem je najučinkovitejša tehnika (Dunlosky 2013; meta-analiza 242 študij, d≈0,56).</li>
          <li><strong>Razpršeno ponavljanje</strong> — FSRS razporejevalnik razporedi kartice po pozabi.</li>
          <li><strong>Interleaving</strong> — mešanje tem olajša ločevanje podobnih pojmov.</li>
          <li><strong>Takojšnja povratna informacija</strong> — vsak odgovor z virom.</li>
          <li><strong>Metakognicija</strong> — ocena zaupanja odkrije pretirano samozavest.</li>
        </ul>
      </section>

      <section className="card">
        <h2 className="font-semibold text-sm mb-2">Ravni avtoritete virov</h2>
        <ul className="text-sm space-y-1">
          {Object.entries(AUTHORITY_LABELS).map(([k, v]) => (
            <li key={k}><span className="font-mono font-bold">{k}</span> — {v}</li>
          ))}
        </ul>
        <p className="text-xs text-stone-600 mt-2">
          ⚠️ Vprašanja z oznako E so spomini študentov — preveri pred izpitom. Generirane variante so označene.
        </p>
      </section>

      <section className="card">
        <h2 className="font-semibold text-sm mb-2">Slovar (sl/en)</h2>
        <dl className="text-sm space-y-2">
          {glossary.map(g => (
            <div key={g.term}>
              <dt className="font-medium">{g.term}</dt>
              <dd className="text-stone-700 text-xs">{g.sl}</dd>
            </div>
          ))}
        </dl>
      </section>

      <section className="card">
        <h2 className="font-semibold text-sm mb-2">Zasebnost</h2>
        <p className="text-sm text-stone-800">
          Brez računov, brez analitike, brez strežnika. Napredek je shranjen lokalno (IndexedDB).
          Izvozi varnostno kopijo (Napredek → Izvozi), ker iOS Safari lahko izbriše lokalne podatke po daljši neaktivnosti.
        </p>
      </section>

      <section className="card">
        <h2 className="font-semibold text-sm mb-2">Namestitev</h2>
        <ul className="text-sm list-disc pl-5 space-y-1 text-stone-800">
          <li><strong>Android/Chrome:</strong> meni → »Namesti aplikacijo«.</li>
          <li><strong>iOS/Safari:</strong> Share → »Add to Home Screen« (ročno, 4 koraki).</li>
          <li><strong>Desktop:</strong> ikona namestitve v naslovni vrstici.</li>
        </ul>
      </section>

      <section className="card">
        <h2 className="font-semibold text-sm mb-2">Napaka v vsebini?</h2>
        <p className="text-sm text-stone-800">
          Prijavi na: <a className="text-blue-600 underline" href="mailto:?subject=MVCP%20Academy%20—%20napaka%20v%20vsebini">e-pošta z opisom napake</a>
          (vključi ime entitete/vprašanja in pravilen podatek z virom).
        </p>
      </section>

      <section className="card">
        <h2 className="font-semibold text-sm mb-2">Avtorske pravice</h2>
        <p className="text-xs text-stone-600">
          Vsebina je sinteza javnih virov (OHCHR, UN, Svet Evrope) in lastnih učnih zapiskov.
          Profesorici gradiva in študentska dela niso razpečavana — prikazane so le derivirane povzetke z navedbo virov.
          Knjiga <em>Dokumenti človekovih pravic</em> je indeksirana (kazipot členov), ne reproducirana.
        </p>
      </section>
    </div>
  )
}
