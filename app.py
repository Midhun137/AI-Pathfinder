from flask import Flask, render_template, request, jsonify
import heapq
import time

app = Flask(__name__)

ROWS = 18
COLS = 24

def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def neighbors(node,maze):
    r,c=node
    moves=[(0,1),(1,0),(0,-1),(-1,0)]

    for dr,dc in moves:
        nr=r+dr
        nc=c+dc

        if 0<=nr<ROWS and 0<=nc<COLS:
            if maze[nr][nc]==0:
                yield (nr,nc)

def solve_astar(maze,start,goal,algo):

    open_list=[]
    heapq.heappush(open_list,(0,start))

    came={}
    cost={start:0}
    visited=[]
    nodes=0

    start_time=time.time()

    while open_list:

        _,current=heapq.heappop(open_list)

        if current in visited:
            continue

        visited.append(current)
        nodes+=1

        if current==goal:
            break

        for nb in neighbors(current,maze):

            new_cost=cost[current]+1

            if nb not in cost or new_cost<cost[nb]:

                cost[nb]=new_cost

                if algo=="A*":
                    priority=new_cost+heuristic(nb,goal)
                elif algo=="Dijkstra":
                    priority=new_cost
                else:
                    priority=heuristic(nb,goal)

                heapq.heappush(open_list,(priority,nb))
                came[nb]=current

    path=[]
    node=goal

    while node in came:
        path.append(node)
        node=came[node]

    path.reverse()

    end=time.time()

    return {
        "visited":visited,
        "path":path,
        "nodes":nodes,
        "time":round(end-start_time,4),
        "length":len(path)
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve",methods=["POST"])
def solve():

    data=request.get_json()

    maze=data["maze"]
    start=tuple(data["start"])
    goal=tuple(data["goal"])
    algo=data["algorithm"]

    result=solve_astar(maze,start,goal,algo)

    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)