import sys
import maze.obstacles as obs

import import_helper
import maze.crazy_world
import maze_operator



obstacles_present = False
if len(sys.argv) > 1 and sys.argv[1] == "turtle":
    import world.turtle.world as module
else:
    import world.text.world as module
    obstacles_present = True

obstacles = []


current_direction_index = 0
command_history = []
robot_name = ""
position_x, position_y = 0, 0


def unpacking_obstacles(obstacles):
    """
    Unpacks the obstacles list
    """

    print("There are some obstacles:")
    for i in obstacles:
        x_coordinates = i[0]
        y_coordinates = i[1]
        print(f"- At position {x_coordinates},{y_coordinates} (to {x_coordinates + 4},{y_coordinates + 4})")


def get_robot_name():
    """
    gets user input and names the robot
    """
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name


def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    Only return a valid command
    """

    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    while len(command) == 0 or not valid_command(command):
        output(robot_name, "Sorry, I did not understand '"+command+"'.")
        command = input(prompt)

    return command.lower()


def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command, as well as the argument(s) for the command
    :return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """
    valid_commands = ['off', 'help', 'replay', 'forward', 'back', 'right', 'left', 'sprint', 'mazerun']

    (command_name, arg1) = split_command_input(command)

    if command_name == 'mazerun':

        if arg1 or not arg1:
            return True


    if command_name.lower() == 'replay':
        if len(arg1.strip()) == 0:
            return True
        elif (arg1.lower().find('silent') > -1 or arg1.lower().find('reversed') > -1) and len(arg1.lower().replace('silent', '').replace('reversed','').strip()) == 0:
            return True
        else:
            range_args = arg1.replace('silent', '').replace('reversed','')
            if is_int(range_args):
                return True
            else:
                range_args = range_args.split('-')
                return is_int(range_args[0]) and is_int(range_args[1]) and len(range_args) == 2
    else:
        return command_name.lower() in valid_commands and (len(arg1) == 0 or is_int(arg1))


def output(name, message):
    """
    prints output to user
    """
    print(''+name+": "+message)


def do_help():
    """
    Provides help information to the user
    :return: (True, help text) to indicate robot can continue after this command was handled
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays all movement commands from history [FORWARD, BACK, RIGHT, LEFT, SPRINT]
"""


def get_commands_history(reverse, relativeStart, relativeEnd, history):
    """
    Retrieve the commands from history list, already breaking them up into (command_name, arguments) tuples
    :param reverse: if True, then reverse the list
    :param relativeStart: the start index relative to the end position of command, e.g. -5 means from index len(commands)-5; None means from beginning
    :param relativeEnd: the start index relative to the end position of command, e.g. -1 means from index len(commands)-1; None means to the end
    :return: return list of (command_name, arguments) tuples
    """
    move_commands = ['forward', 'back', 'right', 'left', 'sprint', 'mazerun']

    commands_to_replay = [(name, args) for (name, args) in list(map(lambda command: split_command_input(command), history)) if name in move_commands]
    if reverse:
        commands_to_replay.reverse()

    range_start = len(commands_to_replay) + relativeStart if (relativeStart is not None and (len(commands_to_replay) + relativeStart) >= 0) else 0
    range_end = len(commands_to_replay) + relativeEnd if  (relativeEnd is not None and (len(commands_to_replay) + relativeEnd) >= 0 and relativeEnd > relativeStart) else len(commands_to_replay)
    return commands_to_replay[range_start:range_end]


def do_replay(robot_name, arguments, position_x, position_y, history, current_direction_index):
    """
    Replays historic commands
    :param robot_name:
    :param arguments a string containing arguments for the replay command
    :return: True, output string
    """

    silent = arguments.lower().find('silent') > -1
    reverse = arguments.lower().find('reversed') > -1
    range_args = arguments.lower().replace('silent', '').replace('reversed', '')

    range_start = None
    range_end = None


    if len(range_args.strip()) > 0:
        if is_int(range_args):
            range_start = -int(range_args)
        else:
            range_args = range_args.split('-')
            range_start = -int(range_args[0])
            range_end = -int(range_args[1])

    commands_to_replay = get_commands_history(reverse, range_start, range_end, history)

    for (command_name, command_arg) in commands_to_replay:
        (do_next, command_output, position_x, position_y, current_direction_index) = call_command(command_name, command_arg, robot_name, position_x, position_y, history, current_direction_index)
        if not silent:
            print(command_output)
            module.show_position(robot_name, position_x, position_y)

    return True, ' > '+robot_name+' replayed ' + str(len(commands_to_replay)) + ' commands' + (' in reverse' if reverse else '') + (' silently.' if silent else '.') ,position_x, position_y, current_direction_index


