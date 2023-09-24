OBIETTIVI DA IMPLEMENTARE:
    -V simulare e cambiare connessione remota con redis-server (per ora locale), prova con AWS redis server o virtual pc
    -V effettuare ack/risposta ai client ()
    -V getEntryData() costruisci data da ritornare correttamente (o vedi un parser su internetèìà)
    -V controlla postgre sql api restful (implementa REST sul db)
    - modifica schema architettura, aggiungi vari container redis + container api restful su db
    -V costruici db (tutorial)
    - aggiusta readstream() in server e cliente, deve leggere i messaggi nuovi non solo 1 (rendere non bloccante direi)
    - generatore crea eventi random: "arrivo" cliente, se aquistare oggetti (dopo snapshot del db), scelta oggetti stessi
    - generatore deve creare nuovi thread per ogni cliente (e poi lo chiude)?, altrimenti non ci sarebbero 2 o piu clienti che usano il sistema contemporaneamente (SOL: lancia funzioni di Cliente in GEneratore su altro tread)
    - modifica redis tra cliente e ServerCliente (ogni coppia cliente/server deve avere 2 code x input/output, così no collo di bottiglia e passo messaggi meglio)
    - Per DB:
        - Venditore per ogni oggetto, inserisce nuove entry (o aggiorna) in "ogginvendita" specificando la quantità, se è un oggetto nuovo per il db, il isstema crea nuove entry in "oggdaconsegn" e "oggconsegnati" con quantità 0
        - se Cliente compra, sottrae la quantita specificata degli oggetti in "ogginvendita" e aggiunge la quantità degli stessi oggetti nelle entry di "oggdaconsegn" 
        -
    - quando cliente esce, chiudi streams? vedere se è worth tenere info messaggi per monitor
    - modifica time.sleep in cliente e ServerCliente
    - controlla che db viene modificato correttamente in ServerCliente
    - controlal che generatore funziona bene
    - controlla req monitor finzionano bene
    - cliente, da cambiare: alla fine del streams solo quando legge ack da server su skeySOUT
    - inserire controllo su clienti/venditori/trasportatori, vengono effettuate operazioni solo se corrispettivo server è running e monitor è running (avviare i server e monitor prima )
    - crea un docker file per lancaire i vari containers
    - rimuovi hashMapServerLastID e cancella ogni messaggio dopola recezione (check se il sistema funziona bene)

OBIETTIVI DA IMPLEMENTARE Per successiva iterazione:
    - V finisci monitor
    - V finisci plotting
    - aggiusta interazione ServerCliente, ServerTrasportatore, ServerFornitore con DB e check funzionamento sistema
    - Traspostatori e Venditori, aggiusta azioni su generatori + server dedicati
    - aggiusta monitor in modo che controlli contemporaneamente da i 3 server dedicati
        idea: lanciare 3 thread, 1 per ogni server dedicato, che aggiungono i comandi add su log, monitor deve leggere direttamente da log e fare controlli, controlli da fare sono diversi tra Cliente, trasportatore, Fornitore? si
            idea aggiuntiva: suddividere log in 3 log diversi, uno per ogni Entità (Cliente, trasportatore, Fornitore), ogni thread scrive su log dedicato e un unico monitor scorre i diversi log in modo equo ed applica le diverse condizioni
            oppure i 3 thread scrivono su un unico log e cotrolli vengono effettuati su linee in log ad es. con stessa porta (solo linee dal Cliente, trasportatore, Fornitore) 
    - carica progetto su github
    - "devo scrivere tutto il progetto in inglese? e anche slide/tesi in inglese?"



POST:
    - script setup sulla futura macchina per creare mydb iniziale?
    - esegui redis-server all'avvio di ServerCliente da bash
    - termina redis-server alla chiusura di ServerCliente da bash (anche in caso di errore)
    - mettere parametri in un file .env? init?

NOTE:
    -
    -
    -
    -
    -

