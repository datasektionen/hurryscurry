# HS - Programmet
I denna mapp finns allt som behövs för att köra programmet som håller koll på hur det går för alla nØllegrupper i Hurry Scurryn. Vissa kan referera till detta program som "HS CC".

## Servern

För att köra serven behövs, förutom jar-filen `HurryScurryServer.jar`, mappen ServerResources.

### Starta servern
Servern startas genom att skriva kommandot:
```
java -jar HurryScurryServer.jar StarWars <SpelNamn> 4711
```

`<SpelNamn>` är namnet på spelomgången. Data om alla spelomgångar sparas, dvs skulle servern krascha under pågående spel är det bara att starta om den med samma spelnamn. All data samlas i mappen `ServerResources/Game/<SpelNamn>`.

Observera att detta gör att tiden för första uppdraget startas när servern startas, alltså bör inte servern startas förrän nØllan lämnar uppdragsutdelningen. Vill man testa programmet bör man därför testköra ett spel med ett annat spelnamn än det man tänkt använda när spelet väl är igång.

### Uppdatera information
I mappen `ServerResources/GameData/StarWars` finns alla filer för allt det grafiska i programmet och för data om grupperna och uppdragen.

#### nØllegrupper
`teamstemplate.xml` - Här är det specificerat vilka namn och startuppdrag varje nØllegrupp har. Varje år kommer man behöva gå in i denna fil och uppdatera gruppernas namn.
> OBS! Se till att grupperna får samma uppdrag i sitt startkit som de faktiskt får via programmet, annars kan det bli knas'

#### Uppdragen
`rulestemplate.xml` - Här är alla uppdrag specificerade. Kan vara bra att uppdatera beskrivningarna så att de stämmer överens med JSON-filerna.

## Klienterna

Det finns två olika klienter; en som körs i Mos Eisley och en som körs i rebellbasen. För att köra klienterna behövs bara respektive jar-fil, klienterna laddar ner resources från servern.

### Uppstart
För att starta en klient, använd något av detta kommandon:

```make
Vanlig klient:
java -Xmx512M -jar HSClient.jar <IP> 4711 -p FuzzyKitten

Rebellbas-specialklient:
java -Xmx512M -jar HSRebelBaseClient.jar <IP> 4711 FuzzyKitten
```
skriv `-f` i slutet för att köra med fullscreen.

Innan programmet startas kommer en inloggningsruta. Det bör inte spela någon roll vad du väljer för karaktär och användarnamn.

### Navigation
I programmet kan man göra följande:
- `F1` - Visa hjälptext
- `F2` - Öppna chattfönstret
- `F5` - Sortera lag efter namn
- `F6` - Sortera lag efter resultat
- Kom tillbaka till översikten genom att klicka någonstans i vänstra övre hörnet (till höger om listan med nØllegrupperna)
- Visa ett lags progress genom att klicka på laget i listan
- Visa information om ett uppdrag genom att högerklicka på det
- De som behöver göra det kan högerklicka på uppdrag och klicka i
checkpoints (vet inte om det är något vi använder dock).

I rebellbasen kan man markera ett pågående uppdrag som avslutat
genom att vänsterklicka på det. För att sedan starta ett nytt
vänsterklickar man på det igen (när man är i lag-vyn). Man kan även högerklicka på ett uppdrag och få upp en meny där man kan välja att avbryta eller ändra tid för uppdraget.