def call_command(command_name, command_arg, robot_name, position_x, position_y, history, current_direction_index):
    """
    Calls the appropriate command function based on the command name
    """
    
    
    if command_name == 'help':
        conti, outpot = do_help()
        return conti, outpot, position_x, position_y, current_direction_index
    elif command_name == 'forward':
        return module.do_forward(robot_name, int(command_arg), position_x, position_y, current_direction_index)
    elif command_name == 'back':
        return module.do_back(robot_name, int(command_arg), position_x, position_y, current_direction_index)
    elif command_name == 'right':
        return module.do_right_turn(robot_name, current_direction_index, position_x, position_y)
    elif command_name == 'left':
        return module.do_left_turn(robot_name, current_direction_index, position_x, position_y)
    elif command_name == 'sprint':
        return module.do_sprint(robot_name, int(command_arg), position_x, position_y, current_direction_index)
    elif command_name == 'replay':
        return do_replay(robot_name, command_arg, position_x, position_y, history, current_direction_index)
    elif command_name == "mazerun":
        direction = "top"
        directions_dict = {"top": "U", "bottom": "D", "left": "L", "right" : "R"}
        output(robot_name, "starting maze run..")
        direct = "top"
        if command_arg:
            direct = command_arg.lower()
        solve_maze(directions_dict[direct])
        
        return True, ''+robot_name+f': I am at the {direct} edge.', position_x, position_y, current_direction_index

    return False, None


def solve_maze(direction):
    """
        Function solves the maze and runs the robot through it
    """
    global command_history, robot_name, position_x, position_y

    obst_import = maze.crazy_world.get_maze_obstacles()
   

    end_x, end_y = maze_operator.find_edge(direction, obst_import)
    solution = maze_operator.search(direction, position_x, position_y,\
                            end_x, end_y, obst_import)
    wayout = maze_operator.backRoute(solution, end_x, end_y, position_x, position_y)

    run_maze(wayout, direction)
    
    
def turn_robot(command):
    """
        function turns the robot to a given direction
    """
    global current_direction_index, command_history, robot_name, position_x, position_y

    directions_dict = {"U": 0, "R": 1, "D": 2, "L": 3}

    while current_direction_index != directions_dict[command]:
        do_next, position_x, position_y, current_direction_index = handle_command(robot_name, "left", position_x, position_y, command_history, current_direction_index)   


def run_maze(wayout, direction):
    """
        function runs the robot through the maze
    """
    global command_history, robot_name, position_x, position_y, current_direction_index

    for each in wayout:
        command, count = each
        turn_robot(command)
        
        do_next, position_x, position_y, current_direction_index = handle_command(robot_name, "forward "+str(count), position_x, position_y, command_history, current_direction_index)

    turn_robot(direction)

    do_next, position_x, position_y, current_direction_index = handle_command(robot_name, "forward 10", position_x, position_y, command_history, current_direction_index)
    
    
def handle_command(robot_name, command, position_x, position_y, history, current_direction_index):
    """
        Function handles the command and calls the appropriate function
    """

    (command_name, arg) = split_command_input(command)

    if command_name == "mazerun":

        (do_next, command_output, position_x, position_y, current_direction_index) = call_command(command_name, arg, robot_name, position_x, position_y, history, current_direction_index)

    elif command_name == 'off':
        return False, position_x, position_y 
    else:
        (do_next, command_output, position_x, position_y, current_direction_index) = call_command(command_name, arg, robot_name, position_x, position_y, history, current_direction_index)

    
        
    print(command_output)
    module.show_position(robot_name, position_x, position_y)
    add_to_history(command, history)

    return do_next, position_x, position_y, current_direction_index


def add_to_history(command, history):
    """
        Function adds the command to the history
    """
    history.append(command)
    return history


def robot_start():
    """
        Function starts the robot
    """
    
    obstacles = []

    robot_name = get_robot_name()
    obstacles = obs.get_obstacles()
    output(robot_name, "Hello kiddo!")
    
    if "crazy_world" in sys.argv:
        file_to_import = import_helper.import_module("maze.crazy_world")
        output(robot_name, "Loaded crazy_world.")
        obstacles = maze.crazy_world.get_maze_obstacles()
    else:
        output(robot_name, "Loaded obstacles.")

        
    obs.obstacles = obstacles
    if not obstacles_present:
        module.draw_obstacles(obstacles)
        module.obstacles = obstacles
        
    if obstacles:
        unpacking_obstacles(obstacles)

    position_x = 0
    position_y = 0
    current_direction_index = 0
    history = []
    do_next = True

    command = get_command(robot_name)
    if command.lower() == "off":
        do_next = False
    while do_next:
        do_next, position_x, position_y, current_direction_index = handle_command(robot_name, command, position_x, position_y, history, current_direction_index)

        command = get_command(robot_name)
        if command.lower() == "off":
            do_next = False

    output(robot_name, "Shutting down..")


if __name__ == "__main__":
    robot_start()