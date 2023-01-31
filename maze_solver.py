from collections import deque
import maze.obstacles

def find_edge(direction, obst_import):
    """
        This function finds the edge of the maze in the direction given
    """
    direction_dict = {"U": (-100,200), "D": (-100,-200), \
                        "R": (100,-200), "L": (-100,-180)}
    x, y  = direction_dict[direction]

    if direction == "U" or direction == "D":
        while maze.obstacles.is_position_blocked(x,y):
            x += 4
    else:
        while maze.obstacles.is_position_blocked(x,y):
            y += 4 
             
    return (x, y)


def compress_instrc(instruct, output_list):
    """
        This function compresses the instructions list
    """
    while True:
        if len(instruct) == 1:
            break

        count = 0
        command = instruct[0]
        while command == instruct[0]:
            count += 4
            command = instruct.pop(0)

        output_list.append((command, count))

    return output_list


def append_handler(value1, value2, positive, negative):
    """
        This function appends the correct instruction to the list
    """
    if value1 < value2:
        return positive
    else:
        return negative


def make_instructions(wayout, instruct):
    """
        This function makes the instructions list
    """
    for j in range(0, len(wayout)-1):

        if wayout[j][0] == wayout[j+1][0]:
            instruct.append(append_handler(wayout[j][1],\
                                    wayout[j+1][1],"U","D"))
        else:
            instruct.append(append_handler(wayout[j][0],\
                                    wayout[j+1][0],"R","L"))

    instruct.append("")

    return compress_instrc(instruct, [])


def backRoute(solution, end_x, end_y, x, y):
    """
        This function backtracks the solution dict to find the route
    """
    wayout = [(x,y)]
    print(solution)

    while (x, y) != (end_x, end_y):
        x, y = solution[x, y] 
        wayout.append((x,y))

    return make_instructions(wayout, [])


def do_x_y(x, y, todo, step):
    """
        This function returns the x and y values of the next cell
    """
    direction_dict = {"U": (x,y+step), "D": (x,y-step), \
                        "R": (x+step,y), "L": (x-step,y)}
    
    return direction_dict[todo]


def search(direction, start_x, start_y, end_x, end_y, obst_import):
    """
        This function searches for the shortest path
    """
    frontier = deque()
    solution = dict()
    visited = set()

    x = end_x
    y = end_y    

    frontier.append((x, y))
    solution[x,y] = x,y

    while len(frontier) > 0:
        x, y = frontier.popleft()

        for j in ["U", "R", "D", "L"]:
            cell = do_x_y(x, y, j, 2)
            if not maze.obstacles.is_path_blocked(x,y, cell[0], cell[1]) and\
                (-101 <= cell[0] <= 101 and -201 <= cell[1] <= 201) and\
                                                 cell not in visited:
                solution[cell] = x, y    
                frontier.append(cell)
                visited.add(cell)

    return solution