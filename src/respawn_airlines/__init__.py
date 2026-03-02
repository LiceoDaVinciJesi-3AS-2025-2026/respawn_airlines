def main() -> None:
    import pygame
    import random 
    
    pygame.init()
    #inizializza i moudli pygame
    
    #controlla la velocità del gioco
    clock = pygame.time.Clock()

    larghezza_schermo = 800
    altezza_schermo = 448
    
    #sistemo la larghezza e l'altezza della finestra
    screen = pygame.display.set_mode((larghezza_schermo, altezza_schermo))

    imgSfondo = pygame.image.load("sfondo.jpg")
    imgSfondo = pygame.transform.scale(imgSfondo, (larghezza_schermo, altezza_schermo))

    font = pygame.font.SysFont('Rewashington', 40)

    # creo il pulsante start
    buttonRect_start = pygame.Rect(larghezza_schermo // 2 + 80, altezza_schermo - 180, 180, 60)
    textStart = font.render('Start', True, "white")
    textStartRect = textStart.get_rect(center=buttonRect_start.center)

    # creo il pulsante regolamento
    buttonRect_reg = pygame.Rect(larghezza_schermo // 2 + 80, altezza_schermo - 100, 180, 60)
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
            screen.fill("darkred")                  #C'è DA FARE IL REGOLAMENTO VERO E PROPRIO SU QUESTA SCHERMATA 
        
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
            imgAereo = pygame.transform.scale(imgAereo,(150,100))
            screen.blit(imgAereo, (aereo_x, aereo_y))
            
            #Gestisco i limiti dello schermo
            #se l'aereo arriva sopra il margine in alto si ferma e scende per effetto di gravità
            if aereo_y < 0:   
                aereo_y = 0
                aereo_vel = 0

            if aereo_y > altezza_schermo - 50:  #ho messo 50 che è l'altezza dell'aereo
                aereo_y = altezza_schermo - 50
                aereo_vel = 0
            
#     # Movimento palazzi (ostacoli)
#         for palazzo in palazzi:
#             palazzo["x"] -= velocità_palazzi
#             screen.blit(imgPalazzo, (palazzo["x"], palazzo["y"]))
# 
#     # Collisioni con palazzi o con il terreno
#         for palazzo in palazzi:
#             if aereo_rect.colliderect(palazzo_rect):
#                 game = False  # game over
#     # Rimuovi palazzo se esce dallo schermo
#             palazzi = [p for p in palazzi if p["x"] > -palazzo_larghezza]
#             
# 
#             if event.type == pygame.KEYDOWN:                             #SAREBBE DA INSERIRE SOTTO for event in pygame.event.get():
#                 #se ci si ritrova nel gioco 
#                 if event.key == pygame.K_SPACE and game:
#                     aereo_vel = -8




        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()



  