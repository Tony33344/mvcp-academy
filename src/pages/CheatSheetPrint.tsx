import { core, topics, greenbook } from '../lib/data'

export default function CheatSheetPrint() {
  return (
    <div className="max-w-4xl mx-auto space-y-8 p-4 bg-white text-black font-sans text-xs leading-relaxed">
      {/* Header */}
      <div className="border-b-2 border-black pb-4 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold uppercase tracking-tight">MVČP — ULTRA CHEAT SHEET (ZADNJI DAN PRED IZPITOM)</h1>
          <p className="text-xs text-stone-600 mt-1">FDV UL · prof. dr. Petra Roter · 75 min · min. 35/60 točk · dovoljena knjiga Dokumenti ČP</p>
        </div>
        <button
          onClick={() => window.print()}
          className="no-print btn !bg-black !text-white text-xs py-1.5 px-3"
        >
          🖨️ Natisni (A4)
        </button>
      </div>

      {/* 10 CORE BLOCKS CONDENSED */}
      <section className="space-y-2">
        <h2 className="font-bold text-sm uppercase bg-stone-100 p-1.5 border-l-4 border-black">
          I. 10 TOČK JEDRA (NA VSAKEM IZPITU — OBLIKA: ALINEJE)
        </h2>
        <div className="grid grid-cols-2 gap-3 text-[11px]">
          <div className="p-2 border border-stone-300 rounded">
            <strong>1. Zgodovinski razvoj:</strong>
            <ul className="list-disc pl-4 space-y-0.5 mt-1">
              <li>Hamurabi (~1700 pr.n.št.): predpostavka nedolžnosti, dokazi obeh strani.</li>
              <li>Magna Carta 1215: kralj podrejen zakonu, določili 39/40 (predhodnica habeas corpus).</li>
              <li>Angleška listina 1689: suverenost parlamenta, svobodne volitve, brez krutih kazni.</li>
              <li>ZDA 1776: prirojene, neodtujljive pravice (življenje, svoboda, sreča).</li>
              <li>Francoska 1789: univerzalnost (vedno, povsod), suverenost ljudstva.</li>
            </ul>
          </div>

          <div className="p-2 border border-stone-300 rounded">
            <strong>2. Vincent — 5 elementov pravice:</strong>
            <ul className="list-disc pl-4 space-y-0.5 mt-1">
              <li>① Subjekt (individualni / kolektivni — problem: kdo je narod?).</li>
              <li>② Objekt (DO nečesa — pozitivna / PRED nečim — negativna).</li>
              <li>③ Uveljavljanje (paradoks posesti: imaš formalno, ne uživaš).</li>
              <li>④ Nosilec dolžnosti (država; <strong>Shue 3 dolžnosti:</strong> izogibanje, zaščita, pomoč).</li>
              <li>⑤ Utemeljitev (moralna racionalnost).</li>
            </ul>
          </div>

          <div className="p-2 border border-stone-300 rounded">
            <strong>3. Mednarodni režim (3 elementi) + ravni:</strong>
            <ul className="list-disc pl-4 space-y-0.5 mt-1">
              <li>3 elementi: <strong>Načela</strong>, <strong>Norme in pravila</strong>, <strong>Nadzorni mehanizmi</strong>.</li>
              <li>Večnivojskost: nobena raven sama ne zadostuje (globalna → regionalna → subregionalna → nacionalna → lokalna).</li>
            </ul>
          </div>

          <div className="p-2 border border-stone-300 rounded">
            <strong>4. Pogodbeni vs. Splošni nadzorni mehanizmi:</strong>
            <ul className="list-disc pl-4 space-y-0.5 mt-1">
              <li><strong>Pogodbeni (treaty-based):</strong> Odbor za ČP (18 strokovnjakov, MPDPP čl. 28), CESCR, CAT odbor. Samo pogodbenice! Priporočila (sprejme/delno/zavrne).</li>
              <li><strong>Splošni (charter-based):</strong> Svet za ČP (47 držav, UPR, Ženeva). Vse članice OZN! (Prej Komisija za ČP 1946–2006 — politizirana).</li>
            </ul>
          </div>

          <div className="p-2 border border-stone-300 rounded">
            <strong>5. Običaj vs. Pogodba (ICJ 38(1)(b)):</strong>
            <ul className="list-disc pl-4 space-y-0.5 mt-1">
              <li>Običaj: <em>state practice</em> + <em>opinio juris</em>. Zavezuje vse države!</li>
              <li>Izjema: <strong>persistent objector</strong> (dosledni ugovarjalec od začetka).</li>
              <li>Pazi: za <strong>jus cogens</strong> (mučenje, genocid) izjeme NE veljajo!</li>
            </ul>
          </div>

          <div className="p-2 border border-stone-300 rounded">
            <strong>6. ESČP formacije & mandat:</strong>
            <ul className="list-disc pl-4 space-y-0.5 mt-1">
              <li>Trenutno <strong>46 sodnikov</strong> (Rusija izključena 2022 — ne pisati 47!).</li>
              <li>Mandat <strong>9 let brez ponovne izvolitve</strong> (P14 čl. 23).</li>
              <li>Kandidat mora biti <strong>mlajši od 65 let</strong> (P15 odpravil mejo 70 let).</li>
              <li>Rok za pritožbo skrajšan s 6 na <strong>4 mesece</strong> po čl. 35 (P15).</li>
              <li>Formacije: Posameznik, Odbori (3), Senati (7), Veliki senat (17). Sodba zavezujoča (čl. 46)!</li>
            </ul>
          </div>
        </div>
      </section>

      {/* 16 SEMINAR TOPICS MATRIX */}
      <section className="space-y-2">
        <h2 className="font-bold text-sm uppercase bg-stone-100 p-1.5 border-l-4 border-black">
          II. 16 SEMINARSKIH TEM — HITRI KAZIPOT (VIR + ČLEN + AVTOR/PRIMER)
        </h2>
        <table className="w-full text-[10px] border-collapse border border-black">
          <thead>
            <tr className="bg-stone-200 text-left">
              <th className="border border-black p-1 w-28">Tema</th>
              <th className="border border-black p-1">Pravni vir in točen člen</th>
              <th className="border border-black p-1">Nadzor</th>
              <th className="border border-black p-1">Ključni avtor / primer / past</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border border-black p-1 font-bold">1. Življenje</td>
              <td className="border border-black p-1">MPDPP 6; EKČP 2; 13. protokol (odprava smrtne kazni)</td>
              <td className="border border-black p-1">ESČP; Odbor za ČP</td>
              <td className="border border-black p-1"><strong>Osman v. UK</strong> (pozitivna obveznost varovanja življenja); femicid.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">2. Mučenje</td>
              <td className="border border-black p-1">CAT 1984 čl. 1 (4 elementi); čl. 2 (absolutnost); čl. 3 (non-refoulement)</td>
              <td className="border border-black p-1">Odbor proti mučenju (čl. 22); SPT+NPM (OPCAT)</td>
              <td className="border border-black p-1"><strong>Tate 2013</strong>; Guantanamo (waterboarding); jus cogens.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">3. Izginotja</td>
              <td className="border border-black p-1">ICPED 2006 čl. 2 (2 elementa: odvzem + zanikanje); čl. 5 (človeškost)</td>
              <td className="border border-black p-1">Odbor za prisilna izginotja</td>
              <td className="border border-black p-1"><strong>Velásquez-Rodríguez</strong>; CIA extraordinary rendition; neprekinjena kršitev.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">4. Otroci</td>
              <td className="border border-black p-1">CRC 1989 čl. 1 (&lt;18); čl. 3 (najboljša korist); P2 (konflikti), P3 (pritožbe)</td>
              <td className="border border-black p-1">Odbor za otrokove pravice</td>
              <td className="border border-black p-1"><strong>Holzscheiter 2019</strong>; Kongo kobalt; ZDA niso ratificirale!</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">5. Ženske</td>
              <td className="border border-black p-1">CEDAW 1979 čl. 1 (diskriminacija); OP 1999; Istanbulska 2011</td>
              <td className="border border-black p-1">CEDAW odbor</td>
              <td className="border border-black p-1"><strong>Mohajan 2022</strong> (4 valovi); Peking 1995; formalna vs. dejanska enakost.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">6. Invalidi</td>
              <td className="border border-black p-1">CRPD 2006 čl. 2 (primerna prilagoditev), 9 (dostopnost), 12 (sposobnost)</td>
              <td className="border border-black p-1">CRPD odbor</td>
              <td className="border border-black p-1"><strong>Oliver</strong> (medicinski → socialni model); <strong>Berghs 2019</strong>.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">7. Begunci</td>
              <td className="border border-black p-1">Konvencija 1951 čl. 1A(2) (utemeljen strah, 5 razlogov); čl. 33 (non-refoulement)</td>
              <td className="border border-black p-1">UNHCR; ESČP</td>
              <td className="border border-black p-1"><strong>Di Nunzio 2023</strong> (Italija–Libija pullbacks); razlika begunec vs. migrant.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">8. Migranti</td>
              <td className="border border-black p-1">ICRMW 1990 čl. 2(1) definicija delavca migranta</td>
              <td className="border border-black p-1">CMW odbor</td>
              <td className="border border-black p-1">Nizka ratifikacija (samo države izhoda); Sredozemlje.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">9. ESKP</td>
              <td className="border border-black p-1">MPESKP čl. 2(1) progresivna realizacija; čl. 6 delo, 11 bivanje, 12 zdravje</td>
              <td className="border border-black p-1">Odbor za ESKP (1985 ECOSOC)</td>
              <td className="border border-black p-1">Minimalno jedro velja TAKOJ; <strong>Breznik/Praznik 2024</strong>.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">10. Okolje</td>
              <td className="border border-black p-1">Stockholm 1972; Aarhuška 1998 (3 procesne pravice); A/RES/76/300 (2022)</td>
              <td className="border border-black p-1">Svet za ČP; sodišča posredno</td>
              <td className="border border-black p-1"><strong>Held v. Montana</strong>; <strong>Ogoni/Shell</strong>; <strong>Karta v. Španija</strong>.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">11. Razvoj</td>
              <td className="border border-black p-1">Deklaracija 1986 (res. 41/128) — NI ZAVEZUJOČA</td>
              <td className="border border-black p-1">Brez posebnega telesa</td>
              <td className="border border-black p-1"><strong>Schrijver</strong> (konvencija) vs. <strong>Subedi</strong> (programski akt).</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">12. Genocid</td>
              <td className="border border-black p-1">Konvencija 1948 čl. II (dolus specialis + 4 skupine + 5 dejanj); čl. IX ICJ</td>
              <td className="border border-black p-1">ICJ (države); ICC (posamezniki)</td>
              <td className="border border-black p-1"><strong>Lemkin 1944</strong>; <strong>Akayesu</strong> (spolno nasilje); R2P 4 načela; Gaza.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">13. Izražanje</td>
              <td className="border border-black p-1">MPDPP 19; EKČP 10 (3-delni test: zakonitost, legitimen cilj, nujnost v demokraciji)</td>
              <td className="border border-black p-1">ESČP; Odbor za ČP (GC 34)</td>
              <td className="border border-black p-1"><strong>Milton 1644</strong>; pozitivna obveznost (medijski pluralizem); Howie 2018.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">14. Veroizpoved</td>
              <td className="border border-black p-1">MPDPP 18; EKČP 9 (forum internum = absolutno; forum externum = omejljivo)</td>
              <td className="border border-black p-1">ESČP; Odbor za ČP</td>
              <td className="border border-black p-1">Reformacija/Luther 1517; verski simboli v šolah; margin of appreciation.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">15. Samoodločba</td>
              <td className="border border-black p-1">MPDPP 1 = MPESKP 1 (identična!); UL OZN 1(2), 55; Afriška 20</td>
              <td className="border border-black p-1">Razpršen nadzor</td>
              <td className="border border-black p-1"><strong>Klabbers 2006</strong>; notranja (avtonomija) vs. zunanja (odcepitev); Palestina.</td>
            </tr>
            <tr>
              <td className="border border-black p-1 font-bold">16. Manjšine</td>
              <td className="border border-black p-1">MPDPP čl. 27; OKVNM 1995/98 (čl. 5, 6, 15); ILO 169 (domorodci)</td>
              <td className="border border-black p-1">Svetovalni odbor (AC); Odbor za ČP</td>
              <td className="border border-black p-1"><strong>Castellino 2010</strong>; DN varstvo za mir (razpad 3 cesarstev); diskriminatornost.</td>
            </tr>
          </tbody>
        </table>
      </section>

      {/* TOP EXAM TRAPS */}
      <section className="space-y-1 border-t-2 border-black pt-3">
        <h2 className="font-bold text-sm uppercase">III. 5 KRITIČNIH PASTI, KJER ŠTUDENTI IZGUBIJO TOČKE</h2>
        <div className="grid grid-cols-2 gap-2 text-[10px]">
          <div className="p-1.5 bg-stone-50 border border-stone-300">
            <strong>⚠️ Odbor za ČP ≠ Svet za ČP:</strong> Odbor ima 18 neodvisnih strokovnjakov po MPDPP čl. 28. Svet za ČP ima 47 držav članic po UL OZN / GA Res 60/251 (UPR).
          </div>
          <div className="p-1.5 bg-stone-50 border border-stone-300">
            <strong>⚠️ MPDPP čl. 41 ≠ Individualne pritožbe:</strong> Čl. 41 ureja MEDDRŽAVNE komunikacije! Individualne pritožbe so v 1. Fakultativnem protokolu (1. OP).
          </div>
          <div className="p-1.5 bg-stone-50 border border-stone-300">
            <strong>⚠️ Pravica do razvoja NI pravno zavezujoča:</strong> Je le deklaracija 1986. Za razliko od okolja (ki je priznano 2022) razvoj nima konvencije.
          </div>
          <div className="p-1.5 bg-stone-50 border border-stone-300">
            <strong>⚠️ Begunec ≠ Migrant:</strong> Begunec ima utemeljen strah pred preganjanjem (5 razlogov, Konvencija 1951). Migrant se seli zaradi ekonomije (ICRMW 1990).
          </div>
        </div>
      </section>
    </div>
  )
}
