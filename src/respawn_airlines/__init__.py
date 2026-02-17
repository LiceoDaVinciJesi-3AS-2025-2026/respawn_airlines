def main() -> None:
    pygame.init()
    #inizializza i moduli pygame
  
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 896

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #larghezza e altezza della finestra
    
    imgSfondo = pygame.image.load("sfondo.jpg") 
    imgSfondo = pygame.transform.scale(imgSfondo,(SCREEN_WIDTH,SCREEN_HEIGHT))

    font = pygame.font.SysFont('Rewashington',100) 
    textRect = font.render('Start' , True , "white") 
    buttonRect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT //2, 270, 100)

    #crea un rettangolo (il pulsante)
    running = True
    #fa funzionare il game loop

    while running:

        # posizione del mouse
        mPos = pygame.mouse.get_pos() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            # quando clicchi SOPRA il pulsante... FAI QUALCOSA!!!
#             if not game_started:
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     if buttonRect.collidepoint(mPos):          #C'E' DA SISTEMARLO IL PULSANTE
#                         game_started = True

        
        screen.blit(imgSfondo,(0,0) )
 
        # ANIMAZIONE DEL PULSANTE (cambia colore quando ci passi sopra)
        buttonColor = "red"
        if buttonRect.collidepoint(mPos):
            buttonColor = "orange"
        button = pygame.draw.rect(screen,buttonColor,buttonRect) 

        screen.blit(textRect , (SCREEN_WIDTH //2 + 50, SCREEN_HEIGHT// 2) )

        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
