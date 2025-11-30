import pygame
import logging

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 140

BALL_SIZE = 20

PADDLE_SPEED = 10
OPPONENT_SPEED = 7

BALL_SPEED_X = 8
BALL_SPEED_Y = 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Paddle class
class Paddle:
    def __init__(self, x, y, width, height, speed, joystick, axis_index=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.joystick = joystick
        self.axis_index = axis_index

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self):
        axis_value = self.joystick.get_axis(self.axis_index)
        self.rect.y += self.speed * axis_value

        # Boundary checking
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Ball class
class Ball:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def move(self, player_paddle, opponent_paddle):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Collision with top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        # Collision with paddles
        if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(
            opponent_paddle.rect
        ):
            self.speed_x *= -1

    def reset(self):
        self.rect.x = SCREEN_WIDTH / 2 - self.rect.width / 2
        self.rect.y = SCREEN_HEIGHT / 2 - self.rect.height / 2
        self.speed_x *= -1


class Game:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [
            pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
        ]
        if not self.joysticks:
            raise RuntimeError("No joysticks found.")

        for joystick in self.joysticks:
            joystick.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.player_score = 0
        self.opponent_score = 0

        joystick1 = self.joysticks[0]

        right_axis = 3 if joystick1.get_numaxes() >= 4 else 1

        self.player_paddle = Paddle(
            SCREEN_WIDTH - PADDLE_WIDTH * 2,
            SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_SPEED,
            joystick=joystick1,
            axis_index=right_axis,
        )
        self.opponent_paddle = Paddle(
            PADDLE_WIDTH,
            SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_SPEED,
            joystick=joystick1,
            axis_index=1,
        )
        self.ball = Ball(
            SCREEN_WIDTH / 2 - BALL_SIZE / 2,
            SCREEN_HEIGHT / 2 - BALL_SIZE / 2,
            BALL_SIZE,
            BALL_SPEED_X,
            BALL_SPEED_Y,
        )

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.ball.move(self.player_paddle, self.opponent_paddle)
            self.player_paddle.move()
            self.opponent_paddle.move()

            if self.ball.rect.left <= 0:
                self.player_score += 1
                self.ball.reset()
            if self.ball.rect.right >= SCREEN_WIDTH:
                self.opponent_score += 1
                self.ball.reset()

            self.screen.fill(BLACK)
            self.player_paddle.draw(self.screen)
            self.opponent_paddle.draw(self.screen)
            self.ball.draw(self.screen)

            player_text = self.font.render(str(self.player_score), True, WHITE)
            self.screen.blit(player_text, (SCREEN_WIDTH / 2 + 50, 20))
            opponent_text = self.font.render(str(self.opponent_score), True, WHITE)
            self.screen.blit(opponent_text, (SCREEN_WIDTH / 2 - 100, 20))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    logging.basicConfig(
        filename="pypong.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    try:
        Game().run()
    except RuntimeError as e:
        logging.error(e)
