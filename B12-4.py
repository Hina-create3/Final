import random
import pyxel
import math

class Ball:
    def __init__(self):
        self.reset()

    def update_position(self, speed):
        if self.x <= 0 or self.x >= 200:
            self.direction *= -1
        self.x += self.vx * speed * self.direction
        self.y += self.vy * speed

    def reset(self):
        self.x = random.randint(0, 199)
        self.y = 0
        angle = math.radians(random.randint(30, 150))
        self.vx = math.cos(angle)
        self.vy = math.sin(angle)
        self.direction = 1
        self.collected = False

class Pad:
    def __init__(self):
        self.x = 100
        self.width = 40
        self.height = 5

    def update_position(self):
        self.x = pyxel.mouse_x

    def check_collision(self, ball):
        if self.x - 20 <= ball.x <= self.x + 20 and ball.y >= 195 and not ball.collected:
            return True
        return False

class App:
    def __init__(self):
        pyxel.init(200, 200)
        self.balls = [Ball() for _ in range(3)]
        self.pad = Pad()
        self.speed = 5
        self.score = 0
        self.lives = 3
        self.game_over = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.restart_game()
            return

        for ball in self.balls:
            ball.update_position(self.speed)

            if self.pad.check_collision(ball):
                self.score += 1
                ball.collected = True
                pyxel.play(0, 1)
                
                if self.score % 5 == 0:
                    self.speed += 1
            elif ball.y >= 200 and not ball.collected:
                self.lives -= 1
                ball.collected = True
                if self.lives <= 0:
                    self.game_over = True
            if ball.y >= 200:
                ball.reset()

        self.pad.update_position()

    def draw(self):
        if self.game_over:
            pyxel.cls(0)
            pyxel.text(80, 90, "Game Over", pyxel.frame_count % 16)
            pyxel.text(60, 110, "Press Enter to Restart", 7)
            return

        pyxel.cls(7)
        for ball in self.balls:
            pyxel.circ(ball.x, ball.y, 10, 6)
        pyxel.rect(self.pad.x - self.pad.width // 2, 195, self.pad.width, self.pad.height, 14)
        pyxel.text(10, 10, 'Score: ' + str(self.score), 0)
        pyxel.text(10, 20, 'Lives: ' + str(self.lives), 0)

    def restart_game(self):
        self.score = 0
        self.speed = 5
        self.lives = 3
        self.game_over = False
        for ball in self.balls:
            ball.reset()

App()
