import pygame

# some colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

pygame.init()

# screen dimensions
size = (1920, 1080)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Block Physics Sandbox')

# loop until close
done = False

# screen updates (for readability)
clock = pygame.time.Clock()

# font
font = pygame.font.SysFont('comicsansms', 58)

# collisions global
collisions = 0

class Block(pygame.sprite.Sprite):
    # Initialise the Super's (Sprite's) Attributes & Methods
    def __init__(self, x, y, mass, colour, name):
        super().__init__()

        # Creating the image of the object
        self.width = 50
        self.height = 50
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()

        # X & Y Positions
        self.rect.x = x
        self.rect.y = y

        # Horisontal & Vertical Velocity
        self.velocity = 0

        # Misc.
        self.mass = mass
        self.other = None
        self.name = name
        self.wallCollided = False

    def stopClipping(self):
        if self.name == 'red':
            self.rect.left = self.otherBlock.rect.right
        else:
            self.rect.right = self.otherBlock.rect.left


    # Call to draw movements on screen
    def update(self):
        global collisions

        # Apply movement
        self.rect.x += self.velocity

        # Collision with sides of screen
        for block in blocksList:
            if block.rect.left < 0:
                block.rect.left = 0
                block.velocity *= -1
                collisions += 1

        # i have to hard code stops in clipping because pygame is terrible for this specific project
        if self.name == 'green':
            if self.rect.left > self.otherBlock.rect.right:
                self.rect.left = self.otherBlock.rect.right




    # Collisions in one dimension
    # Because there is only an x and no y I can purely focus on checking their raw positions in space
    # My last iteration of this code prepared for all possible cases but this just focuses on the task at hand
    def collide(self):
        if self.rect.x + self.width < self.otherBlock.rect.x \
                or self.rect.x > self.otherBlock.rect.x + self.otherBlock.width:
            return False
        else:
            return True

    # The bounce function
    # This and the colisions are now made for any block but I call them only for one block to avoid confusion and minute
    # errors.
    def bounce(self):
        # Formula Taken from Wikipedia: https://en.wikipedia.org/wiki/Momentum
        o = self.otherBlock # Shorthand so the code looks less cluttered
        sumMasses = self.mass + o.mass # Sum of masses comes up quite a bit
        newVelocity = (self.mass - o.mass)/sumMasses * self.velocity
        newVelocity += ((2*o.mass)/sumMasses) * o.velocity
        return newVelocity




# Object Initialization
blocksList = pygame.sprite.Group()
blockHitlist = pygame.sprite.Group()

# Position X, Position Y, Mass, Colour, Identifier for Debugging
block = Block(400, 400, 10000, red, 'red')
block2 = Block( 100, 400, 1, green, 'green')
blocksList.add(block)
blocksList.add(block2)
block.otherBlock = block2
block2.otherBlock = block

# program loop
while not done:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                block.velocity = -
            if event.key == pygame.K_d:
                block.velocity = 1

    # game logic

    # screen clearing code
    screen.fill(white)

    # drawing code
    blocksList.update()
    if block.collide():
        print(True)
        block.stopClipping()
        newVelocity1 = block.bounce()
        newVelocity2 = block2.bounce()
        block.velocity = newVelocity1
        block2.velocity = newVelocity2
        collisions += 1
    blocksList.draw(screen)
    screen.blit(font.render(str(collisions) + ' collisions', False, black), [100, 100])
    screen.blit(font.render('ratio: ' + str(block2.mass) + ':' + str(block.mass), False, black), [100, 50])

    # update display
    pygame.display.flip()

    # 60 frames
    clock.tick(1000)

# close window and quit
pygame.quit()