# placeholder
import heapq


def heuristic(a, b):
    # Euclidean heuristic for A*
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5


def astar(start, goal, blocked_cells):
    """
    A* Algorithm on a simple grid.
    For PostGIS routing, swap with pgRouting.
    """

    neighbors = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for dx, dy in neighbors:
            next_cell = (current[0] + dx, current[1] + dy)

            if next_cell in blocked_cells:
                continue

            new_cost = g[current] + heuristic(current, next_cell)

            if next_cell not in g or new_cost < g[next_cell]:
                g[next_cell] = new_cost
                f = new_cost + heuristic(goal, next_cell)
                heapq.heappush(open_set, (f, next_cell))
                came_from[next_cell] = current

    return []


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def compute_rescue_route():
    """
    For demo:
    Returns a static route. In production, use A* or pgRouting.
    """

    return [
        {"team": "A1", "route": ["90.41,23.81", "90.415,23.815", "90.42,23.82"], "eta_min": 12},
        {"team": "B2", "route": ["90.40,23.80", "90.405,23.805", "90.41,23.81"], "eta_min": 15},
    ]
