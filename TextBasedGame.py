# Christopher O'Dell
# IT-140 Module 7 - Text Based Game

rooms = {  # Dictionary for rooms and their connections / items
    'Arithmetic Atrium': {'North': 'Geometry Gateway', 'South': 'Trigonometry Tower',
                          'East': 'Limit Labyrinth', 'West': 'Algebraic Archives'},
    'Algebraic Archives': {'East': 'Arithmetic Atrium', 'item': 'Algebra Amulet'},
    'Geometry Gateway': {'South': 'Arithmetic Atrium', 'East': 'Probability Parlor',
                         'item': 'Geometric Gem'},
    'Probability Parlor': {'West': 'Geometry Gateway', 'item': 'Destiny Dice'},
    'Trigonometry Tower': {'North': 'Arithmetic Atrium', 'East': 'Number Nexus',
                           'item': 'Trigonic Triangle'},
    'Number Nexus': {'West': 'Trigonometry Tower', 'item': 'Prime Prism'},
    'Limit Labyrinth': {'West': 'Arithmetic Atrium', 'East': 'Calculus Catacombs',
                        'item': 'Limit Lantern'},
    'Calculus Catacombs': {'West': 'Limit Labyrinth', 'item': 'The Evil Lord Calculus'}  # Villain / Final Room
}
inventory = []
DIRECTIONS = ['go north', 'go south', 'go east', 'go west']
ITEM_COMMAND = "get"
EXIT_COMMAND = "exit"
VALID_INPUTS = DIRECTIONS + [ITEM_COMMAND] + [EXIT_COMMAND]
INVALID_DIRECTION = "That is not a valid direction. You need to enter one of: " + \
                    str(VALID_INPUTS) + "."
CANNOT_GO_THAT_WAY = "You bumped into a wall."
GAME_OVER = "Thanks for playing."
EXIT_ROOM_SENTINEL = "exit"
STARTING_ROOM = list(rooms)[0]

current_room = STARTING_ROOM


def print_colored_word(sentence, color, word=None):
    color_code = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }

    # Check if the specified color is supported
    if color not in color_code:
        print("Invalid color")
        return

    # Replace the word with the colored version
    colored_word = f"{color_code[color]}{word}{color_code['reset']}"
    colored_sentence = sentence.replace(word, colored_word)

    print(colored_sentence)


def show_instructions():
    # Print the main menu and commands
    print('*' * 75)
    print("""
The Evil Lord Calculus - Text Adventure Game
Collect 6 items to win the game, or be conquered by The Evil Lord Calculus.
Move commands: go South, go North, go East, go West
Add to Inventory: get 'item name'
To exit the game, type: exit
""")
    print('*' * 75)


def get_current_status():
    global current_room
    print(f'You are in the {current_room}.')
    if 'item' in rooms[current_room]:
        print_colored_word(f'This room contains a {rooms[current_room]['item']}.',
                           "purple", rooms[current_room]['item'])
    print(f'Your inventory: {inventory}.')
    print('-' * 40)


def navigate(curr_room: str, user_input: str):
    next_room = curr_room
    err_msg = ''

    # Convert user input to lowercase
    user_input_lower = user_input.lower()

    # Check for valid user input
    if user_input_lower in VALID_INPUTS:
        # Logic for executing a valid move
        if user_input_lower.startswith('go '):
            direction = user_input_lower[3:]
            if direction.capitalize() in rooms[curr_room]:
                next_room = rooms[curr_room][direction.capitalize()]
            else:
                err_msg = CANNOT_GO_THAT_WAY
        # Logic for executing an invalid direction
        else:
            err_msg = INVALID_DIRECTION
    else:
        # Do not execute move. Send a message to the user about an invalid direction entered.
        err_msg = INVALID_DIRECTION

    # Return next room and error message (if applicable)
    return next_room, err_msg


def get_item(item: str):
    global current_room, inventory
    # Capitalize each word in the item name
    requested_item = ' '.join(word.capitalize() for word in item.split()[1:])
    # Check if the current room has the specified item
    if 'item' in rooms[current_room] and requested_item == rooms[current_room]['item']:
        # Add the item to the inventory
        inventory.append(requested_item)
        print_colored_word(f'You picked up {requested_item}.', "purple", requested_item)
        # Remove the item from the room
        del rooms[current_room]['item']
        get_current_status()
    else:
        # Print cannot pick up item statements
        if requested_item in inventory:
            print(f'You already picked up the {requested_item}.')
        else:
            print(f'There is no {requested_item} here.')


def main():
    show_instructions()
    get_current_status()
    while True:
        # Get user input
        user_input = input("Enter your command: ").strip().lower()

        # Check if the user has decided to exit the game
        if user_input.startswith('exit'):
            print_colored_word(GAME_OVER, "cyan", GAME_OVER)
            break

        # Handle user input for get 'item'
        if user_input.startswith('get '):
            get_item(user_input)

        # Handle user input for movement / exit
        if user_input.startswith('go '):
            global current_room
            next_room, error_message = navigate(current_room, user_input)

            # Update the current room if the user provided a valid input
            if not error_message:
                current_room = next_room
                get_current_status()
                # Check if the player has won
                if current_room == 'Calculus Catacombs':
                    if len(inventory) == len(rooms) - 2:
                        print_colored_word("Congratulations! You have collected all items and defeated The Evil"
                                           " Lord Calculus. You win!", "green", "Congratulations!")
                        break
                    else:
                        print_colored_word("The Evil Lord Calculus has vanquished the mathematical realms!"
                                           " GAME OVER.", "red", "GAME OVER")
                        break

            # Print error message for invalid input
            if error_message:
                print(error_message)


main()
