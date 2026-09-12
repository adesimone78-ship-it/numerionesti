"""Pagine di contenuto statico (non dipendono dai dati aggiornati): analisi,
metodologia, privacy, cookie, gioco responsabile. Importano page()/write() da
generate.py per restare coerenti con lo stile del sito."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import page, write

# ---------------------------------------------------------- analisi -------
ANALISI_BODY = """
<h1>Perché i sistemi per il Lotto non funzionano</h1>
<p class="sub">Non è un'opinione: è quello che succede quando testi qualunque metodo — inclusi quelli che sembrano funzionare nello storico — sui numeri reali.</p>

<h2>1. Il costo reale del biglietto</h2>
<p>Calcolo combinatorio esatto, indipendente da qualunque dato storico — discende solo dalle regole del gioco:</p>
<table>
<thead><tr><th>Giocata</th><th class="tnum">Probabilità</th><th class="tnum">Moltiplicatore</th><th class="tnum">Ritorno atteso</th></tr></thead>
<tbody>
<tr><td>Ambata (1 numero)</td><td class="tnum">1 su 18</td><td class="tnum">11,23x</td><td class="tnum">62,4%</td></tr>
<tr><td>Ambo (2 numeri)</td><td class="tnum">1 su 401</td><td class="tnum">250x</td><td class="tnum">62,4%</td></tr>
<tr><td>Terno (3 numeri)</td><td class="tnum">1 su 11.748</td><td class="tnum">4.500x</td><td class="tnum" style="color:var(--red)">38,3%</td></tr>
<tr><td>Quaterna (4 numeri)</td><td class="tnum">1 su 511.038</td><td class="tnum">120.000x</td><td class="tnum" style="color:var(--red)">23,5%</td></tr>
<tr><td>Cinquina (5 numeri)</td><td class="tnum">1 su 43.949.268</td><td class="tnum">6.000.000x</td><td class="tnum" style="color:var(--red)">13,7%</td></tr>
</tbody>
</table>
<p style="font-size:.88rem;color:var(--ink-2)">Più la giocata è "ricca", peggiore il ritorno atteso: il contrario di quello che si pensa istintivamente.</p>

<h2>2. Il metodo più diffuso, testato sui numeri veri</h2>
<p>L'idea più comune: trovare l'ambo che ha "funzionato meglio" nello storico e rigiocarlo. Su 87 anni di
estrazioni ufficiali (1939–oggi), divisi in periodi consecutivi, abbiamo scelto ogni volta l'ambo più
frequente in un periodo e verificato — con i dati reali — cosa succede quando lo si rigioca nel periodo
storico immediatamente successivo, mai visto durante la scelta.</p>

<div class="note">
<b>Risultato su 55 test reali (tutte le 11 ruote, 1939–2026):</b> il 100% degli ambi selezionati era, per
costruzione, in profitto nel periodo usato per sceglierli (+135% medio). Rigiocati nel periodo successivo:
solo il <b>14,5%</b> è rimasto in attivo. Il resto ha reso in media <b>-38%</b>, identico a un ambo scelto
a caso. La correlazione tra quanto un ambo sembrava buono e quanto ha reso dopo è <b>negativa</b>: più
sembrava vincente, peggio ha fatto.
</div>

<h3>Un esempio concreto, non inventato</h3>
<p>Ambo <b>10-19</b> su ruota Nazionale: scelto perché il più frequente tra il 20/10/2012 e il 5/07/2016
(+244% in quel periodo) → rigiocato dal 7/07/2016 al 21/03/2020: <b style="color:var(--red)">-14%</b>.<br>
Ambo <b>11-59</b>, stesso meccanismo, periodo successivo: <b style="color:var(--red)">-100%</b> — zero
centri in oltre 3 anni di estrazioni reali.</p>

<h2>3. E lo stop-loss? ("mi fermo dopo N tentativi a vuoto")</h2>
<p>Anche questa idea è stata testata sui dati reali: fermarsi dopo N tentativi consecutivi senza vincita e
sceglierne uno nuovo riduce il rischio di restare bloccati in una serie catastrofica (il ROI medio migliora
da -45% a circa -36%). Ma è un vantaggio di <b>gestione del rischio</b>, non di previsione: scegliendo l'ambo
successivo <b>a caso</b> invece che per frequenza, con la stessa regola di stop, il risultato è statisticamente
identico. Il vantaggio non viene dall'aver trovato un ambo "caldo" — viene solo dal non restare incollati a
una singola giocata sfortunata per sempre.</p>

<h2>4. La scansione completa: 4.005 combinazioni, un solo verdetto</h2>
<p>Abbiamo calcolato il risultato per <b>tutte</b> le 4.005 combinazioni di ambo possibili sulla ruota
Nazionale. Il 76% risultava "in attivo" in un dato momento — non perché speciali, ma perché con l'8-9% circa
di probabilità di uscire almeno una volta ogni 500-600 colpi per puro caso, la maggioranza qualsiasi coppia
lo soddisfa. Tra le coppie che avevano superato il +200% in un periodo storico (23 casi reali osservati), solo
il 13% è rimasto profittevole in quello successivo.</p>

