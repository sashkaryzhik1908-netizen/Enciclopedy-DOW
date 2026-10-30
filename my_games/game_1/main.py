import pygame

pygame.init()

from random import choice, randint


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = choice(['blue', 'red', 'orange', 'purple'])

# Цвет змейки
SNAKE_COLOR = choice(['white', 'yellow', 'green'])

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Отрисовывает игровой объект на экране."""
        pass


class Apple(GameObject):
    """Класс обычного яблока."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake):
        """Выбирает случайную позицию для яблока, не занятую змейкой."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)

            if position not in snake.positions:
                self.position = position
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class ToxicApple(GameObject):
    """Класс ядовитого яблока."""

    def __init__(self):
        super().__init__()

    def randomize_color(self):
        """Выбирает ядовитому яблоку случайный цвет."""
        self.body_color = choice(
            ['blue', 'red', 'green', 'yellow', 'orange', 'purple'])
        return self.body_color

    def randomize_position(self, apple, snake):
        """Выбирает случайную позицию для ядовитого яблока"""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)

            if (position not in snake.positions
                    and position != apple.position):
                self.position = position
                break

    def draw(self):
        """Отрисовывает ядовитое яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.randomize_color(), rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last_positions = []
        self.speed = SPEED

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple, toxic_apple):
        """Перемещает змейку на одну клетку игрового поля."""
        self.update_direction()
        x, y = self.get_head_position()
        dx, dy = self.direction
        x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.last_positions.append(self.positions.pop())
        if self.positions[0] in self.positions[1:]:
            self.reset(apple, toxic_apple)

    def reset(self, apple, toxic_apple):
        """сбрасывает состояние игры к началу"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.speed = SPEED
        self.last_positions.clear()
        apple.randomize_position(self)
        toxic_apple.randomize_position(apple, self)
        screen.fill(BOARD_BACKGROUND_COLOR)

    def eat(self, apple, toxic_apple):
        """Обрабатывает столкновение змейки с яблоками."""
        if apple.position == self.positions[0]:
            apple.randomize_position(self)
            self.length += 1

            if self.length % 3 == 0:
                self.speed += 1

        if toxic_apple.position == self.positions[0]:
            toxic_apple.randomize_position(apple, self)

            if self.length == 1:
                self.reset(apple, toxic_apple)
                return

            self.length -= 1
            self.last_positions.append(self.positions.pop(-1))

    def draw(self):
        """Отрисовывает змейку и удаляет старые сегменты с экрана."""
        for position in self.last_positions:
            last_rect = pygame.Rect(
                position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        self.last_positions.clear()

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)


def main():
    """Запускает игру и управляет игровым циклом."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake)
    toxic_apple = ToxicApple()
    toxic_apple.randomize_position(apple, snake)

    game = True
    while game:

        handle_keys(snake)
        snake.move(apple, toxic_apple)
        snake.eat(apple, toxic_apple)

        snake.draw()
        apple.draw()
        toxic_apple.draw()

        pygame.display.update()

        clock.tick(snake.speed)


if __name__ == '__main__':
    main()
