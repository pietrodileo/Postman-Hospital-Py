# Descrizione di una Raccolta Postman in formato JSON

Il documento fornito spiega come è composta una raccolta di richieste (*collection*) utilizzata da Postman. La raccolta è un file in formato JSON con la seguente struttura:

## "info" - Informazioni sulla Raccolta

L'oggetto "info" contiene le informazioni generali sulla raccolta Postman. Le seguenti proprietà sono incluse:

* "_postman_id": Un identificativo univoco assegnato alla raccolta.
* "name": Il nome della raccolta.
* "description": Una descrizione dettagliata della raccolta.
* "schema": Un riferimento allo schema JSON utilizzato per definire la raccolta.
* "_exporter_id": Un identificativo relativo all'esportazione della raccolta.

## "item" - Elementi della Raccolta

L'array "item" rappresenta le cartelle all'interno della raccolta, ciascuna delle quali può contenere una o più richieste HTTP. Ogni elemento dell'array "item" è definito da:

* "name": Il nome della cartella.
* "item": Un array che contiene le singole richieste HTTP incluse nella cartella.
* "description": Una descrizione della cartella.

## "event" - Eventi Associati

L'array "event" definisce gli eventi associati alla raccolta o alle richieste al suo interno. Gli eventi possono essere di due tipi: "prerequest" (eseguiti prima dell'invio della richiesta) e "test" (eseguiti dopo l'invio della richiesta). Ciascun evento contiene uno script in JavaScript eseguire, specificato tramite le seguenti proprietà:

* "listen": Il tipo di evento, che può essere "prerequest" o "test".
* "script": Lo script da eseguire, con "exec" contenente il codice e "type" indicante il linguaggio (solitamente "text/javascript").

## "variable" - Variabili di Raccolta

L'array "variable" definisce variabili utilizzate nella raccolta per l'elaborazione dinamica delle richieste. Le variabili possono rappresentare URL, porte o altri parametri configurabili. Ciascuna variabile ha le seguenti proprietà:

* "key": Il nome della variabile.
* "value": Il valore assegnato alla variabile.
* "type": Il tipo di variabile (ad esempio, "string" o "any").

## Contenuto di "item.item" - Richieste HTTP

Ogni elemento dell'array "item.item" rappresenta una richiesta HTTP.

Ogni richiesta contiene le seguenti proprietà:

* "name": Il nome della richiesta.
* "event": Gli eventi associati a questa specifica richiesta, analogamente a quanto spiegato in precedenza.
* "request": Le informazioni sulla richiesta HTTP, tra cui il metodo (ad esempio, "POST"), gli header, il corpo della richiesta e l'URL di destinazione. Saranno spiegate dettagliatamente in seguito.
* "response": Il campo "response" è simile al campo "request", ma si riferisce alle risposte che possono essere generate da un eventuale mock server.

## Struttura del Campo "item.item.request" - informazioni sulla richiesta HTTP

Il campo "request" definisce una richiesta HTTP all'interno della raccolta Postman. Esso è strutturato nel seguente modo:

* "method": Il metodo HTTP utilizzato per la richiesta (ad esempio, "POST" o "GET").
* "header": Un array contenente gli header della richiesta.
* "body": Questo campo definisce il body della richiesta, che è definito dalle seguenti proprietà:
  * "mode": La modalità con cui viene inserito il body del messaggio. Da impostare come "raw" per indicare che stiamo inserendo un JSON o un altro formato di testo nel body della richiesta.
  * "raw": I dati effettivi della richiesta, che possono includere un messaggio in formato JSON, XML o altri formati.
  * "options": Le opzioni associate al corpo del messaggio. Possiamo qui specificare che il body è scritto in linguaggio "json".
* "url": Questo campo definisce l'URL di destinazione della richiesta. È suddiviso in diverse proprietà:
  * "raw": L'URL completo.
  * "protocol": Il protocollo utilizzato (ad esempio, "http").
  * "host": Un array che elenca il nome dell'host o del server (ad esempio, "localhost").
  * "port": La porta utilizzata per la connessione.
  * "path": Un array che definisce il percorso dell'URL.
  * "query": Un array contenente parametri di query da inserire nell'URL, ognuno dei quali è definito da "key" (chiave) e "value" (valore).
