# monkeys on typewriter
# this code is straight buns
import random

possible_characters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", ",", ".", "\'"]
                       
                       

target_string = "BANANAS"
MAX_CHARS = len(target_string)

current_string = ""
total_characters = 0


try:
    while current_string != target_string:
        current_string = current_string + random.choice(possible_characters)
        total_characters += 1
        
        if total_characters % 10000000 == 0:
            print(f"Total characters attempted: {total_characters:,}")
            
        if len(current_string) > MAX_CHARS:
            current_string = ""
            
        
    print(f"!! FOUND {target_string} after {total_characters:,} character attempts !!")
    
except KeyboardInterrupt:
    print(f"Stopped manually after {total_characters:,} character attempts")
        