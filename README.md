# NumeriOnesti

Sito statico con statistiche pubbliche sulle estrazioni del Lotto italiano (ritardi,
frequenze) e un'analisi onesta, basata su dati reali (1939–oggi), di perché nessun
sistema di gioco ha un ritorno atteso positivo.

## Struttura

- `data/storico.txt` — archivio ufficiale delle estrazioni (aggiornato automaticamente)
- `scripts/generate.py` — genera la homepage (ritardi/frequenze) dai dati
- `scripts/generate_static_pages.py` — genera le pagine di analisi/metodologia/legali
- `docs/` — output statico servito da GitHub Pages
- `.github/workflows/update.yml` — aggiornamento automatico settimanale (scarica i
  nuovi dati e rigenera il sito)

## Sviluppo locale

```bash
pip install numpy
python3 scripts/generate.py
python3 scripts/generate_static_pages.py
```

Apri `docs/index.html` nel browser.

## Attivare GitHub Pages (una tantum)

Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, cartella `/docs`.

## Aggiungere un dominio personalizzato

Settings → Pages → Custom domain → inserisci il dominio e configura i DNS come
indicato da GitHub (record CNAME verso `<utente>.github.io`).
