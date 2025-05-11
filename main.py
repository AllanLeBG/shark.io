import pygame
import sys
import random
from obstacles import Roche, Avion, Mouette, Humain

# Initialisation
pygame.init()
pygame.mixer.init()

try:
    shark_img = pygame.image.load("assets/shark.png")
    print("✅ Assets chargés avec succès !")
except:
    print("❌ Fichiers manquants dans assets/ !")

# Configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
SKY_BLUE = (135, 206, 235)
OCEAN_BLUE = (0, 105, 148)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shark.io")
clock = pygame.time.Clock()

# Chargement des assets
def load_image(path, width, height):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (width, height))

shark_img = load_image("assets/shark.png", 80, 50)
shark_rect = shark_img.get_rect(center=(400, 450))

# Groupes
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Score
score = 0
font = pygame.font.Font(None, 36)

# Sons
try:
    collect_sound = pygame.mixer.Sound("assets/sounds/collect.wav")
    hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
except:
    print("Avertissement : Sons non chargés")

# Fonction pour spawn des objets
def spawn_objects():
    # Spawn aléatoire d'obstacles/collectibles
    if random.random() < 0.02:  # 2% de chance par frame
        obstacles.add(Avion(SCREEN_WIDTH, SCREEN_HEIGHT))
    
    if random.random() < 0.03:
        collectibles.add(
            Mouette(SCREEN_WIDTH, random.randint(100, 200)) 
            if random.choice([True, False]) else
            Humain(SCREEN_WIDTH, random.randint(400, 500))
)

# Rochers fixes
for x in [200, 400, 600]:
    rock = Roche(x, SCREEN_HEIGHT)
    obstacles.add(rock)
    all_sprites.add(rock)

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Mouvement du requin
    keys = pygame.key.get_pressed()
    shark_rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
    shark_rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5
    
    # Contrôle des limites
    shark_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Spawn et mise à jour des objets
    spawn_objects()
    obstacles.update()
    collectibles.update()
    
    # Collisions
    for obstacle in obstacles:
        if shark_rect.colliderect(obstacle.rect):
            if isinstance(obstacle, Avion):
                score = max(0, score - 1)
                hit_sound.play()
                obstacle.kill()
    
    for collectible in collectibles:
        if shark_rect.colliderect(collectible.rect):
            score += collectible.points
            collect_sound.play()
            collectible.kill()
    
    # Affichage
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, OCEAN_BLUE, (0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2))
    
    all_sprites.draw(screen)
    obstacles.draw(screen)
    collectibles.draw(screen)
    screen.blit(shark_img, shark_rect)
    
    # Affichage du score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()