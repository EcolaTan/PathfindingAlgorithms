from tkinter import *
import threading
import time
import tkinter.messagebox

directions = [[0,1],[1,0],[0,-1],[-1,0]]
maze = []
n = 0
timer = 0.01

with open("maze.txt") as f:
    n = [int(i) for i in next(f).split()][0]
    for i in range(n):
        maze.append(list(next(f))[0:n])
    if(n <= 16):
        timer = 0.1
    elif(n <= 24):
        timer = 0.04
    elif(n <= 48):
        timer = 0.025
    else:
        timer = 0.01

cell_size = 600/n #pixels

def create():
    for row in range(n):
        color = 'White'
        for col in range(n):
            if maze[row][col] == '.':
                color = 'White'
            elif maze[row][col] == 'G':
                color = 'Yellow'
            elif maze[row][col] == 'S':
                color = 'Blue'
            elif maze[row][col] == '#':
                color = 'grey'
            draw(row, col, color)

def draw(row, col, color):
    x1 = col*cell_size
    y1 = row*cell_size
    x2 = x1+cell_size
    y2 = y1+cell_size
    canvas.create_rectangle(x1, y1, x2, y2,fill=color)

class node:
    def __init__(self, x, y, path = []):
        self.x = x
        self.y = y
        self.path = path

def checkInbound(x,y,n):
    if(x < 0 or x >= n):
        return False
    if(y >= n or y < 0):
        return False
    return True

def isWall(maze,x,y):
    if(maze[x][y] == "#"):
        return True
    return False

def isGoal(maze,x,y):
    if(maze[x][y] == "G"):
        return True
    return False

def isStart(maze,x,y,x2,y2):
    if x == x2 and y == y2:
        return True
    return False

#find the start of the robot
def findInitial(n,maze):
    for i in range(n):
        for j in range(n):
            if(maze[i][j] == 'S'):
                return i,j

#result window
def resultPopUp(result,states):
    path = "Path is found" if result else "Path is not found"
    tkinter.messagebox.showinfo(path,'States Visited : ' + str(states))

def iterativeDFS(n,maze,initial_X,initial_Y):
    start = node(initial_X,initial_Y)
    states = 1

    stack = []
    stack.append(start)

    visited = [[initial_X,initial_Y]]

    while(stack):

        currentNode = stack.pop()
        x = currentNode.x
        y = currentNode.y

        if(not isStart(maze, x, y, initial_X, initial_Y) and not isGoal(maze, x, y)):
            time.sleep(timer)
            draw(x,y,"green")
            
        states += 1

        for drc in range(4):
            
            path = currentNode.path

            if(checkInbound(x+directions[drc][0],y+directions[drc][1],n)):
                next_X = x+directions[drc][0]
                next_y = y+directions[drc][1]

                if(not isWall(maze,next_X, next_y)):
                    if([next_X,next_y] not in visited):

                        visited.append([next_X,next_y])
                        stack.append(node(next_X,next_y,path + [[next_X,next_y]]))

                        if(isGoal(maze, next_X,next_y)):
                            
                            for i in path:
                                time.sleep(timer)
                                draw(i[0], i[1], 'red')

                            return True,states

    return False,states


#first window
window = Tk()
window.title('DFS')
canvas_side = n*cell_size
canvas = Canvas(window, width = canvas_side, height = canvas_side, bg = 'grey')
canvas.pack()

create()

x,y = findInitial(n, maze)

def run():
    result,states = iterativeDFS(n,maze,x,y)
    resultPopUp(result,states)

t = threading.Thread(target=run)
t.daemon = True
t.start()

window.mainloop()