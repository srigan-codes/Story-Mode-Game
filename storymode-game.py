import pygame
import time

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
stage = 1
heart = 3
complete = 0

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WORLD_MAP = [
    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 's', ' ', ' ', ' ', ' ', ' ', 'sk', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'p', 'x'],
    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
]

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.camera = pygame.math.Vector2(0, 0)
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites])
                if col == 's':
                    self.skele = NPC1((x, y), [self.visible_sprites])
                if col == 'v':
                    self.vamp = NPC2((x, y), [self.visible_sprites])
                if col == 'sk':
                    self.skull = NPC3((x, y), [self.visible_sprites])
                if col == ' ':
                    back((x, y), [self.visible_sprites])

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()

        self.camera = pygame.math.Vector2(-self.player.rect.x + WIDTH / 2, -self.player.rect.y + HEIGHT / 2)

        for sprite in self.visible_sprites:
            sprite.rect.x += self.camera.x
            sprite.rect.y += self.camera.y

class back(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load("assets/back.png").convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft=pos)

class NPC1(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.ani_list = [
            pygame.transform.scale(pygame.image.load("assets/skele/move1.png").convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load("assets/skele/move2.png").convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load("assets/skele/move3.png").convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load("assets/skele/move4.png").convert_alpha(), (64, 64)),
        ]
        self.frame = 0
        self.image = self.ani_list[self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.frame_change_delay = 7
        self.collided = False

    def input(self, player_rect):
        global heart, complete
        if self.rect.colliderect(player_rect) and not self.collided:
            print('YOU: Hey Skeleton, did you know I lost my job because of the recession?')
            time.sleep(0.8)
            print("SKELETON: What is a recession?")
            time.sleep(0.8)
            print("YOU: A recession is a significant, widespread, and prolonged downturn in economic activity. A common rule of thumb is that two consecutive quarters of negative gross domestic product (GDP) growth mean recession, although more complex formulas are also used.")
            time.sleep(1.5)

            question = input("SKELETON: Do you want to talk about it? (y/n): ").lower()
            if question == "y":
                complete += 1
                print("SKELETON: That's very mature of you. When problems like this occur, it's important to consult a loved one.")
                time.sleep(0.8)
                print("YOU: Thank you Skeleton, I feel a lot better.")
            elif question == 'n':
                heart -= 1
                complete += 1
                time.sleep(0.8)
                print("SKELETON: are you sure?")
                time.sleep(0.8)
                print("YOU: I'm just going to go to the bar...")

            self.collided = True

class NPC2(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.ani_list = [
            pygame.transform.scale(pygame.image.load("assets/vamp/move1.png").convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load("assets/vamp/move2.png").convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load("assets/vamp/move3.png").convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load("assets/vamp/move4.png").convert_alpha(), (64, 64)),
        ]
        self.frame = 0
        self.image = self.ani_list[self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.frame_change_delay = 7
        self.collided2 = False

    def input(self, player_rect):
        global heart, complete
        if self.rect.colliderect(player_rect) and not self.collided2:
            print('YOU: Hey Vampire, I heard a lot of people are losing their houses due to this recession.')
            time.sleep(0.8)
            print("VAMPIRE: Oh really? I heard nationally, new housing starts dropped to 118,000 from an average of existing homes fell by 40% from their peak. The national resale price for a house dropped by 9.5% fell by 3.5%.")
            time.sleep(0.8)
            print("YOU: Damn, that's quite scary, I'm feeling really stressed out right now.")
            time.sleep(1.5)

            question = input("VAMPIRE: Do you need any help? (y/n): ").lower()
            if question == "y":
                complete += 1
                print("VAMPIRE: That's great, I can try and find you a job that can help ends meet.")
                time.sleep(0.8)
                print("YOU: Really, that would mean a lot to me. I used to be a Real Estate Agent, but I got fired due to the recession. Thank you for this opportunity.")
            elif question == 'n':
                heart -= 1
                complete += 1
                print("VAMPIRE: Alright, if anything my doors are open.")
                time.sleep(0.8)
                print("YOU: It's okay. I'll figure it out.")

            self.collided2 = True

class NPC3(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.ani_list = [
            pygame.transform.scale(pygame.image.load("assets/skully/move1.png").convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load("assets/skully/move2.png").convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load("assets/skully/move3.png").convert_alpha(), (64, 64)),
            pygame.transform.scale(pygame.image.load("assets/skully/move4.png").convert_alpha(), (64, 64)),
        ]
        self.frame = 0
        self.image = self.ani_list[self.frame]
       
