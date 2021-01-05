<h3>Beskrivelse</h3>
<p>Bruk Raspberry Pi sammen med en strekkode-leser som du kobler til med USB-kabel.</p>
<p>Skann varen sin strekkode og strekkoden på hyllen for å oppdatere vareplassering i databasen.</p>

<h3>Hvordan bruke denne</h3>
<p>Kjør filen main.py for å starte applikasjonen. Bruke flaggene beskrevet i main.py for tilleggsfunksjoner</p>
<p>For å bygge en database i json fra alle skanninger, koble usb fra raspberry pi og inn i en pc med python installert</p>
<p>Gå inn på minnebrikken og kjør: "./main.py build" for å bygge databasen</p>

<h3>Oppsett for Raspberry Pi</h3>
<p>Raspberry pi må konfigureres med auto login, autostart av applikasjon, sql konfigurering sammen med odbc data kilden</p>
<p>Det er flere "dependencies" som må innstalleres sammen med FreeTDS driveren og modulen pyodbc for at python skal kunne kommunisere med MSSQL server</p>
<p>Les pi_setup.txt og gå igjennom steg for steg med oppsett av Raspberry Pi</p>
<p>Jeg har skrevet denne på engelsk for for å gjøre det enklere for andre å kopiere</p>

<h3>Velg modus</h3>
<p>Du kan endre modus ved å kjøre "./main.py sql" for å aktivere eller deaktivere sql</p>
<p>Alternativt så kan du endre verdiene i debug.json (true/false)</p>
<p>Hvis raspberry pi er koblet på batteri</p>
<p>"sql": true,"shutdown": true,"passwordhide": true,"led": true,""showcred": true,"live": false</p>
<p>Hvis raspberry pi er koblet på strøm med kbalet nett</p>
<p>"sql": true,"shutdown": true,"passwordhide": true,"led": false,""showcred": true,"live": true</p>
