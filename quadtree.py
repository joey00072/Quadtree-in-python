import pygame
from math import sin,cos,pi
import math
from pygame.draw import line,circle,rect
from pygame.gfxdraw import aacircle 
from pygame import gfxdraw
import random
import time
import numpy as np
import sys

sys.setrecursionlimit(10000)
# random.seed(0)
pygame.init()


HIGHT,WIDTH= 600,600
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,0,255)
GRAY=(120,120,120)
DARKGRAY = (10,10,10)
GREEN = (0,250,0)
RED=(255,0,0)
PointRadius=3
CAPACITY = 5
ox,oy = WIDTH//2,HIGHT//2

screen = pygame.display.set_mode((WIDTH,HIGHT))

clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS', 30)

class QuadTree(object):
	"""docstring for QuadTree"""
	def __init__(self, START=(0,0),capacity=5,HIGHT=HIGHT,WIDTH=WIDTH,depth=0,name="ROOT"):
		super(QuadTree, self).__init__()
		# print(HIGHT,WIDTH,depth,name)
		

		self.Points   = []
		self.capacity = capacity
		self.childern = False

		self.START    = START
		self.NW       = None
		self.NE       = None
		self.SW       = None
		self.SE       = None
		self.depth    = depth
		self.name     = name
		self.HIGHT    = WIDTH
		self.WIDTH    = WIDTH
		# print(f"START:{START} {self.name} ")
	def divide(self):
		# print(len(self.Points))
		# if len(self.name)>1000:
		# 	self.capacity=30
		self.NW       = QuadTree((self.START[0]               ,self.START[1]              ),               capacity=self.capacity, HIGHT=self.HIGHT//2,  WIDTH=self.WIDTH//2,  depth=self.depth+1,  name=f"{self.name}-NW")
		self.NE       = QuadTree((self.START[0]+self.WIDTH//2 ,self.START[1]              ),               capacity=self.capacity, HIGHT=self.HIGHT//2,  WIDTH=self.WIDTH//2,  depth=self.depth+1,  name=f"{self.name}-NE")
		self.SW       = QuadTree((self.START[0]               ,self.START[1]+self.HIGHT//2),               capacity=self.capacity, HIGHT=self.HIGHT//2,  WIDTH=self.WIDTH//2,  depth=self.depth+1,  name=f"{self.name}-SW")
		self.SE       = QuadTree((self.START[0]+self.WIDTH//2 ,self.START[1]+self.HIGHT//2),               capacity=self.capacity, HIGHT=self.HIGHT//2,  WIDTH=self.WIDTH//2,  depth=self.depth+1,  name=f"{self.name}-SE")

	def insert(self,Point):
		if not self.childern:

			if len(self.Points)< self.capacity:
				self.Points.append(Point)
			else:
				self.Points.append(Point)
				self.childern = True
				self.divide()
				x,y=self.START
				for point in self.Points:
					# print(f"point: {point.x} , {point.y}")
					if (point.x<=x+self.WIDTH//2 and point.y<=y+self.HIGHT//2):
						self.NW.insert(point)
					elif (point.y<=y+self.HIGHT//2):
						self.NE.insert(point)
					elif (point.x<=x+self.WIDTH//2):
						self.SW.insert(point)
					else:
						self.SE.insert(point)
		else:
			self.Points.append(Point)
			point=Point
			x,y=self.START
			if (point.x<=x+self.WIDTH//2 and point.y<=y+self.HIGHT//2):
				self.NW.insert(point)
			elif (point.y<=y+self.HIGHT//2):
				self.NE.insert(point)
			elif (point.x<=x+self.WIDTH//2):
				self.SW.insert(point)
			else:
				self.SE.insert(point)

	def query(self,box):

		cnt=0
		START_x,START_y,END_x,END_y=box
		self.x,self.y=self.START
		if self.x>=START_x and self.y>=START_y and self.x+self.WIDTH<=END_x and self.y+self.HIGHT<=END_y :
			return len(self.Points)
		if self.x>END_x or self.y>END_y or self.x+self.WIDTH<START_x or self.y+self.HIGHT<START_y :
			return 0
		if self.childern:
			cnt+=self.NW.query(box)
			cnt+=self.NE.query(box)
			cnt+=self.SW.query(box)
			cnt+=self.SE.query(box)
		else:
			for point in self.Points:
				if point.x>=START_x and point.y>=START_y and point.x<=END_x and point.y<=END_y:
					cnt+=1
		# print(self.name,cnt)
		return cnt

	def getPointInRange(self,box):

		cnt=[]
		START_x,START_y,END_x,END_y=box
		self.x,self.y=self.START

		if self.x>=START_x and self.y>=START_y and self.x+self.WIDTH<=END_x and self.y+self.HIGHT<=END_y :
			# print("HDHH")
			return self.Points

		if self.x>END_x or self.y>END_y or self.x+self.WIDTH<START_x or self.y+self.HIGHT<START_y :
			EMPTY=[]
			# print(type(EMPTY),"EMPTY")
			return EMPTY

		if self.childern:
			# print(type(cnt),type(self.NW.query(box)) , self.NW.query(box))
			cnt=cnt+self.NW.getPointInRange(box)
			cnt=cnt+self.NE.getPointInRange(box)
			cnt=cnt+self.SW.getPointInRange(box)
			cnt=cnt+self.SE.getPointInRange(box)

		else:
			for point in self.Points:
				if point.x>=START_x and point.y>=START_y and point.x<=END_x and point.y<=END_y:
					cnt.append(point)
		# print(self.name,len(cnt))
		# print("74HDHH")
		return cnt

	def draw(self,deplth=0):
		# print(deplth)
		if self.childern:
			x,y = self.START
			line(screen,GRAY,(x,y+(self.HIGHT//2)) , (x+(self.WIDTH),y+(self.HIGHT//2)),1)
			line(screen,GRAY,(x+(self.WIDTH//2),y) , (x+(self.WIDTH//2) ,y+(self.HIGHT)),1)
			self.NW.draw(deplth+1)
			self.NE.draw(deplth+1)
			self.SW.draw(deplth+1)
			self.SE.draw(deplth+1)




ox,oy = WIDTH//2,HIGHT//2


class Point(object):
	"""docstring for Points"""
	def __init__(self, x=None,y=None,vx=0,vy=0,mass=1):
		super(Point, self).__init__()
		self.x = x if x else random.randint(10,WIDTH-12)
		self.y = y if y else random.randint(10,WIDTH-12)
		self.vx = vx
		self.vy = vy
		self.mass = mass
		self.intersect=False
		

	def display(self,Color=None):
		# circle(screen, WHITE if self.intersect else GRAY ,(int(self.x),int(self.y)),PointRadius)
		aacircle(screen,int(self.x),int(self.y),PointRadius,WHITE if self.intersect else GRAY )
		gfxdraw.filled_circle(screen,int(self.x),int(self.y),PointRadius,WHITE if self.intersect else GRAY )


	def randomWalk(self):
		global ox,oy
		self.x += random.randint(-10,10)/3
		self.y += random.randint(-10,10)/3

		# dist=self.dist((ox,oy),(self.x,self.y))+5
		# self.x += (ox-self.x)/dist
		# self.y += (oy-self.y)/dist


		# ox,oy = WIDTH//2,HIGHT//2
		# ox+=100
		# oy+=100
		# print(ox,oy)
		# self.x -= (self.x-ox ) *0.001
		# self.y -= (self.y-oy ) *0.001
		# dx=self.dist((ox,oy),(self.x,self.y))

		# if self.x<WIDTH//2:
		# 	self.x+=dx*0.001
		# else:
		# 	self.x-=dx*0.001

		# if self.y<WIDTH//2:
		# 	self.y+=dx*0.001
		# else:
		# 	self.y-=dx*0.001

	def move(self):
		self.x +=self.vx
		self.y +=self.vy

	def dist(self,p1,p2):
		p1x,p1y=p1
		p2x,p2y=p2
		return math.sqrt(  (p2x-p1x)**2  + (p2y-p1y)**2 )

	def getCoordinate(self):
		return (self.x,self.y)

	def setIntersect(self,isIntersect):
		# print(isIntersect)
		self.intersect = isIntersect




class Universe(object):
	"""docstring for Universe"""
	def __init__(self, no_of_points=10):
		super(Universe, self).__init__()
		self.no_of_points = no_of_points
		self.allPoints    = []
		self.Tree = QuadTree(capacity=CAPACITY)
		self.initUniverse()
		self.g = 1000

	def initUniverse(self):
		for i in range(self.no_of_points):
			point=Point()
			self.allPoints.append(point)
			self.Tree.insert(point)

		for i in range(30):
			point=Point(HIGHT//2+100+random.randint(-30,30),WIDTH//2+100+random.randint(-30,30))
			self.allPoints.append(point)
			self.Tree.insert(point)

		for i in range(30):
			point=Point(HIGHT//2-100+random.randint(-30,30),WIDTH//2-100+random.randint(-30,30))
			self.allPoints.append(point)
			self.Tree.insert(point)


	def display(self):
		for Point in self.allPoints:
			Point.display()
			Point.randomWalk()
		self.Tree.draw()
	def walk(self):
		for Point in self.allPoints:
			Point.move()
	def dist(self,p1,p2):
		return math.sqrt(  (p2.x-p1.x)**2  + (p2.y-p1.y)**2 )

	def isColiding(self,p1,p2):
		if self.dist(p1,p2)<=PointRadius+10:
			# print(PointRadius,self.dist(p1,p2))
			return True
		else:
			return False
	def collision(self):
		for Point in self.allPoints:
			Point.setIntersect(False)
		# for i in range(len(self.allPoints)):
		# 	for j in range(i,len(self.allPoints)):
		# 		p1=self.allPoints[i]
		# 		p2=self.allPoints[j]
		# 		if not(p1.x==p2.x and p1.y==p2.y):
		# 			if self.isColiding(p1,p2):
		# 				p1.setIntersect(True)
		# 				p2.setIntersect(True)

		for p in self.allPoints:
			x,y=p.x,p.y
			SIDE=4*PointRadius
			lst=U.Tree.getPointInRange((x-SIDE,y-SIDE,x+SIDE,y+SIDE))
			for point in lst:
				if not (point.x==p.x and point.y==p.y):
					ans=self.isColiding(p,point)
					p.setIntersect(ans)
					if ans:
						continue

	def gForce(self,p1,p2):
		return self.g * p1.mass * p2.mass/ (self.dist(p1,p2))**2

	def findAngle(self,p1,p2):

		d=self.dist(p1,p2)
		x = p1.x -p2.x
		y = p1.y -p2.y

		return math.atan2(y,x)


	def gravity(self):
		for p1 in self.allPoints:
			for p2 in self.allPoints:
				if not (p1.x-p2.x<10 and p1.y-p2.y<10) :
					v = self.gForce(p1,p2)/p1.mass
					# print(v)
					angle =  self.findAngle(p1,p2)
					# print(angle,"A")
					p1.vx += -v*cos(angle)
					p1.vy += -v*sin(angle)
	def addPoint(self,pos):
		x,y = pos
		p = Point(x,y)
		self.allPoints.append(p)
		self.Tree.insert(p)

def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text


		

def lightup(ROOT,vis):
	if vis:
		return Tree
	if ROOT.childern:
		if lightup(ROOT.NW,vis):
			return True
		if lightup(ROOT.NE,vis):
			return True
		if lightup(ROOT.SW,vis):
			return True
		if lightup(ROOT.SE,vis):
			return True



		# if not vis:
		# 	if lightup(ROOT.NE,vis):
		# 	return True 
		# if not vis:
		# 	vis=lightup(ROOT.NW,vis)  
		# if not vis:
		# 	vis=lightup(ROOT.SW,vis)  
		# if not vis:
		# 	vis=lightup(ROOT.SE,vis)    
	else:
		
		rt=False
		for point in ROOT.Points:
			if not point.intersect:
				print(ROOT.name)
				print(point.x,point.y)
				point.intersect=True
				rt=True
				break
		return rt
		# return True   



# def drawRect(ROOT):
# 	rect(screen,DARKGRAY,(ROOT.START[0],ROOT.START[1],ROOT.WIDTH,ROOT.HIGHT),1)
# 	if ROOT.childern:
# 		drawRect(ROOT.NW)
# 		drawRect(ROOT.NE)
# 		drawRect(ROOT.SW)
# 		drawRect(ROOT.SE)
lst=[]
def drawRect(arg):
	global lst
	lst=[]
	if arg:
		x,y = arg
		SIDE=200
		rect(screen,GREEN,(x,y,SIDE,SIDE ),1)
		cnt=U.Tree.query((x,y,x+SIDE,y+SIDE))
		lst=U.Tree.getPointInRange((x,y,x+SIDE,y+SIDE))
		# print(len(lst))
		for p in lst:
			p.intersect=True
			# print(p.x,p.y)
		cnt_text = font.render(str(cnt), 1, pygame.Color("coral"))
		screen.blit(cnt_text, (WIDTH-50,0))
	else:
		for pos in lst:
			x,y = pos

			rect(screen,GREEN,(x,y,100,100 ),1)



def light(ROOT):
	try:
		NODE=ROOT.NE.SE
		lst = NODE.Points
		circle(screen,WHITE,(NODE.START[0],NODE.START[1]),10)
		print(NODE.START,NODE.HIGHT,NODE.WIDTH)
		for point in lst:
			point.intersect=True
	except Exception as e:
		print(e)

U =Universe(100)

# p1=Point(x=HIGHT//2,y=WIDTH//2+100,vx=-5,mass=10)
# p2=Point(x=HIGHT//2,y=WIDTH//2-100,vx=5,mass=10)
# p3=Point(x=0,y=0,mass=5)
# U.allPoints.append(p1)
# U.allPoints.append(p2)
# U.allPoints.append(p3)
# U.allPoints.append(Point(x=10,y=250,vx=10,vy=10,mass=1))
RUN = True
angle=0
# lightup(U.Tree,False)
# lightup(U.Tree,False)
lst=[]	
Inital_pos = (int(WIDTH/2),int(HIGHT))
while RUN:
	screen.fill(DARKGRAY)
	# time.sleep(0.1)
	# screen.blit(update_fps(), (10,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			RUN=False
			break
		if event.type == pygame.MOUSEBUTTONUP:
			# pass
			pos = pygame.mouse.get_pos()
			ox,oy = pos
			print(pos,ox,oy)
			# lst.append(pos)
			# print(pos)
			# U.addPoint(pos)

	# lightup(U.Tree,False)
	
	# light(U.Tree)
	U.walk()
	ox,oy =pygame.mouse.get_pos()
	
	# U.gravity()
	U.display()
	U.collision()
	t=time.time()
	Tree = QuadTree(capacity=CAPACITY)
	for p in U.allPoints:
		Tree.insert(p)
	U.Tree =Tree
	# print(time.time()-t)
	# for p in U.allPoints:
	# 	p.intersect=False
	# drawRect(pygame.mouse.get_pos())
	# print(f"p1 {p1.x} {p1.x}")
	# print(f"p2 {p2.x} {p2.x}")
	clock.tick(60)
	pygame.display.update()
