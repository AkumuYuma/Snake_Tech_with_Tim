import pygame

#Size of pygame window
width = 500
heigh = 500

#Rows and columns
col_size = 25
row_size = 25


class Cube:

    size = 25 #cube size
    
    def __init__(self, start, color = (255, 0, 0), dirx = 1, diry = 0):
        """Cube class, attributes:
        color
        start
        direction"""
        self.pos = start
        self.color = color
        self.dirx = dirx
        self.diry = diry

    def move(self):
        """Moves a cube from self.pos computing new position from dirx and diry"""
        xvelocity = Cube.size*self.dirx
        yvelocity = Cube.size*self.diry
        self.pos = self.pos[0] + xvelocity, self.pos[1] + yvelocity  

    def draw(self, surface, eyes = False):
        """Draws a cube on the surface"""
        pygame.draw.rect(surface, self.color, pygame.Rect(self.pos, (Cube.size, Cube.size)))

        if eyes: #If this cube is the head of the snake
            radius = 3
            centre = self.pos[0]+(Cube.size//2), self.pos[1]+(Cube.size//2) #Only one eye, at the centre
            pygame.draw.circle(surface, (0,0,0), centre, radius)


        
class Snake:
    body = []
    turns = {}
    
    def __init__(self, pos, dirx, diry):
        pass

    def move(self):
        pass

    def draw(self, surface):
        pass

    def add_cube(self):
        pass

    def reset(self, pos):
        pass



def drawGrid(surface, width, heigh, row_size, column_size):
    """Draws a grid on the surface made of rows and columns"""
    nrows = heigh//row_size  #Compute the number of rows and cols
    ncol = width//col_size
    xpos = 0 #Positions where to draw raws and cols
    ypos = 0
    for i in range(nrows):
        xpos += column_size
        ypos += row_size
        pygame.draw.line(surface, (255, 255, 255), (0, ypos), (heigh, ypos))
        pygame.draw.line(surface, (255, 255, 255), (xpos, 0), (xpos, width))


def redrawWindow():
    global win, cube1
    win.fill((0,0,0))
    drawGrid(win, width, heigh, row_size, col_size)
    cube1.draw(win)
    #Disegna snake
    #Disegna snack
    pygame.display.update()

    
def main():
    global width, heigh, row_size, column_size, win, cube1
    win = pygame.display.set_mode((width, heigh))
    clock = pygame.time.Clock()
    cube1 = Cube([250,250])
    while True:
        pygame.time.delay(50)
        clock.tick(10)
        cube1.move()
        
        redrawWindow()


if __name__ == '__main__':
    main()
