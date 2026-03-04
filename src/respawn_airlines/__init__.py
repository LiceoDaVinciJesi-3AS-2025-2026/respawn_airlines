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

    # creo il pulsante regolamento
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
    imgPalazzo = pygame.image.load("imgPalazzo.png").convert_alpha() #per la trasparenza
    maskPalazzo= pygame.mask.from_surface(imgPalazzo)     #considera solo le parti delle immagini opache ignorando quelle trasparenti intorno

    imgPalazzoSopra = pygame.transform.flip(imgPalazzo, False, True)
    maskPalazzoSopra= pygame.mask.from_surface(imgPalazzoSopra) 

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
                    aereo_vel = -10
                      
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
        elif game:
            
#             screen.blit(sfondi_gioco[indice_sfondo], (0, 0))
            # Disegna lo sfondo del gioco
            imgSfondoGame = pygame.image.load("imgSfondoNY.png")    
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
            imgAereo = pygame.image.load("imgAereo.png").convert_alpha() 
            imgAereo = pygame.transform.scale(imgAereo,(150,100))
            screen.blit(imgAereo, (aereo_x, aereo_y))
            
            maskAereo=pygame.mask.from_surface(imgAereo)
            
            
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
            aereo_rect = pygame.Rect(aereo_x + 25, aereo_y + 20, 60, 30) 
              
                        # --- CREA I PALAZZI OGNI 90 MILLISECONDI ---
            timer_palazzi += 1
            if timer_palazzi > 90:
                buco_y = random.randint(120, 320) # Punto centrale del passaggio
                
                # Crea il rettangolo per il palazzo sopra e quello sotto
                # (x, y, larghezza, altezza)
                p_sopra = pygame.Rect(800, 0, 80, buco_y - 130)
                p_sotto = pygame.Rect(800, buco_y + 130, 80, 448)
                
                palazzi.append(p_sopra)
                palazzi.append(p_sotto)
                timer_palazzi = 0
            

            # muovi e disegna i palazzi
            for p in palazzi[:]:
                # Se il palazzo parte dall'alto
                if p.y == 0:
                    pos_palazzo = (p.x, p.bottom - 448)
                    screen.blit(imgPalazzoSopra, pos_palazzo)
                    maskCorrente = maskPalazzoSopra
                else:
                    pos_palazzo = (p.x, p.top)
                    screen.blit(imgPalazzo, pos_palazzo)
                    maskCorrente = maskPalazzo

                    # Movimento
                p.x -= 5

                    #collisioni
                offset = (pos_palazzo[0] - aereo_rect.x, pos_palazzo[1] - aereo_rect.y)    #!!!
                

                if maskAereo.overlap(maskCorrente, offset):
#                     palazzi.clear()
                    game = False
                    home = True
                    timer_palazzi = 0


                        
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()



  
