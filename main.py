import pygame

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

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
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self):
        mouse_y = pygame.mouse.get_pos()[1]
        self.rect.y = mouse_y - self.rect.height / 2

        # Boundary checking
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class OpponentPaddle(Paddle):
    def move(self, ball):
        if self.rect.centery < ball.rect.centery:
            self.rect.y += self.speed
        if self.rect.centery > ball.rect.centery:
            self.rect.y -= self.speed

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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.player_score = 0
        self.opponent_score = 0

        self.player_paddle = Paddle(
            SCREEN_WIDTH - PADDLE_WIDTH * 2,
            SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_SPEED,
        )
        self.opponent_paddle = OpponentPaddle(
            PADDLE_WIDTH,
            SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            OPPONENT_SPEED,
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
            self.opponent_paddle.move(self.ball)

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
    game = Game()
    game.run()
