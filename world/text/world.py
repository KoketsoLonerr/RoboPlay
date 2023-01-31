import maze.obstacles


obstacles = []
directions = ['forward', 'right', 'back', 'left']

def show_position(robot_name, position_x, position_y):
    """
    prints position of the robot to the user
    """
    print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    
    """
    min_y, max_y = -200, 200
    min_x, max_x = -100, 100

    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


def update_position(robot_name, steps, position_x, position_y, current_direction_index):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """


    new_x = position_x
    new_y = position_y
    obstacle_present = False

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
        if maze.obstacles.is_position_blocked(new_x, new_y) or maze.obstacles.is_path_blocked(new_x, position_y, new_x, new_y):
            obstacle_present = True
        
 
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
        if maze.obstacles.is_position_blocked(new_x, new_y) or maze.obstacles.is_path_blocked(position_x, new_y, new_x, new_y):
            obstacle_present = True
    
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
        if maze.obstacles.is_position_blocked(new_x, new_y) or maze.obstacles.is_path_blocked(new_x, new_y, new_x, position_y):
            obstacle_present = True
        
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps
        if maze.obstacles.is_position_blocked(new_x, new_y) or maze.obstacles.is_path_blocked(new_x, new_y, position_x, new_y):
            obstacle_present = True
                
    if is_position_allowed(new_x, new_y) and not obstacle_present:
        position_x = new_x
        position_y = new_y
        return True, position_x, position_y, obstacle_present
    return False, position_x, position_y, obstacle_present



def do_forward(robot_name, steps, position_x, position_y, current_direction_index):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    update, position_x, position_y, obstacle = update_position(robot_name, steps, position_x, position_y, current_direction_index)
    if obstacle:
        return True, ' > '+robot_name+' Sorry, there is an obstacle in the way.', position_x, position_y, current_direction_index
    elif update:
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.', position_x, position_y, current_direction_index
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.', position_x, position_y, current_direction_index


def do_back(robot_name, steps, position_x, position_y, current_direction_index):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    update, position_x, position_y, obstacle = update_position(robot_name, -steps, position_x, position_y, current_direction_index)

    if obstacle:
        return True, ' > '+robot_name+' Sorry, there is an obstacle in the way.', position_x, position_y, current_direction_index
    elif update:
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.', position_x, position_y, current_direction_index
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.', position_x, position_y, current_direction_index


def do_right_turn(robot_name, current_direction_index, position_x, position_y):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """

    current_direction_index += 1
    if current_direction_index > 3:
        current_direction_index = 0

    return True, ' > '+robot_name+' turned right.', position_x, position_y, current_direction_index


def do_left_turn(robot_name, current_direction_index, position_x, position_y):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """

    current_direction_index -= 1
    if current_direction_index < 0:
        current_direction_index = 3

    return True, ' > '+robot_name+' turned left.', position_x, position_y, current_direction_index

def do_sprint(robot_name, steps, position_x, position_y, current_direction_index):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1, position_x, position_y, current_direction_index)
    else:
        (do_next, command_output,  position_x, position_y, current_direction_index) = do_forward(robot_name, steps, position_x, position_y, current_direction_index)
        print(command_output)
        return do_sprint(robot_name, steps - 1, position_x, position_y, current_direction_index)

        

