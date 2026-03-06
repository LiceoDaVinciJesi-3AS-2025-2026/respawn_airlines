def main() -> None:
    import pygame
    import random 
    from platformdirs import PlatformDirs
    from pathlib import Path                #MODIFICARE PUNTEGGI, AGGIUNGERE COMMENTI

    pygame.init()
    #inizializza i moudli pygame
    
    #controlla la velocità del gioco
    clock = pygame.time.Clock()

    larghezza_schermo = 1200
    altezza_schermo = 672
    
    
    #sistemo la larghezza e l'altezza della finestra
    screen = pygame.display.set_mode((larghezza_schermo, altezza_schermo))
    

    # "ensure_exists=True" crea automaticamente la cartella se non esiste
    dirs = PlatformDirs("respawn_airlines", ensure_exists=True)
    # Trasformiamo il percorso in un oggetto Path per usare .exists()
    file_path = Path(dirs.user_data_dir) / "classifica.txt"
# 
#     high_score = 0
#     if file_path.exists():
#         f = open(file_path, "r")
#         contenuto = f.read()
#         if contenuto != "":
#             high_score = int(contenuto)
#             f.close()
    
    # CARICAMENTO IMMAGINI

    imgSfondo = pygame.image.load("sfondo.jpg")
    imgSfondo = pygame.transform.scale(imgSfondo, (larghezza_schermo, altezza_schermo))

    imgReg = pygame.image.load("imgRegolamento.png")   
    imgReg = pygame.transform.scale(imgReg,(larghezza_schermo,altezza_schermo))

    imgSfondoGame = pygame.image.load("imgSfondoNY.png")    
    imgSfondoGame = pygame.transform.scale(imgSfondoGame,(larghezza_schermo,altezza_schermo))

    imgSfondoGameOver = pygame.image.load("imgGameOver.jpg")
    imgSfondoGameOver = pygame.transform.scale(imgSfondoGameOver, (larghezza_schermo, altezza_schermo))

    imgAereo = pygame.image.load("imgAereo.png").convert_alpha() 
    imgAereo = pygame.transform.scale(imgAereo,(150,100))
    maskAereo=pygame.mask.from_surface(imgAereo)

    # Carica l'immagine e crea quella sottosopra del palazzo
    imgPalazzo = pygame.image.load("imgPalazzo.png").convert_alpha() #per la trasparenza
    maskPalazzo= pygame.mask.from_surface(imgPalazzo)     #considera solo le parti delle immagini opache ignorando quelle trasparenti intorno

    imgPalazzoSopra = pygame.transform.flip(imgPalazzo, False, True)
    maskPalazzoSopra= pygame.mask.from_surface(imgPalazzoSopra) 


    #CREAZIONE PULSANTI
    font = pygame.font.SysFont('Rewashington', 65)

    # creo il pulsante start
    buttonRect_start = pygame.Rect(larghezza_schermo // 2 + 40, altezza_schermo - 320, 300, 90)
    textStart = font.render('Start', True, "white")
    textStartRect = textStart.get_rect(center=buttonRect_start.center)

    # creo il pulsante regolamento
    buttonRect_reg = pygame.Rect(larghezza_schermo // 2 + 40, altezza_schermo - 200, 300, 90)
    textReg = font.render('Regolamento', True, "white")
    textRegRect = textReg.get_rect(center=buttonRect_reg.center)
    
    
    #AGGIUNTA SUONI
    pygame.mixer.init() 
    
    # Musica di background
    musica_background = "suonoGioco.mp3"
    pygame.mixer.music.load(musica_background)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # loop infinito

    # Suono di esplosione
    suono_esplosione = pygame.mixer.Sound("esplosione.mp3")
    suono_esplosione.set_volume(0.5)
    
    
    #variabili aereo
    aereo_x = 200
    aereo_y = altezza_schermo // 2
    aereo_vel = 0
    gravity = 0.6
    vel_max = 10

    running = True #fa funzionare il game loop
    home = True   #corrisponde alla schermata home
    regolamento = False  #regolamento=True -> schermata del regolamento
    game = False  #gioco=True -> schermata del gioco
    gameOver = False #gameOver=True-> schermata "hai perso"
    paused = False
    
    # Variabili dei palazzi
    palazzi = []
    palazzi_superati = []
    timer_palazzi = 0
    timer_base_palazzi = 90
    score = 0
    vel_base = 5  # velocità iniziale palazzi
    
    while running:

        # posizione del mouse
        mPos = pygame.mouse.get_pos()
        
        #regola la velocità del gioco
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #con esc si torna al menu se sei nel regolamento o nel gioco
                    if regolamento or game or gameOver:
                        home = True       
                        regolamento = False
                        game = False
                        gameOver=False
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
                    
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                
                #se ci si ritrova nel gioco e si preme spazio l'aereo viene spinto verso l'alto
                if event.key == pygame.K_SPACE and game: 
                    aereo_vel = -10
                    
                # PREMI "P" per mettere in pausa (o uscire dalla pausa)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if paused:
                        paused = False
                        pygame.mixer.music.play()
                    else:
                        paused = True
                        pygame.mixer.music.pause()

            if paused:
                continue
                      
            #gestione pulsanti          
            if event.type == pygame.MOUSEBUTTONDOWN:          
                if buttonRect_start.collidepoint(mPos):
                    #se clicchi sul pulsante start esci dalla schermata iniziale e inizia il gioco (gioco=True)
                    home=False
                    game=True           

                if buttonRect_reg.collidepoint(mPos):
                    #se clicchi sul pulsante start esci dalla schermata iniziale e apre il regolamento (regolamento=True)
                    home=False
                    regolamento=True
            
            


        #ora opero sulla schermata iniziale 
        if home:
        
            screen.blit(imgSfondo, (0, 0))

            #creo animazione del pulsante start
            buttonColor_start = "red"
            if buttonRect_start.collidepoint(mPos):
                buttonColor_start = "orange"
            button_start = pygame.draw.rect(screen,buttonColor_start,buttonRect_start)
            
            #creo animazione del pulsante regolamento
            buttonColor_reg = "blue"
            if buttonRect_reg.collidepoint(mPos):
                buttonColor_reg = "green"
            button_reg = pygame.draw.rect(screen,buttonColor_reg,buttonRect_reg)

            screen.blit(textStart, textStartRect)
            screen.blit(textReg, textRegRect)
        
        elif regolamento:
            screen.blit(imgReg, (0, 0)) 
        
        #opero nella schermata del gioco
        elif game:
            
            # Disegna lo sfondo del gioco
            screen.blit(imgSfondoGame, (0, 0))

            # Gravità e movimento aereo
            #aggiungo la gravità alla velocità dell'aereo 
            aereo_vel += gravity
            
            #evita che la velocità aumenti a dismisura, arrivato a 10 l'aereo non aumenta la velocità
            if aereo_vel > vel_max:
                aereo_vel = vel_max
            
            #permette di far muovere l'aereo in base al fatto che vada verso su o giù
            aereo_y+=aereo_vel
                
            # Disegna l'aereo
            screen.blit(imgAereo, (aereo_x, aereo_y))
            
           
            #Gestisco i limiti dello schermo
            #se l'aereo arriva sopra il margine in alto si ferma e scende per effetto di gravità
            if aereo_y < 0:   
                aereo_y = 0
                aereo_vel = 0

            if aereo_y > altezza_schermo - 50:  #ho messo 50 che è l'altezza dell'aereo
                aereo_y = altezza_schermo - 50
                aereo_vel = 0

            
            # Crea un rettangolo attorno all'aereo per vedere se tocca i palazzi
            aereo_rect = pygame.Rect(aereo_x + 25, aereo_y + 20, 60, 30)
            aereo_right = aereo_x + 150
              
#             # --- CREA I PALAZZI OGNI 90 MILLISECONDI ---
            timer_palazzi += 1
            vel_palazzi = vel_base + score * 0.5
            timer_limite = max(20, int(timer_base_palazzi * vel_base / vel_palazzi))  # adatta timer alla velocità
            if timer_palazzi >= timer_limite:
                buco_y = random.randint(120, 320) # Punto centrale del passaggio
                centro_buco = random.randint(150 + buco_y // 2, altezza_schermo - 150 - buco_y // 2)
                    
                # Crea il rettangolo per il palazzo sopra e quello sotto
                # (x, y, larghezza, altezza)
#                 p_sopra = pygame.Rect(800, 0, 80, centro_buco - 130)
#                 p_sotto = pygame.Rect(800, centro_buco + 130, 80, 448)
                p_sopra = pygame.Rect(larghezza_schermo, 0, 80, centro_buco - buco_y // 2)
                p_sotto = pygame.Rect(larghezza_schermo, centro_buco + buco_y // 2, 80, altezza_schermo)
                    
                palazzi.append(p_sopra)
                palazzi.append(p_sotto)
                timer_palazzi = 0
            


            for p in palazzi[:]:
                p.x -= vel_palazzi  # Muovi il palazzo verso sinistra
                
                score= len(palazzi_superati)
                
                if p.y == 0:
                    if p.right < aereo_right and p not in palazzi_superati:
                        palazzi_superati.append(p)
#         
                # Se il palazzo parte dall'alto
                if p.y == 0:
                    pos_palazzo = (p.x, p.bottom - 448)
                    screen.blit(imgPalazzoSopra, pos_palazzo)
                    maskCorrente = maskPalazzoSopra
                else:
                    pos_palazzo = (p.x, p.top)
                    screen.blit(imgPalazzo, pos_palazzo)
                    maskCorrente = maskPalazzo
               
                if p.x < -500:
                    palazzi.remove(p)  
                    continue

                #collisioni
                offset = (pos_palazzo[0] - aereo_rect.x, pos_palazzo[1] - aereo_rect.y)    #!!!
                if maskAereo.overlap(maskCorrente, offset):
                    
                    # Riproduci il suono di esplosione
                    suono_esplosione.play()
                        
                    # Ferma la musica di background
                    pygame.mixer.music.stop()
                    
                    # --- SALVATAGGIO PUNTEGGIO SU FILE ---
                    # Usiamo 'a' per aggiungere il punteggio in fondo al file                  
                    f = open(file_path, "a")
                    f.write("Punteggio: " + str(score) + "\n")
                    f.close()
                    
                    game = False
                    home = False
                    gameOver = True
                    
                    palazzi.clear()
                    timer_palazzi = 0
            

            # mostra punteggio in tempo reale
            score = len(palazzi_superati)
            scoreText = font.render("Score: " + str(score), True, "darkred")
            screen.blit(scoreText, (50, 50))
                               
            
        
        elif gameOver:
            
            fontScore= pygame.font.SysFont('Rewashington', 40)
            
            screen.blit(imgSfondoGameOver, (0, 0))
            # Mostra punteggio finale
            fScoreText = fontScore.render(f"Palazzi superati: {len(palazzi_superati)}", True, "darkred")
            # posizione in alto a sinistra ma un po' più in basso e leggermente staccato dal bordo
            screen.blit(fScoreText, (10, 60))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()



  
