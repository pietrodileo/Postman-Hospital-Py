# Github Commands

## Nomenclature

### Repository Remoto

Un repository remoto è una copia del tuo progetto ospitata su un server esterno, come GitHub. È una versione condivisa del tuo codice che può essere accessibile da più persone. I repository remoti consentono di collaborare, sincronizzare e condividere il lavoro con altri sviluppatori.

### Repository Locale

Un repository locale è una copia del tuo progetto memorizzata sul tuo computer locale (cartella di lavoro). Questa copia ti consente di lavorare sul codice, apportare modifiche e testarle senza influenzare il codice nel repository remoto. Una volta che le modifiche sono state testate e validate localmente, puoi sincronizzarle con il repository remoto.

## Comandi

* Clonare il repository in una cartella locale:

```
git clone "URLrepository"
```

* Verificare il repository remoto collegato al tuo repository locale: 
```
git remote -v
```

* Scaricare gli ultimi aggiornamenti dal repository remoto: 
```
git pull
```

* Aggiungere alcuni file alle modifiche da committare: 
```
git add file1.js file2.css file3.html
```

* Aggiungere tutti i file alle modifiche da committare: 
```
git add .
```

* Eseguire un commit con un commento descrittivo: 
```
git commit -m "commento del commit"
```

* Verificare il branch attuale del repository su cui stiamo lavorando: 
```
git branch
```

* Inviare il commit al server remoto, al branch attuale su cui stiamo lavorando: 
```
git push
```

* Inviare il commit al server remoto, al branch che specifichiamo (non necessariamente quello attuale). "origin" è il nome predefinito del repository remoto quando lo cloni o lo colleghi. L'opzione -u imposta anche "origin nomeBranch" come repository e branch predefiniti per i futuri comandi di push: 
```
git push origin nomeBranch
```
* Eseguire una fusione (merge) tra il branch attuale e un altro branch: 
```
git merge nomeAltroBranch
```

* Passare a un altro branch esistente: 
```
git checkout nomeAltroBranch
```

* Creare un nuovo branch e spostarsi su di esso: 
```
git checkout -b nomeNuovoBranch
```

* Collegare un repository remoto al repository locale: 
```
git remote add origin URLrepository
```

* Creare un nuovo repository su GitHub: Si può fare sul sito di GitHub.
* Creare una nuova pull request su GitHub: Si può fare sul sito di GitHub.


* Verificare lo stato dei file non ancora committati:
```
git status
```
* Visualizzare le differenze tra le modifiche non committate e l'ultima versione committata:
```
git diff
```
* Visualizzare la cronologia dei commit:
```
git log
```
* Inizializzare un nuovo repository locale:
```
git init
```
* Visualizzare le modifiche effettuate in un commit specifico:
```
git show ID_commit
```
* Rimuovere un file dall'area di staging (dopo git add):
```
git reset fileDaRimuovere
```
* Annullare un commit e riportare i file alle modifiche non committate:
```
git reset HEAD~
```
* Riportare i file a uno stato specifico, annullando tutte le modifiche:
```
git checkout -- .
```
* Rimuovere un file dal repository e dallo storico dei commit:
```
git rm nomeFile
git commit -m "Rimozione file"
```