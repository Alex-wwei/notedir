#coding:utf-8
import pygame
import random
from pygame.locals import * 
import time
import thread
import math

WINDOWS_WIDTH = 440
WINDOWS_HIGHT = 720

#pygame.init()
#mainClock = pygame.time.Clock()

class Hero(object):
	def __init__(self, heroimg):
		self.img = heroimg
		self.x = 170
		self.y = 620
		self.bullets = []
	def display(self, screen, x, y):
		self.frame = screen.blit(self.img, (x, y))
	def mov_left(self):
		if self.x > -40:
			self.x -= 15
	def mov_right(self):
		if self.x < 380:
			self.x += 15
	def mov_up(self):
		if self.y > 100:
			self.y -= 15
	def mov_down(self):
		if self.y < 630:
			self.y += 15
	def  add_bullet(self, blt):
		self.bullets.append(blt)

class Enemy_plane(object):
	def __init__(self, enemyimg, e_x, e_y):
		self.img = enemyimg
		self.x = e_x
		self.y = e_y
		self.bullets = []
	def mov_down(self, speed):
		self.y += speed
	def display(self, screen, x, y):
		self.frame = screen.blit(self.img, (x, y))
	def __del__(self):
		#print('YOU  WIN !')
		pass

class Bomb(object):
	def __init__(self, bombimg, start_x, start_y):
		self.x = start_x
		self.y = start_y
		self.img = bombimg
	def display(self, screen, now_x, now_y):
		self.frame = screen.blit(self.img, (now_x, now_y))
	def mov_down(self, speed):
		self.y += speed
	def mov_random(self, speed):
		i = random.randint(-10, 10)
		for x in range(0, abs(i)):
			if i < 0:
				self.x -= 1
			else:
				self.x += 1

def fork(enemy, screen):
	#enemy_dead_music.pay()
	for ii in range(1, 5):
		enemy.img = pygame.image.load('enemy1_down%d.png'%(ii))
		enemy.display(screen, enemy.x, enemy.y)
		time.sleep(0.3)


if __name__ == '__main__':

	screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HIGHT), 0,32)
	#加载资源图片
	bgimg = pygame.image.load('background.png')
	enemyimg = pygame.image.load('enemy1_hit.png')
	bullet = pygame.image.load('bullet%d.png'%(random.randint(0, 2)))
	heroimg = pygame.image.load('hero1.png')

	#enemy_dead_music = pygame.mixer.Sound('./music/dis.wav')

	pygame.display.set_caption('飞机大战 From:WangWei')
	#初始化变量
	hero = Hero(heroimg)
	enemy = Enemy_plane(enemyimg, 100, 20)

	k1 = 0
	k2 = 0
	k3 = 0
	k4 = 0
	enemy_list = []
	bomb_list = []

	def bomb_display():
		global k4, bullet
		if k4 == 300:
			k4 = 0
			b = Bomb(pygame.image.load('prop_type_1.png'), random.random()*(WINDOWS_WIDTH - 40), -100)
			bomb_list.append(b)
		#子弹包显示以及与自己的飞机碰撞检测
		if len(bomb_list) > 0:
			for b in bomb_list:
				b.mov_down(3)
				b.mov_random(5)

				b.display(screen, b.x, b.y)
				#thread.start_new_thread(drifting, (b, screen))
				if hero.frame.contains(b.frame):
					#print(dir(hero.frame), '----------------------')
					bullet = pygame.image.load('bullet-%d.gif'%(random.randint(1,3)))
					bomb_list.remove(b)
					print('=====吃到子弹包=====')

	def enemy_display():
		global k2
		if k2 == 40:
				k2 = 0
				e = Enemy_plane(pygame.image.load('enemy1_hit.png'), random.random()*(WINDOWS_WIDTH - 40), -100)
				enemy_list.append(e)

		#让敌机显示
		if len(enemy_list) > 0:
			for i, e in enumerate(enemy_list):
				e.display(screen, e.x, e.y)
				e.mov_down(2)

	def bullet_display():
		global k1
		if k1 == 15:
			k1 = 0
			l1=[]
			for i in range(0, 3):
				#screen。blit()返回一个rect对象，可以理解为frame
				l1.append(screen.blit(bullet, (hero.x + 42, hero.y-20)))
				#print(dir(l1[0]), '------------')
			hero.bullets.append(l1)		

		if len(hero.bullets) > 0:
			for x in hero.bullets:
				#print(len(l))
				x[0].x -= 2
				x[0].y -= 5
				x[1].y -= 6
				x[2].x += 2
				x[2].y -= 5
				k = 0
				#遍历出屏幕子弹然后删除
				for b in x:
					if len(enemy_list) > 0:
						for i,enemy in enumerate(enemy_list):
							#判断敌机是否被打中	
							if enemy.frame.contains(b):
								#另开一个线程对消灭的敌机进行暂缓消失，为了更形象
								thread.start_new_thread(fork, (enemy, screen))
								#enemy.display(screen, enemy.x, enemy.y)
								enemy_list.pop(i)

					screen.blit(bullet, (b.x, b.y))
					if b.x < 0 or b.y < 0:
						k+=1
						if k == 3:
							hero.bullets.remove(x)

	while True:
	
		screen.blit(bgimg, (0,0))
		hero.display(screen, hero.x, hero.y)

		#让子弹包陆续出现
		k4 += 1
		bomb_display()

		#让敌机陆续出现
		k2 += 1
		enemy_display();
		
		#让子弹延迟发射
		k1 += 1
		bullet_display()

		for event in pygame.event.get():

			if event.type == QUIT:
				print('quit')
				exit()

			elif event.type == KEYDOWN:

				if event.key == K_a or event.key == K_LEFT:
					hero.mov_left()

				elif event.key == K_d or event.key == K_RIGHT:
					hero.mov_right()

				elif event.key == K_SPACE:
					print("space")

				elif event.key == K_UP:
					hero.mov_up()

				elif event.key == K_DOWN:
					hero.mov_down()

		#在肉眼分辨不出情况下，通过延时的方式，来降低循环速度，从而降低了cpu占用率
		time.sleep(0.01)
		pygame.display.update()
