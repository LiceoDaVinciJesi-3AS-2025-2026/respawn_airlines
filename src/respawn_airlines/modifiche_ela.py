def main() -> None:
    import pygame
    import random
    
    pygame.init()
    #inizializza i moudli pygame
    
    #controlla la velocità del gioco
    clock = pygame.time.Clock()

    larghezza_schermo = 1200
    altezza_schermo = 672
    
    #sistemo la larghezza e l'altezza della finestra
    screen = pygame.display.set_mode((larghezza_schermo, altezza_schermo))

    imgSfondo = pygame.image.load("sfondo.jpg")
    imgSfondo = pygame.transform.scale(imgSfondo, (larghezza_schermo, altezza_schermo))

    font = pygame.font.SysFont('Rewashington', 65)

    # creo il pulsante start
    buttonRect_start = pygame.Rect(larghezza_schermo // 2 + 40, altezza_schermo - 320, 300, 90)
    textStart = font.render('Start', True, "white")
    textStartRect = textStart.get_rect(center=buttonRect_start.center)

    # creo il pulsante regolamento (più grande)
    buttonRect_reg = pygame.Rect(larghezza_schermo // 2 + 40, altezza_schermo - 200, 300, 90)
    textReg = font.render('Regolamento', True, "white")
    textRegRect = textReg.get_rect(center=buttonRect_reg.center)
    
    
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

    
    # Carica l'immagine e crea quella sottosopra
    imgPalazzo = pygame.image.load("imgPalazzo.png").convert_alpha()
    
    imgPalazzo = pygame.transform.scale(imgPalazzo, (150, 450)) 
    imgPalazzoSopra = pygame.transform.flip(imgPalazzo, False, True)

    # Variabili dei palazzi
    palazzi = []
    timer_palazzi = 0
    
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
                    if regolamento or game:
                        home = True       
                        regolamento = False
                        game = False
                    else:
                        #chiude il gioco se sei già nel menu
                        running = False
                
                #se ci si ritrova nel gioco e si preme spazio l'aereo viene spinto verso l'alto
                if event.key == pygame.K_SPACE and game: 
                    aereo_vel = -11
                      
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
            imgReg = pygame.image.load("imgRegolamento.png")   
            imgReg = pygame.transform.scale(imgReg,(larghezza_schermo,altezza_schermo))      
            
            screen.blit(imgReg, (0, 0))
        
        #opero nella schermata del gioco
        elif game:    #GIUSTO
            # Disegna lo sfondo del gioco
            imgSfondoGame = pygame.image.load("imgSfondoNY.png")    #C'è DA SISTEMARE LO SFONDO + FAR PARTIRE L'AEREO DA PIù DIETRO????
            imgSfondoGame = pygame.transform.scale(imgSfondoGame,(larghezza_schermo,altezza_schermo))
            
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
            imgAereo = pygame.image.load("imgAereo.png") 
            imgAereo = pygame.transform.scale(imgAereo,(150,100))                       #RIVEDI MISURA AEREO
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
            aereo_rect = pygame.Rect(aereo_x, aereo_y, 50, 20) 
              
                        # --- CREA I PALAZZI OGNI 90 MILLISECONDI ---
            timer_palazzi += 1
            if timer_palazzi > 90: 
                buco_y = random.randint(120, 320) # Punto centrale del passaggio
                
                # Crea il rettangolo per il palazzo sopra e quello sotto
                # (x, y, larghezza, altezza)
                p_sopra = pygame.Rect(800, 0, 100, buco_y - 100)
                p_sotto = pygame.Rect(800, buco_y + 100, 120, 448)
                
                palazzi.append(p_sopra)
                palazzi.append(p_sotto)
                timer_palazzi = 0

            # --- MUOVI E DISEGNA I PALAZZI ---
            for p in palazzi[:]:
                p.x -= 5 # Sposta a sinistra

                if p.y == 0: # Se il palazzo parte dall'alto
                    screen.blit(imgPalazzoSopra, (p.x, p.bottom - 448))
                else:        # Se il palazzo parte dal basso
                    screen.blit(imgPalazzo, (p.x, p.top))
                
                # Se il palazzo esce dallo schermo, cancellalo dalla lista
                if p.right < 0:
                    palazzi.remove(p)

                for p in palazzi:
                    if aereo_rect.colliderect(p):
                        game = False
                        home = True
                        palazzi.clear() # Svuota i palazzi per la prossima partita
                        timer_palazzi = 0
    

#, AEREO 



        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()