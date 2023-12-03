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
                self.validate_map()

        except FileNotFoundError:
            print(f"Error: Map file '{map_filename}' not found.")

        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in map file '{map_filename}'.")


    def validate_map(self):
       
        room_validation = True

        if not self.game_map:
            print("Error: There is no game map initialized.")
            room_validation = False
            return False
       
        for room_id, room_data in enumerate(self.game_map):  
            
            required_properties = ["name", "desc", "exits"]
            missing_properties = [property for property in required_properties if property not in room_data]

            if missing_properties:
                room_validation = False
                for property in missing_properties:
                    print(f'Error: The room {room_id} is missing {property} property.')
                
        if room_validation:
           return True
        
        else:
            return False


    def display_room(self):
        print(">", self.game_map[self.current_room].get("name", ""))
        print("\nCurrent Room Description:", self.game_map[self.current_room].get("desc", ""))
        print("\nExits:", ' '.join(self.game_map[self.current_room].get("exits", {}).keys() or ["No Exits"]))
        print("\nItems:", ", ".join(self.game_map[self.current_room].get("items", ["No Items"])))


    def parse_input(self, player_input):
        
        commands_dict = {
            'drop': self.cmd_drop,
            'd': self.cmd_drop,  
            'get': self.cmd_get,
            'go': self.cmd_go,
            'help': self.cmd_help,
            'h': self.cmd_help,
            'i': self.cmd_inventory,
            'inventory': self.cmd_inventory,
            'l': self.cmd_look,
            'look': self.cmd_look,
            'q': self.cmd_quit,
            'quit': self.cmd_quit,
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
                print(f'Only one word can follow an input command.\nIn this case, the input"{player_command} {player_argument}" will be attempted.') 
            else: 
                player_argument = None
            
            if player_command in commands_dict:
                commands_dict[player_command](player_argument)
            else:
                print("Invalid command provided. Type 'help' for a list of commands.")

        else:
            print("Please provide a valid command. Type 'help' for a list of commands.")


    def cmd_drop(self, player_argument):

        """drop ... [shortcut: d ...]"""

        if player_argument in self.inventory:
            self.game_map[self.current_room]["items"].append(player_argument)
            self.inventory.remove(player_argument)
            print(f'You\'ve removed the {player_argument} from your inventory. It\'s been left in the {self.game_map[self.current_room].get("name", "current room")}.')

        else:
            print(f'No {player_argument} can be found in your inventory.')


    def cmd_get(self, player_argument):

        """get ..."""
        
        if player_argument in self.game_map[self.current_room].get("items", []):
            self.game_map[self.current_room]["items"].remove(player_argument)
            self.inventory.append(player_argument)
            print(f'You\'ve added the {player_argument} to your inventory.')

        else:
            print(f'No {player_argument} can be found in this room.')


    def cmd_go(self, player_argument):

        """go ..."""
        
        if not player_argument: 
            print('You need to go somewhere.')

        elif (player_argument in self.game_map[self.current_room].get("exits", [])):
            self.current_room = self.game_map[self.current_room]["exits"][player_argument]
            self.display_flag = True
            print(f'You head {player_argument}.')

        else:
            print(f'You cannot head {player_argument}.')


    def cmd_help(self, player_argument):

        """help ... [shortcut: h ...]"""
            
        commands = [function[4:] for function in dir(self) if function.startswith('cmd_')]
        
        print(f'You can use the following commands:')

        for command in commands: 
            
            print(getattr(self, f'cmd_{command}', None).__doc__)

    def cmd_inventory(self, player_argument):
        
        """inventory [shortcut: i]"""

        if self.inventory: 
            print(self.inventory)

        else:
            print('No items inventory.')


    def cmd_look(self, player_argument):
        
        """look [shortcut: l]"""

        self.display_room()


    def cmd_quit(self):
        
        """quit [shortcut: q]"""
        
        print("You're trap here forever.\n\nJust kidding. Goodbye!")
        exit()


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
                print("You're never getting out of this grocery store.\n\nUnless you type 'quit' to exit.")

            except KeyboardInterrupt:
                print("\nGame ended by keyboard interrupt. Goodbye!")
                exit()

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")

    else:
        game = AdventureGame()
        game.load_world(sys.argv[1])
        game.loop_game()