# cs515_project2

**Connor S. Durkin (cdurkin@stevens.edu)
https://github.com/csdurkin/cs515_project2**

**Hours Estimate**
12 - 16 (Worked throughout two days)

**How Tested**

I conducted thorough testing of my code using the terminal and carefully compared the generated outputs to those listed on the Canva site. I read the tracebacks to pinpoint any incorrect behaviors and then implemented necessary changes within the code. The testing approach involved running the code with different inputs, assessing the results, and iteratively refining the implementation to ensure the desired functionality.

To note, I struggled in implementing the test harness last week. Although I've  marked it as an important task to revisit, my focus this week was on successfully implementing and refining the adventure game. I know I need to learn how to implement the test harness to properly check many scenarios, including the use of valid and invalid inputs.

**Any Bugs or Issues You Could Not Resolve**

First and foremost, my code still fails on the autograder's "test #14 on tunnel.01.in." Therefore, I know there is a bug/issue with my code, and yet, I've been unable to determine what this is.

**An Example of a Difficult Issue or Bug and How You Resolved**

I'll start by noting some new functionalities I learned by doing this project:

- Enumerate: Initially, I attempted to use .items() on the game's map, re: self.game_map.items(), but this failed because the map is an array, not a dictionary. I learned to use enumerate to similarly pull the index and value of the iterable object.
  
- Strip: It's another smaller functionality, but I did not know that strip() could remove the whitespace before and after a string.

The parse and help functions were bigger learning lessons. 

- Parse: For the parse function, I loathed the idea of continued if/elif/else statements and preferred the idea of using a dictionary that could be referenced. The dictionary lists possible inputs and the associated functions. To implement this, I had to learn how to write out the functions in the dictionary and then later write a code that would execute the function with the user's input.

- Help: The requirement for help to be dynamic also made me remember the ability to learn about dir(self) more thoroughly, which pulls attributes and methods from the object in a self-referential act. Staring every command with "cmd_" then allowed for the list of commands to be easily pulled, parsed, and stored in the help's dictionary. The help function also makes use of the docstrings for each method, and I wrote these to be exactly what needs to be included in the dictionary. If the game were to be expanded, it is important to remember to write the docstrings in the methods, but this is an easier task than always remembering to update help.

The biggest issue involved whitespace. 

- Display Room: The method display_room() continued to add a space after each of the printed lines, which did not match what was being produced by the autograder. After going to Sunday's office hours (many thanks for holding these), I realized that this issue needed to be resolved. Previously, I was just adding \n to the strings being printed, but now these prints use "end='\n\n'" to add the needed line breaks without extra spaces. 

**A List of the Extensions You’ve Chosen to Implement**

*Help Verb*

- Description: I added a help verb to assist players by listing valid verbs and their associated shortcuts. These also use ellipses to demonstrate whether the player is expected to provide an argument.
- Usage: Typing "help" or "h" in the game prompts the system to display a list of valid commands.
- Implementation: The help text is dynamically generated based on the defined verbs, each of which is implemented using a name that starts with "cmd_". Therefore, I am able to pull the name of the commands using a for loop and store them in an array. Thereafter, the associated docstring provides the additional text needed. If new verbs are added, they are automatically included in the help text, as long as they follow these formatting principles.
  
*Directions as Verbs*

- Description: I implemented the use of exit directions as standalone verbs (e.g., "north" instead of "go north"). I also included shortcuts for these, so 'n' could be typed instead of 'north,' for example.
- Usage: Typing the exit direction or the first initial of the diction allows the player to move in that direction. These directional commands are therefore: 'north', 'n', 'south', 's', 'east', 'e', 'west', 'w'
- Implementation: I implemented this by adding additional functions to the object and included these within the dictionary (commands_dict), which is used in the parse_input function. When the player types in the direction or the associated abbreviation, these commands are called, which subsequently call the go command using the correct direction.
- Possible Improvement: As I wrote that last sentence, I realized the code could likely be implemented in a more efficient manner by simply using the go command as the values for the directional indexes within the command_dict. Respectfully, I am not going to make these changes now, because my code is working well and the assignment is due shortly.

*Drop Verb*
- Description: I created a drop verb to allow players to remove items from their inventory and leave them within the room that they are in. It's basically the opposite of the get command.
- Usage: Typing "drop [item]" puts the specified item from the player's inventory into the current room. If the item is not within the inventory, this will notification will be printed out.
- Implementation: Drop verb only allows dropping items from the inventory, and the dropped item is visible in the room description after executing the "look" command. It's implemented by confirming the item is within the inventory, adding it to the current room's items, and removing it from the player's inventory.


***A Partially Implemented Extension**

As I was working alone, I needed to implement three extensions fully. I did start working on the extension to use abbreviations for verbs and directions before settling on the three listed above. In short, I did not implement abbreviations for items. Nevertheless, you can still choose to use the implemented abbreviations with the gameplay. The abbreviations for the directions can also be used by themselves without the go command.

- 'd' for 'drop'
- 'e' for 'east'
- 'h' for 'help'
- 'i' for 'inventory'
- 'l' for 'look'
- 'n' for 'north'
- 'q' for 'quit'
- 's' for 'south'
- 'w' for 'west'
