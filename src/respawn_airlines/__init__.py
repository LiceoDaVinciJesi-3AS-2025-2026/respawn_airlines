def main() -> None:
    #libreria Standard
    import random
    from pathlib import Path
    
    #librerie pip
    import pygame
    from platformdirs import PlatformDirs

    
    pygame.init()
    # inizializza i moudli pygame
    
    # controlla la velocità del gioco (FPS)
    clock = pygame.time.Clock()

    # dimensioni finestra del gioco
    larghezza_schermo = 1200
    altezza_schermo = 672
    
    # creazione finestra
    screen = pygame.display.set_mode((larghezza_schermo, altezza_schermo))

    # crea automaticamente la cartella se non esiste
    dirs = PlatformDirs("respawn_airlines", ensure_exists=True)

    # percorso della cartella dati
    data_dir = Path(dirs.user_data_dir)

    # percorso del file classifica
    file_classifica = data_dir / "classifica.txt"

    # se il file non esiste lo crea
    if not file_classifica.exists():
        file_classifica.write_text("")
        
    # la variabile highscore crea il punteggio più alto, da 0 in su
    highscore = 0
    
    # lettura del file dei punteggi riga per riga
    # "with" serve per gestire il file automaticamente: quando il blocco finisce il file viene chiuso da solo
    with open(file_classifica, "r") as f:
        for riga in f:
            riga = riga.strip()

            if riga == "":
                continue

            numero = int(riga.replace("Punteggio: ", ""))

            if numero > highscore:
                highscore = numero

            
#--------------------------------------------------------------------------------------------------    
    # CARICAMENTO IMMAGINI
    # carica l'immagine come sfondo della home
    # riadatta l'immagine alla finestra
    imgSfondo = pygame.image.load("src/respawn_airlines/sfondo.jpg")
    imgSfondo = pygame.transform.scale(imgSfondo, (larghezza_schermo, altezza_schermo))

    # carica l'immagine del regolamento
    # riadatta l'immagine alla finestra
    imgReg = pygame.image.load("src/respawn_airlines/imgRegolamento.png")   
    imgReg = pygame.transform.scale(imgReg,(larghezza_schermo,altezza_schermo))

    # carica l'immagine del regolamento
    # riadatta l'immagine alla finestra
    imgSfondoGame = pygame.image.load("src/respawn_airlines/imgSfondoNY.png")    
    imgSfondoGame = pygame.transform.scale(imgSfondoGame,(larghezza_schermo,altezza_schermo))

    # carica l'immagine della schermata di quando perdi
    # riadatta l'immagine alla finestra
    imgSfondoGameOver = pygame.image.load("src/respawn_airlines/imgGameOver.jpg")
    imgSfondoGameOver = pygame.transform.scale(imgSfondoGameOver, (larghezza_schermo, altezza_schermo))

    # carica l'immagine dell'aereo
    # riadatta l'immagine secondo la grandezza desiderata e con la trasparenza
    # convert_alpha() serve a mantenere la trasparenza e a renderlo più veloce e semplice da disegnare
    imgAereo = pygame.image.load("src/respawn_airlines/imgAereo.png").convert_alpha() 
    imgAereo = pygame.transform.scale(imgAereo,(150,100))
    maskAereo=pygame.mask.from_surface(imgAereo)

    # Carica l'immagine del palazzo con la trasparenza
    imgPalazzo = pygame.image.load("src/respawn_airlines/imgPalazzo.png").convert_alpha()
    #mask serve a rilevare le collisioni precise lungo i bordi
    maskPalazzo= pygame.mask.from_surface(imgPalazzo)    

    # crea una versione capovolta verticalmente del palazzo
    # servirà per il palazzo che sta sopra
    imgPalazzoSopra = pygame.transform.flip(imgPalazzo, False, True)
    maskPalazzoSopra= pygame.mask.from_surface(imgPalazzoSopra) 

