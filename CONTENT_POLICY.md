# Content Policy

## Kaj je v aplikaciji

1. **Javni uradni dokumenti** (pogodbe, resolucije, splošni komentarji) — z navedbo vira in povezavo na uradno stran. Preneseni PDF-ji: GA Res 60/251, A/RES/76/300 (OHCHR/UN).
2. **Derivirane povzetke** profesoricih gradiv in študentskih del — struktura (tema → podlaga → nadzor → težave), ne besedilne kopije.
3. **Lastne sinteze** (master guide) z oznako ravni avtoritete (A–E).

## Kaj NI v aplikaciji

- Reprodukcija knjige *Dokumenti človekovih pravic z uvodnimi pojasnili* — samo kazipot (tema → členi).
- Besedilne kopije profesoricih docx/datotek ali študentskih seminarskih del.
- Vsebina z nejasnim avtorskim statusom.

## Označevanje

- Vsako vprašanje nosi `provenance` (izpitni rok / banka / generirano) in `officialStatus`.
- Vsaka kartica nosi raven avtoritete (A–E).
- ⚠️ = spomin študentov, preveri pred izpitom.

## Posodabljanje

1. Uredi `tools/build-content.py` (strukturirani podatki) ali korpus.
2. `npm run content` → regenerira `src/data/*.json`.
3. `npm run build` → nova verzija PWA (service worker obvesti uporabnike).
