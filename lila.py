import platform
import subprocess
import sys

def install_pygame():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("Библиотека Pygame успешно установлена.")
    except Exception as e:
        print(f"Произошла ошибка при установке Pygame: {e}")

def windows_code():
    print("Вы используете Windows.")

def mac_code():
    try:
        # Попробуйте импортировать pygame, чтобы проверить, установлена ли она уже
        import pygame
        print("Библиотека Pygame уже установлена.")
    except ImportError:
        # Если pygame не установлена, выполните установку с помощью pip
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            print("Библиотека Pygame успешно установлена.")
        except Exception as e:
            print("Произошла ошибка при установке Pygame:", str(e))

# Получаем имя операционной системы
os_name = platform.system()

# Выполняем соответствующий код в зависимости от операционной системы
if os_name == "Windows":
    windows_code()
elif os_name == "Darwin":
    mac_code()
else:
    print("Неизвестная операционная система.")


import pygame
import random

# Ініцыялізацыя Pygame
pygame.init()

# Памеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Колеры
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Памер блока
BLOCK_SIZE = 30

# Ініцыялізацыя экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Тэтрыс")

# Затрымка абнаўлення
clock = pygame.time.Clock()
FPS = 10  # Зменшаная затрымка абнаўлення для замедлення падымання блокаў

# Клас блока
class Block:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def draw(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (self.x + j * BLOCK_SIZE, self.y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        # Паварот блока на 90 градусаў
        self.shape = list(zip(*self.shape[::-1]))

    def smooth_rotate(self):
        temp_shape = list(zip(*self.shape[::-1]))
        new_shape = []
        for row in temp_shape:
            new_shape.append(list(row))
        self.shape = new_shape

# Клас гульні
class Game:
    def __init__(self):
        self.score = 0
        self.grid = [[BLACK] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_block = self.generate_block()
        self.fall_count = 0  # Лічыльнік для вызначэння хуткасці падымання блока
        self.rotation_count = 0  # Лічыльнік для плавнага павароту блока
        self.rotation_delay = 5  # Затрымка перад наступным паваротам блока

    def generate_block(self):
        shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 1], [0, 1, 0]]
        ]
        shape = random.choice(shapes)
        x = (SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2) * BLOCK_SIZE
        y = 0
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        return Block(x, y, shape, color)

    def check_collision(self):
        for i in range(len(self.current_block.shape)):
            for j in range(len(self.current_block.shape[0])):
                if (
                    self.current_block.shape[i][j] == 1 and
                    (self.current_block.y // BLOCK_SIZE + i >= len(self.grid) or
                     self.current_block.x // BLOCK_SIZE + j < 0 or
                     self.current_block.x // BLOCK_SIZE + j >= len(self.grid[0]) or
                     self.grid[self.current_block.y // BLOCK_SIZE + i][self.current_block.x // BLOCK_SIZE + j] != BLACK)
                ):
                    return True
        return False

    def lock_block(self):
        for i in range(len(self.current_block.shape)):
            for j in range(len(self.current_block.shape[0])):
                if self.current_block.shape[i][j] == 1:
                    self.grid[self.current_block.y // BLOCK_SIZE + i][self.current_block.x // BLOCK_SIZE + j] = self.current_block.color

        full_rows = []
        for i in range(len(self.grid)):
            if BLACK not in self.grid[i]:
                full_rows.append(i)

        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [BLACK] * (SCREEN_WIDTH // BLOCK_SIZE))

        self.score += len(full_rows) * 10
        self.current_block = self.generate_block()

        if self.check_collision():
            # Гульня скончана
            pygame.quit()
            quit()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.current_block.move(-BLOCK_SIZE, 0)
            if self.check_collision():
                self.current_block.move(BLOCK_SIZE, 0)  # Адмяніць рух, калі ўзнікае калізія

        if keys[pygame.K_RIGHT]:
            self.current_block.move(BLOCK_SIZE, 0)
            if self.check_collision():
                self.current_block.move(-BLOCK_SIZE, 0)  # Адмяніць рух, калі ўзнікае калізія

        if keys[pygame.K_DOWN]:
            self.current_block.move(0, BLOCK_SIZE)
            if self.check_collision():
                self.current_block.move(0, -BLOCK_SIZE)  # Адмяніць рух, калі ўзнікае калізія

        if keys[pygame.K_UP]:
            if self.rotation_count >= self.rotation_delay:  # Праверка затрымкі перад наступным паваротам
                self.current_block.rotate()
                if self.check_collision():
                    self.current_block.rotate()  # Адмяніць паварот, калі ўзнікае калізія
                self.rotation_count = 0  # Скід лічыльніка пасля павароту
        else:
            self.rotation_count += 1

    def update(self):
        # Праверка лічыльніка для замедлення падымання блока
        if self.fall_count == FPS // 2:  # Змяншэнне хуткасці падымання блока напаловіну
            self.current_block.move(0, BLOCK_SIZE)
            if self.check_collision():
                self.current_block.move(0, -BLOCK_SIZE)  # Адмяніць рух, калі ўзнікае калізія
                self.lock_block()
                if self.check_collision():  # Праверка на сканчэнне гульні
                    pygame.quit()
                    quit()  # Выхад з гульні
            self.fall_count = 0
        else:
            self.fall_count += 1

    def draw(self):
        screen.fill(BLACK)

        self.current_block.draw()

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                pygame.draw.rect(screen, self.grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        font = pygame.font.Font(None, 36)
        text_surface = font.render("Score: " + str(self.score), True, WHITE)
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()
            self.update()
            self.draw()

            clock.tick(FPS)

        pygame.quit()
        quit()

# Запуск гульні
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
