"""
Generatore statico del sito NumeriOnesti.
Legge data/storico.txt (archivio ufficiale delle estrazioni del Lotto) e produce
tutte le pagine HTML in docs/. Nessuna dipendenza da server: sito 100% statico,
pensato per GitHub Pages. Rilanciato automaticamente ogni settimana dalla
GitHub Action (.github/workflows/update.yml).
"""
import os
import numpy as np
from collections import defaultdict, Counter
from itertools import combinations
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "storico.txt")
OUT_DIR = os.path.join(ROOT, "docs")

CODE2NAME = {"BA":"Bari","CA":"Cagliari","FI":"Firenze","GE":"Genova","MI":"Milano",
             "NA":"Napoli","PA":"Palermo","RM":"Roma","RN":"Nazionale","TO":"Torino","VE":"Venezia"}
ORDER = ["BA","CA","FI","GE","MI","NA","PA","RM","TO","VE","RN"]

MULT_AMBO = 250.0
LOOKBACK_FREQ = 500  # finestra "recente" per le frequenze, puramente descrittiva

# ---------------------------------------------------------------- parsing --
def parse():
    raw = defaultdict(list)
    with open(DATA_PATH, encoding="latin-1") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 7:
                continue
            data, ruota = parts[0], parts[1]
            try:
                nums = [int(x) for x in parts[2:7]]
            except ValueError:
                continue
            if len(nums) != 5 or any(n < 1 or n > 90 for n in nums):
                continue
            raw[ruota].append((data, nums))
    series = {}
    for code, rows in raw.items():
        rows.sort(key=lambda r: r[0])
        series[code] = {
            "dates": [r[0] for r in rows],
            "draws": np.array([r[1] for r in rows], dtype=np.int16),
            "n": len(rows),
        }
    return series

def ritardi_attuali(draws, n):
    ultimo_visto = np.full(91, -1, dtype=np.int64)
    for d in range(n):
        for num in draws[d]:
            ultimo_visto[int(num)] = d
    ritardo = np.where(ultimo_visto == -1, n, n - 1 - ultimo_visto)
    return ritardo  # index 1..90

def frequenze_recenti(draws, n, lookback):
    w0 = max(0, n - lookback)
    counts = np.zeros(91, dtype=np.int64)
    for row in draws[w0:n]:
        counts[row] += 1
    return counts, n - w0

# ------------------------------------------------------------------ HTML --
CSS = """
:root{
  color-scheme: light;
  --page:#f9f9f7; --surface:#fcfcfb; --card:#ffffff; --ink:#0b0b0b; --ink-2:#52514e;
  --muted:#898781; --grid:#e1e0d9; --baseline:#c3c2b7; --border:rgba(11,11,11,.10);
  --blue:#2a78d6; --red:#e34948; --green:#0ca30c;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme: dark;
    --page:#0d0d0d; --surface:#1a1a19; --card:#232322; --ink:#fff; --ink-2:#c3c2b7;
    --muted:#898781; --grid:#2c2c2a; --baseline:#383835; --border:rgba(255,255,255,.10);
    --blue:#3987e5; --red:#e66767; --green:#0ca30c;
  }
}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.6}
.wrap{max-width:920px;margin:0 auto;padding:0 20px 60px}
nav{border-bottom:1px solid var(--grid);margin-bottom:8px}
.navin{max-width:920px;margin:0 auto;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}
.brand{font-weight:700;font-size:1.15rem;color:var(--ink);text-decoration:none}
.brand span{color:var(--blue)}
.navlinks{display:flex;gap:18px;flex-wrap:wrap}
.navlinks a{color:var(--ink-2);text-decoration:none;font-size:.92rem}
.navlinks a:hover{color:var(--blue)}
h1{font-size:1.7rem;margin:28px 0 8px;letter-spacing:-0.01em}
h2{font-size:1.25rem;margin:36px 0 6px}
h3{font-size:1.05rem;margin:22px 0 6px}
.sub{color:var(--ink-2);margin:0 0 24px}
a{color:var(--blue)}
.note{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 16px;font-size:.9rem;color:var(--ink-2);margin:16px 0}
.note b{color:var(--ink)}
.grid-ruote{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:18px 0}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 18px}
.card h3{margin:0 0 10px;font-size:1.05rem}
.card .meta{font-size:.78rem;color:var(--muted);margin-bottom:10px}
.numlist{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 10px}
.num{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:50%;background:var(--surface);border:1px solid var(--border);font-size:.85rem;font-weight:600}
.numlist.freq .num{background:rgba(42,120,214,.10);border-color:rgba(42,120,214,.25)}
table{width:100%;border-collapse:collapse;font-size:.9rem;margin:12px 0}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--grid)}
th{color:var(--muted);font-weight:600;font-size:.76rem;text-transform:uppercase;letter-spacing:.02em}
td.tnum,th.tnum{text-align:right;font-variant-numeric:tabular-nums}
.conclusion{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--blue);border-radius:10px;padding:16px 20px;margin:16px 0}
footer{margin-top:50px;padding-top:16px;border-top:1px solid var(--grid);font-size:.78rem;color:var(--muted)}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 16px 8px;margin:14px 0}
.legend{display:flex;gap:16px;font-size:.8rem;color:var(--ink-2);margin-bottom:4px;flex-wrap:wrap}
.legend span{display:inline-flex;align-items:center;gap:6px}
.swatch{width:10px;height:10px;border-radius:2px;display:inline-block}
"""

