import pygame
def credit(fenetre,largeur,longueur):
    image_de_fond = pygame.image.load("image/credits.png").convert()
    pygame.display.set_caption("crédits")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        image_de_fond_redimensionnee = pygame.transform.scale(image_de_fond, (largeur, longueur))
        fenetre.blit(image_de_fond_redimensionnee, (0, 0))
        pygame.display.flip()
        clock.tick(60)
