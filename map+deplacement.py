class Perso(pygame.sprite.Sprite):

    def __init__(self, image_path, start_pos):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (300, 200))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = start_pos
        self.y_eau = 850
        self.speed = 3
        self.vitesse_y = 0
        self.en_saut = False
        self.gravite = 0.086
        self.live = True

    def deplacer(self, touches, keys, screen_width, screen_height):


        #Dans l'eau
        if self.rect.top > self.y_eau:
            if keys[touches['left']] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[touches['right']] and self.rect.right < screen_width:
                self.rect.x += self.speed
            if keys[touches['up']]:
                self.rect.y -= self.speed
            if keys[touches['down']] and self.rect.bottom < screen_height:
                self.rect.y += self.speed


        #Sortie de l'eau 01
        elif self.rect.top <= self.y_eau:

            if keys[touches['left']] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[touches['right']] and self.rect.right < screen_width * 2:  # Limite sur la droite augmentée
                self.rect.x += self.speed

            if keys[touches['down']] and self.rect.bottom < screen_height:  # Limite en hauteur augmentée
                self.rect.y += self.speed

            if keys[touches['space']] and not self.en_saut:
                self.vitesse_y = -11
                self.en_saut = True

            if self.en_saut:
                self.vitesse_y += self.gravite
                self.rect.y += self.vitesse_y


                if keys[touches['left']] and self.rect.left > 0:
                    self.rect.x -= self.speed
                if keys[touches['right']] and self.rect.right < screen_width * 2:
                    self.rect.x += self.speed

                #Fin du saut : quand on touche l'eau
                if self.rect.top >= self.y_eau:
                    self.rect.top = self.y_eau
                    self.vitesse_y = 0
                    self.en_saut = False



    def dessiner(self, screen, camera_offset_x,camera_offset_y): # permet de suivre le personnage ( avec la caméra )
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y - camera_offset_y))




class Coin:
    def __init__(self, position, img):
        self.pos = (10,10)
        self.img = pygame.transform.scale(pygame.image.load(img), (50, 50))
        self.nombre_de_piece=0
        self.ramassee = False
        self.rect = self.img.get_rect(topleft=self.pos)
        self.font = pygame.font.SysFont("None", 36)

    def ajouter_des_pieces (self,nb=1):
        self.nombre_de_piece+=nb

    def ramasser(self):
        if not self.ramassee:
            self.ajouter_des_pieces(1)
            self.ramassee = True

    def get_pieces (self):
        return self.nombre_de_piece

    def dessiner_menu(self, screen):
        if not self.ramassee:
            screen.blit(self.img, (self.rect.x , self.rect.y) )


    def dessiner(self, screen,camera_offset_x,camera_offset_y):
        if not self.ramassee:
            screen.blit(self.img, (self.rect.x - camera_offset_x, self.rect.y - camera_offset_y))
