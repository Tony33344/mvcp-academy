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
 {"id":"zgodovina","title":"Zgodovinski razvoj","titleEn":"Historical development","points":2,
  "body":"**Hamurabi (~1700 pr.n.št.)**: 282 zakonov, zapisani, javni, pogovorni (akadijski) jezik; **predpostavka nedolžnosti**; dokazi obeh strani; varstvo šibkejšega.\n\n**Magna Carta (1215)**: baroni vs. kralj Ivan; **habeas corpus** (določili 39/40); kralj podrejen zakonu; nadzor: komisija 25 baronov; koristniki = fevdalni sloji.\n\n**Angleška listina pravic (1689)**: listina **parlamenta** — suverenost parlamenta, svoboda govora v parlamentu, svobodne volitve, prepoved krutih kazni.\n\n**Deklaracija neodvisnosti ZDA (1776)**: **naravne, prirojene, neodtujljive** pravice (življenje, svoboda, sreča); izključeni: sužnji, ženske, staroselci.\n\n**Francoska deklaracija (1789)**: **univerzalnost** (vedno, povsod, za vsakogar); suverenost ljudstva; čl. 1, 5, 7, 10, 12, 13.\n\n**Mednarodno:** verska toleranca (po 30-letni vojni) → varstvo manjšin → humanitarno pravo (Ženeva 1864/1949, Haag 1899/1907) → **DN**: Pakt DN NE omenja ČP; varstvo manjšin = za mir in stabilnost novih meja, ne humanitarno — diskriminatoren sistem (poražene: Avstrija, Bolgarija, Madžarska, Turčija; nove: Poljska, SHS, Češkoslovaška, Romunija, Grčija; kasneje vstopajoče: Finska, Albanija, baltske, Irak; **zmagovalke izključene**) → **OZN**: »nikoli več«; čl. 1(3): *razvijati* (konvencije) in *spodbujati* (implementacija) spoštovanje ČP.\n\n**Bistvo:** dokumenti odražajo konflikte in boj — ČP si je bilo treba izboriti."},
 {"id":"koncept","title":"Koncept ČP — Vincent: 5 elementov pravice","titleEn":"Concept of human rights — Vincent's 5 elements","points":6,
  "body":"**Vincent (1986): 5 elementov pravice:**\n1. **Subjekt** (nosilec): individualne / kolektivne pravice (narod pri samoodločbi — problem: kdo je »narod«?)\n2. **Objekt**: pravica DO nečesa (pozitivna) / PRED nečim (negativna)\n3. **Uveljavljanje**: trditi, zahtevati, imeti korist, uživati, opravnomočiti; **paradoks posesti** (formalno imaš pravico, praktično je ne uživaš)\n4. **Nosilec dolžnosti**: predvsem država; tudi posamezniki; **Shue: 3 dolžnosti** — izogibanje prikrajšanju, zaščita pred prikrajšanjem, pomoč prikrajšanim\n5. **Utemeljitev**: moralna racionalnost, filozofska osnova\n\n*Opomba: v rokopisnih izpitnih vprašanjih »Benko/Fenko elementi MS« = Vincentovi elementi.*\n\n**Načela režima:** univerzalnost/splošnost · neodtujljivost · **nedeljivost** (Dunaj 1993 — ni izbire ALI/ALI med pakta) · soodvisnost · **nediskriminacija** (UL OZN 1(3); SDČP 2; MPDPP 2(1); MPESKP 2(2); EKČP 14)."},
 {"id":"rezim","title":"Mednarodni režim (3 elementi) + večnivojskost","titleEn":"International regime — 3 elements, multilevel","points":2,
  "body":"Režim = institucije za upravljanje določenega področja (issue area). **Trije elementi režima za varstvo ČP:**\n1. **Načela** (nedeljivost, temeljnost …)\n2. **Norme in pravila** (konkretna določila — pravica do življenja, svoboda govora …)\n3. **Nadzorni mehanizmi** (institucije, ki nadzorujejo uresničevanje)\n\n**Večnivojski režim — nivoji upravljanja:** globalna (OZN) → regionalna (SE, OAD, AU, arabska) → subregionalna (EU) → bilateralna → nacionalna (ustava, zakonodaja) → lokalna (občine). Zakaj večnivojski: **nobena raven sama ne zadostuje**."},
 {"id":"nadzor","title":"Nadzorni mehanizmi: pogodbeni vs. splošni","titleEn":"Monitoring mechanisms: treaty-based vs charter-based","points":4,
  "body":"**2 vrsti nadzornih mehanizmov:**\n\n**Pogodbeni (treaty-based)** — določeni v vsaki pogodbi, veljajo samo za pogodbenice:\n- **Odbor za človekove pravice** (MPDPP **čl. 28: 18 neodvisnih strokovnjakov**; poročila držav čl. 40 + priporočila)\n- Odbor za ESKP (1985, resolucija ECOSOC 1985/17; delovno telo ECOSOC)\n- Odbor proti mučenju (CAT), CEDAW Odbor, Odbor za otrokove pravice, Odbor za prisilna izginotja, CMW Odbor, CRPD Odbor\n- Država lahko priporočila **sprejme / delno sprejme / zavrne**\n\n**Splošni (charter-based)** — iz UL OZN, veljajo za vse članice:\n- **Komisija za ČP (1946–2006)**: pomožno telo ECOSOC; **preveč politizirana, kršiteljice ČP v njej** → reforma 2006\n- **Svet za ČP (2006)**: stalno telo v Ženevi, **47 držav** (tajno glasovanje, regionalno načelo); **UPR** vsakih 4–4,5 let; posebni postopki (posebni poročevalci); postopek za pritožbe glede vzorcev hudih kršitev; mandat lahko preneha državi s hudimi kršitvami\n- OHCHR (Visoki komisar)\n\n⚠️ **Profesorica izrecno: Odbor za ČP NI ENAKO Svet za ČP.**\n\n**UPR — ocena:** dobro: pregled vseh pravic, tudi nepogodbenic; hitrejše in preglednejše po reformi; slabo: priporočila **neobvezna**, politizacija (države sledijo interesom).\n\n**Individualne pritožbe — 2 načina vzpostavitve pristojnosti:** ① poseben **opcijski protokol** (1. OP k MPDPP, OP CEDAW 1999, OP MPESKP 2008, OP CRC 2011, OP CRPD) ② **izjava države po členu konvencije** (CAT čl. 22; ICPED čl. 31). Pogoji: izčrpanje domačih sredstev, ne anonimno, žrtev pod jurisdikcijo. **MPDPP čl. 41 = meddržavne, ne individualne komunikacije.**"},
 {"id":"obicaj","title":"Običajno pravo vs. pogodbeno; jus cogens; persistent objector","titleEn":"Customary vs treaty law","points":2,
  "body":"- Običaj = **state practice + opinio juris**; vir: **čl. 38(1)(b) Statuta ICJ** (»splošna praksa, sprejeta kot pravo«)\n- Zavezuje **vse države**; edina izjema: **persistent objector** (država, ki je dosledno, aktivno in eksplicitno nasprotovala od začetka nastajanja pravila)\n- Izjema ne velja za **jus cogens** (imperativne norme: prepoved mučenja, genocida) — zavezujejo brezpogojno\n- Člen konvencije zavezuje **samo pogodbenice** (ratifikacija/pristop); pogodbe lahko kodificirajo običaj ali k njemu prispevajo\n- Primeri običajnega prava: prepoved mučenja, prepoved genocida, non-refoulement, deli SDČP"},
 {"id":"ratifikacije","title":"Ratifikacijska omrežja — 3 obdobja; kdaj dokument zavezuje","titleEn":"Ratification networks — 3 periods","points":3,
  "body":"**Analiza omrežja ratifikacij (predavanja):**\n1. **15 let pred koncem hladne vojne**: notranji krog ozek, regionalno mešan (avtokratske LA/EVR + demokratične EVR); Afrika/Azija izključene; **ZDA nič ne ratificira**\n2. **Ob koncu HV**: krog se širi (+10 držav: LA, Madžarska, Sirija …), Jugoslavija izstopi iz notranjega kroga; Afrika/Azija začenjajo; ZDA še vedno obrobje\n3. **15 let po koncu HV**: vse države vsaj 1 pogodba — sistem **resnično svetoven**; razpad blokov → bivše komunistične države množično ratificirajo (vključitev v OZN); notranji krog = države, ki iščejo odobravanje\n\n**Kdaj dokument postane pravno zavezujoč:** ratifikacija **35 držav** (pakta) / **10** (opcijski protokoli) + notranja potrditev (pri nas DZ); izjema: SFRJ-nasledstvo (dokumenti pred 1991). **Zadržek (reservation)** = prvi filter: država zapiše, kako bo razumela določilo."},
 {"id":"regionalni","title":"Regionalni sistemi + azijske vrednote (Sen)","titleEn":"Regional systems","points":4,
  "body":"- **EKČP (1950/53)**: čl. 2 življenje, 3 mučenje, 9 veroizpoved, 10 izražanje, 14 nediskriminacija\n- **ESČP**: št. sodnikov = št. pogodbenic; **mandat 9 let, brez ponovne izvolitve** (P14 čl. 23); izbira: **Parlamentarna skupščina SE**; formacije: posamezni sodnik / odbori (3) / senati (7) / **Veliki senat (17)**; individualne pritožbe čl. 34; dopustnost čl. 35; sodba **zavezujoča čl. 46**; **P14** = reforma zamašitve (backlog)\n- **ESL**: ekonomske/socialne; **kolektivne pritožbe** (sindikati, NGO) → Evropski odbor za socialne pravice → Odbor ministrov (priporočilo)\n- **Ameriška konvencija (1969/78)**; **Afriška listina (1981/86** — samoodločba ljudstev čl. 20, dolžnosti posameznika); **Arabska listina (1994; 2004/08)**; **Azija: ni regionalne listine**\n- **Azijske vrednote — Sen (2015)**: kulturni relativizem = **izgovor** avtoritarnih režimov; univerzalnost je združljiva z azijskimi tradicijami; + Jenco 2013, Lind 2009\n- **Populizem**: Roth 2017; **Helfer 2020** (napad na institucije ČP)"},
 {"id":"listina","title":"Listina človekovih pravic + zakaj 2 pakta","titleEn":"International Bill of Rights","points":2,
  "body":"**Listina človekovih pravic (International Bill of Rights)** = SDČP (1948) + MPDPP (1966/76) + MPESKP (1966/76).\n\n**Zakaj 2 pakta (3 razlogi):**\n1. razmerje mednarodnega varstva ČP ↔ nacionalna suverenost (komunistični blok se je vzdržal glasovanja o SDČP)\n2. interes posameznika (Zahod) vs. interes skupnosti (Vzhod)\n3. vsebina ČP: Zahod = civilno-politične; Vzhod = ekonomske-socialne; bogati vs. revni\n\n**Generacije ČP:** 1. civilno-politične; 2. ekonomske-socialne-kulturne; 3. solidarnostne (razvoj, okolje, mir — pogosto nezavezujoče). Macklem: *three generations or one?* — nedeljivost (Dunaj 1993).\n\n**SDČP**: res. GS 217 A (III), 10. 12. 1948; 30 členov; **politično, ne pravno zavezujoča**; čl. 1 dostojanstvo; čl. 2 nediskriminacija."},
 {"id":"dn_ozn","title":"DN → OZN: vloga in prelomi","titleEn":"League of Nations → UN","points":2,
  "body":"**DN (1920)**: Pakt NE omenja ČP; toda: prepoved suženjstva v nesamoupravnih ozemljih, svoboda misli in veroizpovedi, ILO (humani delovni pogoji), nadzor bolezni (→WHO), Rdeči križ.\n\n**Varstvo manjšin v DN**: razpad 3 cesarstev (Avstro-Ogrske, Otomanskega, Ruskega) → nove heterogene države → manjšine = nevarnost za stabilnost → norme **za mir, ne humanitarno**; diskriminatoren sistem (samo poražene/nove/vstopajoče); nadzor pri DN; ni preprečil 2. sv. vojne. Prispevek: zaščita posameznikov/skupnosti, ne sistematičen pristop.\n\n**OZN (1945)**: »nikoli več«; ČP = sestavni del miru in varnosti; UL čl. 1(3); ECOSOC → Komisija za ČP (1946) → Svet za ČP (2006). **SDČP (1948)**: skupni ideal; pravice pripadajo z rojstvom, neodtujljive."},
 {"id":"aktualno","title":"Aktualne teme: Gaza, Ukrajina, AI, populizem, relativizem","titleEn":"Current events","points":4,
  "body":"- **Gaza** → genocid: čl. II (dolus specialis), čl. IX ICJ; pomanjkljivosti: dokaz namere, enforcement, politika, ozke 4 skupine\n- **Ukrajina** → 2 najbolj kršeni normi: **pravica do življenja + prepoved mučenja/izginotja**; humanitarno pravo\n- **AI/mediji** → izražanje (negativni/pozitivni aspekt; algoritmi, dezinformacije); zasebnost (Citizenfour)\n- **Populizem** → Helfer 2020, Roth 2017: napad na institucije ČP\n- **Kulturni relativizem** → Sen: izgovor; univerzalnost združljiva z azijskimi tradicijami"},
]
w("core.json", CORE)

