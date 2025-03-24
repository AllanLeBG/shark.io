#call the main functions (see in notion)

import pygame
# Création du groupe de sprites pour les obstacles
obstacles = pygame.sprite.Group()
screen_width = screen.get_width()
screen_height = screen.get_height()

# Ajouter des rochers (dans l'eau)
obstacles.add(Roche(300, screen_height))
obstacles.add(Roche(500, screen_height))

# Ajouter des avions (dans l'air)
obstacles.add(Avion(800, screen_height, -5))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Récupéreration des touches pressées
    keys = pygame.key.get_pressed()

    # Déplacer les personnages  (équivalent vidéo ytb.. la jsp cque j'ai fait)
    screen_width = screen.get_width()   #initialiser la taille --> init screen / taille du screen
    screen_height = screen.get_height()
    personnage1.deplacer(touches_personnage1, keys, screen_width, screen_height)
    personnage2.deplacer(touches_personnage2, keys, screen_width, screen_height)

    # Mettre à jour les vagues..? 
    vagues.update()

    # caméra suit le personnage
    camera_offset_x = max(0, followed_character.rect.x - screen_width // 2)
    camera_offset_y = max(0, followed_character.rect.y - screen_height // 2)

    # couleur fond
    screen.fill((0, 0, 0))

    # Dessiner l'eau sur le premier tiers ?? à revoir selon décision du groupe
    water_rect = pygame.Rect(0, screen_height * 2 // 3, screen_width, screen_height // 3)
    pygame.draw.rect(screen, water_color, water_rect)

    # Les vagues (appel?)
    vagues.dessiner(screen, camera_offset_x)

    # 🛠️  ÉTAPE 4 : Mise à jour et affichage des obstacles 🛠️
    for obstacle in obstacles:
        if isinstance(obstacle, Avion):  # Seuls les avions bougent
            obstacle.update()

    for obstacle in obstacles:  # On dessine les obstacles en tenant compte de la caméra
        obstacle.dessiner(screen, camera_offset_x)

    # Dessiner les personnages sur l'écran
    personnage1.dessiner(screen, camera_offset_x)
    personnage2.dessiner(screen, camera_offset_x)

    # Mettre à jour l'affichage
    pygame.display.flip()