#-------------------------------------------------------------------------------------------------------------
    #CREAZIONE PULSANTI
    #creo il font per scrivere il testo nei pulsanti
    font = pygame.font.SysFont('Rewashington', 65)

    # creo il rettangolo del pulsante start cpn le scritte dentro
    # (x, y, larghezza, lunghezza)
    # x e y sarebbero il punto da dove parte il bottone
    buttonRect_start = pygame.Rect(larghezza_schermo // 2 + 40, altezza_schermo - 320, 300, 90)
    textStart = font.render('Start', True, "white")
    #centro la scritta dentro il pulsante
    textStartRect = textStart.get_rect(center=buttonRect_start.center)

    # creo il pulsante regolamento con la scritta centrata
    buttonRect_reg = pygame.Rect(larghezza_schermo // 2 + 40, altezza_schermo - 200, 300, 90)
    textReg = font.render('Regolamento', True, "white")
    textRegRect = textReg.get_rect(center=buttonRect_reg.center)
    
#----------------------------------------------------------------------------------------------------------   
    #AGGIUNTA SUONI
    #inizializza il modulo mixer per riprodurre i suoni
    pygame.mixer.init() 
    
    # Musica di background
    #file musicale
    musica_background = "src/respawn_airlines/suonoGioco.mp3"
    #caricamento file
    pygame.mixer.music.load(musica_background)
    #volume 50%
    pygame.mixer.music.set_volume(0.5)
    # -1 per un loop infinito
    pygame.mixer.music.play(-1) 

    # Suono di esplosione
    # caricamento suono
    suono_esplosione = pygame.mixer.Sound("src/respawn_airlines/esplosione.mp3")
    #volume 50%
    suono_esplosione.set_volume(0.5)
    
#---------------------------------------------------------------------------   
    # AEREO
    # posizione orizzontale iniziale (spostato in avanti)
    aereo_x = 200
    # posizione verticale iniziale (centro dello schermo)
    aereo_y = altezza_schermo // 2
    # velocità iniziale = 0 
    aereo_vel = 0
    # forza di gravità con la quale preicipita
    gravity = 0.6
    # velocità massima a cui arriva
    vel_max = 10
    
    # controlla il loop del game
    running = True
    # True = schermata iniziale
    home = True
    # True = schermata regolamento
    regolamento = False
    # True = schermata gioco
    game = False
    # True = schermata Game Over
    gameOver = False
    # True = gioco in pausa
    paused = False

#---------------------------------------------------------------------
    # PALAZZI
    #liste palazzi 
    palazzi = []
    palazzi_superati = []
    # timer per spawn palazzi
    timer_palazzi = 0
    # intervallo tra un palazzo e l'altro
    timer_base_palazzi = 90
    # punteggio da cui si parte
    score = 0
    # velocità dcon la quale i palazzi si muovono
    vel_base = 5  
#------------------------------------------------------------------------  
    
    while running:

        # posizione del mouse
        mPos = pygame.mouse.get_pos()
        
        # regola la velocità del gioco (frame al secondo)
        clock.tick(60)
        
        # gestione eventi
        # quando clicchi la X sul gioco, ti fa uscire
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # se premi un tasto:
            if event.type == pygame.KEYDOWN:
                # #con esc si torna al menu se sei nel regolamento o nel gioco
                if event.key == pygame.K_ESCAPE:
                    if regolamento or game or gameOver:
                        home = True       
                        regolamento = False
                        game = False
                        gameOver=False
                        score=0
                        
                        # Svuota i palazzi
                        palazzi.clear()
                        palazzi_superati.clear() 
                        timer_palazzi = 0
                    else:
                        #chiude il gioco se sei già nel menu
                        running = False
                        
                #se sei nella schermata game over e premi R, il gioco riparte
                if event.key == pygame.K_r and gameOver:
                    # Reset variabili aereo
                    score=0
                    aereo_y = altezza_schermo // 2
                    aereo_vel = 0

                    # Svuota i palazzi
                    palazzi.clear()
                    palazzi_superati.clear() 
                    timer_palazzi = 0

                    # Torna alla schermata di gioco
                    gameOver = False
                    game = True
                    # aggiunge la musica
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                
                #se ci si ritrova nel gioco e si preme spazio l'aereo viene spinto verso l'alto
                if event.key == pygame.K_SPACE and game: 
                    aereo_vel = -10
                    
                # se premi "P" per mettere in pausa (o uscire dalla pausa)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if paused:
                        paused = False
                        pygame.mixer.music.play()
                    else:
                        paused = True
                        pygame.mixer.music.pause()
                        
            # se è già in pausa, salta il ciclo
            if paused:
                continue

            # PULSANTI
            #se clicchi con il mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # inizia il gioco
                if buttonRect_start.collidepoint(mPos):
                    #se clicchi sul pulsante start esci dalla schermata iniziale e inizia il gioco (gioco=True)
                    home=False
                    game=True           

                if buttonRect_reg.collidepoint(mPos):
                    #se clicchi sul pulsante start esci dalla schermata iniziale e apre il regolamento (regolamento=True)
                    home=False
                    regolamento=True

        # SCHERMATA INIZIALE: 
        if home:
            # disegna lo sfondo del menù di gioco
            screen.blit(imgSfondo, (0, 0))

            # animazione del pulsante start, da rosso ad arancione se ci si passa col mouse
            buttonColor_start = "red"
            if buttonRect_start.collidepoint(mPos):
                buttonColor_start = "orange"
            button_start = pygame.draw.rect(screen,buttonColor_start,buttonRect_start)
            
            # animazione del pulsante regolamento, da blu a verde
            buttonColor_reg = "blue"
            if buttonRect_reg.collidepoint(mPos):
                buttonColor_reg = "green"
            button_reg = pygame.draw.rect(screen,buttonColor_reg,buttonRect_reg)
            
            # disegna il testo sopra i pulsanti
            screen.blit(textStart, textStartRect)
            screen.blit(textReg, textRegRect)
        
        # REGOLAMENTO:
        # disegna la schermata a schermo intero
        elif regolamento:
            screen.blit(imgReg, (0, 0)) 
        
        # GIOCO:
        elif game:
            
            # Disegna lo sfondo del gioco
            screen.blit(imgSfondoGame, (0, 0))

            # gravità aggiunta alla velocità dell'aereo 
            aereo_vel += gravity
            
            # evita che la velocità aumenti a dismisura, arrivato a 10 non accelera più
            if aereo_vel > vel_max:
                aereo_vel = vel_max
            
            # permette di far muovere l'aereo in base al fatto che vada verso su o giù
            aereo_y+=aereo_vel
                
            # disegna l'aereo
            screen.blit(imgAereo, (aereo_x, aereo_y))
            
           
            # gestisco i limiti dello schermo
            # limite dei bordi
            if aereo_y < 0:   
                aereo_y = 0
                aereo_vel = 0
            # 50 è l'altezza dell'aereo
            if aereo_y > altezza_schermo - 50:  
                aereo_y = altezza_schermo - 50
                aereo_vel = 0
            
            # rettangolo attorno all'aereo per vedere se tocca i palazzi
            # (x, y, larghezza, lunghezza)
            # aereo_x e aereo_y è la posizione in alto a sinistra
            # figura larga 150 e alta 100
            aereo_rect = pygame.Rect(aereo_x + 25, aereo_y + 20, 60, 30)
            aereo_right = aereo_x + 150
              

            #creazione palazzi 
            timer_palazzi += 1
            # la velocità di spawn aumenta con il punteggio più alto
            vel_palazzi = vel_base + score * 0.5
            # impone un limite allo spawn, lo adatta in base alla  velocità
            # max 20 frame, più punti fai e vai veloce ---> spawn più frequente
            timer_limite = max(20, int(timer_base_palazzi * vel_base / vel_palazzi))
            
            # quando deve spawnare un palazzo:
            if timer_palazzi >= timer_limite:
                # altezza del buco random
                buco_y = random.randint(120, 320)
                # centro random, con un minimo di altezza di 150 più metà del buco e un massimo del palazzo sopra più metà del buco - 150
                centro_buco = random.randint(150 + buco_y // 2, altezza_schermo - 150 - buco_y // 2)
                    
                # Crea il rettangolo per il palazzo sopra e quello sotto
                # (x, y, larghezza, altezza)
                # parte da destra,  altezza = 0, largo 80 e finisce quando il rettangolo del buco inizia
                p_sopra = pygame.Rect(larghezza_schermo, 0, 80, centro_buco - buco_y // 2)
                # parte da destra, appena finisce il rettangolo del buco, è largo 80 e arriva fino a giù
                p_sotto = pygame.Rect(larghezza_schermo, centro_buco + buco_y // 2, 80, altezza_schermo)
                
                # aggiungo alla lista dei palazzi attivi
                palazzi.append(p_sopra)
                palazzi.append(p_sotto)
                # reset timer
                timer_palazzi = 0
            
            
            # FUNZIONAMENTO
            # ciclo sui palazzi attivi
            # [:] crea una copia per rimuoveregli elementi
            for p in palazzi[:]:
                # muove verso  sx
                p.x -= vel_palazzi  
                # il numero di palazzi superati è uguale al punteggio
                score= len(palazzi_superati)
                
                # per il palazzo in alto (p.y == 0) si controlla se il bordo dx è passato oltre l'aereo
                if p.y == 0:
                    if p.right < aereo_x and p not in palazzi_superati:
                        palazzi_superati.append(p)
   
                # se il palazzo parte dall'alto lo inverte e guarda quello che è di sotto (p.bottom)
                # se è già quello sotto mette la mask
                if p.y == 0:
                    pos_palazzo = (p.x, p.bottom - 448)
                    screen.blit(imgPalazzoSopra, pos_palazzo)
                    # collisione precisa con l'aereo
                    maskCorrente = maskPalazzoSopra
                else:
                    pos_palazzo = (p.x, p.top)
                    screen.blit(imgPalazzo, pos_palazzo)
                    maskCorrente = maskPalazzo
                    
                # rimuove palazzi fuori schermo
                if p.x < -500:
                    palazzi.remove(p)  
                    continue

                # COLLISIONI
                # offset serve perchè indica alle maschere dove posizionarsi
                # dalla coordinata x del palazzo, alla coordinata x dell'aereo, dalla loro distanza in x e in y
                offset = (pos_palazzo[0] - aereo_rect.x, pos_palazzo[1] - aereo_rect.y)
                if maskAereo.overlap(maskCorrente, offset):
                    # Riproduci il suono di esplosione
                    suono_esplosione.play()
                    # Ferma la musica di background
                    pygame.mixer.music.stop()


                    # SALVATAGGIO PUNTEGGIO SU FILE 
                    # si usa 'a' per aggiungere il punteggio in fondo al file                  
                    with open(file_classifica, "a") as f:
                        f.write("Punteggio: " + str(score) + "\n")
                    
                    # se fai un punteggio più alto dell'highscore, si aggiorna
                    # apre il file e scrive il nuovo punteggio massimo
                    if score > highscore:
                        highscore = score
                        with open(file_classifica, "a") as f:
                            f.write("Punteggio: " + str(highscore) + "\n")
                    
                    #aggiunge stati del gioco
                    game = False
                    home = False
                    gameOver = True
                    
                    #reset palazzi
                    palazzi.clear()
                    timer_palazzi = 0
            

            # mostra punteggio in tempo reale in base ai palzzi superati
            score = len(palazzi_superati)
            scoreText = font.render("Score: " + str(score), True, "darkred")
            screen.blit(scoreText, (50, 50))
                               

        # schermata game over
        elif gameOver:
            # scritta
            fontScore= pygame.font.SysFont('Rewashington', 40)
            # apparizione dell'immagine
            screen.blit(imgSfondoGameOver, (0, 0))
            # punteggio finale
            fScoreText = fontScore.render(f"Palazzi superati: {len(palazzi_superati)}", True, "darkred")
            # posizione in alto a sinistra ma un po' più in basso e leggermente staccato dal bordo
            screen.blit(fScoreText, (10, 60))
            # scritta highscore
            highScoreText = fontScore.render("High Score: " + str(highscore), True, "darkred")
            screen.blit(highScoreText, (10,120))
        
        # il tutto viene mostrato nella finestra
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()





