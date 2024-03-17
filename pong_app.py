# from app import app
import time
from lis2hh12_accel import LIS2HH12
import neopixel
from adafruit_ssd1306 import SSD1306_I2C
from audiobusio import I2SOut

from buttons import Buttons
from display import Display
from app_base import AppBase


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)


MARGIN_MIN = Point(0, 0)
MARGIN_MAX = Point(128, 32)
WINNING_POINTS = 3

PLAYER_COLORS = [(0, 64, 0), (0, 0, 64)]


# Return true if line segments AB and CD intersect
# Source: https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def intersect(A, B, C, D):
    def ccw(A, B, C):
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def move_dim(x0: float, dx: float, length: float, margin: float) -> Tuple(float, bool):
    collision = False
    x0n = x0 + dx
    if dx < 0:
        if x0n <= 0:
            collision = True
            dx = x0
    elif dx > 0:
        x1n = x0n + length
        if x1n >= margin:
            collision = True
            dx = margin - x0 - length
    return (x0 + dx, collision)


class Paddle:
    def __init__(self, center: Point) -> None:
        self.center = center
        self.width = 1
        self.height = 3
        self.velocity = Point(0, 0)

    def get_origin(self) -> Point:
        x0 = 0.5 + self.center.x - self.width / 2
        y0 = 0.5 + self.center.y - self.height / 2
        return Point(x0, y0)

    def move(self, dt: float) -> bool:
        assert self.velocity.x == 0, "Not supported"
        dy = self.velocity.y * dt

        origin = self.get_origin()
        # (x0n, collision_x ) = move_dim(origin.x,dx,self.width, MARGIN_MAX.x)
        (y0n, collision_y) = move_dim(origin.y, dy, self.height, MARGIN_MAX.y)
        self.center.y = y0n + self.height / 2 - 0.5
        return collision_y

    def render(self, display: SSD1306_I2C) -> None:
        p0 = self.get_origin()
        display.fill_rect(int(p0.x), int(p0.y), self.width, self.height, 1)


class Ball:
    def __init__(self, center: Point) -> None:
        self.center = center
        self.velocity = Point(0, 0)

    def move(self, dt: float) -> Tuple(bool, bool):
        dx = self.velocity.x * dt
        dy = self.velocity.y * dt

        (x0n, collision_x) = move_dim(self.center.x, dx, 1, MARGIN_MAX.x)
        (y0n, collision_y) = move_dim(self.center.y, dy, 1, MARGIN_MAX.y)
        self.center.x = x0n
        self.center.y = y0n
        return collision_x, collision_y

    def render(self, display: SSD1306_I2C) -> None:
        p0 = self.center
        display.fill_rect(int(p0.x), int(p0.y), 1, 1, 1)


class PongApp(AppBase):
    def __init__(
        self,
        accelorometer: LIS2HH12,
        audio: I2SOut,
        buttons: Buttons,
        pixels: neopixel.NeoPixel,
        display: SSD1306_I2C,
    ) -> None:
        self.accelerometer = accelorometer
        self.audio = audio
        self.buttons = buttons
        self.pixels = pixels
        self.display = display

        self.paddles = [Paddle(Point(5, 16)), Paddle(Point(120, 16))]
        self.paddles[0].velocity.y = 20
        self.paddles[1].velocity.y = 30

        self.paddles[0].height = 15
        self.paddles[1].height = 15

        self.ball = Ball(Point(10, 10))
        self.ball.velocity = Point(50, -20)

        self.points = [0, 0]
        self.winner = None

    def check_inputs(self) -> None:
        if self.buttons.A_pressed:
            self.paddles[0].velocity.y *= -1
        if self.buttons.B_pressed:
            self.paddles[1].velocity.y *= -1

    def check_paddle_collision(self, paddle: Paddle, old_ball_center: Point) -> bool:
        paddle_top = Point(paddle.center.x, paddle.center.y - paddle.height / 2)
        paddle_bottom = Point(paddle.center.x, paddle_top.y + paddle.height)
        return intersect(old_ball_center, self.ball.center, paddle_top, paddle_bottom)

    def animate(self, dt: float) -> None:
        if self.winner is not None:
            return

        for paddle in self.paddles:
            if paddle.move(dt):
                paddle.velocity.y *= -1

        old_ball_center = self.ball.center.copy()
        (wall_collision_x, wall_collision_y) = self.ball.move(dt)

        # Check for collision with paddles
        if self.ball.velocity.x < 0:
            relevant_paddle = self.paddles[0]
        else:
            relevant_paddle = self.paddles[1]
        paddle_collision = self.check_paddle_collision(relevant_paddle, old_ball_center)
        if paddle_collision:
            wall_collision_x = False
            self.ball.velocity.x *= -1
            self.ball.center.x = relevant_paddle.center.x + dt * self.ball.velocity.x

        # Check for collision with walls
        if wall_collision_x:
            # Score points on x collision!
            if self.ball.velocity.x > 0:
                self.points[1] += 1
                if self.points[1] > WINNING_POINTS:
                    self.winner = 1
            else:
                self.points[0] += 1
                if self.points[0] > WINNING_POINTS:
                    self.winner = 0

            self.ball.velocity.x *= -1
        if wall_collision_y:
            self.ball.velocity.y *= -1

    def render(self) -> None:
        self.display.fill(0)
        for paddle in self.paddles:
            paddle.render(self.display)
        self.ball.render(self.display)
        self.display.show()

        # Points
        if self.winner is not None:
            now = time.monotonic()
            if int(now) % 2 == 0:
                self.pixels.fill(PLAYER_COLORS[self.winner])
            else:
                self.pixels.fill((0, 0, 0))
        else:
            self.pixels.fill((0, 0, 0))
            for i in range(self.points[0]):
                self.pixels[i] = PLAYER_COLORS[0]
            for i in range(self.points[1]):
                self.pixels[16 - i] = PLAYER_COLORS[1]

    def update(self, dt: float) -> None:
        self.check_inputs()
        self.animate(dt)
        self.render()

    def exit(self) -> None:
        pass
