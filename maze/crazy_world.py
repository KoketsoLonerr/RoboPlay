import random
obstacles = []
obstacle = ()

global list_of_obstacles
list_of_obstacles = []

def read_text():
    """
        function reads maze.txt and returns list of lines
    """
    with open("maze/maze.txt", "r") as file:
        file = file.readlines()

    final_file = []
    for line in file:

        final_file.append(line.replace('\n', ''))

    return final_file

def get_maze_obstacles():
    """
        function reads maze.txt and returns list of obstacles
    """

    final_file = read_text()
    obstacles = []

    for y in range(len(final_file)):
        for x in range(len(final_file[y])):

            if final_file[y][x] == "X":

                obstacles.append((x*4 - 100, y*-4 + 196))

    return obstacles


def create_random_obstacles():
    """
        function creates random obstacles
    """
    random_num = random.randint(0, 10)
    obstacles= []
    if random_num==0:
        return[]
    for i in range(random_num):
        obstacles.append((random.randint(-100, 96), random.randint(-200, 196)))
    return obstacles


def is_position_blocked(x, y):
    """
        function checks if position is blocked with an obstacle
    """
    global list_of_obstacles

    for obstacles in list_of_obstacles:
        if x in range(obstacles[0], obstacles[0]+5) and y in range(obstacles[1], obstacles[1]+5):
            return True

    return False

def is_path_blocked(x1,y1, x2, y2):
    """
        function checks if path between two points is blocked with an obstacle
    """
    for obstacle in obstacles:
        if x1 == x2 and x1 in range(obstacle[0], obstacle[0] + 5) and obstacle[1] in range(y1, y2 + 1):
            return True
        if y1 == y2 and y1 in range(obstacle[1], obstacle[1] + 5) and obstacle[0] in range(x1, x2 + 1):
            return True