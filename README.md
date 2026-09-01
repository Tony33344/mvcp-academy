# MVČP Academy

Izobraževalna PWA za **Mednarodno varstvo človekovih pravic** (FDV UL, prof. dr. Petra Roter) — in za vse, ki jih zanima tema.

## Zagon

```bash
npm install
npm run content        # generira src/data/*.json iz korpusa (pot v skripti)
npm run dev            # razvoj (http://localhost:5173)
npm run build          # produkcijski build + PWA (dist/)
npm run preview        # predogled builda (http://localhost:4173)
```

## Funkcije

- **Izpitni način**: jedro snovi, 16 seminarskih pasportov (4 sidra + model odgovora), zeleni priročnik (kazipot členov), simulator izpita (75 min, samopreverjanje po točkah)
- **Flashcards**: FSRS razpršeno ponavljanje (ts-fsrs), 170 kartic (dejstva, členske družine, pasti, slovar), IndexedDB napredek
- **Vprašanja**: 28 vprašanj (izpiti 2025/2026 + banka + scenariji) z modeli odgovorov in rubrikami
- **Graf znanja**: 130 kanoničnih entitet (pogodbe, institucije, pravice, postopki, primeri) s filtri in dostopnim seznamom
- **Viri**: povezave na OHCHR (splošni komentarji), UHRI/UPR, HUDOC, UN Treaty Collection + preneseni ključni dokumenti (GA Res 60/251, A/RES/76/300)
- **PWA**: namestitvena (desktop + iOS + Android), deluje brez povezave, temni način, brez računov/sledenja

## Metoda (raziskava učenja)

Retrieval practice + razpršeno ponavljanje (Dunlosky 2013; meta-analiza 2021: d≈0,56), interleaving, takojšnja povratna informacija z virom, metakognicija (ocena zaupanja, rdeča/rumena/zelena obvladanost).

## Ravni avtoritete

| Nivo | Vir |
|---|---|
| A | primarni dokumenti (pogodbe, resolucije) — preverjeno v besedilih |
| B | profesorica (izvedbeni načrt, kolokvijski zapiski, banka vprašanj) |
| C | znanstveni članki |
| D | sinteza zapiskov |
| E | spomin študentov (⚠️ preveri pred izpitom) |

## Vsebina

Vsebina se generira z `tools/build-content.py` iz korpusa (pot nastavi v skripti). Profesorici gradiva in študentska dela niso razpečavana — prikazane so le derivirane povzetke z navedbo virov. Knjiga *Dokumenti človekovih pravic* je indeksirana (kazipot), ne reproducirana.

## Struktura

```
src/data/       generirani JSON (entities, topics, flashcards, quiz, comparisons, sources, greenbook, exams, glossary)
public/docs/    preneseni uradni PDF-ji (on-demand cache)
tools/          build-content.py, fetch-public-docs.py
src/pages/      Home, ExamDashboard, Guide, GreenBook, Simulator, Learn, Practice, Flashcards, Quiz, Graph, Sources, Progress, About
```

## Varnostna kopija

Napredek je v IndexedDB. **iOS Safari lahko izbriše lokalne podatke po neaktivnosti** — redno izvozi (Napredek → Izvozi).
