import sys              # used for file reading
from settings import *  # use a separate file for all the constant settings
import heapq

# the class we will use to store the map, and make calls to path finding
class Grid:
    # set up all the default values for the frid and read in the map from a given file
    def __init__(self, filename):
        # 2D list that will hold all of the grid tile information
        self.__grid = []
        self.__load_data(filename)
        self.__width, self.__height = len(self.__grid), len(self.__grid[0])
        self.sectors = [[[0 for y in range(0,self.width())] for x in range(0,self.height())] for z in range(0,MAX_SIZE+1)]
        self.precompute_sectors()
       
           
            # loads the grid data from a given file name
    def __load_data(self, filename):
        # turn each line in the map file into a list of integers
        temp_grid = [list(map(int,line.strip())) for line in open(filename, 'r')]
        # transpose the input since we read it in as (y, x)
        self.__grid = [list(i) for i in zip(*temp_grid)]

    # return the cost of a given action
    # note: this only works for actions in our LEGAL_ACTIONS defined set (8 directions)
    def __get_action_cost(self, action):
        return CARDINAL_COST if (action[0] == 0 or action[1] == 0) else DIAGONAL_COST

    # returns the tile type of a given position
    def get(self, tile): return self.__grid[tile[0]][tile[1]]
    def width(self):     return self.__width
    def height(self):    return self.__height

    # Student TODO: Implement this function
    # returns true of an object of a given size can navigate from start to goal
    #def is_connected(self, start, goal, size):
       # return True

    # Student TODO: Replace this function with your A* implementation
    # returns a sample path from start tile to end tile which is probably illegal
    def get_path(self, start, end, size):
        path = []
        closed = []

        if self.is_connected(start,end,size):
            path,closed = self.AStarSearch(start,end,size)

        # return the path, the cost of the path, and the set of expanded nodes (for A*)
        return path, sum(map(self.__get_action_cost, path)), closed


    # Student TODO: Replace this function with a better (but admissible) heuristic
    # estimate the cost for moving between start and end
    def estimate_cost(self, start, end):
        cost = 0

        x = abs(start[0] - end[0])
        y = abs(start[1] - end[1])
        cost = cost + (max(x,y) - min(x,y)) * CARDINAL_COST
        cost = cost + (min(x,y) * DIAGONAL_COST)
        return cost

# Student TODO: You should implement AStar as a separate class
#               This will help keep things modular


    def is_connected(self,start,goal,size):
        if(self.sectors[size][start[0]][start[1]] == 0): return False
        if (self.sectors[size][start[0]][start[1]] == self.sectors[size][goal[0]][goal[1]]):
            return True
        
        return False
    def is_connected_diag(self,start, action, size):
        if(self.sectors[size][start[0]][start[1]] == 0): return False
        if ( start[0] + action[0] < 0  or start[1] + action[1] < 0 or start[0] + action[0] >= self.width() or start[1] + action[1] >= self.height() ): return False
        if self.sectors[size][start[0]][start[1]] != self.sectors[size][start[0] + action[0]][start[1]]: return False
        if self.sectors[size][start[0]][start[1]] != self.sectors[size][start[0]][start[1] + action[1]]: return False
       
        return True

    def precompute_sectors(self): 
        sector_num = 1
        for z in range(1,MAX_SIZE+1):
            for x in range(0,self.width()):
                for y in range(0,self.height()):
                    if (self.sectors[z][x][y] != 0):
                        continue
                    self.flood_fill(x,y,sector_num,z,self.get((x,y)))
                    sector_num += 1

        return self.sectors

    def flood_fill(self,x,y,secNum,size, type):
        if not self.check_tile(x,y,size,type): return
        if self.sectors[size][x][y] != 0:      return
        self.sectors[size][x][y] = secNum
        for a in [(0,1),(0,-1),(1,0),(-1,0)]:
            self.flood_fill(x + a[0], y + a[1], secNum, size, type)
        
    def check_tile(self,x,y,size,type):
        
        if ( x < 0  or y < 0 or x >= self.width() or y >= self.height() ):
            return False
        if size == 1:  return self.get((x,y)) == type

        elif size != 1:
            if( x+size-1 >= self.width() or y+size-1 >= self.height() ):return False
            

        for i in range(0,size):
            for j in range(0,size):
                if self.get((x+i,y+j)) != type: return False
        return True
        
        #We could not figure out how to access grid class methods from the AStar class to there is no AStar Class
    def AStarSearch(self, start, goal,size):
        open = [] 
        node = Node(start)
        node.f = self.estimate_cost(start,goal)
        heapq.heappush(open,(node.f,0,node))
        #open  = [node]
        closed = []
        path = []
        while len(open) > 0:
            i,j,node = heapq.heappop(open)
            if node.state == goal:
                path = self.reconstruct_path(node)
                return path,closed
            if node.state in closed:
                continue
            closed.append(node.state)
            for child in self.expand(node,size):

                if child.state in closed:
                    continue

                child.f = child.g + self.estimate_cost(child.state, goal)
                
                #if self.is_in_open_lower(child,open): continue
                #if self.is_in_open_better(child,open):continue
               # if ( i in open: i[2] == child.state and -child.g < i[1]): continue
                #else:
                #    heapq.heappush(open,(child.f,- child.g, child))
                    
                   
                heapq.heappush(open,(child.f,- child.g, child))
                
        return [],[]

    def reconstruct_path(self,node): 
        current = node
        path = []
       # path.append(current.action) # This action is not taken into account on the solution so gives errors on the test
        while current.parent != None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        return path

    def expand(self,node,size): #Method for expanding nodes, using predefined legal actions
        expanded = []
        for action in LEGAL_ACTIONS:
            n = Node((node.state[0] + action[0],node.state[1] + action[1]))
            n.parent = node
            n.action = (action)
            if ( n.state[0] < 0 or n.state[1] < 0 or n.state[0] >= self.width() or n.state[1] >= self.height()):continue
            
            if self.is_connected(node.state,n.state , size):
                if n.action[0] != 0 and n.action[1] != 0:
                    if not self.is_connected_diag(node.state,action,size): continue
        
                if action[0] != 0 and action[1] != 0:
                    n.g = node.g + DIAGONAL_COST
                else:
                    n.g = node.g + CARDINAL_COST
                expanded.append(n)
        return expanded

  

    def is_in_open_lower(self,node, open): #Part of grid optimization
        for i in range(len(open)):
            if node.state == open[i][2].state and node.g >= open[i][2].g:
                return True
        else: return False
    """
    def is_in_open_better(self,node, open): #Part of grid optimization
        for i in range(len(open)):
            if node.state == open[i][2].state and node.g < open[i][2].g:
                open[i] = (node
                return True
        else: return False
    """


    def remove_min_from_open(self,list): #Get min open using simple scan, optimize later
        m_index = 0
        m_fval = 10000000
        for i in range(len(list)):
            if list[i].f < m_fval:
                m_fval = list[i].f
                m_index = i
        return list.pop(m_index)

# Student TODO: You should implement a separate Node class
# AStar search should use these Nodes in its open and closed lists
class Node:
    def __init__(self,tile):
        self.state = tile
        self.g,h,f = 0,0,0
        self.parent = None
        self.action = (0,0)

    def __lt__(self, other):
        return self.f < other.f
