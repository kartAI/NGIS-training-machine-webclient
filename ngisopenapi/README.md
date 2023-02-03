
1. create a virtual env (```python3 -m venv venv```)
2. activate: (```source venv/bin/activate```)
3. install deps (```pip -r requirements.txt```)
4. create .env based on .env_template, add values
5. run: ```python demo.py```

Guide til oppsett:

1. Åpne Visual Studio Code med et blankt vindu
2. Last ned plugin github pull requests and issues
3. Gå inn på source control i VS code sin toolbar og klikk clone repository.
4. Lim inn denne linken: https://github.com/Norkart/gis-introkurs-2023.git i tekst feltet som kommer opp
5. Velg et sted å lagre mappen slik at du finner den igjen.
6. Velg branch geojson2 nede i venstre hjørne hvor det står main fra før av
7. Åpne git bash og naviger til git-introkurs-2023/ngisopenapi mappen (evt finne mappen i filutforsker, også høyreklikk, deretter trykk “Gitbash here”)
8. Kjør: python3 -m venv venv (ikke tenk på dette steget om du allerede har en venv fil)
9. Kjør: source venv/Scripts/activate
10. Kjør: pip install -r requirements.txt (ikke tenk på dette steget om du har forket repoet)
11. Gå tilbake til vs code og lag en fil som heter .env i samme mappe som du finner demo.py (ngisopenapi)
12. Lim inn dette i .env filen du har laget: 
    NGISAPI_URL=
    NGISAPI_USER=
    NGISAPI_PASS=
13. Skriv inn URL for databasen og innlogging i sine respektive plasser (Husk å lagre etter du har limt inn teksten over).
14. Gå inn i filen "demo.py"
15. Endre file_path til ønsket plassering av geojson filen som blir opprettet.
16. Kjør kode i git-bash/terminal: pip install psycopg2
17. Gå i transfer.py
18. Legg til filepath i koden som åpner geoJSON filen og i koden som sletter geoJSON filen.
18. Gå tilbake til git bash og kjør koden: python demo.py
19. Voila
