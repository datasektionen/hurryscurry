# Jabbascript
Detta program används för att generera formaterade _PDF-dokument_ utifrån innehållet som är specificerat i mappen `/src/rpu/data/`. Bortsett från att generara PDFer utifrån templates har den även möjlighet att utföra lite validering av textinnehållet, så att t.ex. inga datafält saknas eller så att inga felaktiga referenser görs.

## KTHs datorer
Programmet genererar dokumenten utifrån en mall m.h.a programmen `latexmk` och `xelatex`. Båda dessa ska ingå som standard på skolans Linux-datorer och jag rekommenderar starkt att ni använder någon av dessa om ni ska **generera PDF-dokument**. Även om ni tror att ni har all mjukvara installerad kan konstiga fel uppstå om **tex** inte är korrekt konfigurerat.

# Hur gör man?
Jabbascript skrivet i _python3_ och måste därför köras på en dator som har detta installerat, t.ex. skolans datorer om du inte har det på din egen. Alla paths som används av skriptet är relativa till denna mapp, så exekvera programmet härifrån (`dev/plan-a`).

Innan ni kan köra programmet måste ni installera ett par python3-paket. Detta göra genom att köra:
```
pip3 install -r requirements.txt
```

För en lista av möjliga command-line options kan du även köra följande rad i terminalen:
```
python3 jabbascript.py --help
```

## Generera PDF
Innan ni genererar filerna är det bäst att dubbelkolla så att textermaterialet inte är felformaterat. För att göra detta kan ni först köra valideringsskritpen som beskrivs i stycket nedan.

* `python3 jabbascript.py --generate-missions` genererar alla uppdrags-dokument.
* `python3 jabbascript.py --generate-events` genererar alla händelse-dokument.
* `python3 jabbascript.py --generate-drifters` genererar alla drifvar-uppdrag.
* `python3 jabbascript.py --generate-characters` ~~genererar alla karaktärsbeskrivningar~~.
* `python3 jabbascript.py --generate-all` kör samtliga kommandon ovan i serie

**Kommentar:** såvitt jag vet har `--generate-characters` inte implementerats helt ännu. Det fanns inte tillräckligt med tid för att färdigställa den delen sommaren 2017 men är fullt möjligt och bör inte ta fruktansvärd tid om man på ett ungefär förstår hur programmet hänger ihop. RPU 2017 verkade dock kunna lösa det oavsett så ni kan också fråga dem hur de bar sig åt. Ifall mottangningen 2018 skulle vilja ha hjälp att implementera den sista biten kan ni skriva till [albinre@kth.se](mailto:albinre@kth.se), så ska jag försöka hjälpa er i mån av tid!

## Validering av textmaterial
Programmet erbjuder som sagt lite validering som kan vara till nytta för _Roller, Platser och Uppdrag_ om de har ändrat i någon av filerna. Det finns tre sätt att validera filerna:

* `python3 jabbascript.py --parse-json` kollar så att JSON-strukturen är rätt, t.ex. så att det är en balanserad mängd citationstecken m.m.
* `python3 jabbascript.py --validate-json` kollar så att alla nödvändiga datafält är närvarande.
* `python3 jabbascript.py --sanity-check` kollar så att alla referenser faktiskt existerar och skriker om ett angivet ID inte stämmer.

# Undermappar
## `logs`
I denna mapp hamnar alla felrapporter som skapas ifall skriptet skulle stöta på problem. När programmet körs ska en del bra information skrivas ut direkt i terminalen, men den bör även hänvisa till en logfil här som innehåller mer detaljerad information.

## `tex`
I denna mapp lagras all data som behövs för att generera PDF ifrån Hurry Scurryns _tex-templates_. I mappen `fonts` lagras alla typsnitt som behövs för att få till den häftiga star-wars texten. Mappen `templates` lagrar template-filerna där textmaterialet injiceras. Du bör varken flytta eller ta bort någonting ur den här mappen om du inte redan ändrat vilka filer som programmet använder sig av.

### templates
Template-systemet är mycket enkelt och i själva verket är det bara en särskild _tag_ som byts ut mot text kopierad från t.ex. en uppdragsfil. Till exempel så kommer uppdragets titel då ersätta alla förekomster av taggen `{{title}}`. PDFernas grafiska utseende specificeras av filen `scurry.cls` vilket är en _tex-klass-fil_. Grafisk formattering med `tex` kan vara ganska knepigt och innebär mycket trial-and-error för de flesta, så jag skulle inte rekommendera att ändra något där om ni kan undvika det.

# Vem ska jag skylla på?
Om ni råkar ut för problem som ni inte kan lösa är ni välkomna att kontakta [Albin Remnestål <albinre@kth.se>](mailto:albinre@kth.se) när ni vill.
