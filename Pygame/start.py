import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 700, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basketball Stars")

BLAKY = (0, 0, 1)
BLACK = (0, 0, 0)
TOP = (255, 0, 0)
BOTTOM = (255, 255, 0)

BORDER = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 10)

#HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 40)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
CHARACTER_WIDTH, CHARACTER_HEIGHT = 135, 120

BOTTOM_HIT = pygame.USEREVENT + 1
TOP_HIT = pygame.USEREVENT + 2

JAMES1 = pygame.image.load(
    os.path.join("pictures", "lejames.png"))
JAMESone = pygame.transform.scale(JAMES1, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
HARDEN1 = pygame.image.load(
    os.path.join("pictures", "harden.png"))
HARDENone = pygame.transform.scale(HARDEN1, (CHARACTER_WIDTH, CHARACTER_HEIGHT)) 

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("pictures", "ball court.png")), (WIDTH, HEIGHT))

def draw_window(top, bottom, top_bullets, bottom_bullets, top_health, bottom_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLAKY, BORDER)

    top_health_text = HEALTH_FONT.render("Health: " + str(top_health), 1, BLAKY)
    bottom_health_text = HEALTH_FONT.render("Health: " + str(bottom_health), 1, BLAKY)

    WIN.blit(JAMESone, (bottom.x, bottom.y))
    WIN.blit(HARDENone, (top.x, top.y))
    for bullet in top_bullets:
        pygame.draw.rect(WIN, TOP, bullet)

    for bullet in bottom_bullets:
        pygame.draw.rect(WIN, BOTTOM, bullet)
    
    pygame.display.update()
    
    
def lebron_movement(keys_pressed, bottom):
        if keys_pressed[pygame.K_LEFT] and bottom.x - VEL > 0: # LEFT
            bottom.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and bottom.x + VEL + bottom.height < 700: # RIGHT
            bottom.x += VEL
        if keys_pressed[pygame.K_UP] and bottom.y - VEL > BORDER.y: # UP
            bottom.y -= VEL
        if keys_pressed[pygame.K_DOWN] and bottom.y + VEL + bottom.width < HEIGHT: # DOWN
            bottom.y += VEL

def harden_movement(keys_pressed, top): 
        if keys_pressed[pygame.K_z] and top.x - VEL > 0: # LEFT
            top.x -= VEL
        if keys_pressed[pygame.K_c] and top.x + VEL + top.height < 700: # RIGHT
            top.x += VEL
        if keys_pressed[pygame.K_s] and top.y - VEL > 0: # UP
            top.y -= VEL
        if keys_pressed[pygame.K_x] and top.y + VEL < 380: # DOWN
            top.y += VEL

def handle_bullets(bottom_bullets, top_bullets, bottom, top):
    for bullet in bottom_bullets:
        bullet.y -= BULLET_VEL
        if top.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TOP_HIT))
            top_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            bottom_bullets.remove(bullet)
    
    for bullet in top_bullets:
        bullet.y += BULLET_VEL
        if bottom.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BOTTOM_HIT))
            bottom_bullets.remove(bullet)
        elif bullet.x < 0:
            top_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLAKY)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    top = pygame.Rect(290, 20, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    bottom = pygame.Rect(290, 820, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    
    top_bullets = []
    bottom_bullets = []

    top_health = 10
    bottom_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bottom_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(bottom.x + bottom.width, bottom.y + bottom.height//2 - 2, 10, 5)
                    bottom_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(top_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(top.x, top.y + top.height//2 - 2, 10, 5)
                    top_bullets.append(bullet)

            if event.type == TOP_HIT:
                top_health -= 1
        
            if event.type == BOTTOM_HIT:
                bottom_health -= 1

        winner_text = ""
        if top_health <= 0:
            winner_text = "LeBron dubbed it"

        if bottom_health <= 0:
            winner_text = "Harden won. It's all good tho he can't do it in the playoffs."
    
        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        lebron_movement(keys_pressed, bottom)
        harden_movement(keys_pressed, top)

        handle_bullets(bottom_bullets, top_bullets, bottom, top)
        
        draw_window(top, bottom, top_bullets, bottom_bullets, top_health, bottom_health)

   

    main()

if __name__ == "__main__":
    main()
