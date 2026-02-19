def main() -> None:
    import pygame
    
    pygame.init()
    #inizializza i moudli pygame

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

    running = True #fa funzionare il game loop
    home = True   #corrisponde alla schermata home
    regolamento = False  #regolamento=True -> schermata del regolamento
    game = False  #gioco=True -> schermata del gioco

    while running:

        # posizione del mouse
        mPos = pygame.mouse.get_pos()

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
                      
            #gestione pulsanti          
            if event.type == pygame.MOUSEBUTTONDOWN:          
                if buttonRect_start.collidepoint(mPos):
                    #se clicchi sul pulsante start esci dalla schermata iniziale e inizia il gioco (gioco=True)
                    home=False
                    #game=True           #PER ALE:se devi fare sta parte decommenta

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
        
        elif game:
            print("ciao")
            #ALE SCRIVICI TU QUI..... NON TOCCARE IL REGOLAMENTO E I TASTI!!!!1




        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()



  