NAV = """
<nav><div class="navin">
  <a class="brand" href="index.html">Numeri<span>Onesti</span></a>
  <div class="navlinks">
    <a href="index.html">Ritardi e frequenze</a>
    <a href="perche-non-funzionano.html">Perché i sistemi non funzionano</a>
    <a href="metodologia.html">Metodologia</a>
    <a href="gioco-responsabile.html">Gioco responsabile</a>
  </div>
</div></nav>
"""

def page(title, description, body, canonical=""):
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<style>{CSS}</style>
</head>
<body>
{NAV}
<div class="wrap">
{body}
<footer>
  NumeriOnesti — statistiche pubbliche sul Lotto, aggiornate automaticamente ogni settimana dall'archivio ufficiale.
  Nessun sistema qui presentato garantisce vincite: leggi <a href="perche-non-funzionano.html">perché</a>.
  · <a href="privacy.html">Privacy</a> · <a href="cookie.html">Cookie</a> · <a href="gioco-responsabile.html">Gioco responsabile</a>
</footer>
</div>
</body>
</html>"""

def write(name, html):
    with open(os.path.join(OUT_DIR, name), "w", encoding="utf-8") as f:
        f.write(html)

# ------------------------------------------------------------------ build --
def build():
    series = parse()
    os.makedirs(OUT_DIR, exist_ok=True)

    cards = []
    for code in ORDER:
        if code not in series:
            continue
        s = series[code]
        n = s["n"]
        rit = ritardi_attuali(s["draws"], n)
        freq_counts, freq_n = frequenze_recenti(s["draws"], n, LOOKBACK_FREQ)

        top_ritardatari = sorted(range(1, 91), key=lambda x: -rit[x])[:8]
        top_frequenti = sorted(range(1, 91), key=lambda x: -freq_counts[x])[:8]

        rit_html = "".join(f'<span class="num" title="{r} colpi di ritardo">{r}</span>' for r in top_ritardatari)
        freq_html = "".join(f'<span class="num" title="{freq_counts[r]} uscite">{r}</span>' for r in top_frequenti)

        cards.append(f"""
<div class="card">
  <h3>{CODE2NAME[code]}</h3>
  <div class="meta">{n:,} estrazioni · ultima: {s['dates'][-1]}</div>
  <div style="font-size:.82rem;color:var(--ink-2);margin-bottom:4px">Numeri più ritardatari</div>
  <div class="numlist">{rit_html}</div>
  <div style="font-size:.82rem;color:var(--ink-2);margin-bottom:4px">Più usciti nelle ultime {freq_n} estrazioni</div>
  <div class="numlist freq">{freq_html}</div>
</div>""".replace(",", "."))

    updated = datetime.utcnow().strftime("%d/%m/%Y")
    body = f"""
<h1>Ritardi e frequenze reali del Lotto</h1>
<p class="sub">Dati aggiornati automaticamente dall'archivio ufficiale ogni settimana. Ultimo aggiornamento: {updated}.</p>

<div class="note">
  <b>Prima di guardare i numeri:</b> ritardi e frequenze qui sotto sono fatti storici, non previsioni.
  Ogni estrazione è indipendente dalle precedenti: un numero "ritardatario" non ha più probabilità di uscire
  della media. Te lo spieghiamo con i dati, non a parole, nella pagina
  <a href="perche-non-funzionano.html">perché i sistemi non funzionano</a>.
</div>

<div class="grid-ruote">
{"".join(cards)}
</div>

<h2>Perché pubblichiamo questi numeri, se non servono a prevedere nulla?</h2>
<p>Perché sono un fatto di cronaca, non un consiglio di gioco: sapere che un numero non esce da 400 colpi è
un'informazione vera. Il problema è cosa se ne deduce. Su questo abbiamo fatto un'analisi seria, con dati
reali dal 1939 a oggi — <a href="perche-non-funzionano.html">la trovi qui</a>.</p>
"""
    write("index.html", page(
        "NumeriOnesti — Ritardi e frequenze reali del Lotto",
        "Ritardi e frequenze aggiornati del Lotto italiano, con analisi statistica onesta su perché nessun sistema garantisce vincite.",
        body))

    print("Homepage generata con", len(cards), "ruote.")
    return series

if __name__ == "__main__":
    build()
