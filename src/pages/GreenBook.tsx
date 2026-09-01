import { greenbook } from '../lib/data'

export default function GreenBook() {
  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-xl font-bold">📗 Zeleni priročnik — kazipot členov</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          <em>Dokumenti človekovih pravic z uvodnimi pojasnili</em> (Cerar/Jamnikar/Smrkolj) — dovoljena na izpitu.
          Uporabi jo <strong>samo za točen prepis členov</strong>, ne za učenje. Ta kazipot poveže temo → točne člene.
        </p>
      </div>
      <div className="card">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-300 dark:border-slate-700 text-left">
              <th className="py-2 pr-3">Tema</th>
              <th className="py-2">Členi / dokumenti</th>
            </tr>
          </thead>
          <tbody>
            {greenbook.map(g => (
              <tr key={g.topic} className="border-b border-slate-100 dark:border-slate-800 align-top">
                <td className="py-2.5 pr-3 font-medium whitespace-nowrap">{g.topic}</td>
                <td className="py-2.5 text-slate-600 dark:text-slate-300">{g.articles}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="card bg-amber-50 dark:bg-amber-950 border-amber-200 dark:border-amber-800">
        <h2 className="font-semibold text-sm mb-1">💡 Open-book taktika</h2>
        <ul className="text-sm list-disc pl-5 space-y-1 text-slate-700 dark:text-slate-300">
          <li>Ne uči se iz knjige — uporabi kazipot za takojšnje sklicevanje med pisanjem.</li>
          <li>Označi (zavihki) ključne strani: SDČP, MPDPP, MPESKP, EKČP, CAT, CRC, CEDAW.</li>
          <li>Če člena ni v knjigi (ICPED, ICRMW, OP-ji) — nauči se ga na pamet ali uporabi OHCHR.</li>
          <li>Citiraj natančno: »MPDPP, čl. 6« ne »pakt o življenju«.</li>
        </ul>
      </div>
    </div>
  )
}
