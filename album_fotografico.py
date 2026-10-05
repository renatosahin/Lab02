def carica_da_file(file_path):
    album = []

    try:
        with open(file_path, "r", encoding="utf-8") as csvfile: #apro il file csv in modalità reading
            header = csvfile.readline() #leggo la prima riga

            for line in csvfile: # itero per ogni riga del file
                line = line.strip() #divido il file in righe
                if not line:    #se c'è una linea vuota la salto
                    continue

                parti = line.split(",")
                codice = parti[0].strip()
                titolo = parti[1].strip()
                autore = parti[2].strip()
                mese = int(parti[3].strip())
                anno = int(parti[4].strip())

                foto = {                        # ogni foto corrisponde a un singolo dizionario
                    "codice": codice,
                    "titolo": titolo,
                    "autore": autore,
                    "mese": mese,
                    "anno": anno,
                }

                anno_trovato = False
                for element in album:
                    if element[0] == anno:
                        element[1].append(foto) # aggiungo la foto alla lista dell'anno già esistente
                        anno_trovato = True
                        break

                if not anno_trovato:
                    album.append([anno, [foto]]) # creo un nuovo elemento nella lista con l'anno e una lista che contiene il dizionario foto

            return album
    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    try:        # Verifico che mese e anno siano valori interi validi
        mese = int(mese)
        anno = int(anno)
    except ValueError:
        return None

    if mese < 1 or mese > 12: # verifico che il mese sia valido
        return None

    for element in album:   # itero su ogni elemento della lista, se il codice c'è già allora la foto non è nuova, quindi restituisco None
        for foto in element[1]:
            if foto["codice"] == codice:
                return None

    nuova_foto = {      # creo il dizionario per la nuova foto
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }

    try:
        with open(file_path, "a", encoding="utf-8") as csvfile: # apro il file in modalità append così scrivo in fondo senza toccare gli elementi già presenti nel file
            csvfile.write(f"\n{codice},{titolo},{autore},{mese},{anno}") # scrivo la nuova riga
    except FileNotFoundError:
        return None

    anno_trovato = False        # aggiorno la lista album
    for element in album:
        if element[0] == anno: # se l'anno c'è già, inserisco la foto nella lista dell'anno stesso
            element[1].append(nuova_foto)
            anno_trovato = True
            break

    if not anno_trovato: # se l'anno non c'è, creo una nuovo elemento nella lista con l'anno che non era presente
        album.append([anno, [nuova_foto]])

    return nuova_foto


def cerca_foto(album, codice):
    for element in album: # itero sulla mia lista
        for foto in element[1]: # itero sulle foto per ciascun anno della lista
            if foto["codice"] == codice: # se il codice corrisponde a quello desiderato, restituisco i dati formattati
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}'"
    return None # altrimenti niente


def elenco_foto_anno_per_titolo(album, anno):
    for element in album:
        if element[0] == anno: #itero su ciascun anno
            titoli = []
            for foto in element[1]: # itero sulle foto di quell'anno
                titoli.append(foto["titolo"]) # estraggo solo il titolo
            titoli.sort() # ordino la lista dei titoli
            return titoli
    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
