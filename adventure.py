import sys
import json


class AdventureGame:

    #__init__: Initializes the AdventureGame object, sets initial state of play
    
    def __init__(self):
        self.current_room = 0
        self.inventory = []
        self.game_map = {}
        self.display_flag = True                            #Flags whether to display room info again or not


   #load_world: Re-intializes player's state with new map

    def load_world(self, map_filename):
        
        try:
            
            with open(map_filename, 'r') as file:
                
                self.game_map = json.load(file)
                return self.validate_map()

        except FileNotFoundError:
            print(f"Error: Map file '{map_filename}' not found.")
            return False

        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in map file '{map_filename}'.")
            return False


    def validate_map(self):
       
        room_validation = True

        if not self.game_map:
            room_validation = False
            raise ValueError("Error: There is no game map initialized.")
       
        for room_id, room_data in enumerate(self.game_map):  
            
            required_properties = ["name", "desc", "exits"]
            missing_properties = [property for property in required_properties if property not in room_data]

            if missing_properties:
                room_validation = False
                for property in missing_properties:
                    print(f'> Error: The room {room_id} is missing {property} property.')
                
        return room_validation


    def display_room(self):
    
        try:
            
            room_data = self.game_map.get(self.current_room) or self.game_map[self.current_room]
            
            print(f'> {room_data.get("name", "")}\n')
            
            print(room_data.get("desc", ""), "\n")

            if room_data.get("items", None):
                print("Items:", ", ".join(room_data.get("items", ["No Items"])), "\n")

            if room_data.get("exits", None):
                print("Exits:", ' '.join(room_data.get("exits", {}).keys() or ["No Exits"]), "\n")

        except KeyError:
            print(f"> Error: The room {self.current_room} is missing some properties.")


    def parse_input(self, player_input):
        
        commands_dict = {
            'drop': self.cmd_drop,
            'd': self.cmd_drop,
            'east': self.cmd_east,
            'e': self.cmd_east,  
            'get': self.cmd_get,
            'go': self.cmd_go,
            'help': self.cmd_help,
            'h': self.cmd_help,
            'i': self.cmd_inventory,
            'inventory': self.cmd_inventory,
            'l': self.cmd_look,
            'look': self.cmd_look,
            'north': self.cmd_north,
            'n': self.cmd_north,
            'q': self.cmd_quit,
            'quit': self.cmd_quit,
            'south': self.cmd_south,
            's': self.cmd_south,
            'west': self.cmd_west,
            'w': self.cmd_west,
        }

        split_input = player_input.strip().lower().split()        #strip: removes white space before/after input; lower(): to make case-insensitiv

        if split_input:

            player_command = split_input[0]

            if player_command == 'quit':
                self.cmd_quit()
            
            if len(split_input) == 2:
                player_argument = split_input[1]
            elif len(split_input) > 2:
                player_argument = split_input[1]
                print(f'> Only one word can follow an input command.\nIn this case, the input"{player_command} {player_argument}" will be attempted.') 
            else: 
                player_argument = None
            
            if player_command in commands_dict:
                commands_dict[player_command](player_argument)
            else:
                print("> Invalid command provided. Type 'help' for a list of commands.")

        else:
            print("> Please provide a valid command. Type 'help' for a list of commands.")


    def cmd_drop(self, player_argument):

        """drop ... [shortcut: d ...]"""

        if player_argument in self.inventory:
            self.game_map[self.current_room]["items"].append(player_argument)
            self.inventory.remove(player_argument)
            print(f'You\'ve removed the {player_argument} from your inventory. It\'s been left in the {self.game_map[self.current_room].get("name", "current room")}.')

        else:
            print(f'No {player_argument} can be found in your inventory.')


    def cmd_east(self, player_argument):
        
        """east [shortcut: e]"""

        self.cmd_go('east')


    def cmd_get(self, player_argument):

        """get ..."""
        
        if player_argument == None:
            print('Sorry, you neet to \'get\' something.')
        
        elif player_argument in self.game_map[self.current_room].get("items", []):
            self.game_map[self.current_room]["items"].remove(player_argument)
            self.inventory.append(player_argument)
            print(f'You pick up the {player_argument}.')

        else:
            print(f'There\'s no {player_argument} anywhere.')


    def cmd_go(self, player_argument):

        """go ..."""
        
        if not player_argument: 
            print('Sorry, you need to \'go\' somewhere.')

        elif (player_argument in self.game_map[self.current_room].get("exits", [])):
            self.current_room = self.game_map[self.current_room]["exits"][player_argument]
            self.display_flag = True
            print(f'You go {player_argument}.\n')

        else:
            print(f'There\'s no way to go {player_argument}.')


    def cmd_help(self, player_argument):

        """help ... [shortcut: h ...]"""
            
        commands = [function[4:] for function in dir(self) if function.startswith('cmd_')]
        
        print(f'You can use the following commands:')

        for command in commands: 
            
            print(getattr(self, f'cmd_{command}', None).__doc__)

    def cmd_inventory(self, player_argument):
        
        """inventory [shortcut: i]"""

        if self.inventory: 
            print('Inventory:')
            for item in self.inventory:
                print(' ', item)

        else:
            print('You\'re not carrying anything.')


    def cmd_look(self, player_argument):
        
        """look [shortcut: l]"""

        self.display_room()


    def cmd_north(self, player_argument):
        
        """north [shortcut: n]"""

        self.cmd_go('north')


    def cmd_quit(self):
        
        """quit [shortcut: q]"""
        
        print('Goodbye!')
        sys.exit(0)


    def cmd_south(self, player_argument):
        
        """south [shortcut: s]"""

        self.cmd_go('south')  


    def cmd_west(self, player_argument):
        
        """west [shortcut: w]"""

        self.cmd_go('west')      


    def loop_game(self):

        while True:

            try:

                if self.display_flag:
                    self.display_room()
                    self.display_flag = False
            
                player_input = input("What would you like to do? ")
            
                self.parse_input(player_input)

                if not player_input:
                    print("Please enter a valid command.")
                    continue

            except EOFError:
                print('\nUse \'quit\' to exit.')

            except KeyboardInterrupt:
                print('Traceback (most recent call last):')
                print('  ...')
                print('KeyboardInterrupt')
                print('Goodbye!')
                sys.exit(1)

if __name__ == "__main__":
    
    try:
    
        if len(sys.argv) != 2:
            print("Usage: python3 adventure.py [map filename]")

        else:
            game = AdventureGame()
            game.load_world(sys.argv[1])
            game.loop_game()
            
    except ValueError as e:
        print(f'Error: {str(e)}')

