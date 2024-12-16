doc = projekt I
src = projekt II

---

test_dmcz - test_kosik.py
1. otevře se stránka https://www.dm.cz/
2. odmítne cookies
3. najde sekci Nechte se okouzlit
4. klikne na položku 9. v pořadí (aktuálně Zvířata)
5. otevře se nová stránka se sekcí Zvířata
6. první a třetí položku z nabídky vloží do košíku
7. přejde do košíku a ověří, že jsou v něm dvě položky

test_oreacz - test_terminy.py
1. otevře se stránka https://www.orea.cz/resort-horal
2. potvrdí cookies
3. zobrazí výběr termínů
4. v kalendáři vybereme první a třetí dostupný den (tedy třídenní pobyt)
5. ověříme, že termín byl vybraný

test_vouchery_kreativniceskocz - test_detail.py
1. otevře se stránka https://vouchery.kreativnicesko.cz/
2. nejdříve klineme na tlačítko Jak se registrovat
3. následně proklikneme tlačítko Vyberte si, a tím se dostaneme na Celostátní galerii kreativců
4. na této stránce přes vyhledávací pole vyhledáme jméno Lenka
5. z vyhledaných vybereme druhou v pořadí
6. ověříme, že je profil načten

