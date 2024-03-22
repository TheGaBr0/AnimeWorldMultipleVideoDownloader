# AnimeWorldMultipleVideoDownloader
Questo è un programma scritto in python per scaricare molteplici video in contemporanea da AnimeWorld in maniera veloce. 
Sfrutta il sistema di archiviazione nei server di AnimeWorld: il nome dei files di una serie sono sempre gli stessi ad eccezione dell'episodio.
E' quindi sufficiente inserire il link diretto del file di un qualsiasi episodio di una serie e specificare un range di episodi da scaricare. 

Se si dovessero specificare più episodi di quelli scaricabili in contemporanea, il programma dividerà in automatico i downloads, ad esempio:
Episodi da scaricare: 20
Episodi scaricabili in contemporanea: 5
Il programma ne scarica i primi 5, terminati procede coi successivi 5 e così via fino al termine. 

Piccola gif di esempio:
![2024-03-2210-24-34-ezgif com-video-to-gif-converter](https://github.com/TheGaBr0/AnimeWorldMultipleVideoDownloader/assets/62567964/fd8b6612-46e5-4f3f-bb3f-7f8dc1274108)

## Requisiti
Se si vuole compilare con python invece che usare l'exe è necessario avere i seguenti moduli: **requests** e **tqdm**. 

## Note sul file exe
Questo file è pensato per chi ci capisce poco di programmazione e preferisce un approccio più immediato: il file exe è abbastanza lento a partire, quindi se ci mette un po' ad avviarsi è normale. 
