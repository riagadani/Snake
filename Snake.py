import pygame
import time
import random
 
class Block:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        #0 for up, 1 for right, 2 for down, 3 for left

class Snake:
    def __init__(self):
        self.snake = [Block(0,0,1)]
        self.speed = 10
    def moveRight(self):
        if self.snake[0].direction != 3:
            self.snake[0].direction = 1
    def moveLeft(self):
        if self.snake[0].direction != 1:
            self.snake[0].direction = 3
    def moveUp(self):
        if self.snake[0].direction != 2:
            self.snake[0].direction = 0
    def moveDown(self):
        if self.snake[0].direction != 0:
            self.snake[0].direction = 2
    def move(self):
        prev = self.snake[0].direction  
        for block in self.snake:
            if block.direction == 0:
                block.y = block.y - self.speed
            if block.direction == 1:
                block.x = block.x + self.speed
            if block.direction == 2:
                block.y = block.y + self.speed           
            if block.direction == 3:
                block.x = block.x - self.speed
            temp = block.direction
            block.direction = prev
            prev = temp
    def check(self):
        head = self.snake[0]
        for i in range(1, len(self.snake)):
            if head.x == self.snake[i].x and head.y == self.snake[i].y:
                return False
        return True
    def draw(self, surface, image):
        for block in self.snake:
            surface.blit(image,(block.x,block.y))
    
    def eat(self, apple, score):
        block = self.snake[0]
        last_block = self.snake[len(self.snake)-1]
        if block.x == apple.x and block.y == apple.y:
            apple.move()
            direction = block.direction
            if direction == 0:
                self.snake.append(Block(last_block.x, last_block.y + 10, direction))
            if direction == 1:
                self.snake.append(Block(last_block.x - 10, last_block.y, direction))
            if direction == 2:
                self.snake.append(Block(last_block.x, last_block.y - 10, direction))
            if direction == 3:
                self.snake.append(Block(last_block.x + 10, last_block.y, direction))
            return score + 1
        return score


class Apple():
    def __init__(self):
        self.x = random.randint(0,79)*10
        self.y = random.randint(0,59)*10
    def move(self):
        self.x = random.randint(0,79)*10
        self.y = random.randint(0,59)*10
    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class App():
    window = width, height = 800, 600
    player = 0
    def __init__(self):
        self.running = True
        self.display_surf = None
        self.image_surf = None
        self.apple_image = None
        self.player = Snake()
        self.apple = Apple()
        self.score = 0

    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.display_surf = pygame.display.set_mode(self.window)
        pygame.display.set_caption("Snake")
        self.running = True
        self.image_surf = pygame.image.load("snake.png").convert()
        self.apple_image = pygame.image.load("apple.png").convert()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.on_cleanup()
        if self.running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.moveRight()
                if event.key == pygame.K_LEFT:
                    self.player.moveLeft()
                if event.key == pygame.K_UP:
                    self.player.moveUp()
                if event.key == pygame.K_DOWN:
                    self.player.moveDown()
        if not self.running:
            self.running = True
            self.display_surf = None
            self.image_surf = None
            self.apple_image = None
            self.player = Snake()
            self.apple = Apple()
            self.score = 0
            self.on_init()
            self.on_execute()

    
    def on_loop(self):
        self.player.move()
        block = self.player.snake[0]
        if block.x < 0 or block.x > 790 or block.y < 0 or block.y > 590:
            self.running = False
        pass

    def on_render(self):
        self.display_surf.fill((0,0,0))
        self.player.draw(self.display_surf, self.image_surf)
        self.apple.draw(self.display_surf, self.apple_image)
        self.print_score()
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
    def print_score(self):
        white = (255,255,255)
        black = (0,0,0)
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render("Your score is: " + str(self.score), True, white)
        textRect = text.get_rect()
        textRect.center = (100, 10)
        self.display_surf.blit(text, textRect)
        pygame.display.update()
    
    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        while self.running:
            pygame.event.pump()
            for event in pygame.event.get():
                self.on_event(event)
            self.score = self.player.eat(self.apple, self.score)
            if not self.player.check():
                self.running = False
            self.on_loop()
            self.on_render()
            time.sleep(.1)
        while not self.running:
            pygame.event.pump()
            for event in pygame.event.get():
                self.on_event(event)
            white = (255,255,255)
            self.display_surf.fill((0,0,0))
            font = pygame.font.Font("freesansbold.ttf", 20)
            text = font.render("You lose. Press any key to retry", True, white)
            textRect = text.get_rect()
            textRect.center = (400,300)
            self.display_surf.blit(text, textRect)
            pygame.display.update()

        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
