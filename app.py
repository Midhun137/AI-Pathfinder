from flask import Flask, render_template, request, jsonify
import heapq
import time

app = Flask(__name__)

ROWS = 18
COLS = 24


def get_neighbors(node, grid):

    r, c = node

    directions = [(0,1),(1,0),(0,-1),(-1,0)]

    for dr,dc in directions:

        nr = r + dr
        nc = c + dc

        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 0:

            yield (nr,nc)


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():

    data = request.get_json()

    grid = data["grid"]
    start = tuple(data["start"])
    goal = tuple(data["goal"])
    algo = data["algorithm"]

    start_time = time.perf_counter()

    visited_order = []
    came_from = {}

    # ------------------ A STAR ------------------

    if algo == "A*":

        pq = [(0,start)]
        g_score = {start:0}

        while pq:

            _, curr = heapq.heappop(pq)

            if curr in visited_order:
                continue

            visited_order.append(curr)

            if curr == goal:
                break

            for nb in get_neighbors(curr,grid):

                temp = g_score[curr] + 1

                if nb not in g_score or temp < g_score[nb]:

                    g_score[nb] = temp

                    f = temp + abs(nb[0]-goal[0]) + abs(nb[1]-goal[1])

                    heapq.heappush(pq,(f,nb))

                    came_from[nb] = curr


    # ------------------ DIJKSTRA ------------------

    elif algo == "Dijkstra":

        pq = [(0,start)]
        dist = {start:0}

        while pq:

            cost, curr = heapq.heappop(pq)

            if curr in visited_order:
                continue

            visited_order.append(curr)

            if curr == goal:
                break

            for nb in get_neighbors(curr,grid):

                new_cost = dist[curr] + 1

                if nb not in dist or new_cost < dist[nb]:

                    dist[nb] = new_cost

                    heapq.heappush(pq,(new_cost,nb))

                    came_from[nb] = curr


    # ------------------ GREEDY BFS ------------------

    elif algo == "Greedy":

        pq = [(0,start)]
        visited = set()

        while pq:

            _, curr = heapq.heappop(pq)

            if curr in visited:
                continue

            visited.add(curr)
            visited_order.append(curr)

            if curr == goal:
                break

            for nb in get_neighbors(curr,grid):

                if nb not in visited:

                    h = abs(nb[0]-goal[0]) + abs(nb[1]-goal[1])

                    heapq.heappush(pq,(h,nb))

                    came_from[nb] = curr


    # ------------------ BUILD PATH ------------------

    path = []
    curr = goal

    while curr in came_from:

        path.append(curr)
        curr = came_from[curr]

    if path:
        path.append(start)

    path.reverse()

    runtime = f"{(time.perf_counter()-start_time)*1000:.2f} ms"

    return jsonify({

        "visited": visited_order,
        "path": path,
        "time": runtime

    })


if __name__ == "__main__":

    app.run(debug=True)
