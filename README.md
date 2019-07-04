
<h1 align="center">
    <b>
        Hurry Scurry
    </b>
</h1>

<p align="center">
    <img src="https://media.giphy.com/media/3ornk57KwDXf81rjWM/giphy.gif" width="100%" />
</p>

# Repostruktur

## `/dev` mappen
Denna mapp innehåller all mjukvara som kan vara till användning för att förbereda och köra Hurry Scurry.

### `plan-a`
Innehåller det senaste programmet för att autogenerera alla trycksaker utifrån textmaterialet. Därav är det främst detta program som _Trycksaker_ kommer behöva använda sig av. Även _Roller, Platser och Uppdrag_ kan vara intresserad av några features. Se `README.md` i denna mapp för lite mer detaljerade instruktioner.

### `plan-b`
Innan _plan-a_ scriptet skrevs under sommaren 2017 gjordes året innan en föregångare som numera kallas _plan-b_. Detta program är inte lika sofistikerat och producerar _Word-dokument_ på det formatet som pre-2016 skrevs och underhölls manuellt. Tanken är egentligen att `plan-b` aldrig ska behöva användas igen, men behålls i repot utifall att behovet skulle uppstå.

### `programmet`
**"programmet"** är namnet på _server/klient_ programmet som används för att räkna nØllans poäng samt för att visualisera den vackra poängtavlan i Mos Eisley. Det här programmet är gammalt (ca 2007) och fungerar inte alltid som man vill; men instruktionerna är rätt så tydliga! Detta program + server ska köras av _Titel_ i rebellbasen och som en klient av _Trycksaker_ när de står i _Mos Eisley_.

### `r2d2`
Detta java-program körs på någon laptop för att agera som R2D2. Detta program är i själva verket inte särskilt avancerat utan är mer eller mindre endast en hashmap som mappar exakta frågor mot svar. På grund av detta kan det vara bra om _R2D2-vakten_ får en utskriven kopia av **de relevanta frågorna + svaren** och inte hela databasen, som av någon anledning består av en väldigt stor mängd outnyttjad information.

## `/src` mappen
Denna mapp innehåller _"alla"_ resurser för Hurry Scurryn.

### `rpu`
Denna mapp har två delmappar:
* `data` som innehåller all textmaterial för _uppdrag + ledtrådar_, _händelser_, _drifvaruppdrag_ och _karaktärer_.
* `schemas` specificerar de JSON-schemas som används för validering av de olika filformat som används i mappen `data`. Om ni t.ex. vill lägga till ett ytterliggare fält i uppdragsfilerna gäller det att ni också uppdaterar `schema.missions.json`. Annars behöver ni nog inte fiffla med dessa.

### `tryck`
Denna mapp innehåller faktiskt ingenting utöver en `.gitignore`-fil om ni precis klonat repot, utan är snarare en placeholder. När ni genererat PDF-dokument m.h.a `jabbascript.py` programmet i mappen `dev/plan-a` kommer dessa dyka upp här! `.gitignore`-filen finns därför på plats för att PDF-dokumenten själva inte ska versionshanteras.

### `rekvisita`
Här är tanken att _rekvisita_ ska kunna versionshantera sitt material. Såvitt jag vet har dock _rekvisita_ kvar majoriteten av sitt material på **Google Drive** istället.

# Git

Är fett najs och *100% bättre* än Google drive på att versionshantera filer som:
* Är annat än google-docs-dokument (dit ska vi inte tillbaka)
* Inte bör versionshanteras i realtid pga snabb uppdatering (autogenerering)
* Vars innehåll måste kunna rullas tillbaka till ett acceptabelt tillstånd
* Vars ändringar måste kunna dokumenteras enhetligt


## Disclaimer
Detta repo inehåller texter på både svenska och engelska för jag tänkte inte innan jag skrev de tidiga README-filerna :facepalm:
**Men** försök hålla er till engelska när det kommer till exempelvis *keys* i *JSON*-filerna eftersom ÅÄÖ alltid brukar jävlas med en i slutändan.

**(OBS)** Framförallt LaTeX hatar svenska alfabetet med ursinne
