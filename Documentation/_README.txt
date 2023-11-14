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
        - (old) Venditore, Cliente, Trasportatore controllano ogni volta nelle tabelle da modificare se esiste l'ennupla con stesso id + varie operazioni

        - Venditore, per ogni oggetto:
                no       - se ogg già esiste in ennupla di "ogginvendita" (se esiste una ennupla con nome, prezzo uguale a ogg)
                no            -> aggiungi a quella ennupla la quantità di ogg
                no        - altrimenti se ogg non esiste in ennupla di "ogginvendita"
                -> crea nuova ennupla in "ogginvendita" con dati di ogg e genera un nuovo id per nuova ennupla, crea nuova ennupla in "oggdaconsegn" e "oggconsegnati" con id uguale e quantità a 0 

        - se Cliente compra, per ogni oggetto ogg:
            - se ogg già esiste in ennupla di "ogginvendita" e la quantità in ennupla è maggiore o uguale a quantità di ogg
                -> sottrae la quantita specificata della ennupla in "ogginvendita" e aumenta la quantita specificata della ennupla in "oggdaconsegn" con stesso id
            - altrimenti se ogg non esiste in ennupla di "ogginvendita" o la quantità in ennupla è inferiore a quantità di ogg
                -> non vengono effettuate modifica in "ogginvendita", (opt. specificare l'errore acquisto in ack)

        - Trasportatore, per ogni ennupla in "oggdaconsegn":
            - se la quantità in ennupla è maggiore di 0
                -> sottrae la quantita rimanente della ennupla in "oggdaconsegn" e aumenta la quantita specificata della ennupla in "oggconsegnati" con stesso id



    - quando cliente esce, chiudi streams? vedere se è worth tenere info messaggi per monitor

    - controlla che db viene modificato correttamente in ServerCliente
    - controlal che generatore funziona bene
    - controlla req monitor finzionano bene
    - cliente, da cambiare: alla fine del streams solo quando legge ack da server su skeySOUT
    - inserire controllo su clienti/venditori/trasportatori, vengono effettuate operazioni solo se corrispettivo server è running e monitor è running (avviare i server e monitor prima )
    - in caso di errore o chiusura prematura di uno o più containers, chiudere in ordine tutti i processi?
    - crea un docker file per lancaire i vari containers
    - rimuovi hashMapServerLastID e cancella ogni messaggio dopola recezione (check se il sistema funziona bene)
    - rendere l'accesso al db sync invece che async? garantirebbe serialità e quindi atomicità operazioni del db?
    - venditori devono "vendere" qualcosa prima che clienti facciano azioni
        -clienti devono "comprare" qualcosa prima che i Traspostatori facciano azioni
    - aggiusta monitor in modo che controlli contemporaneamente da i 3 server dedicati
        idea: lanciare 3 thread, 1 per ogni server dedicato, che aggiungono i comandi add su log, monitor deve leggere direttamente da log e fare controlli, controlli da fare sono diversi tra Cliente, trasportatore, Fornitore? si
            idea aggiuntiva: suddividere log in 3 log diversi, uno per ogni Entità (Cliente, trasportatore, Fornitore), ogni thread scrive su log dedicato e un unico monitor scorre i diversi log in modo equo ed applica le diverse condizioni
            oppure i 3 thread scrivono su un unico log e cotrolli vengono effettuati su linee in log ad es. con stessa porta (solo linee dal Cliente, trasportatore, Fornitore)
    - moniotor cancella lines in log dopo averle analizzate? non credo. pushare il log su un db? se si quando?   



OBIETTIVI DA IMPLEMENTARE Per successiva iterazione:

    
    - V Testare Traspostatori e Venditori (azioni su generatori, azioni su server dedicati, interazioni con DB)
        - finisci testing Trasportatore e ServerTrasportatore. cambiare tInvio in db con timestamp e scrivi timestamp in "oggconsegnati" quando trasportatore fa azione
    - V finisci script per generatore clienti/venditori/trasportatori sono 0/pochi/molti

    - V modifica time.sleep in cliente e ServerCliente e negli altri containers
        - "come modifico?"
            - sol. dopo 1 sec che non arrivano nuovi messaggi vai avanti? implementato
            - cliente invia numero x di messaggi che server deve ricevere, server legge quando ci sono x messaggi nuovi da leggere (nel frattempo aspetta)

    - SMC:
    - V aggiusta generatori e passa seed ai generatori, ed essi devono usare quel seed
    - V su tabella db "monitorerror" salva anche timestamp della run nel momento in cui viene rilevato errore
    - V total runs = M = ln(\delta)/ ln(1 − \epsilon) con \delta e \epsilon = 1E-3 oppure 1E-4
    - V merge dei due branch del codice
    
    - V fai domanda di laurea
    - per le run dividire time.sleep() in generatori per un fattore X, cosi da velocizzare simulazione SMC
    - pusha su github
    


    


POST:
    - script setup sulla futura macchina per creare mydb iniziale?
    - mettere parametri in un file .env? init?

NOTE:
    - scrivere progetto e slide possibilmente in inglese per riuso futuro, tesi in italiano
    -
    -
    -
    -

