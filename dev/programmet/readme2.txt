Det fanns ett par saker med HS CC som inte är helt självklara.
Servern

För att köra serven behövs förutom jar-filen mappen ServerResources. Har man den ska det bara vara att starta servern med kommandot:
java -jar HurryScurryServer.jar StarWars <SpelNamn> 4711
<SpelNamn> är namnet på spelomgången. Data om alla spelomgångar sparas, dvs skulle servern krascha under pågående spel är det bara att starta om den med samma spelnamn.

Observera att detta gör att tiden för första uppdraget startas när servern startas, alltså bör inte servern startas förän nØllan lämnar uppdragsutdelningen (ev. så borde HS CC kodas om så att man kan starta tiden efter att servern har startas). Man kan dock köra ett spel med ett annat spelnamn än det man tänkt använda när spelet väl är igång.

Data för alla spel sparas i ServerResources/Game mappen.

I ServerResources finns en fil, GameData/StarWars/teamstemplate.xml. I den filen specificeras vilket lag som börjar med vilket uppdrag. Se till att synca detta med uppdragsanvarig!! Detta år misslyckades vi med det, vilket orskade en del kaos.
Klienterna

För att köra klienterna behövs bara respektive jar-fil, klienterna laddar ner resources från servern.

För att få igång klienterna:
Den vanliga klienten:
java -Xmx512M -jar HurryScurryClient.jar <IP> 4711 -p FuzzyKitten -f
(ev -f för fullscreen)

Rebellbas-specialklienten:
java -Xmx512M -jar HurryScurryRebelBaseClient.jar <IP> 4711 FuzzyKitten

Den vanliga klienten används till allt förutom att ändra uppdragsstatus
för lagen i rebellbasen.

När klienten väl är igång kan man göra följande:
Visa hjälptext: F1
Chatta: F2
Sortera lagen efter resultat: F6
Sortera lagen efter namn: F5

För att komma till översikten klickar man längst upp i fönstret / på
utropstecknet uppe till höger (typ). Man kan även visa ett lags progress
genom att klicka på laget.

De som behöver göra det kan högerklicka på uppdrag och klicka i
checkpoints (vet inte om det är något vi använder dock).

I rebellbasklienten kan man markera ett pågående uppdrag som avslutat
genom att vänsterklicka på det. För att sedan starta ett nytt
vänsterklickar man på det igen (när man är i lag-vyn). Man kan även
högerklicka på ett uppdrag och få upp en meny där man kan välja att
avbryta eller ändra tid för uppdraget.