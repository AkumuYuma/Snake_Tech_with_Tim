import pygame
import random
import tkinter
from tkinter import messagebox
from tkinter import simpledialog

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

    def move(self, dirx, diry):
        global width, heigh
        self.dirx = dirx
        self.diry = diry
        """Moves a cube from self.pos computing new position from dirx and diry"""
        #Managing the end of the window
        if self.pos[0] == - Cube.size: #Going out on the left side
            self.pos = width - Cube.size, self.pos[1]
        elif self.pos[0] == width:  #Going out on the right side
            self.pos = 0, self.pos[1]
        elif self.pos[1] == - Cube.size: #Out on top 
            self.pos = self.pos[0], heigh - Cube.size 
        elif self.pos[1] == heigh: #Out on bottom
            self.pos = self.pos[0], 0 
        else: #If no wall has been found, just keep going
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
    body = [] #List of pieces in the snake. Made of cubes
    turns = {} #Dict, position_of_turn : New_direction
    
    def __init__(self, color, pos):
        #Position must be given as coordinates on the grid
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head) #Add just one piece at the beginning
        self.dirx = 0
        self.diry = 1 


    def move(self):
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #Just to exit without errors
                pygame.quit()

            keys = pygame.key.get_pressed() 

            for key in keys:
                if keys[pygame.K_LEFT]: #Change direction and save turn command in a dict 
                    self.dirx = -1 
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx,self.diry]
                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx,self.diry]
                elif keys[pygame.K_UP]:
                    self.diry = -1
                    self.dirx = 0
                    self.turns[self.head.pos[:]] = [self.dirx,self.diry]
                elif keys[pygame.K_DOWN]:
                    self.diry = 1
                    self.dirx = 0
                    self.turns[self.head.pos[:]] = [self.dirx,self.diry]

        for i, c in enumerate(self.body):
            p = c.pos
            if p in self.turns: #If position of a piece is saved before as turn command, the cube changes direction
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1: #When p is the last piece, pop it from the dict of turns command
                    self.turns.pop(p)

            else: #Else it just goes ahead
                c.move(c.dirx, c.diry)


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0: 
                c.draw(surface, True) #Draw the first piece with the eye
            else:
                c.draw(surface)

    def add_cube(self):
        tail = self.body[-1] 
        dx, dy = tail.dirx, tail.diry 
        if dx == 1 and dy == 0: #Add a new piece of the body in the right direction
            self.body.append(Cube((tail.pos[0]-Cube.size, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+Cube.size, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-Cube.size)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+Cube.size)))

        self.body[-1].dirx = dx #Set the new tail direction
        self.body[-1].diry = dy

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1




def randomSnack(snake):
    """Returns a random position to place the snack in the grid"""
    global width, heigh, row_size, col_size

    positions = snake.body
    
    nrows = heigh//row_size
    ncol = width//col_size
    
    while True:
        xpos = (random.randint(0, ncol-1))*col_size
        ypos = (random.randint(0, nrows-1))*row_size
        if len(list(filter(lambda z: z.pos == (xpos,ypos), positions))) > 0:
            """positions is a list of snake pieces.
            This conditional filters positions of snake pieces with the x e y
            random generated. If (x,y) matches with at leat one snake piece, must
            regen x and y. Else, we can break the loop and take the touple (xpos,ypos)
            as the position of random snack."""
            continue
        else:
            break
    
    return xpos,ypos



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
    global win, snake, snack
    win.fill((0,0,0))
    drawGrid(win, width, heigh, row_size, col_size)
    snake.draw(win)
    snack.draw(win)
    pygame.display.update()

    
def main():
    global width, heigh, win, snake, snack
    win = pygame.display.set_mode((width, heigh))
    clock = pygame.time.Clock()
    flag = True
    
    snake = Snake((255, 0, 0), (250,250)) #Create the snake
    snake.add_cube()
    snack = Cube(randomSnack(snake), color = (0, 255, 0)) #Create the snack
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()

        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(randomSnack(snake),color = (0, 255, 0))

        for i in range(len(snake.body)):
            if snake.body[i].pos in list(map(lambda z: z.pos, snake.body[i+1:])):
                score = len(snake.body)
                print('Your score is: ', score)
                pygame.quit()
                root = tkinter.Tk()
                root.withdraw()
                answer = messagebox.askyesno('Game over', 'Do you want to play again?')
                if answer:              
                    snake.reset((250,250))
                    pygame.init()
                    win = pygame.display.set_mode((width,heigh))
                    break
                else:
                    flag = False

        redrawWindow()


if __name__ == '__main__':
    main()