<h2>Conclusione</h2>
<div class="conclusion">
<p><b>Sia la matematica sia il test empirico sui dati reali dicono la stessa cosa:</b> nessuno schema — ritardatari,
ambi ricorrenti, sistemi a ruota, stop-loss — mantiene un vantaggio fuori dal periodo in cui è stato scelto.
Le serie che sembrano "vincenti" nello storico sono statistica normale su migliaia di combinazioni testate,
non segnali. Se giochi, gioca solo ambate/ambi (il minor danno atteso), frazionati su più uscite, e considera
la spesa persa in partenza: è il prezzo dell'intrattenimento, non un investimento.</p>
</div>
"""

# ------------------------------------------------------------ metodologia -
METODOLOGIA_BODY = """
<h1>Metodologia e trasparenza</h1>
<p class="sub">Come sono calcolati i numeri di questo sito, e da dove vengono i dati.</p>

<h2>Fonte dei dati</h2>
<p>Estrazioni ufficiali del Lotto, dal 1939/01/07 a oggi, scaricate dall'archivio storico ufficiale del
concessionario. Il sito si aggiorna automaticamente ogni settimana.</p>

<h2>Cosa mostriamo in homepage</h2>
<p><b>Ritardi:</b> numero di estrazioni consecutive in cui un numero non è uscito su una determinata ruota,
a oggi. <b>Frequenze recenti:</b> quante volte un numero è uscito nelle ultime 500 estrazioni di quella
ruota. Sono fatti storici verificabili, non proiezioni.</p>

<h2>Cosa NON facciamo</h2>
<p>Non vendiamo sistemi, non affermiamo che un numero abbia più probabilità di uscire di un altro, non
offriamo consulenza di gioco, non abbiamo link di affiliazione a siti di scommesse. Ogni estrazione del
Lotto è un evento indipendente e casuale — lo mostriamo con i dati nella pagina
<a href="perche-non-funzionano.html">perché i sistemi non funzionano</a>.</p>

<h2>Verifica di equità</h2>
<p>Su oltre 7.000 estrazioni per ruota, ogni numero esce con uno scostamento medio dalla frequenza attesa
del 3,5-5,5% — esattamente il rumore statistico previsto dal calcolo binomiale per questi volumi. Nessun
numero è strutturalmente favorito.</p>

<h2>Codice e dati aperti</h2>
<p>La pipeline che genera questo sito è pubblica. Se trovi un errore nei calcoli, segnalalo.</p>
"""

PRIVACY_BODY = """
<h1>Privacy</h1>
<p class="sub">Ultimo aggiornamento: generato automaticamente.</p>
<p>Questo sito è statico e non richiede registrazione. Se sono presenti spazi pubblicitari (Google AdSense),
Google può utilizzare cookie per mostrare annunci pertinenti; puoi gestire le preferenze pubblicitarie su
<a href="https://adssettings.google.com" target="_blank" rel="noopener">adssettings.google.com</a>. Non
raccogliamo dati personali diretti. Per richieste, contattaci tramite il repository del progetto.</p>
"""

COOKIE_BODY = """
<h1>Cookie</h1>
<p>Questo sito può utilizzare cookie tecnici necessari al funzionamento e, se attivi, cookie pubblicitari di
terze parti (Google AdSense) per la personalizzazione degli annunci. Puoi disattivare i cookie pubblicitari
dalle impostazioni del tuo browser o su <a href="https://adssettings.google.com" target="_blank" rel="noopener">adssettings.google.com</a>.</p>
"""

RESPONSABILE_BODY = """
<h1>Gioco responsabile</h1>
<p class="sub">Se il gioco smette di essere intrattenimento, è il momento di fermarsi.</p>
<div class="note">
<b>Segnali a cui prestare attenzione:</b> giocare somme che non ti puoi permettere di perdere, rincorrere le
perdite, mentire su quanto giochi, sentire ansia se non giochi. Se riconosci questi segnali in te o in
qualcuno vicino a te, parlarne con un professionista o chiamare un numero di aiuto dedicato è un passo
concreto, non una sconfitta.</div>
<p>Il gioco d'azzardo è vietato ai minori di 18 anni. Le informazioni su questo sito sono a scopo puramente
statistico/informativo: nessun contenuto qui presente costituisce incentivo al gioco né garanzia di vincita —
anzi, il contrario: <a href="perche-non-funzionano.html">leggi perché</a>.</p>
"""

def build():
    write("perche-non-funzionano.html", page(
        "Perché i sistemi per il Lotto non funzionano — NumeriOnesti",
        "Analisi statistica con dati reali dal 1939 al 2026: perché ritardatari, ambi ricorrenti e sistemi non hanno valore predittivo.",
        ANALISI_BODY))
    write("metodologia.html", page(
        "Metodologia — NumeriOnesti",
        "Come sono calcolati ritardi e frequenze, da dove vengono i dati, cosa mostriamo e cosa no.",
        METODOLOGIA_BODY))
    write("privacy.html", page("Privacy — NumeriOnesti", "Informativa privacy.", PRIVACY_BODY))
    write("cookie.html", page("Cookie — NumeriOnesti", "Informativa cookie.", COOKIE_BODY))
    write("gioco-responsabile.html", page(
        "Gioco responsabile — NumeriOnesti",
        "Informazioni sul gioco responsabile e segnali di attenzione.",
        RESPONSABILE_BODY))
    print("Pagine statiche generate.")

if __name__ == "__main__":
    build()
