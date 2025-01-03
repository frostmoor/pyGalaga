import pygame
import random

# 3. 에너지 개념 및 충돌 이벤트 추가
# 에너지 10이 0이되면 게임오버.

# Pygame 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galaga")

# 플레이어 클래스 정의
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 50
        self.speed_x = 0
        self.energy = 10  # 에너지 추가

    def update(self):
        self.rect.x += self.speed_x
        # 화면 경계 확인
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

    def move_left(self):
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5

    def stop(self):
        self.speed_x = 0

# 적 클래스 정의
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.speed_y = random.randint(1, 3)

# 총알 클래스 정의
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = pygame.Surface([5, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = -5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y < 0:
            self.kill()

def game_over_handler():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 74)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    font = pygame.font.SysFont(None, 36)
    text = font.render("Press R to Restart", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

# 스프라이트 그룹 생성
player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(10):
    enemy = Enemy()
    enemies.add(enemy)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemies)

# 게임 루프
running = True
clock = pygame.time.Clock()
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)
                all_sprites.add(bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.speed_x < 0:
                player.stop()
            elif event.key == pygame.K_RIGHT and player.speed_x > 0:
                player.stop()

    all_sprites.update()

    # 총알과 적 충돌 확인
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)

    # 적과 플레이어 충돌 확인
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.energy -= 1
        if player.energy <= 0:
            game_over_handler()
            # 게임 재시작
            player = Player()
            enemies.empty()
            bullets.empty()
            for i in range(10):
                enemy = Enemy()
                enemies.add(enemy)
            all_sprites.empty()
            all_sprites.add(player)
            all_sprites.add(enemies)
            score = 0

    screen.fill(BLACK)
    all_sprites.draw(screen)

    # 점수 및 에너지 표시
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))
    text = font.render(f'Energy: {player.energy}', True, WHITE)
    screen.blit(text, (10, 40))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
