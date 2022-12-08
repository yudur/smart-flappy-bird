import pygame
import os
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

PICTURE_OF_THE_BARREL = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
FLOOR_PICTURE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
PICTURES_OF_THE_BIRD = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

pygame.font.init()
SOURCE_POINTS = pygame.font.SysFont('arial', 50)

class Bird:
    IMGS = PICTURES_OF_THE_BIRD
    # rotation animations
    MAXIMUM_ROTATION = 25
    ROTATION_SPEED = 20
    ANIMATION_TIME = 5

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.height = self.y
        self.width = self.x
        self.time = 0
        self.image_count = 0
        self.image = self.IMGS[0]

    def jump(self) -> None:
        self.velocity = -10.5
        self.time = 0
        self.height = self.y

    def to_move(self) -> None:
        # calculate the displacement
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.velocity * self.time

        # restrict displacement
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # the angle of the bird
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAXIMUM_ROTATION:
                self.angle = self.MAXIMUM_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED

    def to_draw(self, screen):
        # define which image the bird will use
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_count < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        elif self.image_count < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME*4 + 1:
            self.image = self.IMGS[0]
            self.image_count = 0

        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.image, self.angle)
        image_center_position = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=image_center_position)
        screen.blit(rotated_image, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self, x: int) -> None:
        self.x = x
        self.heigth = 0
        self.top_position = 0
        self.base_position = 0
        self.TOP_BARREL = pygame.transform.flip(PICTURE_OF_THE_BARREL, False, True)
        self.BASE_HAPE = PICTURE_OF_THE_BARREL
        self.passed_on = False
        self.set_height()
        
    def set_height(self) -> None:
        self.heigth = random.randrange(50, 450)
        self.top_position = self.heigth - self.TOP_BARREL.get_height()
        self.base_position = self.heigth + self.DISTANCE
        
    def to_move(self):
        self.x -= self.SPEED

    def to_draw(self, screen):
        screen.blit(self.TOP_BARREL, (self.x, self.top_position))
        screen.blit(self.BASE_HAPE, (self.x, self.base_position))
        
    def collide(self, bird) -> bool:
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_BARREL)
        base_mask = pygame.mask.from_surface(self.BASE_HAPE)

        distance_from_the_top = (self.x - bird.x, self.top_position - round(bird.y))
        distance_from_the_base = (self.x - bird.x, self.base_position - round(bird.y))

        top_collision_point = bird_mask.overlap(top_mask, distance_from_the_top)
        base_collision_point = bird_mask.overlap(base_mask, distance_from_the_base)

        if top_collision_point or base_collision_point:
            return True
        else:
            return False


class Floor:
    SPEED = 5
    WIDTH = FLOOR_PICTURE.get_width()
    IMAGE = FLOOR_PICTURE

    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def to_move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 +self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def to_draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))


def draw_screen(screen, birds, pipes, floor, spots):
    screen.blit(BACKGROUND_IMAGE, (0,0))
    
    for bird in birds:
        bird.to_draw(screen)
    for pipe in pipes:
        pipe.to_draw(screen)

    text = SOURCE_POINTS.render(f'Pontuação: {spots}', 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    floor.to_draw(screen)
    pygame.display.update()

def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    spots = 0
    watch = pygame.time.Clock()

    running = True
    while running:
        watch.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()
        
        for bird in birds:
            bird.to_move()
        floor.to_move()

        add_pipe = False
        remove_pipes = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    bird.pop(i)
                if not pipe.passed_on and bird.x > pipe.x:
                    pipe.passed_on = True
                    add_pipe = True
            pipe.to_move()
            if pipe.x + pipe.TOP_BARREL.get_width() < 0:
                remove_pipes.append(pipe)
        
        if add_pipe:
            spots += 1
            pipes.append(Pipe(600))
        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if(bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, spots)


if __name__ == "__main__":
    main()