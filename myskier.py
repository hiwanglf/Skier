import pygame
import random

skier_images = ["skier_down.png", "skier_right1.png", "skier_right2.png", "skier_left1.png", "skier_left2.png"]

class skierClass(pygame.sprite.Sprite):
    #创建滑雪者
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("skier_down.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320,100]
        self.angle = 0
    #滑雪者转向
    def turn(self,derection):
        self.angle = self.angle+derection
        if self.angle < -2:
            self.angle = -2
        if self.angle >2:
            self.angle = 2
        center = self.rect.center
        self.image = pygame.image.load(skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle,6-abs(self.angle)*2]
        return speed
    #滑雪者左右移动
    def move(self,speed):
        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20:
            self.rect.centerx = 20
        if self.rect.centerx > 620:
            self.rect.centerx = 620
#创建树和小旗
class obstracleClass(pygame.sprite.Sprite):
    def __init__(self,image_file,location,type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False
    #让场景向上滚动
    def update(self):
        global speed
        self.rect.centery -= speed[1]
        #删除从屏幕上方滚下的障碍物
        if self.rect.centery < -32:
            self.kill()
#创建一个窗口(地图)，包含随机的树和小旗
def create_map():
    global obstracles
    locations = []
    for i in range(10):
        row = random.randint(0,9)
        col = random.randint(0,9)
        location = [col*64+20,row*64+20+640]
        if not (location in locations):
            locations.append(location)
            type = random.choice(["tree","flag"])
            if type == "tree":
                img = "skier_tree.png"
            elif type == "flag":
                img = "skier_flag.png"
            obstracle = obstracleClass(img,location,type)
            obstracles.add(obstracle)
#重新绘制屏幕
def animate():
    screen.fill([255,255,255])
    obstracles.draw(screen)
    screen.blit(skier.image,skier.rect)
    screen.blit(score_text,[10,10])
    pygame.display.flip()
pygame.init()
screen = pygame.display.set_mode([640,640])
clock = pygame.time.Clock()
skier = skierClass()
speed = [0,6]
obstracles = pygame.sprite.Group()
map_position = 0;
points = 0
create_map()
font = pygame.font.Font(None,50)

running = True
while running:
    #美妙更新30次图形
    clock.tick(30)
    #检查按键或者窗口是否关闭；
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT:
                speed = skier.turn(1)
    #移动滑雪者
    skier.move(speed)
    #滚动场景
    map_position += speed[1]

    if map_position >=640:
        create_map()
        map_position = 0
    hit = pygame.sprite.spritecollide(skier,obstracles,False)
    if hit:
        if hit[0].type == "tree" and not hit[0].passed:
            points = points - 100
            skier.image = pygame.image.load("skier_crash.png")
            animate()
            pygame.time.delay(1000)
            skier.image = pygame.image.load("skier_down.png")
            skier.angle = 0
            speed = [0,6]
            hit[0].passed = True
        elif hit[0].type == "flag" and not hit[0].passed:
            points += 10
            hit[0].kill()
    obstracles.update()
    #显示得分
    score_text = font.render("Score: "+str(points),1,(0,0,0))
    animate()
pygame.quit()