# ============================================================
# 3. 16 SEMINAR PASSPORTS
# ============================================================
TOPICS = [
 {"id":"zivljenje","n":1,"title":"Pravica do življenja","titleEn":"Right to life","status":"seminar",
  "legal":"MPDPP čl. 6 (omejitve: smrtna kazen po sodbi, nuja, vojni akt); EKČP čl. 2; 13. protokol (odprava smrtne kazni); Afriška listina čl. 4; AmK čl. 4 (od spočetja)",
  "monitoring":"ESČP; Odbor za ČP",
  "problems":"pozitivne obveznosti (preiskava umorov, zaščita življenja); smrtna kazen; femicid",
  "model":"definicija → členi po ravneh (globalno/regionalno) → negativne + pozitivne obveznosti → omejitve → primer",
  "materials":["MVČP_life.pdf","01_pravica_do_zivljenja.md","Vzorec-Pravice do življenja"]},
 {"id":"mucenje","n":2,"title":"Prepoved mučenja","titleEn":"Prohibition of torture","status":"jedro+seminar",
  "legal":"CAT 1984 čl. 1 (definicija: namerna huda bolečina/trpljenje + namen + uradna oseba; izključene zakonite sankcije); čl. 2 absolutnost; čl. 3 non-refoulement; EKČP čl. 3; MPDPP čl. 7; SDČP čl. 5; jus cogens",
  "monitoring":"Odbor proti mučenju (čl. 20 preiskave, 21 meddržavne, 22 individualne); ESČP; ICJ (čl. 30) za spore; OPCAT: SPT + NPM",
  "problems":"Tate 2013 — absolutna prepoved v praksi zataji (tajni pripori, izročitev, »ticking bomb«)",
  "model":"kdaj prvič (Ženevske konvencije — vojni ujetniki) → najnatančneje CAT čl. 1 → pritožba: ESČP/Odbor (ICJ za državne spore) → jus cogens → Tate kritika",
  "materials":["p. 2. povzetek-prepoved-mucenja-v2.pdf","P2_Prepoved mučenja_pisni izdelek.pdf","02_prepoved_mucenja.md","OPCAT quicksheet"]},
 {"id":"izginotja","n":3,"title":"Varstvo pred prisilnimi izginotji","titleEn":"Enforced disappearances","status":"seminar",
  "legal":"ICPED 2006: čl. 1 nederogabilnost; čl. 2 definicija (odvzem svobode + zanikanje usode); čl. 4 kriminalizacija; čl. 5 široka praksa = zločin proti človeškosti; čl. 6 odgovornost nadrejenih",
  "monitoring":"Odbor za prisilna izginotja (individualne + meddržavne); ESČP; Medameriško sodišče",
  "problems":"Velásquez-Rodríguez — država odgovorna, če ne preiskuje/preprečuje (clandestine repression)",
  "model":"definicija (2 elementa!) → členi → zločin proti človeškosti → Velásquez → Ukrajina/Sirija",
  "materials":["P1_pogodba.pdf","P1_Varstvo pred prisilnimi izginotji.pdf","Aguilar 2019","ICPED quicksheet"]},
 {"id":"otroci","n":4,"title":"Otrokove pravice","titleEn":"Children's rights","status":"seminar",
  "legal":"CRC 1989 (res. 44/25): čl. 1 (<18); čl. 3 najboljša korist; P2 (oboroženi konflikti, prostitucija/pornografija); P3 (komunikacijski postopek, 2011); 196 ratifikacij (ne ZDA); Afriška listina o otrokih 1990",
  "monitoring":"Odbor za otrokove pravice (P3)",
  "problems":"Holzscheiter 2019 (child rights governance); neregistrirani otroci (~290 mio), kobalt/Kongo, otroci vojaki (Sirija, Sudan, Ukrajina)",
  "model":"definicija otroka → CRC členi → najboljša korist → P2/P3 → primeri",
  "materials":["P4_Konvencija_o_otrokovih_pravicah.pdf","otrokove pravice.pdf","04_otrokove_pravice.md"]},
 {"id":"zenske","n":5,"title":"Pravice žensk","titleEn":"Women's rights","status":"seminar",
  "legal":"CEDAW 1979 (res. 34/180) čl. 1 (diskriminacija); OP 1999 (individualne pritožbe + preiskave); Deklaracija 1967; Pekinška 1995; Istanbulska konvencija 2011 (nasilje); 189 ratifikacij (ZDA ne)",
  "monitoring":"CEDAW Odbor",
  "problems":"Mohajan 2022 — 4 valove feminizma (1: volilna pravica; 2: 1960s–90s delo/nasilje; 3: 1990s–2000s; 4: 2012+ digitalna, #MeToo); femicid; plače",
  "model":"zgodovina valov → CEDAW čl. 1 → OP → Istanbulska → težave v praksi",
  "materials":["p. 3. povzetek-pravice-zensk.pdf","Pravice zensk.pdf","05_pravice_zensk.md","Pogodba_p3_CEDAW.pdf"]},
 {"id":"invalidi","n":6,"title":"Pravice oseb z invalidnostjo","titleEn":"Disability rights","status":"seminar",
  "legal":"CRPD 2006: čl. 2 (univerzalno oblikovanje; primerna prilagoditev — odklonitev = diskriminacija); čl. 9 dostopnost; čl. 12 pravna sposobnost",
  "monitoring":"CRPD Odbor (+ OP)",
  "problems":"Berghs 2019 — »stronger social model: a social model of human rights«; medicinski → socialni model; izolacija, institucionalizacija",
  "model":"medicinski vs. socialni model → CRPD členi → primerna prilagoditev → primer",
  "materials":["PI_Pravice oseb z invalidnostmi-2.pdf","06_pravice_oseb_z_invalidnostjo.md","Berghs 2019"]},
 {"id":"begunci","n":7,"title":"Begunci","titleEn":"Refugees","status":"seminar",
  "legal":"Konvencija o statusu beguncev 1951 + Protokol 1967: čl. 1A(2) definicija (utemeljen strah pred preganjanjem: rasa, vera, narodnost, mnenje, socialna skupina); čl. 33 non-refoulement; SDČP čl. 14 (azil)",
  "monitoring":"UNHCR; ESČP; Odbor za ČP",
  "problems":"Italy–Libya Memorandum (Di Nunzio 2023): pullbacks = kolektivni izgon + refoulement; zunanja meja EU",
  "model":"definicija begunca (5 razlogov!) → čl. 33 → razlika od migranta → primer",
  "materials":["Konvencija o statusu beguncev.pdf","07_status_in_varstvo_pravic_beguncev_in_migrantov.md"]},
 {"id":"migranti","n":8,"title":"Delavci migranti","titleEn":"Migrant workers","status":"seminar",
  "legal":"ICRMW 1990: čl. 2(1) definicija delavca migranta; nizka ratifikacija (samo države izhoda)",
  "monitoring":"CMW Odbor",
  "problems":"razlika begunec (preganjanje) vs. migrant (ekonomski/socialni razlogi); Sredozemlje",
  "model":"2 konvenciji (1951 + 1990) → definiciji → non-refoulement po begunski konvenciji čl. 33 (+ širša zaščita CAT čl. 3) → primer",
  "materials":["Mednarodna konvencija o zaščiti delavcev migrantov.pdf","07_status_in_varstvo...md","ICRMW quicksheet"]},
 {"id":"eskp","n":9,"title":"Ekonomske in socialne pravice","titleEn":"Economic and social rights","status":"seminar",
  "legal":"MPESKP: čl. 2(1) progresivna realizacija + minimalne osnovne obveznosti; čl. 6 delo, 9 socialno varstvo, 12 zdravstvo, 13 izobraževanje; OP 2008 (individualne pritožbe); ESL (kolektivne pritožbe)",
  "monitoring":"Odbor za ESKP (1985, ECOSOC)",
  "problems":"»2 najslabše implementirana člena + primeri«: stanovanje (brezdomstvo), zdravstvo (dostop), hrana (Jemen, Sudan); neoliberalizem/privatizacija (Breznik/Praznik 2024)",
  "model":"1. vs. 2. generacija → progresivna realizacija → členi → primeri",
  "materials":["08_socialne_pravice.md","09_ekonomske_pravice.md","p 12 EKONOMSKE PRAVICE SEMINARSKA NALOGA.pdf","mvčp-socialne pravice_pisni povzetek1.pdf"]},
 {"id":"okolje","n":10,"title":"Pravica do čistega okolja","titleEn":"Right to a healthy environment","status":"jedro+seminar",
  "legal":"pred 1972 ni omembe (SDČP, pakta, EKČP, AmK) → Stockholmska deklaracija 1972 (rojstvo; 26 načel; UNEP) → Brundtland 1987 (trajnostni razvoj) → Rio 1992 → Aarhuška 1998 (procesne pravice) → Resolucija Sveta za ČP 2021 → A/RES/76/300 (2022)",
  "monitoring":"Svet za ČP; ICJ advisory opinion (preveri status); ESČP posredno",
  "problems":"onemogočalo: suverenost nad viri, razvojne prioritete Juga, okolje kot »nova« kategorija; Held v. Montana; Ogoni/Shell (Nigerija)",
  "model":"kdaj (Stockholm 1972) → kaj je onemogočalo → razvoj do 2022 → procesne pravice (Aarhuška) → primeri",
  "materials":["p. 10. povzetek-pravica-do-okolja.pdf","okolje_seminarska_P3.txt","10_pravica_do_cistega_okolja.md"]},
 {"id":"razvoj","n":11,"title":"Pravica do razvoja","titleEn":"Right to development","status":"seminar",
  "legal":"Deklaracija o pravici do razvoja 1986 (res. 41/128) — NI pravno zavezujoča (politična); individualna + kolektivna",
  "monitoring":"brez posebnega telesa",
  "problems":"Schrijver — potreba po konvenciji; Subedi — programski dokument; Sever–Jug razlike",
  "model":"definicija → ni zavezujoča (za razliko od okolja!) → Sever–Jug → argumenti za konvencijo",
  "materials":["11_pravica_do_razvoja.md","Declaration on the Right to Development.pdf","Schrijver članek"]},
 {"id":"genocid","n":12,"title":"Prepoved genocida","titleEn":"Prohibition of genocide","status":"jedro+seminar",
  "legal":"Konvencija o genocidu 1948/1951: čl. II definicija (dolus specialis + 4 skupine: rasna, verska, etnična, nacionalna + 5 dejanj); čl. III kazniva dejanja; čl. VI sojenje; čl. IX ICJ; Lemkin 1944: genos + cide; Lauterpacht: individualna odgovornost; Nürnberg 1945–46; GA Res 96(I) 1946",
  "monitoring":"ICJ (čl. IX); ICC (Rimski statut)",
  "problems":"Gaza → pomanjkljivosti: dokaz dolus specialis, enforcement, politika, ozke 4 skupine (brez političnih/socialnih)",
  "model":"Lemkin + etimologija → čl. II (4 skupine + 5 dejanj + namernost) → čl. IX ICJ → Gaza pomanjkljivosti",
  "materials":["p. 10. povzetek-prepoved-genocida.pdf","12_prepoved_genocida.md","An Unfulfilled Promise.pdf","GenocideConvention quicksheet"]},
 {"id":"izrazanje","n":13,"title":"Svoboda izražanja","titleEn":"Freedom of expression","status":"seminar",
  "legal":"SDČP čl. 19; MPDPP čl. 19; EKČP čl. 10; Afriška čl. 9; Ameriška čl. 13; Milton Areopagitica 1644 (iskanje, prejemanje, razširjanje); Švedski zakon o svobodi tiska 1766",
  "monitoring":"ESČP; Odbor za ČP (Splošni komentar 34); 4 posebna poročevalca (Joint Declaration 2019)",
  "problems":"omejitve (10(2)/19(3)): zakonita + legitimen cilj + nujna v demokratični družbi; sovražni govor, dezinformacije, algoritmi/AI; negativni (od vmešavanja) vs. pozitivni aspekt",
  "model":"definicija + 3 vidiki → členi → negativni/pozitivni aspekt → 3-delni test omejitev → AI/mediji",
  "materials":["p. 13. povzetek-svoboda-izrazanja.pdf","Svoboda Izražanja Pisni Izdelek.pdf","13_svoboda_izrazanja.md","Howie 2018"]},
 {"id":"veroizpoved","n":14,"title":"Svoboda veroizpovedi","titleEn":"Freedom of religion","status":"seminar",
  "legal":"EKČP čl. 9; MPDPP čl. 18; SDČP 18; forum internum (prepričanje — absolutno) vs. forum externum (manifestiranje — omejljivo)",
  "monitoring":"ESČP; Odbor za ČP",
  "problems":"verska diskriminacija; reformacija (Luther); Poročilo MVČP 2024 (Frank/Šinigoj/Jelerčič)",
  "model":"členi → internum/externum → omejitve → primer",
  "materials":["Poročilo MVČP.pdf","Pravica do veroizpovedi_koncni izdelek","14_svoboda_veroizpovedi.md"]},
 {"id":"samoodlocba","n":15,"title":"Pravica do samooodločbe","titleEn":"Self-determination","status":"seminar",
  "legal":"MPDPP čl. 1 = MPESKP čl. 1 (identična); UL OZN 1(2), 55; Afriška listina čl. 20 (dekolonizacija); jus cogens (po nekaterih)",
  "monitoring":"brez posebnega telesa",
  "problems":"kolektivni subjekt — kdo je »narod«? (Vincent); notranja/zunanja samoodločba; Palestina",
  "model":"člena paktov → kolektivna pravica → dekolonizacija → problem definicije naroda",
  "materials":["PI_PRAVICA DO SAMOODLOČBE MATIJA I DANICA.pdf","15_pravica_do_samoodlocbe.md","Klabbers 2006"]},
 {"id":"manjsine","n":16,"title":"Manjšinske pravice","titleEn":"Minority rights","status":"seminar",
  "legal":"MPDPP čl. 27 (edini globalni zavezujoč); Deklaracija 1992; OKVNM 1995/98 (čl. 5, 6, 15); Arabska listina čl. 25; ILO 169 (domorodci)",
  "monitoring":"Svetovalni odbor (AC, Svet Evrope); Odbor za ČP",
  "problems":"Castellino 2010; DN: varstvo manjšin za mir (diskriminatoren sistem); identiteta (jezik, kultura, vera)",
  "model":"DN zgodovina (cilj: mir!) → čl. 27 → OKVNM → težave",
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
card("CAT 1–2–3?", "čl. 1 definicija mučenja · čl. 2 absolutnost · čl. 3 non-refoulement", topics=["mucenje"], authority="A")
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
card("Magna Carta — 2 ključni prispevka?", "habeas corpus (določili 39/40) · kralj podrejen zakonu; nadzor: 25 baronov", topics=["zgodovina"], authority="B")
card("Hamurabi — 3 sodobni pomeni?", "predpostavka nedolžnosti · dokazi obeh strani · varstvo šibkejšega", topics=["zgodovina"], authority="B")
card("DN in manjšine — pravi cilj?", "mir in stabilnost novih meja, ne humanitarne vzgibe; diskriminatoren sistem", topics=["zgodovina"], authority="B")
card("Paradoks posesti?", "formalno poseduješ pravico (zapisana), praktično je ne uživaš", topics=["koncept"], authority="B")
card("OPCAT — telesa in funkcija?", "SPT (podkomisija za preprečevanje) + NPM (nacionalni mehanizmi); preventivni obiski", topics=["mucenje"], authority="A")
card("Aarhuška konvencija 1998?", "procesne pravice okolja: dostop do informacij, sodelovanje, pravno varstvo", topics=["okolje"], authority="A")
card("Istanbulska konvencija 2011?", "preprečevanje in boj proti nasilju nad ženskami in nasilju v družini", topics=["zenske"], authority="A")
card("Kolektivne pritožbe — kje?", "ESL (sindikati, NGO) → Evropski odbor za socialne pravice → Odbor ministrov", topics=["regionalni"], authority="B")
card("Held v. Montana?", "klimatska sodba — pravica do čistega okolja (ZDA, državna raven)", topics=["okolje"], authority="C")
card("Italy–Libya Memorandum (Di Nunzio 2023)?", "pullbacks = kolektivni izgon + refoulement; zunanja meja EU", topics=["begunci"], authority="C")

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
  ["št. sodnikov = št. pogodbenic EKČP","mandat 9 let, brez ponovne izvolitve (P14 čl. 23)","izbira: Parlamentarna skupščina SE","formacije: posamezni sodnik/odbori(3)/senati(7)/Veliki senat(17)","naloge: individualne + meddržavne zadeve; sodba zavezujoča (čl. 46)"],"1. rok 2025 + 1. rok 2026","pastRecall")
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
 {"topic":"Nediskriminacija","articles":"UL OZN 1(3); SDČP 2; MPDPP 2(1); MPESKP 2(2); EKČP 14; Listina EU 21; AmK 1; Afriška 2; Arabska 3"},
 {"topic":"Pravica do življenja","articles":"SDČP 3; MPDPP 6; EKČP 2 + P13; Listina EU 2; Afriška 4; AmK 4"},
 {"topic":"Prepoved mučenja","articles":"SDČP 5; MPDPP 7; CAT čl. 1 (definicija); EKČP 3; Listina EU 4; OPCAT"},
 {"topic":"Genocid","articles":"Konvencija o genocidu 1948 čl. II (definicija); Rimski statut; ICTY/ICTR statuta"},
 {"topic":"Samoodločba","articles":"MPDPP 1; MPESKP 1; UL OZN 1(2), 55; Afriška listina 20"},
 {"topic":"Manjšinske pravice","articles":"MPDPP 27; Deklaracija 1992; OKVNM 5, 6, 15; Arabska 25; ILO 169"},
 {"topic":"Pravice žensk","articles":"CEDAW čl. 1; OP CEDAW 1999; Pekinška deklaracija 1995; Istanbulska 2011"},
 {"topic":"Begunci in migranti","articles":"SDČP 14; Konvencija 1951 čl. 33 (nevračanje); ICRMW 1990; P7 EKČP"},
 {"topic":"Okolje","articles":"Resolucija Sveta za ČP 2021; A/RES/76/300 (2022); Aarhuška konvencija 1998 čl. 1; Afriška 24"},
 {"topic":"Izražanje","articles":"SDČP 19; MPDPP 19; EKČP 10; Afriška 9; AmK 13"},
 {"topic":"Veroizpoved","articles":"SDČP 18; MPDPP 18; EKČP 9"},
 {"topic":"Socialne/ekonomske","articles":"MPESKP 6–13 (delo 6/7, socialno varstvo 9, zdravstvo 12, izobraževanje 13); ESL"},
 {"topic":"Otrokove pravice","articles":"CRC 1989 (čl. 1, 3); P2, P3; Afriška listina o otrokih 1990"},
 {"topic":"Invalidi","articles":"CRPD 2006 (čl. 2, 9, 12) + OP"},
 {"topic":"Prisilna izginotja","articles":"ICPED 2006 (čl. 1, 2, 4, 5, 6)"},
 {"topic":"Nadzorni mehanizmi","articles":"MPDPP čl. 28 (Odbor); GA Res 60/251 (Svet za ČP); CAT čl. 20–22; OP-ji"},
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
