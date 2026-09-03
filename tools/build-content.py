#!/usr/bin/env python3
"""MVČP Academy — deterministic content pipeline.
Reads verified corpus outputs (canonical graph, master guide data embedded below,
exam files) and generates app JSON into ../src/data/.

Sources of truth:
  A = primary treaty/UN texts (verified in corpus)
  B = professor materials (syllabus, kolokvij notes, question bank)
  C = academic articles
  D = student-derived synthesis (master guide)
  E = student-recalled exam questions (labelled)
"""
import json, re, sys
from pathlib import Path

CORPUS = Path("/home/mark/CascadeProjects/mvcp koncni (Copy)")
OUT = Path(__file__).resolve().parent.parent / "src" / "data"
OUT.mkdir(parents=True, exist_ok=True)

def w(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {name}: {len(obj) if isinstance(obj, list) else 'ok'}")

# ============================================================
# 1. ENTITIES — from canonical graph
# ============================================================
cg = json.loads((CORPUS / "graphify-out/canonical/canonical_graph.json").read_text(encoding="utf-8"))
TYPE_SL = {"history": "zgodovina", "treaty": "pogodba", "institution": "institucija",
           "procedure": "postopek", "right": "pravica", "concept": "koncept",
           "problem": "težava", "case": "primer", "author": "avtor", "material": "gradivo", "exam": "izpit"}
entities = []
for n in cg["nodes"]:
    entities.append({
        "id": n["id"], "type": n.get("type", "concept"),
        "typeSl": TYPE_SL.get(n.get("type", "concept"), n.get("type", "concept")),
        "label": n.get("label", n["id"]),
        "facts": n.get("facts", ""),
        "authority": n.get("authority", "B"),
    })
edges = [{"source": e["source"], "target": e["target"], "relation": e["relation"],
          "authority": e.get("authority", "B"), "note": e.get("note", "")} for e in cg["edges"]]
w("entities.json", {"entities": entities, "edges": edges})

# ============================================================
# 2. CORE BLOCKS (10) — from MASTER_STUDY_GUIDE_V2 Part II
# ============================================================
CORE = [
 {"id":"zgodovina","title":"Zgodovinski razvoj varstva ČP","titleEn":"Historical development","points":2,
  "body":"**1. Hamurabijev zakonik (~1700 pr. n. št., Babilon)**: 282 zakonov, **zapisanih, javnih, v pogovornem (akadijskem) jeziku** — dostopni vsakomur; **predpostavka nedolžnosti**; dokazi obeh strani postopka; izrazito varstvo šibkejšega (vdove, sirote, dolžnika). Prvi znani poskus pravne enakosti pred zapisanim pravom.\n\n**2. Magna Carta (1215, Anglija)**: baroni vs. kralj Ivan Brez dežele; **habeas corpus** (določili 39/40 — nihče ne sme biti prijet, zaprt, razlastnjen ali izgnan brez zakonite sodbe vrstnikov); **kralj je podrejen zakonu** (prvič!); nadzor: komisija 25 baronov; koristniki = **fevdalni sloji** (ne vsi ljudje).\n\n**3. Angleška listina pravic (1689)**: listina **parlamenta** (ne ljudstva) — suverenost parlamenta, svoboda govora v parlamentu, svobodne volitve, prepoved krutih in nenavadnih kazni; po slavni revoluciji 1688 (konec absolutizma v Angliji).\n\n**4. Deklaracija neodvisnosti ZDA (1776)**: **naravne, prirojene, neodtujljive pravice** (življenje, svoboda, stremeljstvo po sreči) — pravice prihajajo od Boga/narave, ne od države; **izključeni: sužnji, ženske, staroselci** (paradoks: »vsi ljudje«, a ne vsi).\n\n**5. Francoska deklaracija o pravicah človeka in državljana (1789)**: **univerzalnost** (velja vedno, povsod, za vsakogar); suverenost ljudstva; ključni členi: čl. 1 (svoboda, enakost), čl. 5 (vse, kar ni prepovedano, je dovoljeno), čl. 7 (ni kazni brez zakona), čl. 10 (veroizpoved), čl. 12 (javna sila za dobro vseh), čl. 13 (skupni prispevek za stroške).\n\n**6. Mednarodni razvoj (19.–20. st.)**: verska toleranca po tridesetletni vojni (Vestfalija 1648) → varstvo manjšin → humanitarno pravo (Ženeva 1864/1949, Haag 1899/1907) → **Društvo narodov (1920)**: Pakt DN **NE omenja človekovih pravic**; varstvo manjšin = **za mir in stabilnost novih mej, ne iz humanitarnih vzgibov** — diskriminatoren sistem (obveznosti le za poražene: Avstrija, Bolgarija, Madžarska, Turčija; nove: Poljska, SHS, Češkoslovaška, Romunija, Grčija; kasneje vstopajoče: Finska, Albanija, baltske države, Irak; **zmagovalke izključene**) → **OZN (1945)**: »nikoli več« po holokavstu; UL čl. 1(3): *razvijati* (konvencije) in *spodbujati* (implementacija) spoštovanje ČP.\n\n**Bistvo (izpitna teza):** dokumenti odražajo konflikte in boj — človekove pravice si je bilo treba **izboriti**, niso bile podarjene od zgoraj."},
 {"id":"koncept","title":"Koncept ČP — Vincent: 5 elementov pravice","titleEn":"Concept of human rights — Vincent's 5 elements","points":6,
  "body":"**Vincent (1986): 5 elementov pravice** (v rokopisnih vprašanjih »Benko/Fenko elementi MS« = Vincentovi elementi):\n1. **Subjekt** (nosilec pravice): individualne / kolektivne pravice (narod pri samoodločbi — problem: **kdo je »narod«?**); danes tudi pravice prihodnjih generacij in narave (ekocentrični pristop).\n2. **Objekt**: pravica **DO** nečesa (pozitivna — zahteva aktivnost države, npr. pravica do izobraževanja) / pravica **PRED** nečim (negativna — zahteva nevmešavanje, npr. prepoved mučenja).\n3. **Uveljavljanje**: trditi, zahtevati, imeti korist, uživati, opravnomočiti; **paradoks posesti** (formalno imaš pravico, praktično je ne uživaš — npr. pravica do dela pri 20 % brezposelnosti).\n4. **Nosilec dolžnosti**: predvsem **država** (mednarodno pravo veže države); tudi posamezniki (mednarodno kazensko pravo); **Shue: 3 korelativne dolžnosti** — ① izogibanje prikrajšanju (*to avoid depriving*), ② zaščita pred prikrajšanjem (*to protect from deprivation*), ③ pomoč prikrajšanim (*to aid the deprived*).\n5. **Utemeljitev**: moralna racionalnost, filozofska osnova (naravno pravo, dostojanstvo, avtonomija); brez utemeljitve pravica ni univerzalno zavezujoča.\n\n**Načela mednarodnega režima varstva ČP:**\n- **Univerzalnost/splošnost** — veljajo za vse ljudi, povsod, brez izjem (SDČP; izpitno: proti kulturnemu relativizmu).\n- **Neodtujljivost** — pravic se ni mogoče odreči niti prostovoljno (npr. prodaja sebe v suženjstvo).\n- **Nedeljivost** — Dunaj 1993 (Svetovna konferenca o ČP): ni izbire ALI/ALI med pakta; civilno-politične in ekonomske pravice so enako pomembne (proti tezi Macklem: *three generations or one?*).\n- **Soodvisnost/medodvisnost** — kršitev ene pravice ogroža druge (revščina → zdravje → dostojanstvo).\n- **Nediskriminacija** — UL OZN 1(3); SDČP 2; MPDPP 2(1); MPESKP 2(2); EKČP 14; Listina EU 21."},
 {"id":"rezim","title":"Mednarodni režim (3 elementi) + večnivojskost","titleEn":"International regime — 3 elements, multilevel","points":2,
  "body":"**Režim** (v teoriji mednarodnih odnosov) = niz **načel, norm, pravil in odločevalskih postopkov**, okoli katerih se združijo pričakovanja akterjev na določenem področju (*issue area*). Režim za varstvo ČP je področje mednarodnih odnosov (MVČP = podpodročje MO).\n\n**Trije elementi režima za varstvo ČP (izpitno jedro):**\n1. **Načela** (principi — prepričanja o dejstvih, vzrokih in pravičnosti): nedeljivost, univerzalnost, temeljnost ČP.\n2. **Norme in pravila** (konkretna določila — standardi ravnanja): pravica do življenja, svoboda izražanja, prepoved mučenja … (v pogodbah: SDČP, pakta, EKČP …).\n3. **Nadzorni mehanizmi** (institucije, ki nadzorujejo uresničevanje): pogodbeni odbori, Svet za ČP, ESČP …\n\n**Večnivojski režim — nivoji upravljanja (izpitno vprašanje: zakaj večnivojski + nivoji):**\n- **globalna** raven (OZN: Svet za ČP, pogodbena telesa, UPR),\n- **regionalna** (Svet Evrope — EKČP/ESČP, OAD — Medameriški sistem, AU — Afriška listina, arabski sistem),\n- **subregionalna** (EU: Listina EU o temeljnih pravicah, Listina EU čl. 2, 4, 21),\n- **bilateralna** (dvostranski sporazumi, pogajanja o ČP v trgovinskih sporazumih),\n- **nacionalna** (ustava, zakonodaja, varuh človekovih pravic, ustavno sodišče),\n- **lokalna** (občine: dostopnost, socialna pomoč).\n\n**Zakaj večnivojski:** **nobena raven sama ne zadostuje** — globalne norme brez nacionalne implementacije ostajajo na papirju; nacionalni sodišči brez mednarodnega pritiska ne zaščitita manjšin; regionalni sistemi (ESČP) dopolnjujejo OZN sistem z zavezujočimi sodami."},
 {"id":"nadzor","title":"Nadzorni mehanizmi: pogodbeni vs. splošni","titleEn":"Monitoring mechanisms: treaty-based vs charter-based","points":4,
  "body":"**2 vrsti nadzornih mehanizmov (izpitno: 4 točke — navedi obe + primere!):**\n\n**A. Pogodbeni (treaty-based)** — določeni v vsaki pogodbi, veljajo **samo za pogodbenice**:\n- **Odbor za človekove pravice** (MPDPP **čl. 28: 18 neodvisnih strokovnjakov**; poročila držav čl. 40 + priporočila; splošni komentarji — npr. GC 34 izražanje, GC 36 življenje)\n- Odbor za ESKP (CESCR; ustanovljen 1985 z resolucijo ECOSOC 1985/17 — sprva delovno telo ECOSOC)\n- Odbor proti mučenju (CAT: čl. 20 preiskave, 21 meddržavne, 22 individualne), CEDAW Odbor, Odbor za otrokove pravice, Odbor za prisilna izginotja (CED), CMW Odbor, CRPD Odbor\n- Rezultat: **sklepne ugotovitve in priporočila** — država jih lahko **sprejme / delno sprejme / zavrne** (ni prisile!)\n\n**B. Splošni (charter-based)** — iz UL OZN, veljajo za **vse članice OZN**:\n- **Komisija za ČP (1946–2006)**: pomožno telo ECOSOC; **preveč politizirana, kršiteljice ČP so bile v njej** (Libija je 2003 celo predsedovala!) → reforma 2006\n- **Svet za ČP (2006, GA Res 60/251)**: stalno telo v Ženevi, **47 držav** (tajno glasovanje GS, regionalno načelo; mandat 3 leta, največ 2 zaporedna mandata); mehanizmi: **UPR** (vsakih 4–4,5 let), posebni postopki (posebni poročevalci), postopek za pritožbe glede vzorcev hudih kršitev; **mandat lahko preneha državi s hudimi in sistematičnimi kršitvami** (izključitev Libije 2011)\n- **OHCHR** (Visoki komisar za ČP, od 1993; sekretariat pogodbenih teles)\n\n⚠️ **Profesorica izrecno: Odbor za ČP NI ENAKO Svet za ČP!** (Odbor = strokovnjaki, pogodba, priporočila; Svet = države, politika, UPR.)\n\n**UPR — ocena (izpitno: dobro/slabo):**\n- **dobro**: pregled vseh pravic in vseh držav (tudi nepogodbenic!), hitrejše in preglednejše po reformi, dialog med državami;\n- **slabo**: priporočila **neobvezna** (država jih »sprejme ali zabeleži«), politizacija (države sledijo interesom, ne kršitvam), preveč priporočil (100+ na državo) → površnost.\n\n**Individualne pritožbe — 2 načina vzpostavitve pristojnosti (izpitno vprašanje 2. roka 2026):**\n① poseben **opcijski protokol** (1. OP k MPDPP 1966/76, OP CEDAW 1999, OP MPESKP 2008, 3. OP CRC 2011, OP CRPD);\n② **izjava države po členu konvencije** (CAT čl. 22; ICPED čl. 31).\nPogoji: izčrpanje domačih sredstev, ne anonimno, žrtev pod jurisdikcijo države. **MPDPP čl. 41 = meddržavne, NE individualne komunikacije** (individualne so v 1. OP)."},
 {"id":"obicaj","title":"Običajno pravo vs. pogodbeno; jus cogens; persistent objector","titleEn":"Customary vs treaty law","points":2,
  "body":"**Običajno mednarodno pravo (izpitno: vir + 2 elementa):**\n- Vir: **čl. 38(1)(b) Statuta ICJ** — »mednarodni običaj, kot dokaz splošne prakse, sprejete kot pravo«.\n- 2 kumulativna elementa: ① **state practice** (splošna in dosledna praksa držav) + ② **opinio juris sive necessitatis** (prepričanje, da praksa obvezuje kot pravo, ne le iz vljudnosti).\n\n**Razlika od pogodbenega prava:**\n- Običaj zavezuje **vse države** (tudi tiste, ki niso ratificirale nobene pogodbe); edina izjema: **persistent objector** — država, ki je od začetka nastajanja pravila **dosledno, aktivno in eksplicitno nasprotovala** (npr. ZDA pri nekaterih delih morja prava).\n- Izjema **ne velja za jus cogens** (imperativne norme, čl. 53 Dunajske konvencije o pravu pogodb): prepoved mučenja, genocida, suženjstva, agresije, rasne diskriminacije — zavezujejo **brezpogojno**, tudi persistent objectorja.\n- **Člen konvencije zavezuje samo pogodbenice** (po ratifikaciji/pristopu); pogodbe lahko **kodificirajo** obstoječ običaj (npr. Ženevske konvencije) ali **k njegovemu nastanku prispevajo** (npr. CAT → običajna prepoved mučenja).\n- **Erga omnes obveznosti**: dolžnost vseh držav, da preprečijo in kaznujejo genocid (ICJ, Bosna v. Srbija 2007).\n\n**Primeri običajnega prava (izpitno navedi vsaj 3):** prepoved mučenja, prepoved genocida, non-refoulement, prepoved suženjstva, deli SDČP (npr. čl. 1, 2, 5, 6)."},
 {"id":"ratifikacije","title":"Ratifikacijska omrežja — 3 obdobja; kdaj dokument zavezuje","titleEn":"Ratification networks — 3 periods","points":3,
  "body":"**Analiza omrežij ratifikacij (predavanja — izpitno: 3 točke, 3 obdobja):**\n1. **15 let pred koncem hladne vojne (~1975–1989)**: notranji krog ozek, regionalno mešan (avtokratske države Latinske Amerike in Vzhodne Evrope + demokratične EVR); Afrika/Azija praktično izključene; **ZDA nič ne ratificirajo** (strah pred notranjimi posledicami).\n2. **Ob koncu hladne vojne (~1989–1991)**: krog se širi (+10 držav: Latinska Amerika, Madžarska, Sirija …); Jugoslavija izstopi iz notranjega kroga; Afrika/Azija začenjajo; ZDA še vedno na obrobju.\n3. **15 let po koncu hladne vojne (~1990–2005)**: vse države imajo vsaj 1 pogodbo — sistem **resnično svetoven**; razpad blokov → bivše komunistične države množično ratificirajo (pogoj za vključitev v OZN/Sveto Evrope); notranji krog = države, ki iščejo **odobravanje in legimitacijo**.\n\n**Kdaj dokument postane pravno zavezujoč (izpitno!):**\n- ratifikacija **35 držav** (pakta MPDPP/MPESKP — čl. 49 oziroma 26 MPESKP) / **10 držav** (opcijski protokoli) + **notranja potrditev** (pri nas: ratifikacija v Državnem zboru RS, objava v UL);\n- izjema: **SFRJ-nasledstvo** (dokumenti, ratificirani pred 1991, zavezujejo naslednice — Slovenija 1992 uradno potrdila);\n- **zadržek (reservation)** = prvi filter: država ob ratifikaciji zapiše, kako bo razumela določilo (npr. zadržki k CAT čl. 20); prepovedani so zadržki, ki so neskladni z objektom in namenom pogodbe (čl. 19 Dunajske konvencije).\n\n**Razlaga pojmov:** ratifikacija (potrditev pogodbe po notranjem postopku) ≠ pristop (accession — vstop v že veljavno pogodbo brez podpisa) ≠ podpis (samo obveza, da ne bo sabotaže)."},
 {"id":"regionalni","title":"Regionalni sistemi + azijske vrednote (Sen)","titleEn":"Regional systems","points":4,
  "body":"- **EKČP (1950/53)**: čl. 2 življenje, 3 mučenje, 9 veroizpoved, 10 izražanje, 14 nediskriminacija\n- **ESČP**: število sodnikov je enako številu pogodbenic EKČP — **trenutno 46 sodnikov** (marca 2022 je bila Rusija po napadu na Ukrajino izključena iz Sveta Evrope; **ne pisati 47!**)\n- **Mandat sodnikov ESČP**: **9 let, brez ponovne izvolitve** (P14 čl. 23); izbira: **Parlamentarna skupščina SE** izmed 3 kandidatov države\n- **P15 k EKČP (1. 8. 2021)**: odpravil starostno mejo 70 let za upokojitev; nov pogoj: kandidat mora biti ob predložitvi liste **mlajši od 65 let**; rok za vložitev pritožbe skrajšan s 6 na **4 mesece** (čl. 35)\n- **Formacije ESČP**: posamezni sodnik / odbori (3) / senati (7) / **Veliki senat (17)**; individualne pritožbe čl. 34; sodba **pravno zavezujoča čl. 46** (izvrševanje nadzira Odbor ministrov SE); **P14** = reforma zamašitve (backlog)\n- **ESL (1961/1996)**: ekonomske/socialne; **kolektivne pritožbe** (sindikati, NGO) → Evropski odbor za socialne pravice → Odbor ministrov (priporočilo/resolucija)\n- **Ameriška konvencija (1969/78)**: Medameriška komisija (Washington) + Medameriško sodišče (San José); čl. 4 (življenje varovano »od spočetja«)\n- **Afriška listina (1981/86** — samoodločba ljudstev čl. 20, dolžnosti posameznika čl. 27–29); **Arabska listina (1994; 2004/08)**; **Azija: ni regionalne listine**\n- **Azijske vrednote — Sen (2015)**: kulturni relativizem = **izgovor** avtoritarnih režimov za zatiranje svobode; univerzalnost in dostojanstvo sta skladna z azijskimi tradicijami; + Jenco 2013, Lind 2009\n- **Populizem**: Roth 2017; **Helfer 2020** (avtokrati napadajo institucije ČP, spodkopavajo sodbe, grozijo z izstopom)"},
 {"id":"listina","title":"Listina človekovih pravic + zakaj 2 pakta","titleEn":"International Bill of Rights","points":2,
  "body":"**Listina človekovih pravic (International Bill of Rights)** = trije dokumenti:\n1. **SDČP (1948)** — Splošna deklaracija človekovih pravic;\n2. **MPDPP (1966/1976)** — Mednarodni pakt o državljanskih in političnih pravicah;\n3. **MPESKP (1966/1976)** — Mednarodni pakt o ekonomskih, socialnih in kulturnih pravicah.\n\n**Zakaj 2 pakta namesto 1 konvencije (izpitno: 3 razlogi):**\n1. **razmerje mednarodnega varstva ČP ↔ nacionalna suverenost**: komunistični blok se je vzdržal glasovanja o SDČP; za zavezujočo pogodbo ni bilo konsenza;\n2. **interes posameznika (Zahod) vs. interes skupnosti (Vzhod)**: Zahod poudarja svobodo od države, Vzhod varstvo s strani države;\n3. **vsebina ČP**: Zahod = civilno-politične (1. generacija); Vzhod/Jug = ekonomske-socialne (2. generacija); bogati (Sever) vs. revni (Jug).\n\n**Generacije ČP (Karel Vasak):**\n- **1. civilno-politične** (svoboda od države; MPDPP) — takojšnja implementacija;\n- **2. ekonomske-socialne-kulturne** (svoboda ZA, od države; MPESKP) — progresivna realizacija;\n- **3. solidarnostne** (razvoj, okolje, mir, pomoč — pogosto nezavezujoče deklaracije).\n- **Macklem (2015): *three generations or one?*** — kritika delitve; **nedeljivost** (Dunaj 1993): pravice niso hierarhične.\n\n**SDČP — ključna dejstva (izpitno!):** resolucija GS OZN **217 A (III)**, sprejeta **10. 12. 1948** (dan ČP = 10. december); **30 členov**; **politično, ne pravno zavezujoča** (deklaracija, ne pogodba — toda deli so se razvili v običajno pravo); čl. 1 (dostojanstvo, enakost, bratstvo), čl. 2 (nediskriminacija), čl. 3–21 (civilno-politične), čl. 22–27 (ekonomske-socialne); predsednica pripravljalne komisije: **Eleanor Roosevelt** (Glendon 2001: *A World Made New*)."},
 {"id":"dn_ozn","title":"DN → OZN: vloga in prelomi","titleEn":"League of Nations → UN","points":2,
  "body":"**Društvo narodov (1920) — omejen prispevek (izpitno: Pakt NE omenja ČP!):**\n- Pakt DN **NE vsebuje splošne klavzule o človekovih pravicah** (duh časa: suverenost, kolonializem);\n- toda: prepoved suženjstva v **nesamoupravnih ozemljih** (čl. 22 mandatni sistem), svoboda misli in veroizpovedi, ILO (humani delovni pogoji — še danes del OZN sistema), nadzor bolezni (→ kasneje WHO), humanitarno delo Rdečega križa;\n- **varstvo manjšin v DN**: po razpadu 3 cesarstev (Avstro-Ogrskega, Otomanskega, Ruskega) → nove heterogene države → manjšine = nevarnost za stabilnost → norme **za mir, ne humanitarno**; **diskriminatoren sistem** (obveznosti samo za poražene/nove/vstopajoče države, zmagovalke izključene); nadzor pri DN (spori → Stalno sodišče mednarodne pravice); **ni preprečil 2. svetovne vojne**;\n- prispevek: prvi poskus **zaščite posameznikov/skupnosti** prek mednarodnih pogodb, a brez sistematičnega pristopa in brez univerzalnosti.\n\n**OZN (1945) — prelom (izpitno: »nikoli več«):**\n- holokavst in 2. svetovna vojna → ČP = **sestavni del miru in varnosti** (ne ločeno področje!);\n- **UL OZN NE vsebuje seznama ČP** — le okvir: čl. 1(3) (mednarodno sodelovanje pri *razvijanju* — konvencije — in *spodbujanju* — implementacija — spoštovanja ČP), čl. 55–56 (ECOSOC: sodelovanje gospodarsko-socialno), čl. 62 (ECOSOC lahko pripravi osnutke priporočil), čl. 68 (pomožna telesa → Komisija za ČP 1946);\n- omejitev: **suverenost** (čl. 2(7) — nevmešavanje v notranje zadeve; ČP sprva »notranja zadeva«);\n- **ECOSOC → Komisija za ČP (1946) → Svet za ČP (2006)**;\n- **SDČP (1948)**: skupni ideal; pravice pripadajo **z rojstvom**, neodtujljive, univerzalne (proti DN diskriminatornemu sistemu)."},
 {"id":"aktualno","title":"Aktualne teme: Gaza, Ukrajina, AI, populizem, relativizem","titleEn":"Current events","points":4,
  "body":"Izpit izrecno preverja »razumevanje aktualnih dogodkov v mednarodni skupnosti glede varstva ČP oz. kršitev človekovih pravic« (Izvedbeni načrt). Za vsako temo: norma + primer + kritika.\n\n- **Gaza (od 2023)** → vprašanje genocida: čl. II Konvencije o genocidu (**dolus specialis** — posebni namen uničiti skupino), postopek pred **ICJ po čl. IX** (JAR v. Izrael, 2024 — začasni ukrepi); **pomanjkljivosti konvencije**: izjemen dokaz namere, enforcement (ICJ nima prisilne moči), politika (veto v VS OZN), ozke 4 skupine (brez političnih/socialnih).\n- **Ukrajina (od 2022)** → **2 najbolj kršeni normi** (izpitno vprašanje 2. roka 2026): ① **pravica do življenja** (MPDPP čl. 6 / EKČP čl. 2 — napadi na civiliste, infrastrukturo) in ② **prepoved mučenja ter prisilnih izginotij** (MPDPP čl. 7, CAT, ICPED — filtracijski tabori, deportacije otrok = genocidno dejanje čl. II(e)!); okvir: mednarodno humanitarno pravo (Ženevske konvencije 1949).\n- **AI/mediji** → svoboda izražanja: negativni/pozitivni aspekt; **algoritemska cenzura**, dezinformacije, deepfakes, SLAPP tožbe; zasebnost in nadzor nad podatki (film **Citizenfour** — Snowden, masovni nadzor); regulacija: EU AI Act, DSA.\n- **Populizem** → **Helfer (2020)** (survival guide: kako institucije ČP preživijo napade — prilagoditev, koalicije, javna komunikacija) in **Roth (2017)** (napad populizma na vrednote ČP); avtokrati spodkopavajo sodbe ESČP, grozijo z izstopom, označujejo NVO za tuje agente.\n- **Kulturni relativizem** → **Sen (2015)**: relativizem = **izgovor** avtoritarnih režimov; univerzalnost združljiva z azijskimi tradicijami (budizem, konfucijanstvo, islam poznajo dostojanstvo in toleranco); + Jenco (2013), Lind (2009)."},
]
w("core.json", CORE)

# ============================================================
# 3. 16 SEMINAR PASSPORTS
# ============================================================
TOPICS = [
 {"id":"zivljenje","n":1,"title":"Pravica do življenja","titleEn":"Right to life","status":"seminar",
  "legal":"MPDPP čl. 6 (omejitve: smrtna kazen le po pravnomočni sodbi pristojnega sodišča za najtežja kazniva dejanja, nuja, zakonit vojni akt); EKČP čl. 2; **13. protokol k EKČP** (popolna odprava smrtne kazni v vseh okoliščinah, tudi v vojni); 6. protokol k EKČP (odprava v miru); Afriška listina čl. 4; **Ameriška konvencija čl. 4 (pravica do življenja varovana »od spočetja«!)**; narava: delno derogabilna v vojni (zakonita bojna dejanja po mednarodnem humanitarnem pravu).",
  "monitoring":"ESČP (pravno zavezujoča sodba čl. 46); Odbor za ČP (Splošni komentar 36 — široka razlaga, pozitivne obveznosti za zdravje in okolje); Medameriško sodišče za ČP.",
  "problems":"**Pozitivne in procesne obveznosti države**: država mora aktivno varovati življenje in učinkovito ter neodvisno preiskati vsako sumljivo smrt → **Osman v. United Kingdom** (ESČP: pozitivna obveznost oblasti preprečiti resnično in neposredno grožnjo življenju s strani tretjih oseb); **smrtna kazen** (moratorij, eksekucije v ZDA, na Kitajskem, v Iranu); **femicid** kot sistemski problem nepripravljenosti policije; odgovornost za smrti v priporu ali policijskem pridržanju.",
  "model":"1. Definicija in narava (temeljna predpostavka vseh pravic) → 2. Globalna raven (MPDPP čl. 6) in regionalna raven (EKČP čl. 2 + 13. protokol popolne odprave; AmK čl. 4 »od spočetja«) → 3. Negativne obveznosti (država ne ubija) vs. pozitivne obveznosti (zaščita, preiskava) → 4. Test dopustnosti posega (nuja, zakonita vojna dejanja) → 5. Vodilni primer: **Osman v. UK** + aktualni primeri (femicid, smrt v priporu).",
  "materials":["MVČP_life.pdf","01_pravica_do_zivljenja.md","Vzorec-Pravice do življenja"]},
 {"id":"mucenje","n":2,"title":"Prepoved mučenja","titleEn":"Prohibition of torture","status":"jedro+seminar",
  "legal":"**CAT 1984 čl. 1 — 4 kumulativni elementi definicije**: ① namerna povzročitev ② hude fizične ali duševne bolečine/trpljenja ③ za določen namen (izsilitev priznanja, zastraševanje, kaznovanje, diskriminacija) ④ s strani uradne osebe ali z njeno privolitvijo/vednostjo; **izrecno izključene**: bolečine, ki izhajajo zgolj iz zakonitih sankcij; **čl. 2 absolutnost** (nobenih izjem, niti vojna, vojna nevarnost ali izredno stanje — derogacija prepovedana); **čl. 3 non-refoulement** (prepoved izgona/vračanja v državo, kjer grozi mučenje); MPDPP čl. 7; EKČP čl. 3; SDČP čl. 5; **jus cogens** (imperativna norma običajnega prava).",
  "monitoring":"Odbor proti mučenju (CAT Odbor): čl. 19 periodična poročila, čl. 20 preiskovalni postopek (inquiry), čl. 21 meddržavne pritožbe, čl. 22 individualne pritožbe (ob izrecni izjavi države); ESČP čl. 3; **ICJ čl. 30 CAT** za spore med državami glede razlage/uporabe; **OPCAT 2002**: preventivni sistem — SPT (Pododbor za preprečevanje mučenja OZN) + NPM (nacionalni preventivni mehanizmi pri varuhu človekovih pravic) z nenapovedanimi obiski zaporov in priporov.",
  "problems":"**Tate (2013)**: zakaj absolutna prepoved v praksi zataji — argument »tempirane bombe« (*ticking bomb*), tajni pripori (black sites), izročanje (*extraordinary rendition*); **Guantanamo / ZDA** (waterboarding, odrekanje spanca kot eufemizem »okrepljene zasliševalne metode«); regionalne razlike (Medameriški sistem izpostavlja psihično mučenje, afriški sistem tradicije in suženjstvo); **paradoks posesti** (norma velja, a se krši); nepripravljenost držav, da preganjajo lastne policiste in obveščevalce.",
  "model":"1. Zgodovina (prvič v Ženevskih konvencijah za vojne ujetnike) → 2. Najnatančnejša definicija: **CAT čl. 1 (4 elementi!)** + izjema zakonitih sankcij → 3. Pravna narava: **čl. 2 absolutnost** + **jus cogens** (nič izjem!) + čl. 3 non-refoulement → 4. Nadzor: Odbor proti mučenju (čl. 20–22), ESČP, ICJ čl. 30, OPCAT (SPT + NPM) → 5. Kritika in praksa: **Tate (2013)**, Guantanamo, ticking bomb.",
  "materials":["p. 2. povzetek-prepoved-mucenja-v2.pdf","P2_Prepoved mučenja_pisni izdelek.pdf","02_prepoved_mucenja.md","OPCAT quicksheet"]},
 {"id":"izginotja","n":3,"title":"Varstvo pred prisilnimi izginotji","titleEn":"Enforced disappearances","status":"seminar",
  "legal":"**ICPED 2006 (Mednarodna konvencija o varstvu vseh oseb pred prisilnim izginotjem)**: **čl. 1 nederogabilnost** (nobene izjemne okoliščine ne opravičujejo izginotja); **čl. 2 definicija — 2 kumulativna elementa**: ① odvzem prostosti s strani državnih organov (ali oseb z njihovo podporo) + ② zavrnitev priznanja odvzema prostosti ali prikrivanje usode/nahajališča osebe; čl. 4 dolžnost kriminalizacije v domačem pravu; **čl. 5**: razširjena ali sistematična praksa pomeni **zločin proti človeškosti**; čl. 6 individualna kazenska odgovornost nadrejenih (*command responsibility*); čl. 24 pravica žrtev in svojcev do resnice.",
  "monitoring":"Odbor za prisilna izginotja (CED): čl. 29 poročila, čl. 30 nujni postopek ukrepanja (*urgent action* na zahtevo svojcev), čl. 31 individualne pritožbe (ob izjavi države), čl. 32 meddržavne komunikacije, čl. 33 preiskave na terenu ob resnih kršitvah; Delovna skupina OZN za prisilna izginotja (WGEID, charter-based); ESČP (prek čl. 2, 3, 5); Medameriško sodišče za ČP.",
  "problems":"**Velásquez-Rodríguez v. Honduras (1988)**: prelomna sodba Medameriškega sodišča — država je odgovorna za prisilno izginotje, če tolerira *clandestine repression* in ne izvede neodvisne ter učinkovite preiskave; doktrina **trajajoče kršitve** (*ongoing violation* — zastaranje ne začne teči, dokler usoda osebe ni pojasnjena); primeri: Latinska Amerika (operacija Kondor, »umazana vojna« v Argentini in Čilu), Sirija (več kot 100.000 izginulih v Asadovih zaporih), ruska okupacija v Ukrajini (ugrabitve civilistov in županov).",
  "model":"1. Izvor (latinskoameriške diktature 70. in 80. let) → 2. Definicija po **čl. 2 ICPED (odvzem prostosti + zanikanje/prikrivanje usode)** → 3. Čl. 1 nederogabilnost + čl. 5 zločin proti človeškosti + pravica do resnice (čl. 24) → 4. Nadzor: Odbor CED (nujni postopek čl. 30!) in Medameriško sodišče → 5. Sodna praksa in primer: **Velásquez-Rodríguez (1988)** + Sirija / Ukrajina.",
  "materials":["P1_pogodba.pdf","P1_Varstvo pred prisilnimi izginotji.pdf","Aguilar 2019","ICPED quicksheet"]},
 {"id":"otroci","n":4,"title":"Otrokove pravice","titleEn":"Children's rights","status":"seminar",
  "legal":"**CRC 1989 (Konvencija o otrokovih pravicah)**: **čl. 1 definicija otroka**: vsako človeško bitje pod 18 let; **čl. 3 načelo otrokove največje koristi** (*best interests of the child* — glavno vodilo pri vseh ukrepih); čl. 6 pravica do življenja in razvoja; čl. 12 pravica otroka do izražanja mnenja in participacije; **trije opcijski protokoli**: 1. OP (vključevanje v oborožene spopade), 2. OP (prodaja otrok, otroška prostitucija in pornografija), **3. OP (2011 — komunikacijski postopek za individualne pritožbe)**; globalna veljava: 196 držav pogodbenic (**ZDA so edina članica OZN, ki CRC NI ratificirala!**); regionalno: **Afriška listina o pravicah in blaginji otroka (1990)**.",
  "monitoring":"Odbor za otrokove pravice (CRC Odbor): 18 strokovnjakov; obravnava poročil držav; po 3. OP obravnava individualne pritožbe otrok ali njihovih zastopnikov.",
  "problems":"**Holzscheiter (2019)**: governance otrokovih pravic in napetost med zaščito (*protection*) ter otrokovo avtonomijo/participacijo (*agency*); **290 milijonov neregistriranih otrok** po svetu (»nevidni otroci« brez rojstnega lista, brez dostopa do šole in zdravstva); izkoriščanje otroškega dela (npr. rudarjenje kobalta v DR Kongo); **otroci vojaki** v konfliktih (Sirija, Jemen, DR Kongo, Sudan); prisilne poroke mladoletnic.",
  "model":"1. Razvoj (Ženeva 1924 → Deklaracija 1959 → CRC 1989) → 2. Ključna člena: **čl. 1 (<18)** in **čl. 3 (največja korist)** + čl. 12 (participacija) → 3. Protokoli (1., 2. in **3. OP 2011 pritožbe**) + ZDA niso ratificirale → 4. Težave v praksi: Holzscheiter (avtonomija vs. zaščita), 290 mio neregistriranih, otroci v rudnikih kobalta in otroci vojaki.",
  "materials":["P4_Konvencija_o_otrokovih_pravicah.pdf","otrokove pravice.pdf","04_otrokove_pravice.md"]},
 {"id":"zenske","n":5,"title":"Pravice žensk","titleEn":"Women's rights","status":"seminar",
  "legal":"**CEDAW 1979 (Konvencija o odpravi vseh oblik diskriminacije žensk)**: **čl. 1 celovita definicija diskriminacije** (vsako razlikovanje, izključevanje ali omejevanje na podlagi spola z namenom ali posledico ogrožanja pravic); čl. 2 obveznost odprave diskriminacije v zakonih in praksi; čl. 4 začasni posebni ukrepi (pozitivna diskriminacija/kvote); **Opcijski protokol k CEDAW (1999)**: individualne pritožbe + preiskovalni postopek Odbora; 189 pogodbenic (**ZDA niso ratificirale!**); **Pekinška deklaracija in Izhodišča za ukrepanje (1995)**; regionalno: **Istanbulska konvencija Sveta Evrope (2011)** o preprečevanju in boju proti nasilju nad ženskami in nasilju v družini; Medameriška konvencija Belém do Pará (1994).",
  "monitoring":"Odbor CEDAW (23 neodvisnih strokovnjakinj): periodična poročila; po OP 1999 individualne komunikacije in terenske preiskave resnih/sistematičnih kršitev; GREVIO (nadzorno telo Istanbulske konvencije).",
  "problems":"**Mohajan (2022) — 4 valovi feminizma**: 1. val (19./začetek 20. st. — volilna pravica), 2. val (60.–80. leta — delo, reproduktivne pravice, nasilje), 3. val (90. leta — intersekcionalnost, rasa, spolna usmerjenost), 4. val (po 2012 — digitalni prostor, družbena omrežja, gibanje #MeToo); razkorak med **formalno (de jure)** in **dejansko (de facto) enakostjo**; **femicid** kot skrajna oblika nasilja; plačna vrzel (*gender pay gap*); politični odpor in izstopi iz Istanbulske konvencije (npr. Turčija 2021).",
  "model":"1. Zgodovina 4 valov (Mohajan 2022) → 2. Normativni okvir: **CEDAW čl. 1 (definicija)** + čl. 4 (posebni ukrepi) + OP 1999 (pritožbe) → 3. Regionalni instrumenti: Istanbulska konvencija 2011 → 4. Težave v praksi: femicid, nepriznavanje de facto enakosti, zlorabe v digitalnem prostoru (#MeToo), odpovedi pogodb.",
  "materials":["p. 3. povzetek-pravice-zensk.pdf","Pravice zensk.pdf","05_pravice_zensk.md","Pogodba_p3_CEDAW.pdf"]},
 {"id":"invalidi","n":6,"title":"Pravice oseb z invalidnostjo","titleEn":"Disability rights","status":"seminar",
  "legal":"**CRPD 2006 (Konvencija o pravicah invalidov)**: **prelom od medicinskega k socialnemu modelu**; **čl. 2 ključni definiciji**: ① **univerzalno oblikovanje** (*universal design*) in ② **primerna prilagoditev** (*reasonable accommodation* — opustitev primerne prilagoditve pomeni diskriminacijo!); čl. 5 enakost in nediskriminacija; čl. 9 dostopnost grajenega okolja, prevoza in informacij; **čl. 12 enaka pravna sposobnost** (*legal capacity* — prehod od odvzema opravilne sposobnosti k podprtemu odločanju); čl. 19 neodvisno življenje in vključenost v skupnost; **Opcijski protokol k CRPD (2006)**: individualne pritožbe in preiskovalni postopek.",
  "monitoring":"CRPD Odbor: obravnava poročil držav; po OP obravnava individualne pritožbe posameznikov in skupin; Evropska komisija in nacionalni mehanizmi (čl. 33).",
  "problems":"**Michael Oliver**: konceptualni preboj — invalidnost ni medicinska okvara telesa, temveč posledica družbenih ovir in izključevanja; **Berghs et al. (2019)**: »socialni model človekovih pravic«; segregacija in **institucionalizacija** (zapiranje v zavode); odvzem volilne in pravne sposobnosti; nesorazmerna prizadetost v krizah in vojnah (triaže v času COVID-19, ujeti invalidi v Gazi in Ukrajini).",
  "model":"1. Konceptualni premik: **medicinski model → socialni model (Oliver)** → 2. CRPD čl. 2 (**univerzalno oblikovanje + primerna prilagoditev**) → 3. Čl. 12 pravna sposobnost (podprto odločanje) + čl. 19 neodvisno življenje → 4. Nadzor: CRPD Odbor + OP → 5. Težave v praksi: Berghs 2019, institucionalizacija, vojna žarišča.",
  "materials":["PI_Pravice oseb z invalidnostmi-2.pdf","06_pravice_oseb_z_invalidnostjo.md","Berghs 2019"]},
 {"id":"begunci","n":7,"title":"Begunci","titleEn":"Refugees","status":"seminar",
  "legal":"**Konvencija o statusu beguncev 1951** + **Protokol o statusu beguncev 1967** (odprava časovne omejitve pred 1951 in geografske omejitve na Evropo); **čl. 1A(2) definicija begunca**: oseba, ki se nahaja zunaj svoje države in ima **utemeljen strah pred preganjanjem iz 5 taksativno določenih razlogov: rasa, vera, narodnost, pripadnost določeni družbeni skupini ali politično mnenje**, in ne more ali noče uživati varstva te države; **čl. 33 načelo non-refoulement**: prepoved izgona ali vračanja na meje ozemelj, kjer bi bilo ogroženo življenje ali svoboda; izjema v 33(2) (grožnja varnosti države — pazi: CAT čl. 3 te izjeme nima!); čl. 31 prepoved kaznovanja za nezakonit vstop; SDČP čl. 14 (pravica iskati azil); Listina EU o temeljnih pravicah čl. 18.",
  "monitoring":"UNHCR (Visoki komisariat ZN za begunce — nadzorna vloga po čl. 35 Konvencije 1951); ESČP (prek čl. 3 prepoved mučenja in 4. protokola čl. 4 prepoved kolektivnih izgonov); Odbor za človekove pravice.",
  "problems":"**Di Nunzio (2023) — Italy-Libya Memorandum**: koncept *pullbacks* (Italija financira in opremlja libijsko obalno stražo, ki prestreza migrante na odprtem morju in jih vrača v libijske centre za pridržanje, kjer se dogaja sistematično mučenje — izogibanje jurisdikciji in neposredna kršitev non-refoulement); *pushbacks* na zunanjih mejah EU (Balkan, Grčija); eksteritorializacija azilnih postopkov (npr. sporazum Italija–Albanija, UK–Ruanda); razlika med beguncem (preganjanje) in ekonomskim migrantom.",
  "model":"1. Definicija po **čl. 1A(2) Konvencije 1951 (5 razlogov preganjanja!)** + Protokol 1967 → 2. Ključna zaščita: **čl. 33 non-refoulement** (primerjava s strožjim CAT čl. 3 brez izjem) → 3. Razlika begunec vs. migrant → 4. Težave v praksi: **Di Nunzio (2023)**, Italy-Libya memorandum, pushbacks, eksteritorializacija.",
  "materials":["Konvencija o statusu beguncev.pdf","07_status_in_varstvo_pravic_beguncev_in_migrantov.md"]},
 {"id":"migranti","n":8,"title":"Delavci migranti","titleEn":"Migrant workers","status":"seminar",
  "legal":"**ICRMW 1990 (Mednarodna konvencija o varstvu pravic vseh delavcev migrantov in članov njihovih družin)**: sprejeta z resolucijo GS OZN 45/158, veljati začela 2003; **čl. 2(1) definicija delavca migranta**: oseba, ki bo opravljala, opravlja ali je opravljala plačano dejavnost v državi, katere državljan ni; varstvo tako dokumentiranih kot nedokumentiranih delavcev v osnovnih pravicah (čl. 18 enakost pred sodišči, delovni pogoji, nujna zdravstvena oskrba); konvencije Mednarodne organizacije dela (ILO št. 97 in 143).",
  "monitoring":"CMW Odbor (Odbor za zaščito pravic delavcev migrantov): 14 strokovnjakov; obravnava periodičnih poročil držav; možnost individualnih pritožb po čl. 77 (še ni zaživela v praksi zaradi premajhnega števila izjav držav).",
  "problems":"**Strukturna težava ratifikacij**: konvencijo so ratificirale skoraj izključno države izvora migrantov (globalni Jug — Mehika, Filipini, Maroko), nobena večja ciljna zahodna država sprejema (niti ZDA, niti članice EU) pa je NI ratificirala, da se ne bi zavezale standardom varstva tujih delavcev; sodobno suženjstvo in vezanost vizuma na delodajalca (*kafala* sistem v zalivskih državah); izkoriščanje nedokumentiranih delavcev v kmetijstvu in gradbeništvu; tisoči umrlih na migracijskih poteh (Sredozemlje, Mehika-ZDA).",
  "model":"1. Normativna podlaga: **ICRMW 1990 čl. 2(1)** (definicija delavca migranta) → 2. Razmejitev: migrant se seli iz ekonomskih/socialnih razlogov (prostovoljno ali zaradi revščine), begunec zaradi preganjanja (prisilno) → 3. Nadzor: CMW Odbor → 4. Ključni problem: **nizka ratifikacija ciljnih držav** (Zahod noče obveznosti) + kafala sistem + smrti v Sredozemlju.",
  "materials":["Mednarodna konvencija o zaščiti delavcev migrantov.pdf","07_status_in_varstvo...md","ICRMW quicksheet"]},
 {"id":"eskp","n":9,"title":"Ekonomske in socialne pravice","titleEn":"Economic and social rights","status":"seminar",
  "legal":"**MPESKP 1966/76 (Mednarodni pakt o ekonomskih, socialnih in kulturnih pravicah)**: **čl. 2(1) progresivna realizacija** (država se zavezuje, da bo z vsemi razpoložljivimi viri postopoma uresničevala pravice); toda: **minimalne osnovne obveznosti** (*minimum core obligations*) in načelo nediskriminacije (čl. 2(2)) veljata TAKOJ; pravice: čl. 6 pravica do dela, čl. 7 pravični in ugodni delovni pogoji, čl. 9 socialna varnost, čl. 11 primeren življenjski standard (hrana, obleka, stanovanje), čl. 12 najvišja raven zdravja, čl. 13 izobraževanje; **Opcijski protokol k MPESKP (2008)**: individualne in meddržavne komunikacije ter preiskovalni postopek; regionalno: **Evropska socialna listina (ESL 1961/1996)** s sistemom kolektivnih pritožb.",
  "monitoring":"Odbor za ekonomske, socialne in kulturne pravice (CESCR): ustanovljen 1985 z resolucijo ECOSOC 1985/17 (sprva telo ECOSOC); 18 neodvisnih strokovnjakov; periodična poročila; po OP 2008 individualne pritožbe; Evropski odbor za socialne pravice (za ESL).",
  "problems":"**2 najslabše uresničevana člena na izpitu**: ① **čl. 11 pravica do primernega stanovanja** (brezdomstvo v evropskih prestolnicah, gentrifikacija, nedostopnost najemniških stanovanj za mlade) in ② **čl. 12 pravica do zdravja** (kolaps zdravstva v vojnih konfliktih — Gaza, Jemen, Sudan, ter privatizacija zdravstvenih storitev); **Breznik in Praznik (2024)**: kritika neoliberalnega zmanjševanja javnih storitev in komercializacije osnovnih dobrin; napačno tolmačenje, da je progresivna realizacija izgovor za nedelovanje vlade.",
  "model":"1. Generacijska razlika: 1. (civilno-politične — takojšnje) vs. 2. generacija (ekonomske-socialne — razvojne) → 2. Ključna norma: **čl. 2(1) progresivna realizacija + minimalno jedro (minimum core) velja TAKOJ** → 3. Členi: 6 (delo), 9 (varnost), 11 (stanovanje/hrana), 12 (zdravstvo), 13 (šolstvo) → 4. Nadzor: CESCR (OP 2008) in ESL (kolektivne pritožbe) → 5. Težave v praksi: brezdomstvo (čl. 11), zdravstvo v vojnah/privatizaciji (čl. 12) + Breznik/Praznik (2024).",
  "materials":["08_socialne_pravice.md","09_ekonomske_pravice.md","p 12 EKONOMSKE PRAVICE SEMINARSKA NALOGA.pdf","mvčp-socialne pravice_pisni povzetek1.pdf"]},
 {"id":"okolje","n":10,"title":"Pravica do čistega okolja","titleEn":"Right to a healthy environment","status":"jedro+seminar",
  "legal":"V temeljnih pogodbah po 2. sv. vojni (SDČP 1948, MPDPP/MPESKP 1966, EKČP 1950) okolje **sploh ni omenjeno**! → **Stockholmska deklaracija 1972** (rojstvo mednarodnega okoljskega prava; 26 načel; ustanovitev UNEP); poročilo Brundtlandove (1987 — koncept trajnostnega razvoja); Deklaracija iz Ria (1992); **Aarhuška konvencija 1998 (UNECE)**: 3 stebri procesnih pravic (dostop do informacij, sodelovanje javnosti pri odločanju, pravno varstvo v okoljskih zadevah); Resolucija Sveta za ČP 48/13 (2021); **Resolucija Generalne skupščine OZN A/RES/76/300 (28. julij 2022)**: zgodovinsko priznanje univerzalne pravice do čistega, zdravega in trajnostnega okolja; regionalno: Afriška listina čl. 24, Protokol San Salvador čl. 11, Sporazum Escazú (Latinska Amerika 2018).",
  "monitoring":"Svet za človekove pravice OZN (Posebni poročevalec za človekove pravice in okolje); posredno sodišča prek drugih pravic (ESČP prek čl. 8 zasebno življenje in čl. 2 življenje; Medameriško sodišče Advisory Opinion OC-23/17); ICJ (svetovalno mnenje o podnebnih spremembah 2024/2025).",
  "problems":"**Kaj je zgodovinsko onemogočalo priznanje (izpitno vprašanje!)**: suverenost držav nad lastnimi naravnimi viri, ekonomske razvojne prioritete globalnega Juga (strah pred okoljskim kolonializmom), tradicionalno antropocentrično pojmovanje ČP; **antropocentrični vs. ekocentrični pristop** (*rights of nature* — npr. sodba Lhaka Honhat proti Argentini); primeri: **Held v. Montana (2023)** (zgodovinska zmaga mladih glede podnebnih sprememb v ZDA), **Ogoni / Shell (Nigerija)** (odgovornost države in multinacionalke za uničenje delte Nigra pred Afriško komisijo), sodba ESČP *KlimaSeniorinnen v. Švica (2024)* (pozitivna obveznost države pri zmanjševanju emisij).",
  "model":"1. Kronologija: pred 1972 tišina → **Stockholm 1972 (UNEP, 26 načel)** → Rio 1992 → **Aarhuška konvencija 1998 (3 procesne pravice)** → **A/RES/76/300 (2022 priznanje GS OZN)** → 2. Kaj je onemogočalo: državna suverenost nad viri, razvojne zahteve Juga, antropocentrizem → 3. Posredno sodno varstvo: greening pravic (čl. 8 EKČP) → 4. Sodni primeri: Held v. Montana, Ogoni/Shell, KlimaSeniorinnen (2024).",
  "materials":["p. 10. povzetek-pravica-do-okolja.pdf","okolje_seminarska_P3.txt","10_pravica_do_cistega_okolja.md"]},
 {"id":"razvoj","n":11,"title":"Pravica do razvoja","titleEn":"Right to development","status":"seminar",
  "legal":"**Deklaracija o pravici do razvoja 1986 (resolucija GS OZN 41/128)**: sprejeta 4. decembra 1986; čl. 1 določa pravico do razvoja kot **neodtujljivo človekovo pravico**, v okviru katere ima vsak posameznik in vsa ljudstva pravico sodelovati pri gospodarskem, družbenem, kulturnem in političnem razvoju ter uživati njegove sadove; hkrati **individualna in kolektivna pravica**; UL OZN čl. 55 in 56 (mednarodno gospodarsko in socialno sodelovanje); regionalno: **Afriška listina o človekovih pravicah in pravicah ljudstev čl. 22** (edini zavezujoči regionalni dokument, ki jo izrecno priznava!).",
  "monitoring":"Nima samostojnega pogodbenega nadzornega telesa; delovna skupina Sveta za človekove pravice za pravico do razvoja; Posebni poročevalec OZN.",
  "problems":"**Ključna pravna narava (izpit!)**: Deklaracija 1986 **NI pravno zavezujoča mednarodna pogodba**, temveč politična resolucija Generalne skupščine; **razkorak Sever–Jug**: države Juga (Gibanje neuvrščenih) zahtevajo pravno zavezujočo konvencijo in prerazdelitev virov, zahodne države (ZDA, EU) pa pravico do razvoja dojemajo zgolj kot programsko načelo in zavračajo pravno odgovornost za globalno neenakost; **Nico Schrijver**: argumentira potrebo po formalni zavezujoči mednarodni konvenciji; **Surya Subedi**: poudarja, da je dokument predvsem programska smernica za oblikovanje mednarodnih politik; razlika od pravice do okolja (okolje je postalo splošno sprejeto s sodno prakso in A/RES/76/300, razvoj pa ostaja politično polariziran).",
  "model":"1. Opredelitev in vir: **Deklaracija 1986 (res. 41/128)** — hkrati individualna in kolektivna pravica ljudstev → 2. Pravni status: **NI zavezujoča** (edina zavezujoča izjema je čl. 22 Afriške listine) → 3. Doktrinarna razprava: **Schrijver (potreba po konvenciji)** vs. **Subedi (programski dokument)** → 4. Konflikt Sever-Jug: boj za pravično delitev tehnologije in virov vs. zahodni odpor proti kolektivnim zahtevam.",
  "materials":["11_pravica_do_razvoja.md","Declaration on the Right to Development.pdf","Schrijver članek"]},
 {"id":"genocid","n":12,"title":"Prepoved genocida","titleEn":"Prohibition of genocide","status":"jedro+seminar",
  "legal":"**Konvencija o preprečevanju in kaznovanju zločina genocida 1948** (veljavnost 1951, resolucija GS 260 A (III)); **Raphael Lemkin (1944)**: skoval izraz iz grškega *genos* (ljudstvo, pleme, rod) in latinskega *cide* (ubijanje); Hersch Lauterpacht (avtor koncepta zločinov proti človeštvu); **čl. II definicija genocida — 3 ključni elementi**:\n  1. **Dolus specialis**: specifični namen uničiti, v celoti ali deloma,\n  2. **4 taksativno naštete skupine**: narodnostno, etnično, rasno ali versko skupino (**politične, ekonomske in socialne skupine so izrecno izpuščene!**),\n  3. **5 prepovedanih dejanj**: a) ubijanje pripadnikov skupine, b) povzročitev hudih telesnih ali duševnih poškodb, c) namerno ustvarjanje življenjskih razmer, ki vodijo v fizično uničenje, d) ukrepi za preprečevanje rojstev v skupini, e) prisilno preseljevanje otrok v drugo skupino;\n  čl. III kazniva dejanja (genocid, zarota, ščuvanje, poskus, sostorilstvo); **čl. VI pristojnost**: domača sodišča ali mednarodno kazensko sodišče; **čl. IX pristojnost Meddržavnega sodišča (ICJ)** za reševanje sporov med državami glede razlage, uporabe ali izpolnjevanja konvencije; **jus cogens**.",
  "monitoring":"Meddržavno sodišče v Haagu (**ICJ** — odgovornost držav po čl. IX); Mednarodno kazensko sodišče (**ICC** po Rimskem statutu čl. 6 — individualna kazenska odgovornost); ad hoc tribunala ICTY (Srebrenica) in ICTR (Ruanda).",
  "problems":"**Gaza in pomanjkljivosti Konvencije (izpitno vprašanje!)**:\n  1. Izjemen dokazni prag za **dolus specialis** (dokazati je treba namen uničenja skupine kot take, ne zgolj vojaški cilj ali nesorazmerno silo),\n  2. **Omejenost na zgolj 4 skupine** (npr. poboji političnih nasprotnikov v Kambodži ali Indoneziji ne ustrezajo definiciji genocida),\n  3. **Enforcement / izvrševanje**: ICJ izda začasne ukrepe (*provisional measures* — npr. JAR v. Izrael 2024), vendar nima lastne policije ali mehanizma prisile; resolucije VS OZN blokira veto stalnih članic,\n  4. **Politizacija pojma**: selektivna uporaba s strani velesil;\nVodilni sodni primeri: **ICTR Jean-Paul Akayesu (1998)** (prva sodba, ki je **sistematično spolno nasilje in posilstva** priznala kot obliko genocida po čl. II(b)); Ruanda 1994 (~800.000 Tutsijev v 100 dneh); Srebrenica 1995 (ICJ Bosna v. Srbija 2007: Srbija ni preprečila genocida); načelo **R2P (Responsibility to Protect 2005)** — 4 merila: pravi namen, zadnje sredstvo, sorazmernost sredstev, razumni obeti (prva uporaba Libija 2011).",
  "model":"1. Izvor in etimologija: **Lemkin 1944 (genos + cide)** → 2. Definicija po **čl. II (dolus specialis + 4 skupine + 5 dejanj)** + čl. IX ICJ → 3. Sodni mejniki: **Akayesu (posilstvo kot genocid)**, Ruanda, Srebrenica → 4. Pomanjkljivosti konvencije na primeru Gaze: izjemen dokaz namere, izpuščene politične skupine, neizvršljivost odločb ICJ in politični veto v VS OZN.",
  "materials":["p. 10. povzetek-prepoved-genocida.pdf","12_prepoved_genocida.md","An Unfulfilled Promise.pdf","GenocideConvention quicksheet"]},
 {"id":"izrazanje","n":13,"title":"Svoboda izražanja","titleEn":"Freedom of expression","status":"seminar",
  "legal":"**SDČP čl. 19**; **MPDPP čl. 19**; **EKČP čl. 10**; Afriška listina čl. 9; Ameriška konvencija čl. 13; zgodovinski vir: **John Milton (Areopagitica 1644)**: 3 vidiki pravice: **iskanje, sprejemanje in širjenje informacij ter idej brez meja**; **Švedski zakon o svobodi tiska 1766** (prvi zakon na svetu, ki je ukinil predhodno cenzuro); **3-delni kumulativni test dopustnosti omejitev (čl. 10(2) EKČP in 19(3) MPDPP)**:\n  1. **Zakonitost**: omejitev mora biti predpisana z jasnim, dostopnim zakonom,\n  2. **Legitimen cilj**: nacionalna varnost, ozemeljska celovitost, javni red, preprečevanje kriminala, varstvo zdravja ali morale, varstvo ugleda ali pravic drugih, varstvo zaupnih podatkov,\n  3. **Nujnost v demokratični družbi**: obstoj nujne družbene potrebe (*pressing social need*), sorazmernost ukrepa s ciljem in ustrezna obrazložitev ob upoštevanju polja proste presoje (*margin of appreciation*);\n  **dvojni aspekt**: negativni (svoboda pred cenzuro in vmešavanjem oblasti) in **pozitivni (dolžnost države, da zagotavlja medijski pluralizem, varnost novinarjev in transparentnost informacij)**.",
  "monitoring":"Evropsko sodišče za človekove pravice (ESČP); Odbor za človekove pravice (**Splošni komentar št. 34 k čl. 19 MPDPP**); 4 posebni poročevalci (OZN, OVSE, OAS, ACHPR — Skupna deklaracija o svobodi izražanja v digitalni dobi 2019).",
  "problems":"**Howie (2018)**: izzivi komunikacijskih revolucij in regulacije interneta; **digitalni prostor in umetna inteligenca (delavnica na FDV!)**: algoritemska cenzura, netransparentno moderiranje vsebin s strani zasebnih spletnih velikanov (Meta, X, TikTok), širjenje sovražnega govora in ciljanih dezinformacij, globoki ponaredki (*deepfakes*), utišanje novinarjev s strateškimi tožbami (SLAPP).",
  "model":"1. Definicija in zgodovina: **Milton 1644 (Areopagitica: iskanje, sprejemanje, širjenje)** + Švedski zakon 1766 → 2. Normativni okvir: MPDPP čl. 19 in EKČP čl. 10 → 3. Negativni aspekt (nevmešavanje) vs. **pozitivni aspekt (zagotavljanje medijskega pluralizma)** → 4. **3-delni test omejitev (zakonitost + legitimen cilj + nujnost v demokratični družbi)** → 5. Izzivi v digitalni dobi: Howie (2018), algoritemska pristranskost, AI, SLAPP tožbe.",
  "materials":["p. 13. povzetek-svoboda-izrazanja.pdf","Svoboda Izražanja Pisni Izdelek.pdf","13_svoboda_izrazanja.md","Howie 2018"]},
 {"id":"veroizpoved","n":14,"title":"Svoboda veroizpovedi","titleEn":"Freedom of religion","status":"seminar",
  "legal":"**EKČP čl. 9**; **MPDPP čl. 18**; **SDČP čl. 18**; ključna delitev:\n  - **Forum internum**: notranje prepričanje, svoboda vesti, sprejetje ali sprememba vere ali prepričanja — je **absolutna pravica, ki je ni mogoče nikoli omejiti ali suspendirati (niti v vojni)**,\n  - **Forum externum**: zunanje izražanje in udejanjanje vere (individualno ali skupaj z drugimi, javno ali zasebno: bogoslužje, poučevanje, obredi, nošenje simbolov) — je **kvalificirana pravica**, ki jo je dovoljeno omejiti po 3-delnem testu (čl. 9(2) EKČP: zakonito + nujno v demokratični družbi zaradi javne varnosti, reda, zdravja, morale ali varstva pravic in svoboščin drugih);\n  zgodovinski kontekst: reformacija (Martin Luther 1517 — razbitje verskega monopola in verske vojne v Evropi, Vestfalski mir 1648 — *cuius regio, eius religio* kot zametek verske tolerance).",
  "monitoring":"ESČP (bogata sodna praksa); Odbor za človekove pravice (**Splošni komentar št. 22 k čl. 18 MPDPP** — varuje teistična, neteistična in ateistična prepričanja); Posebni poročevalec OZN za svobodo veroizpovedi ali prepričanja.",
  "problems":"**Verska diskriminacija in nošenje verskih simbolov v javnih institucijah/šolah**: ESČP dosledno priznava široko polje proste presoje državam (*margin of appreciation*) pri ohranjanju laičnosti (npr. *Leyla Şahin v. Turčija*, *S.A.S. v. Francija* — prepoved zakrivanja obraza/burke); vprašanja prepovedi obrednega klanja in obrezovanja dečkov (konflikt z otrokovo telesno integriteto); položaj verskih manjšin v Sloveniji (**Poročilo MVČP 2024: Frank, Šinigoj, Jelerčič** — vprašanja pokopališč, verske prehrane v šolah in registracije verskih skupnosti); verski fundamentalizem in zloraba vere za zanikanje pravic žensk in LGBT+ oseb.",
  "model":"1. Normativni viri: EKČP čl. 9 in MPDPP čl. 18 → 2. Bistvena razlika: **forum internum (absolutno, brez izjem)** vs. **forum externum (omejljivo po čl. 9(2))** → 3. Zgodovinski prelom: reformacija (Luther) in verska toleranca → 4. Sodna praksa ESČP: polje proste presoje (verska oblačila, naglavne rute, križi v učilnicah) → 5. Aktualne dileme: Poročilo MVČP 2024 (Slovenija), obrezovanje, sovražni govor.",
  "materials":["Poročilo MVČP.pdf","Pravica do veroizpovedi_koncni izdelek","14_svoboda_veroizpovedi.md"]},
 {"id":"samoodlocba","n":15,"title":"Pravica do samooodločbe","titleEn":"Self-determination","status":"seminar",
  "legal":"**MPDPP čl. 1 in MPESKP čl. 1**: identična skupna določba v obeh paktih (»Vsi narodi imajo pravico do samoodločbe. Na podlagi te pravice svobodno določajo svoj politični status in svobodno zagotavljajo svoj gospodarski, socialni in kulturni razvoj«); **Ustanovna listina OZN**: čl. 1(2) (razvijanje prijateljskih odnosov med narodi na podlagi spoštovanja načela enakopravnosti in samoodločbe ljudstev) ter čl. 55; Deklaracija o podelitvi neodvisnosti kolonialnim deželam in ljudstvom (resolucija GS 1514 (XV) iz leta 1960); Deklaracija o načelih mednarodnega prava o prijateljskih odnosih (resolucija GS 2625 (XXV) iz leta 1970); regionalno: **Afriška listina čl. 20** (eksplicitna pravica koloniziranih ali zatiranih ljudstev do osvoboditve); po mnenju mnogih pravnikov ima status **jus cogens**;\n  razmejitev oblik samoodločbe:\n  - **Notranja samoodločba**: pravica naroda/prebivalstva do demokratičnega političnega sistema, participacije, lokalne ali kulturne avtonomije znotraj obstoječe države,\n  - **Zunanja samoodločba**: pravica do odcepitve (*secession*) in oblikovanja neodvisne suverene države ali priključitve k drugi državi — priznana pri dekolonizaciji, tuji okupaciji ali kot skrajni izhod (*remedial secession*) ob sistematičnem zatiranju.",
  "monitoring":"Nima posebnega pogodbenega telesa; razpravlja se v Generalni skupščini OZN, Odboru za dekolonizacijo (Odbor 24); Meddržavno sodišče (ICJ — svetovalna mnenja: Zahodna Sahara 1975, Kosovo 2010, Čagos 2019, Palestina 2004/2024).",
  "problems":"**Jan Klabbers (2006)**: analiza pravne narave samoodločbe — prehod od političnega načela k pravni normi ter neizbežna napetost z **ozemeljsko celovitostjo obstoječih držav** (teritorialna integriteta); **vprašanje definicije subjekta (R. J. Vincent)**: kdo je pravzaprav »narod« (*people*)? Ali so to vsi državljani države ali etnična manjšina? (če ima vsaka manjšina pravico do odcepitve, pride do neskončne drobitve držav); primeri: Palestina (pravica do lastne države pod tujo okupacijo), Zahodna Sahara, Kosovo, Katalonija, Tajvan.",
  "model":"1. Viri: **čl. 1 MPDPP = čl. 1 MPESKP (skupni temelj paktov!)** + UL OZN 1(2) + Afriška listina čl. 20 → 2. Narava pravice: kolektivna pravica ljudstev (jus cogens) → 3. Razlika: **notranja (avtonomija, demokracija)** vs. **zunanja samoodločba (odcepitev)** → 4. Doktrina in problem subjekta: **Klabbers (2006)** in **Vincent (kdo je narod?)** v napetosti s suverenostjo → 5. Primeri: dekolonizacija, Palestina, Kosovo.",
  "materials":["PI_PRAVICA DO SAMOODLOČBE MATIJA I DANICA.pdf","15_pravica_do_samoodlocbe.md","Klabbers 2006"]},
 {"id":"manjsine","n":16,"title":"Manjšinske pravice","titleEn":"Minority rights","status":"seminar",
  "legal":"**MPDPP čl. 27**: edina globalno pravno zavezujoča določba splošnega varstva manjšin (pripadnikom etničnih, verskih ali jezikovnih manjšin se ne sme odrekati pravica, da skupaj z drugimi člani svoje skupine uživajo svojo kulturo, izpovedujejo in opravljajo svojo vero ali uporabljajo svoj jezik); Deklaracija OZN o pravicah oseb, ki pripadajo narodnim ali etničnim, verskim in jezikovnim manjšinam (resolucija GS 47/135 iz leta 1992); **regionalno (Svet Evrope — najrazvitejši sistem)**: **Okvirna konvencija za varstvo narodnih manjšin (OKVNM 1995/1998)**: ključni členi: **čl. 5** (ohranjanje in razvoj kulture ter identitete), **čl. 6** (spodbujanje strpnosti in medkulturnega dialoga), **čl. 15** (ustvarjanje pogojev za učinkovito sodelovanje manjšin v javnem in družbenem življenju); Evropska listina o regionalnih ali manjšinskih jezikih (1992); Konvencija Mednarodne organizacije dela št. 169 o domorodnih in plemenskih ljudstvih (ILO 169 iz leta 1989); Deklaracija OZN o pravicah domorodnih ljudstev (UNDRIP 2007).",
  "monitoring":"Odbor za človekove pravice (nadzor nad čl. 27 MPDPP prek poročil in 1. OP); **Svetovalni odbor za Okvirno konvencijo (ACFC - Advisory Committee)** pri Svetu Evrope: strokovnjaki ocenjujejo poročila držav in izvajajo obiske na terenu, Odbor ministrov SE sprejema resolucije; Visoki komisar OVSE za narodne manjšine (tiha diplomacija za preprečevanje konfliktov).",
  "problems":"**Zgodovinski razvoj v Društvu narodov (DN) — ključno izpitno vprašanje!**: po razpadu treh cesarstev (Avstro-Ogrske, Otomanskega in Ruskega cesarstva) so nastale nove večnacionalne države; varstvo manjšin v sistemu DN je bilo vzpostavljeno **izključno zaradi ohranjanja miru in stabilnosti novih meja, NE pa iz humanitarnih vzgibov do posameznikov**; sistem je bil izrazito **diskriminatoren**: obveznosti so veljale le za poražene države (Avstrija, Madžarska, Bolgarija, Turčija), novonastale države (Poljska, Kraljevina SHS, Češkoslovaška, Romunija, Grčija) in kasneje vstopajoče (baltske države, Albanija, Irak), medtem ko so bile **velesile zmagovalke (Francija, Velika Britanija, Italija) popolnoma izvzete**;\n  **Joshua Castellino (2010)**: teoretska analiza dileme med individualnim nediskriminacijskim pristopom in posebnimi kolektivnimi pravicami manjšin; problem definicije manjšine (države pogosto samovoljno določajo, koga priznajo kot manjšino — npr. razlikovanje med »avtohtonimi« in »novimi« manjšinami); nizka ratifikacija ILO 169 s strani držav, kjer živijo domorodna ljudstva.",
  "model":"1. Zgodovina in cilj v DN: **mir in varnost novih meja (ne humanitarni vzgibi!) + diskriminatoren sistem (zmagovalke izključene)** → 2. Globalna raven: **MPDPP čl. 27 (edina globalna zavezujoča norma)** → 3. Regionalna raven: **OKVNM (Svet Evrope — čl. 5 identiteta, čl. 6 toleranca, čl. 15 participacija)** → 4. Nadzor: Odbor za ČP in Svetovalni odbor OKVNM → 5. Doktrina: **Castellino (2010)** + dilema definicije manjšin in položaj domorodnih ljudstev (ILO 169).",
  "materials":["p 6Manjšinske pravice.pdf","16_varstvo_manzinskih_pravic.md","Castellino 2010","1992 Declaration"]},
]
w("topics.json", TOPICS)

# ============================================================
# 4. COMPARISON TABLES (15) — from guide Part IV
# ============================================================
COMPARISONS = [
 {"id":"odbor-svet-komisija","title":"Odbor za ČP vs. Svet za ČP vs. Komisija za ČP","rows":[
   ["","Odbor za ČP","Svet za ČP","Komisija za ČP (1946–2006)"],
   ["Podlaga","MPDPP čl. 28","GA Res 60/251 (2006)","ECOSOC (1946)"],
   ["Tip","treaty-based","charter-based","charter-based"],
   ["Člani","18 neodvisnih strokovnjakov","47 držav (regionalno)","države (tudi kršiteljice)"],
   ["Ključni postopek","poročila + priporočila; individualne po 1. OP","UPR, posebni postopki, complaint procedure","politizirana → reforma"],
   ["Velja za","samo pogodbenice","vse članice OZN","vse"]]},
 {"id":"mpdpp-mpeskp","title":"MPDPP vs. MPESKP","rows":[
   ["","MPDPP","MPESKP"],
   ["Pravice","civilno-politične (1. gen.)","ekonomske-socialne-kulturne (2. gen.)"],
   ["Takojšnje/progresivno","takojšnje","progresivna realizacija (čl. 2(1)) + minimalno jedro"],
   ["Nadzor","Odbor za ČP (18)","Odbor za ESKP (1985, ECOSOC)"],
   ["Pritožbe","1. OP (1966/76)","OP 2008"]]},
 {"id":"begunec-migrant","title":"Begunec vs. migrant","rows":[
   ["","Begunec","Migrant"],
   ["Razlog","preganjanje (5 razlogov: rasa, vera, narodnost, mnenje, socialna skupina)","ekonomski/socialni"],
   ["Konvencija","1951 + Protokol 1967","ICRMW 1990"],
   ["Ključna zaščita","non-refoulement (čl. 33)","čl. 2(1) definicija; nizka ratifikacija"]]},
 {"id":"cat-opcat","title":"CAT vs. OPCAT","rows":[
   ["","CAT","OPCAT"],
   ["Fokus","definicija + obveznosti","preventiva (obiski)"],
   ["Telesa","Odbor proti mučenju","SPT + NPM"]]},
 {"id":"ekcp-esl","title":"EKČP vs. ESL","rows":[
   ["","EKČP","ESL"],
   ["Pravice","civilno-politične","ekonomske-socialne"],
   ["Nadzor","ESČP (sodba zavezujoča, čl. 46)","Odbor strokovnjakov + Odbor ministrov (priporočilo)"],
   ["Pritožbe","individualne (čl. 34)","kolektivne (sindikati, NGO)"]]},
 {"id":"postopki","title":"Postopki — ne zamešaj","rows":[
   ["Postopek","Kdo začne","Pogoj","Rezultat"],
   ["Poročanje države","država pogodbenica","periodična obveznost","sklepne ugotovitve"],
   ["Individualna komunikacija","posameznik/skupina","pristojnost + izčrpanje domačih sredstev","stališča/priporočila"],
   ["Meddržavna komunikacija","država proti državi","sprejeta pristojnost","poravnava/stališče/sodba"],
   ["Preiskava","odbor","hude/sistematične kršitve + pristojnost","zaupna preiskava + priporočila"],
   ["UPR","druge države (Svet)","vse članice OZN","priporočila: sprejme ali zabeleži"],
   ["Individualna pritožba ESČP","posameznik/NGO","žrtev + jurisdikcija + domača sredstva","zavezujoča sodba"],
   ["Kolektivna pritožba ESL","organizacije","država sprejela sistem","odločitev + priporočilo"]]},
 {"id":"narava-pravic","title":"Absolutne vs. kvalificirane pravice","rows":[
   ["","Absolutne","Kvalificirane"],
   ["Primeri","mučenje (EKČP 3, CAT), forum internum","izražanje 10(2), veroizpoved externum 9(2), zasebno življenje 8, zborovanje 11"],
   ["Test","ni omejitev","zakonita + legitimen cilj + nujna v demokratični družbi (+ sorazmernost, margin of appreciation)"]]},
 {"id":"generacije","title":"3 generacije ČP","rows":[
   ["Generacija","Pravice","Dokument"],
   ["1. civilno-politične","življenje, mučenje, izražanje, veroizpoved","MPDPP"],
   ["2. ekonomske-socialne-kulturne","delo, zdravstvo, izobraževanje","MPESKP"],
   ["3. solidarnostne","razvoj, okolje, mir","Deklaracije (pogosto nezavezujoče)"]]},
 {"id":"regionalni-sistemi","title":"Regionalni sistemi","rows":[
   ["Regija","Dokument","Nadzor"],
   ["Evropa","EKČP (1950/53)","ESČP (zavezujoče sodbe)"],
   ["Evropa (socialne)","ESL","Evropski odbor + Odbor ministrov"],
   ["Ameriki","Ameriška konvencija (1969/78)","Medameriško sodišče/komisija"],
   ["Afrika","Afriška listina (1981/86)","Afriška komisija/sodišče"],
   ["Arabske države","Arabska listina (1994; 2004/08)","Arabska komisija"],
   ["Azija","ni listine","— (azijske vrednote — Sen)"]]},
 {"id":"nadzorni-mehanizmi","title":"2 vrsti nadzornih mehanizmov","rows":[
   ["","Pogodbeni (treaty-based)","Splošni (charter-based)"],
   ["Podlaga","pogodba (npr. MPDPP čl. 28)","UL OZN / GA Res 60/251"],
   ["Velja za","samo pogodbenice","vse članice OZN"],
   ["Primeri","Odbor za ČP (18), CESCR, CAT Odbor","Komisija (1946–2006) → Svet za ČP (2006, 47), OHCHR"],
   ["Rezultat","priporočila (sprejme/delno/zavrne)","UPR priporočila (neobvezna)"]]},
 {"id":"iccp-icescr-nadzor","title":"Nadzor po paktih","rows":[
   ["","MPDPP","MPESKP"],
   ["Telo","Odbor za ČP (čl. 28)","Odbor za ESKP (1985)"],
   ["Poročila","čl. 40","čl. 16–17 (prek ECOSOC)"],
   ["Individualne","1. OP","OP 2008"],
   ["Meddržavne","čl. 41","OP 2008"]]},
 {"id":"okolje-razvoj","title":"Okolje vs. razvoj","rows":[
   ["","Okolje","Razvoj"],
   ["Ključni dokument","A/RES/76/300 (2022); Stockholm 1972","Deklaracija 1986"],
   ["Pravna narava","priznana (GS OZN)","nezavezujoča deklaracija"],
   ["Nadzor","Svet za ČP; sodišča posredno","brez posebnega telesa"]]},
 {"id":"forum-internum-externum","title":"Veroizpoved: internum vs. externum","rows":[
   ["","Forum internum","Forum externum"],
   ["Kaj","notranje prepričanje","manifestiranje (čaščenje, obredi, izražanje)"],
   ["Narava","absolutno","omejljivo (9(2): zakonito, javna varnost/red/zdravje/morala, pravice drugih)"]]},
 {"id":"genocid-zlocin","title":"Genocid vs. zločin proti človeškosti","rows":[
   ["","Genocid","Zločin proti človeškosti"],
   ["Namere","dolus specialis (uničiti skupino)","ni posebne namere do skupine"],
   ["Skupine","4 zaščitene (rasna, verska, etnična, nacionalna)","širše (tudi civilno prebivalstvo)"],
   ["Vir","Konvencija 1948 čl. II","Rimski statut čl. 7; ICPED čl. 5"]]},
 {"id":"pritozbe-pogodbe","title":"Individualne pritožbe — kje so možne","rows":[
   ["Pogodba/protokol","Instrument","Opomba"],
   ["MPDPP","1. OP (1966/76)","čl. 41 = meddržavne"],
   ["CAT","čl. 22 (izjava države)","čl. 21 meddržavne; čl. 20 preiskave"],
   ["CEDAW","OP 1999","+ preiskave"],
   ["MPESKP","OP 2008","+ meddržavne + preiskave"],
   ["CRC","3. OP (2011)","+ P2/P3 vsebinska"],
   ["CRPD","OP","+ preiskave"],
   ["ICPED","čl. 31 (izjava države)","+ čl. 32 meddržavne, čl. 33 preiskave"],
   ["EKČP","čl. 34 (posamezniki, NGO, skupine)","sodba zavezujoča čl. 46"]]},
]
w("comparisons.json", COMPARISONS)

# ============================================================
# 5. FLASHCARDS — atoms + article clusters + traps + entity facts
# ============================================================
cards = []
def card(prompt, answer, kind="fact", topics=None, authority="B", source=""):
    cards.append({"id": f"fc{len(cards)+1:03d}", "prompt": prompt, "answer": answer,
                  "kind": kind, "topics": topics or [], "authority": authority, "source": source})

# Atoms (guide §6.8)
card("MPDPP čl. 28 → katero telo in koliko članov?", "Odbor za človekove pravice — 18 neodvisnih strokovnjakov", topics=["nadzor"], authority="A", source="MPDPP čl. 28")
card("Svet za ČP — koliko držav in kateri mehanizem?", "47 držav (regionalno, tajno glasovanje); UPR vsakih 4–4,5 let", topics=["nadzor"], authority="A", source="GA Res 60/251")
card("CAT čl. 1 — 4-elementna definicija mučenja?", "① namerna ② huda fizična/psihična bolečina ③ za namen (priznanje, zastraševanje, kaznovanje, diskriminacija) ④ s strani/s privolitvijo uradne osebe; izključene zakonite sankcije", topics=["mucenje"], authority="A", source="CAT čl. 1")
card("CAT čl. 2 in čl. 3?", "čl. 2 absolutnost (noben izjem, niti vojna/nuja) · čl. 3 non-refoulement (ne vračati kjer grozi mučenje)", topics=["mucenje"], authority="A")
card("Konvencija o beguncih: čl. 1A(2) in čl. 33?", "1A(2) definicija begunca (5 razlogov preganjanja) · čl. 33 non-refoulement", topics=["begunci"], authority="A")
card("Genocid: čl. II in čl. IX?", "čl. II definicija (dolus specialis, 4 skupine, 5 dejanj) · čl. IX spori pred ICJ", topics=["genocid"], authority="A")
card("Izražanje: MPDPP in EKČP člen?", "MPDPP čl. 19 · EKČP čl. 10", topics=["izrazanje"], authority="A")
card("Veroizpoved: MPDPP in EKČP člen?", "MPDPP čl. 18 · EKČP čl. 9", topics=["veroizpoved"], authority="A")
card("Življenje: MPDPP in EKČP člen?", "MPDPP čl. 6 · EKČP čl. 2", topics=["zivljenje"], authority="A")
card("Manjšine: ključna člena?", "MPDPP čl. 27 (edini globalni zavezujoč) · OKVNM 1995/98 (čl. 5, 6, 15)", topics=["manjsine"], authority="A")
card("Okolje: od Stockholma do danes?", "Stockholm 1972 → A/RES/76/300 (2022)", topics=["okolje"], authority="A")
card("Pravica do razvoja — pravna narava?", "Deklaracija 1986 (res. 41/128) — NI pravno zavezujoča", topics=["razvoj"], authority="A")
card("ESČP: pritožba, dopustnost, zavezujočost?", "čl. 34 pritožba · čl. 35 dopustnost · čl. 46 zavezujoča sodba", topics=["regionalni"], authority="A")
card("Običajno pravo — vir in 2 elementa?", "ICJ Statut čl. 38(1)(b); state practice + opinio juris", topics=["obicaj"], authority="A")
card("Persistent objector — kaj in izjema?", "edina izjema od zavezujočnosti običaja; ne velja za jus cogens", topics=["obicaj"], authority="A")
card("Vincent: 5 elementov pravice?", "subjekt · objekt (do/pred) · uveljavljanje (paradoks posesti) · nosilec dolžnosti (Shue: 3 dolžnosti) · utemeljitev", topics=["koncept"], authority="B", source="Vincent 1986")
card("Shue: 3 korelativne dolžnosti?", "izogibanje prikrajšanju · zaščita pred prikrajšanjem · pomoč prikrajšanim", topics=["koncept"], authority="C")
card("Kdaj dokument postane pravno zavezujoč?", "ratifikacija 35 držav (pakta) / 10 (protokoli) + notranja potrditev (DZ)", topics=["ratifikacije"], authority="B")
card("3 razlogi za 2 pakta (1966)?", "suverenost vs. nadzor · posameznik (Z) vs. skupnost (V) · vsebina ČP (civilno-politične vs. ekonomske-socialne)", topics=["listina"], authority="B")
card("3 obdobja ratifikacijskih omrežij?", "15 let pred koncem HV (ozek krog, ZDA nič) → ob koncu (širitev) → 15 let po (vse vsaj 1; bivše komunistične množično)", topics=["ratifikacije"], authority="B")
card("Komisija → Svet za ČP: kdaj in zakaj?", "2006; Komisija preveč politizirana, kršiteljice v njej", topics=["nadzor"], authority="B")
card("CEDAW: letnica, čl. 1, ratifikacije?", "1979 (res. 34/180); čl. 1 diskriminacija; 189 ratifikacij (ZDA ne)", topics=["zenske"], authority="A")
card("CRC: letnica, čl. 1, čl. 3, ratifikacije?", "1989 (res. 44/25); čl. 1 <18; čl. 3 najboljša korist; 196 ratifikacij (ZDA ne)", topics=["otroci"], authority="A")
card("CRPD čl. 2 — 2 ključna pojma?", "univerzalno oblikovanje · primerna prilagoditev (odklonitev = diskriminacija)", topics=["invalidi"], authority="A")
card("ICPED čl. 5 — kaj določa?", "široka/sistemska praksa prisilnega izginotja = zločin proti človeškosti", topics=["izginotja"], authority="A")
card("ICRMW čl. 2(1)?", "definicija delavca migranta; nizka ratifikacija", topics=["migranti"], authority="A")
card("Velásquez-Rodríguez — doktrina?", "država odgovorna, če ne preiskuje/preprečuje prisilna izginotja (clandestine repression)", topics=["izginotja"], authority="C")
card("Lemkin — genos + cide?", "genos (grško: rasa/pleme/narod) + cide (latinsko: ubijanje); skoval 1944", topics=["genocid"], authority="A")
card("Sen — azijske vrednote?", "kulturni relativizem = izgovor avtoritarnih režimov; univerzalnost združljiva z azijskimi tradicijami", topics=["regionalni"], authority="C", source="Sen 2015")
card("Helfer 2020 — tema?", "populizem in mednarodne institucije ČP (survival guide)", topics=["aktualno"], authority="C")
card("Milton, Areopagitica 1644 — 3 vidiki izražanja?", "iskanje · prejemanje · razširjanje informacij", topics=["izrazanje"], authority="B")
card("EKČP 10(2) — 3-delni test omejitev?", "zakonita + legitimen cilj + nujna v demokratični družbi (+ sorazmernost)", topics=["izrazanje"], authority="A")
card("Forum internum vs. externum?", "internum (prepričanje) absolutno · externum (manifestiranje) omejljivo", topics=["veroizpoved"], authority="A")
card("Progresivna realizacija — člen in omejitev?", "MPESKP čl. 2(1); minimalne osnovne obveznosti in nediskriminacija veljata takoj", topics=["eskp"], authority="A")
card("Stockholm 1972 — pomen?", "rojstvo pravice do okolja; 26 načel; ustanovljen UNEP", topics=["okolje"], authority="A")
card("A/RES/76/300?", "2022: GS OZN priznala pravico do čistega, zdravega in trajnostnega okolja", topics=["okolje"], authority="A")
card("Dolus specialis?", "posebni namen uničiti zaščiteno skupino — najtežji dokazni element genocida", topics=["genocid"], authority="A")
card("Non-refoulement — 2 vira?", "CAT čl. 3 (vračanje v mučenje) · Konvencija o beguncih čl. 33", topics=["mucenje","begunci"], authority="A")
card("UPR — 3 lastnosti ocene?", "dobro: vse pravice, tudi nepogodbenice; slabo: priporočila neobvezna, politizacija", topics=["nadzor"], authority="B")
card("2 načina vzpostavitve individualne pristojnosti?", "① opcijski protokol (1. OP MPDPP, OP CEDAW, OP MPESKP, OP CRC) ② izjava po členu konvencije (CAT čl. 22, ICPED čl. 31)", topics=["nadzor"], authority="B")
card("ESČP formacije?", "posamezni sodnik · odbori (3) · senati (7) · Veliki senat (17)", topics=["regionalni"], authority="A")
card("Magna Carta 1215 — ključni prispevek?", "kralj podrejen zakonu; določila 39/40 (predhodnica habeas corpus); nadzor: 25 baronov; koristniki = fevdalci (ne ČP)", topics=["zgodovina"], authority="B")
card("Habeas Corpus Act 1679 — pomen?", "prvi zakonodajni dokument habeas corpus (nihče brez sodne podlage); povezava s SDČP 3, 9, 10 in EKČP 5(4)", topics=["zgodovina"], authority="B")
card("Hamurabi — 3 sodobni pomeni?", "predpostavka nedolžnosti · dokazi obeh strani · varstvo šibkejšega", topics=["zgodovina"], authority="B")
card("DN in manjšine — pravi cilj?", "mir in stabilnost novih meja, ne humanitarne vzgibe; diskriminatoren sistem", topics=["zgodovina"], authority="B")
card("Paradoks posesti?", "formalno poseduješ pravico (zapisana), praktično je ne uživaš", topics=["koncept"], authority="B")
card("OPCAT — telesa in funkcija?", "SPT (podkomisija za preprečevanje) + NPM (nacionalni mehanizmi); preventivni obiski", topics=["mucenje"], authority="A")
card("Aarhuška konvencija 1998?", "procesne pravice okolja: dostop do informacij, sodelovanje, pravno varstvo", topics=["okolje"], authority="A")
card("Istanbulska konvencija 2011?", "preprečevanje in boj proti nasilju nad ženskami in nasilju v družini", topics=["zenske"], authority="A")
card("Kolektivne pritožbe — kje?", "ESL (sindikati, NGO) → Evropski odbor za socialne pravice → Odbor ministrov", topics=["regionalni"], authority="B")
card("Held v. Montana?", "klimatska sodba — pravica do čistega okolja (ZDA, državna raven)", topics=["okolje"], authority="C")
card("Italy–Libya Memorandum (Di Nunzio 2023)?", "pullbacks = kolektivni izgon + refoulement; zunanja meja EU", topics=["begunci"], authority="C")
card("Osman v. United Kingdom?", "ESČP: država ima pozitivno obveznost preprečiti resnično grožnjo življenju (pravica do življenja)", topics=["zivljenje"], authority="A")
card("Akayesu (ICTR)?", "spolno nasilje kot genocid — prva sodba, ki je silovanje kvalificirala kot dejanje genocida", topics=["genocid"], authority="A")
card("R2P — 4 načela?", "prava namere · zadnje sredstvo · sorazmernost · razumne možnosti (Libija 2011 = prva uporaba)", topics=["genocid","aktualno"], authority="C")
card("Genocid — 5 dejanj (čl. II)?", "ubijanje · huda telesna/duševna škoda · uničevanje življenjskih pogojev · preprečevanje rojstev · nasilno preseljevanje otrok", topics=["genocid"], authority="A", source="Konvencija čl. II")
card("Klabbers 2006 — samoodločba?", "analiza pravne narave samoodločbe; notranja (avtonomija) vs. zunanja (odcepitev)", topics=["samoodlocba"], authority="C")
card("Howie 2018 — izražanje?", "svoboda izražanja v digitalni dobi; izzivi algoritmov in cenzure", topics=["izrazanje"], authority="C")
card("Joint Declaration 2019?", "4 posebni poročevalci za svobodo izražanja (skupna izjava o digitalni dobi)", topics=["izrazanje"], authority="A")
card("Oliver — socialni model invalidnosti?", "invalidnost = družbena bariera (ne bolezen); prehod od medicinskega k socialnemu modelu", topics=["invalidi"], authority="C")
card("Breznik/Praznik 2024?", "kritika neoliberalizma in privatizacije ekonomske/socialne pravice", topics=["eskp"], authority="C")
card("Pekinška deklaracija 1995?", "4. svetovna konferenca o ženskah; platforma za enakost", topics=["zenske"], authority="A")
card("Ogoni/Shell (Nigerija)?", "državna odgovornost za onesnaževanje (pravica do okolja); Afriška komisija", topics=["okolje"], authority="C")
card("Karta v. Španija?", "ESČP: greenning of human rights — okolje prek pravice do zasebnega življenja (EKČP 8)", topics=["okolje"], authority="A")
card("Habeas Corpus Act 1679 — povezave?", "prvi zakonodajni habeas corpus; povezava s SDČP 3 (življenje), 9 (prijetje), 10 (sodba) in EKČP 5(4)", topics=["zgodovina"], authority="B")
card("Mohajan 2022 — 4 valovi feminizma?", "1. volilna pravica · 2. 1960s–90s delo/nasilje · 3. 1990s–2000s intersekcionalnost · 4. 2012+ digitalna #MeToo", topics=["zenske"], authority="C")
card("Tate 2013 — mučenje?", "absolutna prepoved v praksi zataji: tajni pripori, ticking bomb argument, izročitev", topics=["mucenje"], authority="C")
card("Guantanamo/USA?", "waterboarding = mučenje; tajni zapori CIA; kljub absolutni prepovedi (CAT čl. 2)", topics=["mucenje"], authority="C")
card("Rwanda 1994?", "~800.000 mrtvih v 100 dneh; ICTR sodišče; Akayesu — spolno nasilje kot genocid", topics=["genocid"], authority="A")
card("Srebrenica 1995?", "UN varno območje padlo; ~8000 bošnjaških moških; ICJ: genocid", topics=["genocid"], authority="A")
card("Held v. Montana?", "klimatska sodba ZDA: država odgovorna za podnebje (pravica do čistega okolja)", topics=["okolje"], authority="C")
card("Aarhuška 1998 — 3 procesne pravice?", "dostop do informacij · sodelovanje pri odločanju · pravno varstvo", topics=["okolje"], authority="A")
card("Antropocentrični vs. ekocentrični pristop?", "antropocentrični: okolje za ljudi; ekocentrični: narava ima lastno vrednost (Lhaka Honhat)", topics=["okolje"], authority="C")
card("Schrijver vs. Subedi — pravica do razvoja?", "Schrijver: potreba po konvenciji (zavezujoča); Subedi: programski dokument (usmerja, ne zavezuje)", topics=["razvoj"], authority="C")
card("Holzscheiter 2019?", "child rights governance — politizacija otrokovih pravic v mednarodnih organizacijah", topics=["otroci"], authority="C")
card("Afriška listina o otrocih 1990?", "edina regionalna konvencija o otrokovih pravicah (ACRWC)", topics=["otroci"], authority="A")
card("P2 CRC vs. P3 CRC?", "P2: oboroženi konflikti, prostitucija/pornografija; P3 (2011): individualne pritožbe", topics=["otroci"], authority="A")
card("Castellino 2010 — manjšine?", "teoretska analiza manjšinskih pravic; napetost med identiteto in enakostjo", topics=["manjsine"], authority="C")
card("ILO 169 — domorodci?", "konvencija o domorodcih in plemenskih ljudstvih; nizka ratifikacija", topics=["manjsine"], authority="A")
card("Razpad 3 cesarstev → manjšine?", "Avstro-Ogrska, Otomanska, Ruska → nove heterogene države → manjšine = nevarnost za mir", topics=["manjsine","zgodovina"], authority="B")
card("ESČP — sodniki, mandat, starost?", "46 sodnikov (ne 47! Rusija izključena 2022); mandat 9 let brez reelekcije (P14 čl. 23); kandidat pod 65 let ob vložitvi (P15 odpravil mejo 70 let); rok za pritožbo 4 mesece (čl. 35); izbira: Parlamentarna skupščina SE", topics=["regionalni"], authority="A")
card("Dunaj 1993 — nedeljivost?", "Svetovna konferenca o ČP: nedeljivost ČP — ni izbire ALI/ALI med pakta", topics=["koncept"], authority="A")

# Article clusters (guide §6.6)
clusters = [
 ("EKČP jedro", "2 življenje · 3 mučenje · 9 vera · 10 izraz · 14 nediskriminacija", ["regionalni"]),
 ("EKČP pritožbe", "34 pritožba · 35 dopustnost · 46 zavezujočost", ["regionalni"]),
 ("CAT jedro", "1 definicija · 2 absolutnost · 3 nevračanje", ["mucenje"]),
 ("CAT pritožbe", "20 preiskava · 21 meddržavne · 22 individualne · 30 ICJ", ["mucenje"]),
 ("MPDPP jedro", "1 samoodločba · 6 življenje · 7 mučenje · 18 vera · 19 izraz · 27 manjšine · 28 Odbor", ["nadzor"]),
 ("Genocid", "II definicija · III kazniva dejanja · VI sojenje · IX ICJ", ["genocid"]),
 ("ICPED", "1 prepoved · 2 definicija · 4 kriminalizacija · 5 človeškost · 6 nadrejeni", ["izginotja"]),
 ("Begunci", "1A(2) definicija · 33 nevračanje", ["begunci"]),
]
for name, body, tops in clusters:
    card(f"Členska družina — {name}?", body, kind="cluster", topics=tops, authority="A")

# Traps (guide IV.7)
TRAPS = [
 ("Odbor za ČP ≠ Svet za ČP ≠ Komisija", "Odbor = MPDPP + 18 strokovnjakov; Svet = 47 držav + UPR; Komisija = predhodnica Sveta do 2006"),
 ("1. OP k MPDPP = individualne; čl. 41 = meddržavne", "2. OP = smrtna kazen"),
 ("CAT ≠ OPCAT", "CAT definira in prepoveduje; OPCAT preventivno obiskuje (SPT + NPM)"),
 ("Begunec ≠ migrant", "begunec: preganjanje (5 razlogov); migrant: ekonomski/socialni razlogi"),
 ("SDČP ≠ pogodba", "deklaracija, skupni ideal; zavezujoča pakta iz 1966"),
 ("UPR ≠ poročanje odboru", "UPR političen, univerzalen, charter-based; odbor nadzoruje svojo pogodbo"),
 ("Stališče odbora ≠ sodba ESČP", "odbor: priporočila; ESČP: zavezujoča sodba (čl. 46)"),
 ("Forum internum ≠ externum", "prepričanje absolutno; manifestiranje omejljivo"),
 ("Progresivna realizacija ≠ nedelovanje", "minimalno jedro + nediskriminacija takoj"),
 ("Genocid ≠ vsak množični zločin", "zahteva dolus specialis + 4 zaščitene skupine"),
 ("Okolje ≠ razvoj", "okolje: A/RES/76/300 (priznano); razvoj: Deklaracija 1986 (nezavezujoča)"),
 ("Prejšnji izpit ≠ letošnji seznam", "dokaz sloga in ponavljajočega se jedra, ne garancija"),
]
for t, a in TRAPS:
    card(f"NE ZAMEŠAJ: {t}", a, kind="trap", topics=["nadzor"], authority="B")

# Entity-derived cards (top facts)
for n in cg["nodes"]:
    if n.get("type") in ("treaty","institution") and n.get("facts") and len(cards) < 260:
        f = n["facts"]
        if 20 < len(f) < 400:
            card(f"{n['label']} — ključna dejstva?", f, kind="entity", topics=[], authority=n.get("authority","B"))

# Topic-derived cards (3 per topic: legal / monitoring / problems)
for t in TOPICS:
    card(f"[{t['title']}] Pravna podlaga (vir + člen)?", t["legal"], kind="topic", topics=[t["id"]], authority="A")
    card(f"[{t['title']}] Kateri nadzor/postopek?", t["monitoring"], kind="topic", topics=[t["id"]], authority="A")
    card(f"[{t['title']}] Težave v praksi / primeri?", t["problems"], kind="topic", topics=[t["id"]], authority="C")

w("flashcards.json", cards)
print(f"  flashcards.json: {len(cards)}")

# ============================================================
# 6. QUIZ — past exams + bank + scenarios
# ============================================================
questions = []
def q(qid, qtype, prompt, points, topics, outline, provenance, official, mcq=None):
    questions.append({"id": qid, "type": qtype, "prompt": prompt, "points": points,
                      "topics": topics, "answerOutline": outline, "provenance": provenance,
                      "officialStatus": official, "mcq": mcq})

# Past exam questions (2025 + 2026 roki, E) with model outlines (D, from verified guide)
q("q01","short","Ali je za vse države običaj enak kot člen? (persistent objector, jus cogens, ICJ 38(1)(b))",2,
  ["obicaj"],
  ["običaj = state practice + opinio juris (ICJ Statut 38(1)(b))","zavezuje vse države; izjema: persistent objector","jus cogens (mučenje, genocid) — brez izjem","člen zavezuje samo pogodbenice"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q02","short","Kaj je bil cilj varstva manjšin v okviru DN?",2,
  ["zgodovina","manjsine"],
  ["mir, stabilnost, varnost novih mej po 1. sv. vojni","ne humanitarne vzgibe","diskriminatoren sistem (zmagovalke izključene)","nadzor pri DN"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q03","short","Zakaj je mednarodni režim večnivojski? Kateri so nivoji?",2,
  ["rezim"],
  ["nobena raven sama ne zadostuje","globalna (OZN) → regionalna (SE, OAD, AU, arabska) → subregionalna (EU) → bilateralna → nacionalna → lokalna"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q04","short","Vincent: 5 elementov pravice — pojasni vsakega in poveži z varstvom ČP",6,
  ["koncept"],
  ["subjekt (individualne/kolektivne)","objekt (do/pred)","uveljavljanje (paradoks posesti)","nosilec dolžnosti (država; Shue: 3 dolžnosti)","utemeljitev","uporaba na primeru"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q05","short","Načela režima varstva ČP",2,
  ["koncept"],
  ["univerzalnost/splošnost","neodtujljivost","nedeljivost (Dunaj 1993)","soodvisnost","nediskriminacija"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q06","short","Nastanek OZN in ČP v UL OZN",2,
  ["zgodovina"],
  ["»nikoli več« — holokavst, nacizem, fašizem","ČP = sestavni del miru in varnosti","UL čl. 1(3): razvijati + spodbujati","ni seznama ČP v UL"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q07","short","2 vrsti nadzornih mehanizmov + primeri",4,
  ["nadzor"],
  ["pogodbeni (treaty-based): Odbor za ČP (18 strokovnjakov), CESCR, CAT Odbor — samo pogodbenice","splošni (charter-based): Komisija (1946–2006) → Svet za ČP (2006, 47 držav), OHCHR — vse članice","rezultat: priporočila (sprejme/delno/zavrne)"],"vsi izpiti","pastRecall")
q("q08","short","Azijske vrednote — Sen članek",4,
  ["regionalni"],
  ["kulturni relativizem kot izgovor avtoritarnih režimov","Sen: univerzalnost združljiva z azijskimi tradicijami","Azija: ni regionalne listine ČP","Jenco 2013, Lind 2009"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q09","short","ESČP: koliko sodnikov, mandat, volitve, naloge",4,
  ["regionalni"],
  ["št. sodnikov = 46 (kolikor je držav članic Sveta Evrope po izključitvi Rusije 2022 — ne pisati 47!)",
   "mandat 9 let, brez ponovne izvolitve (P14 čl. 23)",
   "izbira: Parlamentarna skupščina SE izmed 3 kandidatov države (kandidat mora biti mlajši od 65 let ob vložitvi po P15)",
   "formacije: posamezni sodnik / odbori (3) / senati (7) / Veliki senat (17)",
   "naloge in postopek: individualne (čl. 34 — rok 4 mesece po P15) + meddržavne zadeve (čl. 33); sodba zavezujoča (čl. 46), izvrševanje nadzira Odbor ministrov SE"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q10","short","Generacije/mreže ratifikacij — 3 ključne spremembe",3,
  ["ratifikacije"],
  ["15 let pred koncem HV: ozek krog, ZDA nič","ob koncu: širitev (+10 držav), Afrika/Azija začenjajo","15 let po: vse vsaj 1 pogodba; bivše komunistične množično ratificirajo"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q11","short","Prepoved mučenja: A) kdaj prvič B) najnatančnejša definicija C) kam pritožba",4,
  ["mucenje"],
  ["A) Ženevske konvencije (vojni ujetniki)","B) CAT čl. 1 (namerna huda bolečina + namen + uradna oseba)","C) ESČP / Odbor proti mučenju (čl. 22); ICJ za državne spore (čl. 30)","jus cogens; čl. 2 absolutnost; čl. 3 non-refoulement"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q12","short","Begunci in migranti: razlika + kje to piše + člena",2,
  ["begunci","migranti"],
  ["begunec: utemeljen strah pred preganjanjem (5 razlogov) — Konvencija 1951 čl. 1A(2)","migrant: ekonomski/socialni razlogi — ICRMW 1990 čl. 2(1)","non-refoulement: čl. 33 begunci; CAT čl. 3"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q13","short","Ekonomske in socialne pravice: 2 najslabše implementirana člena + primeri",4,
  ["eskp"],
  ["MPESKP: progresivna realizacija (čl. 2(1)) + minimalno jedro","kandidati: stanovanje (čl. 11 — brezdomstvo), zdravstvo (čl. 12 — dostop), hrana","primeri: brezdomstvo v EU, dostop do zdravstva v konfliktih (Jemen, Sudan)"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q14","short","Okolje: kdaj 1. prepoznana kot ČP, kaj je onemogočalo hitrejši sprejem",4,
  ["okolje"],
  ["Stockholmska deklaracija 1972 (rojstvo; UNEP)","pred 1972: ni omembe v SDČP/paktih/EKČP","onemogočalo: suverenost nad viri, razvojne prioritete Juga, nova kategorija","razvoj: Brundtland 1987 → Aarhuška 1998 → A/RES/76/300 (2022)"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q15","short","Genocid: Lemkin, genos+cide, Gaza — pomanjkljivosti konvencije",4,
  ["genocid"],
  ["Lemkin 1944: genos (grško) + cide (latinsko)","čl. II: dolus specialis + 4 skupine + 5 dejanj","Gaza: dokaz namere, enforcement, politika, ozke skupine","čl. IX ICJ"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q16","short","Svoboda izražanja: kaj je, negativni/pozitivni aspekt, mediji/AI",4,
  ["izrazanje"],
  ["SDČP 19; MPDPP 19; EKČP 10","Milton: iskanje, prejemanje, razširjanje","negativni (od vmešavanja) vs. pozitivni (država zagotavlja pogoje)","omejitve 10(2): zakonita + legitimen cilj + nujna v demokratični družbi","AI: algoritmi, dezinformacije, pluralizem"],"1. rok 2025 + 1. rok 2026","pastRecall")
q("q17","short","Razlika med pristojnostmi: Odbor za ČP, Svet za ČP, Komisija za ČP",4,
  ["nadzor"],
  ["Odbor: treaty-based, 18 strokovnjakov, samo pogodbenice","Svet: charter-based, 47 držav, UPR + posebni postopki","Komisija: 1946–2006, politizirana → reforma"],"2. rok 2026 + banka","pastRecall")
q("q18","short","Individualne komunikacije — v katerih pogodbah so možne?",4,
  ["nadzor"],
  ["1. OP MPDPP; OP CEDAW 1999; OP MPESKP 2008; 3. OP CRC 2011; OP CRPD","CAT čl. 22; ICPED čl. 31 (izjava države)","pogoji: izčrpanje domačih sredstev, ne anonimno","2 načina: opcijski protokol ali člen konvencije"],"2. rok 2026","pastRecall")
q("q19","short","Ukrajina: 2 najbolj kršeni normi + na katero doktrino se navezujeta",4,
  ["aktualno","zivljenje","mucenje"],
  ["pravica do življenja (MPDPP čl. 6 / EKČP čl. 2)","prepoved mučenja (čl. 7 / CAT) + prisilna izginotja (ICPED)","humanitarno pravo (Ženevske konvencije)"],"2. rok 2026","pastRecall")
q("q20","short","UPR: potek + ocena (dobro/slabo)",4,
  ["nadzor"],
  ["vsakih 4–4,5 let; poročilo države + shadow reports + poročila OZN","delovna skupina + priporočila držav članic","dobro: vse pravice, tudi nepogodbenice","slabo: priporočila neobvezna, politizacija"],"banka (mvčp-vprašanja) + Seminar 3","professor")
q("q21","short","Pojasnite razliko med Komisijo za ČP, Odborom za ČP in Svetom za ČP",4,
  ["nadzor"],
  ["Komisija: ECOSOC 1946, politizirana → reforma 2006","Svet: 47 držav, UPR, Ženeva","Odbor: treaty-based (MPDPP čl. 28), 18 strokovnjakov"],"banka","professor")
q("q22","short","2 različna načina vzpostavitve pristojnosti odbora za individualne pritožbe (2 primera)",4,
  ["nadzor"],
  ["opcijski protokol: CEDAW OP 1999 (posameznik/skupina, ne anonimno, po izčrpanju)","člen konvencije: CAT čl. 22 (izjava države)"],"banka","professor")
q("q23","short","EKČP vs. ESL: primerjajte varstvo ČP",4,
  ["regionalni"],
  ["EKČP: civilno-politične, ESČP, zavezujoče sodbe","ESL: ekonomske-socialne, kolektivne pritožbe, priporočila","oba pod okriljem Sveta Evrope"],"banka","professor")
q("q24","scenario","Scenarij: država vrača prosilca v državo, kjer mu grozi mučenje. Kateri viri in postopki?",4,
  ["mucenje","begunci"],
  ["Konvencija o beguncih čl. 33 (non-refoulement)","CAT čl. 3 (širša zaščita pred vračanjem v mučenje)","ESČP čl. 3 (posredno); Odbor proti mučenju čl. 22","Italy–Libya primer (Di Nunzio)"],"generated","generatedVariant")
q("q25","scenario","Scenarij: platforma izbriše politično objavo, država nima varovalk. Razloži obveznosti.",4,
  ["izrazanje"],
  ["negativna obveznost (nevmešavanje) + pozitivna (pluralizem)","MPDPP 19 / EKČP 10 + 3-delni test omejitev","zasebne platforme: državna pozitivna obveznost regulacije","AI: algoritemska pristranskost, netransparentnost"],"generated","generatedVariant")
q("q26","scenario","Scenarij: država ne preiskuje serije skrivnih odvzemov prostosti.",4,
  ["izginotja"],
  ["ICPED čl. 2 definicija (2 elementa)","čl. 5 zločin proti človeškosti; čl. 6 nadrejeni","Velásquez-Rodríguez: pozitivna/procesna obveznost","Odbor za izginotja; ESČP"],"generated","generatedVariant")
q("q27","scenario","Scenarij: množični poboji politične skupine. Je genocid?",4,
  ["genocid"],
  ["čl. II: 4 zaščitene skupine — politična NI med njimi","dolus specialis potreben","alternativa: zločin proti človeškosti (Rimski statut čl. 7)"],"generated","generatedVariant")
q("q28","scenario","Scenarij: država trdi, da si ne more privoščiti nujne zdravstvene oskrbe.",4,
  ["eskp"],
  ["MPESKP čl. 2(1): progresivna realizacija ni prazna oprostitev","minimalne osnovne obveznosti takoj","nediskriminacija takoj","Odbor za ESKP; OP 2008 pritožbe"],"generated","generatedVariant")
# Missing bank questions (from mvčp-vprašanja)
q("q29","short","Analizirajte ključne zgodovinske vire: kaj je njihov ključni prispevek pri oblikovanju koncepta ČP?",4,
  ["zgodovina"],
  ["Hamurabi (~1700 pr.n.št.): predpostavka nedolžnosti, dokazi obeh strani, predpisan postopek","Magna Carta 1215: kralj podrejen zakonu, določila 39/40 (predhodnica habeas corpus), nadzor 25 baronov","Angleška listina pravic 1689: parlament — suverenost parlamenta, svoboda govora v parlamentu, svoboda veroizpovedi","Deklaracija neodvisnosti ZDA 1776: naravne, prirojene, neodtujljive pravice (življenje, svoboda, sreča) — izključeni sužnji/ženske/staroselci","Francoska deklaracija 1789: univerzalnost (vedno, povsod, za vsakogar), suverenost ljudstva, čl. 1, 5, 7, 10, 12, 13"],"banka (mvčp-vprašanja)","professor")
q("q30","short","Kakšno mesto zavzemajo ČP v UL OZN (kje in kako so omejene)?",2,
  ["zgodovina","nadzor"],
  ["UL OZN NE vsebuje seznama ČP","čl. 1(3): uresničevati mednarodno sodelovanje — razvijati (konvencije) in spodbujati (implementacija) spoštovanje ČP","UL OZN je okvir — podrobne pravice so v konvencijah (SDČP, pakta, CAT, CEDAW, CRC...)","omejitev: suverenost držav (čl. 2(7) — nevmešavanje v notranje zadeve)"],"banka (mvčp-vprašanja)","professor")
q("q31","short","Kako so razlike med Severom in Jugom vplivale na oblikovanje vsebine MVČP?",4,
  ["ratifikacije","listina"],
  ["Zahod (Sever): civilno-politične pravice (1. generacija) — posameznik, svoboda","Vzhod/Jug: ekonomske-socialne pravice (2. generacija) — skupnost, blaginja","razlog za 2 pakta (1966): suverenost vs. nadzor, posameznik vs. skupnost, vsebina ČP","3. generacija (solidarnostne): razvoj, okolje, mir — pogosto nezavezujoče (Jug potrebuje)"],"banka (mvčp-vprašanja)","professor")
q("q32","short","3 vrste pritožbenih postopkov pred Svetom za ČP",4,
  ["nadzor"],
  ["individualne pritožbe (podpisana, izčrpana domača sredstva, razlaga kršitve, podlaga v pogodbi)","meddržavne pritožbe (suverenost, nevmešavanje — občutljivo, soočenje mnenj)","preiskave (zaupna preiskava na podlagi zanesljivih informacij o hudih kršitvah)","mandat lahko preneha državi s hudimi kršitvami"],"banka (mvčp-vprašanja)","professor")
q("q33","short","Kako uporabiš postopek pred ESČP, če meniš, da ti je bila kršena pravica iz EKČP?",4,
  ["regionalni"],
  ["čl. 34: posameznik, NGO ali skupina lahko vloži pritožbo","pogoji dopustnosti (čl. 35): žrtev, jurisdikcija države, izčrpanje domačih sredstev, 6-mesečni rok","sodišče odloči — sodba je končna in pravno zavezujoča (čl. 46)","Odbor ministrov nadzoruje izvršitev"],"banka (mvčp-vprašanja)","professor")
q("q34","short","Primerjaj individualne/kolektivne pritožbe v EKČP in ESL (2 primera)",4,
  ["regionalni"],
  ["EKČP individualne (čl. 34): posameznik/NGO proti državi — sodba zavezujoča (čl. 46)","ESL kolektivne: sindikati/NGO → Evropski odbor za socialne pravite → Odbor ministrov (priporočilo)","EKČP: civilno-politične, zavezujoče sodbe; ESL: ekonomske-socialne, priporočila","skupno: obe pod Svetom Evrope, Odbor ministrov nadzoruje"],"banka (mvčp-vprašanja)","professor")
q("q35","scenario","Scenarij: država prepoveduje nošenje verskih simbolov v šolah. Kateri členi in test?",4,
  ["veroizpoved"],
  ["EKČP čl. 9; MPDPP čl. 18","forum externum (manifestiranje vere — omejljivo, ne internum)","9(2): zakonita + legitimen cilj (pravice drugih, javni red) + nujno v demokratični družbi","ESČP: margin of appreciation (ocenitveni prostor držav)"],"generated","generatedVariant")
q("q36","scenario","Scenarij: narod zahteva odcepitev. Katera pravica in kaj je problem?",4,
  ["samoodlocba"],
  ["MPDPP čl. 1 = MPESKP čl. 1 (pravica do samoodločbe)","zunanja samoodločba (odcepitev) vs. notranja (avtonomija)","problem: kdo je 'narod'? (Vincent — kolektivni subjekt)","Klabbers 2006: pravna narava sporna; Palestina kot primer"],"generated","generatedVariant")
q("q37","scenario","Scenarij: država ne preprečuje diskriminacije manjšine v šolah. Kateri členi?",4,
  ["manjsine"],
  ["MPDPP čl. 27 (edini globalni zavezujoč — jezik, kultura, vera)","OKVNM čl. 5, 6, 15 (regionalni — Svet Evrope)","ILO 169 (domorodci — če applicable)","Odbor za ČP; Svetovalni odbor (AC)"],"generated","generatedVariant")
w("quiz.json", questions)
print(f"  quiz.json: {len(questions)}")

# ============================================================
# 7. SOURCES — curated deep links
# ============================================================
SOURCES = [
 {"id":"ohchr-gc","title":"General Comments (OHCHR)","titleEn":"General comments","url":"https://www.ohchr.org/en/treaty-bodies/general-comments","body":"Splošni komentarji vseh pogodbenih teles — interpretacija pogodb.","topics":[]},
 {"id":"tb-database","title":"Treaty Body Database","url":"https://tbinternet.ohchr.org/_layouts/15/treatybodyexternal/TBSearch.aspx?Lang=en","body":"Poročila držav, sklepna ugotovitve, splošni komentarji.","topics":[]},
 {"id":"uhri","title":"Universal Human Rights Index (UHRI)","url":"https://uhri.ohchr.org/en/","body":"Priporočila UPR + pogodbenih teles + posebnih postopkov, iskanje po državah.","topics":["nadzor"]},
 {"id":"upr-info","title":"UPR Info","url":"https://upr-info.org","body":"UPR proces, priporočila, sledenje izvedbi.","topics":["nadzor"]},
 {"id":"hudoc","title":"HUDOC (ESČP)","url":"https://hudoc.echr.coe.int","body":"Sodbe ESČP — iskanje po členu EKČP.","topics":["regionalni"]},
 {"id":"un-treaties","title":"UN Treaty Collection","url":"https://treaties.un.org","body":"Besedila pogodb, ratifikacije, zadržki.","topics":["ratifikacije"]},
 {"id":"gov-si","title":"gov.si — mednarodne pogodbe","url":"https://www.gov.si/assets/ministrstva/MZZ/Dokumenti/multilaterala/clovekovepravice/","body":"Slovenska besedila pogodb (MPDPP itd.).","topics":[]},
 {"id":"ohchr-instruments","title":"OHCHR — Core Instruments","url":"https://www.ohchr.org/EN/ProfessionalInterest/Pages/CoreInstruments.aspx","body":"Temeljne konvencije (tudi tiste, ki niso v knjigi Dokumenti).","topics":[]},
 {"id":"icj","title":"Meddržavno sodišče (ICJ)","url":"https://www.icj-cij.org","body":"Sodbe in advisory opinions (genocid čl. IX, okolje).","topics":["genocid","okolje"]},
 {"id":"icc","title":"Mednarodno kazensko sodišče (ICC)","url":"https://www.icc-cpi.int","body":"Rimski statut; individualna kazenska odgovornost.","topics":["genocid"]},
 {"id":"upr-slo","title":"UPR — Slovenija","url":"https://www.upr-info.org/en/state/slovenia","body":"Priporočila Sloveniji po krogih UPR.","topics":["nadzor"]},
 {"id":"ccpr-gc34","title":"CCPR Splošni komentar 34 (svoboda izražanja)","url":"https://tbinternet.ohchr.org/_layouts/15/treatybodyexternal/TBSearch.aspx?Lang=en&TreatyID=8&DocTypeID=11","body":"Podrobna razlaga čl. 19 MPDPP in omejitev.","topics":["izrazanje"]},
 {"id":"cescr-gc","title":"CESCR splošni komentarji (3, 13, 14 …)","url":"https://tbinternet.ohchr.org/_layouts/15/treatybodyexternal/TBSearch.aspx?Lang=en&TreatyID=9&DocTypeID=11","body":"GC 3 (obveznosti), GC 13 (izobraževanje), GC 14 (zdravstvo).","topics":["eskp"]},
]
w("sources.json", SOURCES)

# ============================================================
# 8. GREEN BOOK INDEX (Dokumenti ČP companion — from master-skripta kazipot)
# ============================================================
GREENBOOK = [
 {"topic":"Nediskriminacija","articles":"UL OZN 1(3); SDČP 2; MPDPP 2(1); MPESKP 2(2); EKČP 14; Listina EU 21; AmK 1; Afriška 2; Arabska 3","inBook":True,"bookPages":"SDČP, MPDPP, EKČP","missingWarning":None},
 {"topic":"Pravica do življenja","articles":"SDČP 3; MPDPP 6; EKČP 2; Listina EU 2; Afriška 4; AmK 4 (od spočetja!)","inBook":True,"bookPages":"MPDPP str. 85, EKČP str. 145","missingWarning":"13. protokol k EKČP (popolna odprava smrtne kazni v vseh okoliščinah) preveri, če je v prilogi!"},
 {"topic":"Prepoved mučenja","articles":"SDČP 5; MPDPP 7; CAT čl. 1 (4 elementi definicije!), čl. 2 (absolutnost), čl. 3 (non-refoulement); EKČP 3","inBook":True,"bookPages":"CAT str. 210, EKČP str. 146","missingWarning":"⚠️ OPCAT 2002 (preventivni obiski SPT + NPM) NI v knjigi! Nauči se na pamet!"},
 {"topic":"Genocid","articles":"Konvencija o genocidu 1948 čl. II (dolus specialis, 4 skupine, 5 dejanj), čl. III, VI, IX (ICJ)","inBook":True,"bookPages":"Konvencija o genocidu str. 45","missingWarning":None},
 {"topic":"Samoodločba","articles":"MPDPP čl. 1 = MPESKP čl. 1 (identična!); UL OZN 1(2), 55; Afriška listina 20","inBook":True,"bookPages":"MPDPP str. 81, MPESKP str. 67","missingWarning":None},
 {"topic":"Manjšinske pravice","articles":"MPDPP čl. 27 (edini globalni zavezujoč); Deklaracija 1992; OKVNM čl. 5, 6, 15","inBook":True,"bookPages":"MPDPP str. 94, OKVNM str. 310","missingWarning":"ILO 169 (domorodna ljudstva) in sistem Društva narodov (za mir, ne humanitarno) nista v besedilih!"},
 {"topic":"Pravice žensk","articles":"CEDAW čl. 1 (definicija diskriminacije), čl. 4 (posebni ukrepi/kvote); OP-CEDAW 1999 (pritožbe)","inBook":True,"bookPages":"CEDAW str. 180","missingWarning":"⚠️ Istanbulska konvencija 2011 (nasilje nad ženskami) in Pekinška deklaracija 1995 NISTA v knjigi!"},
 {"topic":"Begunci","articles":"Konvencija o statusu beguncev 1951 čl. 1A(2) (utemeljen strah pred preganjanjem — 5 razlogov!), čl. 33 (non-refoulement)","inBook":True,"bookPages":"Konvencija o beguncih str. 115","missingWarning":"Protokol 1967 (odprava časovnih in geografskih omejitev) je kratek, preveri vsebino!"},
 {"topic":"Delavci migranti (ICRMW)","articles":"ICRMW 1990 čl. 2(1) (definicija delavca migranta); čl. 18 (enakost pred sodišči)","inBook":False,"bookPages":"NI V KNJIGI","missingWarning":"⚠️ ICRMW 1990 NI V KNJIGI! Nauči se na pamet: čl. 2(1) definicija, ratificirale le države izvora (nizka ratifikacija na Zahodu)!"},
 {"topic":"Pravica do čistega okolja","articles":"Stockholm 1972 (UNEP); Aarhuška konvencija 1998 (3 procesne pravice); A/RES/76/300 (2022 priznanje GS OZN)","inBook":False,"bookPages":"NI V KNJIGI","missingWarning":"⚠️ A/RES/76/300 (2022) in Aarhuška konvencija NISTA v knjigi! Nauči se na pamet kronologijo 1972 → 2022!"},
 {"topic":"Pravica do razvoja","articles":"Deklaracija o pravici do razvoja 1986 (res. 41/128) — individualna + kolektivna pravica","inBook":False,"bookPages":"NI V KNJIGI","missingWarning":"⚠️ Deklaracija 1986 NI v knjigi! Zapomni si: NI pravno zavezujoča (Schrijver za konvencijo, Subedi programski dokument)!"},
 {"topic":"Svoboda izražanja","articles":"SDČP 19; MPDPP 19; EKČP 10 (10(2) 3-delni test: zakonito + legitimen cilj + nujno v demokratični družbi)","inBook":True,"bookPages":"MPDPP str. 90, EKČP str. 152","missingWarning":"Milton (Areopagitica 1644), Splošni komentar 34 in vprašanja AI/algoritmov se nauči na pamet!"},
 {"topic":"Svoboda veroizpovedi","articles":"SDČP 18; MPDPP 18; EKČP 9 (forum internum = absolutno / forum externum = omejljivo po 9(2))","inBook":True,"bookPages":"MPDPP str. 89, EKČP str. 151","missingWarning":"Razlikovanje internum (absolutno) vs. externum (omejljivo) ni v besedilu izrecno poimenovano z latinskimi izrazi — nauči se terminologijo!"},
 {"topic":"Ekonomske in socialne pravice","articles":"MPESKP čl. 2(1) (progresivna realizacija + minimalno jedro TAKOJ!), čl. 6-13; ESL 1961/1996","inBook":True,"bookPages":"MPESKP str. 67, ESL str. 260","missingWarning":"⚠️ Opcijski protokol k MPESKP (2008 — individualne pritožbe) NI v knjigi!"},
 {"topic":"Otrokove pravice","articles":"CRC 1989 čl. 1 (<18), čl. 3 (najboljša korist otroka), čl. 12 (participacija)","inBook":True,"bookPages":"CRC str. 235","missingWarning":"⚠️ 3. opcijski protokol k CRC (2011 — komunikacijski postopek/pritožbe) NI v stari knjigi!"},
 {"topic":"Pravice oseb z invalidnostjo (CRPD)","articles":"CRPD 2006 čl. 2 (univerzalno oblikovanje + primerna prilagoditev), čl. 9 (dostopnost), čl. 12 (pravna sposobnost)","inBook":False,"bookPages":"NI V KNJIGI","missingWarning":"⚠️ CRPD 2006 NI V KNJIGI! Nauči se na pamet: socialni model (Oliver), čl. 2, 9 in 12 + Berghs 2019!"},
 {"topic":"Prisilna izginotja (ICPED)","articles":"ICPED 2006 čl. 1 (nederogabilnost), čl. 2 (definicija: odvzem + prikrivanje usode), čl. 5 (zločin proti človeškosti)","inBook":False,"bookPages":"NI V KNJIGI","missingWarning":"⚠️ ICPED 2006 NI V KNJIGI! Nauči se na pamet: čl. 1, 2, 5 + sodba Velásquez-Rodríguez!"},
 {"topic":"Nadzorni mehanizmi (Odbor vs. Svet)","articles":"MPDPP čl. 28 (Odbor za ČP: 18 strokovnjakov, poročila čl. 40, meddržavne čl. 41; 1. OP individualne pritožbe)","inBook":True,"bookPages":"MPDPP str. 94","missingWarning":"⚠️ Resolucija GA Res 60/251 (ustanovitev Sveta za ČP 2006, 47 držav, UPR) NI v knjigi!"},
 {"topic":"Reforma ESČP (Protokola 14 in 15)","articles":"EKČP čl. 23 (mandat 9 let brez ponovne izvolitve), čl. 34 (individualne), čl. 35 (dopustnost: 4 mesečni rok!), čl. 46 (zavezujočnost)","inBook":True,"bookPages":"EKČP str. 145","missingWarning":"⚠️ 14. in 15. protokol (46 sodnikov, kandidatura pod 65 let, 4-mesečni rok po P15) sta novejša od knjige! Nauči se te številke na pamet!"},
]
w("greenbook.json", GREENBOOK)

# ============================================================
# 9. EXAMS (structure for simulator)
# ============================================================
EXAMS = [
 {"id":"rok1-2026","title":"1. rok 2026","year":2026,"durationMin":75,"questionIds":["q01","q02","q03","q04","q05","q06","q07","q08","q09","q10","q11","q12","q13","q14","q15","q16"],"formatNote":"15 vprašanj (rokpisni zapiski ⚠️)"},
 {"id":"rok2-2026","title":"2. rok 2026","year":2026,"durationMin":75,"questionIds":["q04","q17","q18","q19","q06","q12","q14","q15"],"formatNote":"6 vprašanj + teme: genocid, mučenje, okolje, ženske (⚠️)"},
 {"id":"rok1-2025","title":"1. rok 2025","year":2025,"durationMin":75,"questionIds":["q01","q02","q03","q04","q05","q06","q07","q08","q09","q10","q11","q12","q13","q14","q15","q16"],"formatNote":"15 vprašanj (~52+ točk)"},
]
w("exams.json", EXAMS)

# ============================================================
# 10. DOC MANIFEST (downloaded primary docs)
# ============================================================
DOCS = [
 {"id":"gc34","title":"CCPR General Comment 34 — Svoboda izražanja (čl. 19)","url":"https://www.ohchr.org/en/treaty-bodies/ccpr","file":"CCPR-GC34.pdf","topics":["izrazanje"],"authority":"A"},
 {"id":"gc36","title":"CCPR General Comment 36 — Pravica do življenja (čl. 6)","url":"https://www.ohchr.org/en/treaty-bodies/ccpr","file":"CCPR-GC36.pdf","topics":["zivljenje"],"authority":"A"},
 {"id":"gc3","title":"CESCR General Comment 3 — Narava obveznosti (čl. 2(1))","url":"https://www.ohchr.org/en/treaty-bodies/cescr","file":"CESCR-GC3.pdf","topics":["eskp"],"authority":"A"},
 {"id":"gc13","title":"CESCR General Comment 13 — Pravica do izobraževanja","url":"https://www.ohchr.org/en/treaty-bodies/cescr","file":"CESCR-GC13.pdf","topics":["eskp"],"authority":"A"},
 {"id":"gc14","title":"CESCR General Comment 14 — Pravica do najvišje dosegljive ravni zdravja","url":"https://www.ohchr.org/en/treaty-bodies/cescr","file":"CESCR-GC14.pdf","topics":["eskp"],"authority":"A"},
 {"id":"res60251","title":"GA Res 60/251 — Svet za človekove pravice","url":"https://www2.ohchr.org/english/bodies/hrcouncil/docs/a.res.60.251_en.pdf","file":"GA-Res-60-251.pdf","topics":["nadzor"],"authority":"A"},
 {"id":"res76300","title":"A/RES/76/300 — Pravica do čistega okolja (2022)","url":"https://docs.un.org/en/A/RES/76/300","file":"A-RES-76-300.pdf","topics":["okolje"],"authority":"A"},
 {"id":"upr-guide","title":"UPR — praktični vodnik","url":"https://www.ohchr.org/en/upr","file":"UPR-guide.pdf","topics":["nadzor"],"authority":"A"},
]
w("docs-manifest.json", DOCS)

# ============================================================
# 11. GLOSSARY (sl/en)
# ============================================================
GLOSSARY = [
 {"term":"non-refoulement","sl":"nevračanje — prepoved vračanja osebe v državo, kjer ji grozi preganjanje/mučenje"},
 {"term":"jus cogens","sl":"imperativne norme, ki zavezujejo vse države brez izjem (mučenje, genocid)"},
 {"term":"persistent objector","sl":"država, ki je dosledno nasprotovala nastajanju običajnega pravila — izjema od zavezujočnosti"},
 {"term":"dolus specialis","sl":"posebni namen uničiti zaščiteno skupino (genocid)"},
 {"term":"forum internum / externum","sl":"notranje prepričanje (absolutno) / manifestiranje vere (omejljivo)"},
 {"term":"progresivna realizacija","sl":"MPESKP čl. 2(1) — pravice uresničevati postopno, toda minimalno jedro takoj"},
 {"term":"margin of appreciation","sl":"ocenitveni prostor držav pri omejevanju pravic (ESČP doktrina)"},
 {"term":"UPR","sl":"splošni periodični pregled — vsaka država OZN pregledana vsakih 4–4,5 let"},
 {"term":"treaty-based / charter-based","sl":"pogodbeni nadzor (samo pogodbenice) / splošni nadzor (vse članice OZN)"},
 {"term":"opcijski protokol","sl":"dopolnilna pogodba (npr. individualne pritožbe); za veljavo 10 ratifikacij"},
 {"term":"paradoks posesti","sl":"formalno imaš pravico, praktično je ne uživaš (Vincent)"},
 {"term":"habeas corpus","sl":"prepoved prijetja brez zakonite sodbe (Magna Carta 39/40)"},
 {"term":"dolus specialis","sl":"posebni namen (genocid) — najtežje za dokazati"},
 {"term":"zadržek (reservation)","sl":"državina izjava, kako bo razumela določilo pogodbe — prvi filter ratifikacij"},
 {"term":"clandestine repression","sl":"skrito državno nasilje (prisilna izginotja) — Velásquez-Rodríguez"},
 {"term":"backlog / zamašitev","sl":"preobremenjenost ESČP — razlog za Protokol 14"},
]
# Glossary cards (appended after GLOSSARY definition)
for g in GLOSSARY:
    cards.append({"id": f"fc{len(cards)+1:03d}", "prompt": f"Kaj je: {g['term']}?", "answer": g["sl"],
                  "kind": "glossary", "topics": [], "authority": "B", "source": ""})
w("glossary.json", GLOSSARY)
w("flashcards.json", cards)
print(f"  flashcards.json (final): {len(cards)}")

print("\nContent build complete.")
