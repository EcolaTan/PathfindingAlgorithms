from tkinter import *
import threading
import heapq
import time
import tkinter.messagebox

directions = [[0,1],[1,0],[0,-1],[-1,0]]
maze = []
n = 0
timer = 0.01

# set the timer base on the size of the maze
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

#pixels per grid
cell_size = 600/n

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
    def __init__(self, x, y, path = [], cost = 0):
        self.x = x
        self.y = y
        self.cost = cost
        self.path = path

    def __lt__(self, other):
        return self.cost < other.cost

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

def findInitial(n,maze):
    for i in range(n):
        for j in range(n):
            if(maze[i][j] == 'S'):
                return i,j

def findGoal(n,maze):
    for i in range(n):
        for j in range(n):
            if(maze[i][j] == 'G'):
                return i,j

#result window
def resultPopUp(result,states):
    path = "Path is found" if result else "Path is not found"
    tkinter.messagebox.showinfo(path,'States Visited : ' + str(states))

def distance(x1,x2,y1,y2):
    return abs(x2-x1) + abs(y2-y1)

def bfs(n,maze,initial_X,initial_Y,goal_x,goal_y):

    #initialize the search by adding the initial position of the robot
    start = node(initial_X,initial_Y)
    states = 1

    q = []
    heapq.heappush(q, start)

    visited = [[initial_X,initial_Y]]

    while(q):
        #take the node and declare its x and y values as variables for easier access
        currentNode = heapq.heappop(q)
        x = currentNode.x
        y = currentNode.y

        #add numbers if the node visited is not the start or goal
        if(not isStart(maze, x, y, initial_X, initial_Y) and not isGoal(maze, x, y)):
            time.sleep(timer)
            draw(x, y, 'green')

        states += 1

        #visit all adjacent possible direcionts
        for drc in range(4):
            
            #the current path of the node
            path = currentNode.path

            #check if the index is still in the maze
            if(checkInbound(x+directions[drc][0],y+directions[drc][1],n)):
                next_X = x+directions[drc][0]
                next_y = y+directions[drc][1]

                #check if the node is a wall or not
                if(not isWall(maze,next_X, next_y)):
                    #if first time visting it
                    if([next_X,next_y] not in visited):
                        #add to queue to process it
                        visited.append([next_X,next_y])
                        cost = distance(next_X, goal_x, next_y, goal_y)
                        heapq.heappush(q, node(next_X,next_y,path + [[next_X,next_y]],cost))

                        #if we found the goal
                        if(isGoal(maze, next_X,next_y)):
                            
                            #change the maze node to red to specify path
                            for i in path:
                                time.sleep(timer)
                                draw(i[0], i[1], 'red')

                            return True,states

    return False,states
            
#first window
window = Tk()
window.title('Greedy BFS')
canvas_side = n*cell_size
canvas = Canvas(window, width = canvas_side, height = canvas_side, bg = 'grey')
canvas.pack()

create()

x,y = findInitial(n, maze)
x2,y2 = findGoal(n, maze)

def run():
    result,states = bfs(n,maze,x,y,x2,y2)
    resultPopUp(result,states)

t = threading.Thread(target=run)
t.daemon = True
t.start()

window.mainloop()