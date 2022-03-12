from ctypes import pointer
import numpy as np
import enum
import pygame

class Ori(enum.Enum):
   cw = -1
   lin = 0
   ccw = 1

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cw = None
        self.ccw = None

    def __eq__(self, p):
            return self.x == p.x and self.y == p.y

    @staticmethod
    def orientation(p1,p2,p3):
        diff = (p2.y - p1.y) * (p3.x - p2.x) - (p2.x - p1.x) * (p3.y - p2.y) 
  
        return Ori(np.sign(diff))

class ConvexHull:

    color_palette=[]
    screen:pygame.Surface
    points=[]
    edges=[]


    def __init__(self,W=300,H=300):
        self.width = W
        self.height = H
   
    def set_color_palette(self,pal=""):
        self.color_palette = pal.split('\n')[1:-1]
        print(self.color_palette)

    def create_points(self,count:int):
        self.points.clear()
        self.edges.clear()

        lim = self.screen.get_size()
        # self.points.append(Point(62,329))
        # self.points.append(Point(249,235))
        # self.points.append(Point(284,282))
        # self.points.append(Point(175,276))
        for i in range(count):

            x,y = int(np.random.normal(lim[0]/2,lim[0]/5,1)) , int(np.random.normal(lim[1]/2,lim[1]/5,1))
            self.points.append(Point(x,y))

    def connect_points(self,points):
        first = self.points.index(points[0])
        last = self.points.index(points[-1])
        self.edges.append([first,last])
        for i in range(len(points)-1):
            p = self.points.index(points[i])
            q = self.points.index(points[i+1])
            self.edges.append([p,q])

    def draw_edges(self):
        for a,b in self.edges:
            x1,y1 =self.points[a].x ,self.points[a].y
            x2,y2 =self.points[b].x ,self.points[b].y
            pygame.draw.line(self.screen,self.color_palette[2],(x1,y1),(x2,y2),2)

    def draw_points(self):
        for i in range(len(self.points)):
            x,y = self.points[i].x,self.points[i].y
            pygame.draw.circle(self.screen,pygame.Color( self.color_palette[1]),(x,y),3)
            img = self.font.render(f"{i}-{(x,y)}", True, self.color_palette[3])
            self.screen.blit(img, (x+3, y+3))

    def sort_points_based_on_x(self):
        self.points = sorted(self.points, key = lambda p: p.x)

            

    def process(self,points):
        return points # delete this line to start implementing convex hull algorithem
        pass

    def merge(self,left,right):
        pass

    def run(self,):

        #----------------Initialization---------------------
        pygame.init()
        # initializing font must be after pygame.init()
        self.font = pygame.font.SysFont('arial.ttf',20)
        self.screen = pygame.display.set_mode((self.width, self.height))

        #----------------Start-----------------------        
        self.create_points(2)
        self.sort_points_based_on_x()
        #--------------------------------------------        
        
        #----------------Update-----------------------        
        running = True
        while running:
            self.screen.fill(self.color_palette[0])
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key  == pygame.K_SPACE:
                        self.create_points(2)
                    if event.key == pygame.K_s:
                        self.edges.clear()
                        self.sort_points_based_on_x()
                        convex_points = self.process(self.points)
                        self.connect_points(convex_points)


            self.draw_edges()
            self.draw_points()

            pygame.display.flip()
        #--------------------------------------------        

        pygame.quit()

if __name__ == "__main__":
    ch = ConvexHull(400,400)
    ch.set_color_palette("""
#1B1A17
#F0A500
#E45826
#E6D5B8
""")

    ch.run()

