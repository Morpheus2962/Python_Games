import pygame
import os 
import time
import random
from pygame.locals import *
pygame.font.init()

restart = []
WIN_WIDTH = 500
WIN_HIEGHT = 800
FLOOR = 730

WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HIEGHT))
pygame.display.set_caption("Flappy Bird")

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
#BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png")).convert_alpha()),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png")).convert_alpha()),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")).convert_alpha())]

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))
STAT_FONT = pygame.font.SysFont("comicsans", 50)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)


class Bird:

	Max_Rotation = 25
	Imgs = BIRD_IMGS
	Rotaion_val = 20
	Animation_time = 5
	
	def __init__(self ,x,y):
		self.x = x
		self.y = y
		self.tick_count = 0
		self.height = self.y
		self.vel = 0
		self.img_count = 0
		self.img = self.Imgs[0]
		self.tilt = 0
	def jump(self):

		self.vel = -10.5
		self.tick_count = 0
		self.height = self.y

	def move(self):

		self.tick_count += 1

		displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # calculate displacement

		if displacement >= 16:
			displacement = 16
		if displacement < 0 :
			displacement -=2

		self.y = self.y + displacement

		if displacement<0 or self.y < self.height+50:
			if self.tilt < self.Max_Rotation:
				self.tilt = self.Max_Rotation
		else:
			if self.tilt >-90:
				self.tilt -= self.Rotaion_val

	def draw(self,win):

		self.img_count +=1

		if self.img_count<=self.Animation_time:
			self.img = self.Imgs[0]		
		elif self.img_count<=self.Animation_time*2:
			self.img = self.Imgs[1]
		elif self.img_count<=self.Animation_time*3:
			self.img = self.Imgs[2]
		elif self.img_count<=self.Animation_time*4:
			self.img = self.Imgs[1]
		elif self.img_count==self.Animation_time*4 +1:
			self.img = self.Imgs[0]
			self.img_count = 0

		if self.tilt <= -80:
			self.img = self.Imgs[1]
			self.img_count = self.Animation_time*2
		print(self.img_count)


		blitRotateCentre(win, self.img, (self.x, self.y), self.tilt)
		#rotated_img = pygame.transform.rotate(self.img,self.tilt)
		#new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
		#win.blit(rotated_img, new_rect.topleft)
	def get_mask(self):

		return(pygame.mask.from_surface(self.img))
#rotated_img = 0
def blitRotateCentre(surface,image,topleft,angle):
	rotated_img = pygame.transform.rotate(image,angle)
	new_rect = rotated_img.get_rect(center = image.get_rect(topleft = topleft).center)

	surface.blit(rotated_img, new_rect.topleft)
class Pipe:

	Gap = 180
	vel = 5

	def __init__(self,x):
		self.x = x
		self.height = 0
		self.top = 0
		self.bottom = 0

		self.Pipe_Top = pygame.transform.flip(PIPE_IMG,False , True)
		self.Pipe_Bottom = PIPE_IMG

		self.passed = False
		self.set_height()

	def set_height(self):

		self.height = random.randrange(50,450)
		self.top = self.height - self.Pipe_Top.get_height()
		self.bottom = self.height + self.Gap
	def move(self):
		self.x -= self.vel

	def draw(self,win):
		win.blit(self.Pipe_Top , (self.x , self.top))
		win.blit(self.Pipe_Bottom , (self.x , self.bottom))

	def collide(self,bird):

		bird_mask = bird.get_mask()
		top_mask = pygame.mask.from_surface(self.Pipe_Top)
		bottom_mask = pygame.mask.from_surface(self.Pipe_Bottom)

		top_offset = (self.x-bird.x ,self.top - round(bird.y))
		bottom_offset = (self.x-bird.x ,self.bottom - round(bird.y))

		b_point = bird_mask.overlap(bottom_mask , bottom_offset)
		t_point = bird_mask.overlap(top_mask , top_offset)

		if b_point or t_point:
			return True
		else:
			return False

class Base:

	Vel = 5
	Width = BASE_IMG.get_width()
	Img = BASE_IMG
	bottom = 700

	def __init__(self,y):

		self.y = y
		self.x1 = 0
		self.x2 = self.Width

	def move(self):
		self.x1 -= self.Vel
		self.x2 -= self.Vel


		if self.x1+self.Width <0:
			self.x1 = self.x2+self.Width
		if self.x2+self.Width <0:
			self.x2 = self.x1+self.Width
	def draw(self,win):

		win.blit(self.Img , (self.x1 , self.y))
		win.blit(self.Img , (self.x2 , self.y))
	def collide(self,bird):
		bird_mask = bird.get_mask()
		base_mask = pygame.mask.from_surface(self.Img)
		if bird.y >= self.y:
			return True
		'''bottom_offset = (self.-bird.x ,self.bottom - round(bird.y))
		b_point = bird_mask.overlap(base_mask , bottom_offset)'''

def draw_window(win , bird , pipes , score , base,over):
	win.blit(BG_IMG, (0,0))

	for pipe in pipes:
		pipe.draw(win)

	base.draw(win)

	bird.draw(win)
	#pygame.display.update()
	score_label = STAT_FONT.render("Score: " + str(score),1,(255,60,11))
	win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
	#pygame.display.update()

	if over:
		game_over = GAME_OVER_FONT.render("GAME OVER",1,(0,0,255))
		restrt = STAT_FONT.render("(Press Tab to Restart)",1,(148,0,211))
		
		win.blit(game_over, (50, 300))
		win.blit(restrt, (90, 390))
		
	pygame.display.update()	


def main():
	global restart
	bird = Bird(230,350)
	base = Base(700)
	pipes = [Pipe(600)]
	win = pygame.display.set_mode((WIN_WIDTH,WIN_HIEGHT))
	clock = pygame.time.Clock()
	key = pygame.key.get_pressed()
	score =0
	run =True
	coll = False
	over = False
	while run:
		clock.tick(30)
		#e = pygame.event.wait()

		add_pipe = False
		rem =[]
		
		for pipe in pipes:
			if pipe.collide(bird):
				coll = True
			if pipe.x + pipe.Pipe_Top.get_width() <0:
				rem.append(pipe)

			if not pipe.passed and pipe.x < bird.x:
				pipe.passed = True
				add_pipe = True

			pipe.move()

		if add_pipe:
			score +=1
			pipes.append(Pipe(600))
		for r in rem:
			pipes.remove(r)


		base.move()
		if base.collide(bird):
			coll = True
		if not coll:
			bird.move()
		else:
			run = False
		#bird.move()
		for e in pygame.event.get():
			if e.type == pygame.MOUSEBUTTONDOWN or (e.type == pygame.KEYDOWN and e.key == K_SPACE):
				bird.jump()
			if e.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
		
         
		draw_window(win,bird,pipes,score,base,over)
	while coll == True:
		over = True
		draw_window(win,bird,pipes,score,base,over)
		for e in pygame.event.get():
			if e.type == pygame.MOUSEBUTTONDOWN or (e.type == pygame.KEYDOWN and e.key == K_TAB):
				restart.append(1)
				run = False
				coll = False
			if e.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()


main()
for i in restart:
	main()


	
