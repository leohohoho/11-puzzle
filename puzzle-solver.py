#Leo Ho - lmh575
import math

""" Function to find the coordinate of a given number """
def find(lst,x):
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            if lst[i][j] == x:
                return i,j

""" Function to join the puzzle number list into a string """
def joinstr(lst):
    sep = ','
    newstr = ''
    for i in range(len(lst)):
        newstr += sep.join(lst[i])
        if i < len(lst) - 1:
            newstr += ','
    return newstr
        

class Node:
    def __init__(self,data,level,fval,move,parent):
        """ The node class, each node is a state """
        self.parent = parent #parent node for backtracking
        self.data = data     #hold the state as list of strings, EX: [['0','1','2','3'],['4','5','6','7'],['8','9','10','11']]
        self.level = level   #level of the node in the tree
        self.fval = fval     #f value (A*)
        self.move = move     #which move lead to this node from previous node (L,R,U,D)

    def generate_child(self):
        """ Generate a list of child nodes from the given node by moving number 0 in four directions """
        x,y = find(self.data,'0')  
        """ val_list contains coordinates for moving the number 0 """
        val_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        children = []
        for i in val_list:
            child = self.move0(self.data,x,y,i[0],i[1]) #function move0 below
            if child is not None:
                if i[0] == x + 1 and i[1] == y:
                    move = "D"
                elif i[0] == x and i[1] == y + 1:
                    move = "R"
                elif i[0] == x-1 and i[1] == y:
                    move = "U"
                elif i[0] == x and i[1] == y - 1:
                    move = "L"
                child_node = Node(child,self.level+1,0,move,self)
                children.append(child_node)
        return children
        
    def move0(self,puz,x1,y1,x2,y2):
        """ Move the number 0 in the given direction and if the position value are out
            of range the return None by creating a new list """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data[0]):
            #check if x2,y2 are in range
            shuff = []
            shuff = self.copy(puz)
            temp = shuff[x2][y2]
            shuff[x2][y2] = shuff[x1][y1]
            shuff[x1][y1] = temp
            return shuff
        else:
            return None
            

    def copy(self,aNode):
        """ Copy the list/data of a node """
        temp = []
        for i in aNode:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
            

class Puzzle:
    def __init__(self,size):
        """ Initialize the puzzle size by the specified size, frontier and reached are empty """
        self.n = size         #number of lines in the puzzle 
        self.frontier = []    #list of open nodes that can be explored
        self.reached = {}     #dictionary, keep state as key and node as value

    def f(self,start,goal):
        """ Heuristic Function: f(x) = h(x) + g(x) """
        return self.h(start.data,goal) + start.level

    def h(self,start,goal):
        """ Using Manhattan distances of tiles from their goal positions """
        manhat = 0
        for i in range(12):
            x1, y1 = find(start,str(i))
            x2, y2 = find(goal,str(i))
            manhat += abs(x1-x2) + abs(y1-y2)
        return manhat
        
    def solvePuzzle(self):
        start = []
        goal = []
        filename = input("Enter input file: ")
        myFile = open(filename, 'r')
        Lines = myFile.readlines()
        i = 1
        """ Get start state and goal state from input file """
        for line in Lines:
            myFile.readline();
            line = line.strip().split(' ')
            if i < 4:
                start.append(line);
            elif i > 4 and i < 8:
                goal.append(line)
            i+=1
        start = Node(start,0,0,0,None)
        start.fval = self.f(start,goal)
        
        """ Put the start node in the frontier """
        self.frontier.append(start)
        self.reached[joinstr(start.data)] = start
        """ List object is unhashable in python so joinstr is needed to make a string of the state
            to use as key in reached """
        total_nodes = 1                #including root node
        while len(self.frontier) > 0:
            cur = self.frontier[0]
            """ If h value is 0 then we found the goal node"""
            if(self.h(cur.data,goal) == 0):
                break
            """ Check if child node's state is already in reached, or have a lower level
                than current level in reached, if so, add the node to the frontier """
            for i in cur.generate_child():
                istate = joinstr(i.data)
                if istate not in self.reached or i.level < self.reached[istate].level:
                    self.reached[istate] = i
                    i.fval = self.f(i,goal)
                    self.frontier.append(i)
                    total_nodes += 1       
            del self.frontier[0]
            
            """ Sort the open list by f value so samllest is in the front """
            self.frontier.sort(key = lambda x:x.fval,reverse=False)

        """ Backtrack from goal node to get the solution path """ 
        move_list = []
        f_list = []
        goal_node = cur                   #goal node is cur since the loop breaks when h of cur is 0
        while cur.parent is not None:
            move_list.insert(0,cur.move)  #backtrack so add moves to the front of list
            f_list.insert(0,cur.fval)     #similar for f-value
            cur = cur.parent
        f_list.insert(0,cur.fval)         #f value of start node
        total_nodes = len(self.frontier) + len(self.reached)
    
        """ create and write output file """
        outName = input("Enter output file name: ")
        outFile = open(outName,'w')

        #print start state
        for i in start.data:
            for j in i:
                outFile.write("%s " % j)
            outFile.write("\n")
        outFile.write("\n")

        #print goal state
        for i in goal:
            for j in i:
                outFile.write("%s " % j)
            outFile.write("\n")
        outFile.write("\n")

        #print results
        outFile.write("%s\n" % goal_node.level)
        outFile.write("%s\n" % total_nodes)
        for i in move_list:
            outFile.write("%s " % i)
        outFile.write("\n")
        for i in f_list:
            outFile.write("%s " % i)
        outFile.write("\n")

puz = Puzzle(3)
puz.solvePuzzle()
