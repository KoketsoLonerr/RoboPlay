import random

obstacles = []

def get_obstacles():
    """
    Returns list of obstacles
    """
    random_num = random.randint(2, 10)
    if random_num == 0:
        return []
    for i in range(random_num):
        obstacles.append((random.randint(-100, 100), random.randint(-200, 200)))
    return obstacles

    
def is_position_blocked(x,y):
    """
    Checks if position is blocked with an obstacle
    """
    for obstacle in obstacles:
        if x in range(obstacle[0], obstacle[0] + 5) and y in range(obstacle[1], obstacle[1] + 5):
            return True


def is_path_blocked(x1,y1, x2, y2):
    """
    Checks if path between two points is blocked with an obstacle
    """
    if y1 == y2:
        if max(x1, x2) == x2:
            for x in range(x1, x2):
                if is_position_blocked(x, y1):
                    return True
        if max(x1, x2) == x1:
            for x in range(x2, x1):
                if is_position_blocked(x, y1):
                    return True
    if x1 == x2:
        if max(y1, y2) == y1:
            for y in range(y2, y1):
                if is_position_blocked(x1, y):
                    return True
        if max(y1, y2) == y2:
            for y in range(y1, y2):
                if is_position_blocked(x1, y):
                    return True 