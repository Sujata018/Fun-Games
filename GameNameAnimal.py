''' This game starts with the user typing a name of an animal, the program
    types the name of another animal starting with the last later of the animal
    user typed. Then user needs to type name of another animal starting with
    last letter of the animal name typed before. No animal name can be repeated.
    If one can not type an animal, and the other can give a name, then the other wins!

    sample game: Tie
    Program : Elephant
    User    : Tortoise
    Program : Elk
    User : No input
    Program : No input
    
    
'''

from DictionariesAnimals import animals
from DictionariesAnimals import birds
from DictionariesAnimals import insects
from DictionariesAnimals import fishes
from DictionariesAnimals import reptiles

def getAnimal(ch):  # This function gets a new animal name from the animal directory, starting the the letter passed as parameter.

    result = ''
    if ch == "":
        ch = "b"
    ch = ch.lower()
    for animal in animals[ch].keys():
        if animals[ch][animal] == 0:
            result = animal
            animals[ch][animal] = 1
            break
    return result

def updateAnimal(animal): # This function marks an animal as used.
    
    animals[animal[0:1]][animal] = 1

def validateAnimal(animal, startsWith = ""):                 # Validates the animal user enterd. Pass nothing in 2nd parameter for the first entry by user.
                                                             # Returns 1 in case the animal is invalid, returns 0 for valid animal.
    animal = animal.lower()                                  # convert to lower letters
    if startsWith == "":
        expected_first_letter = animal[0:1]                  # if it is enters by user for the first time, then no check on first letter of the animal
    else:
        expected_first_letter = startsWith.lower()           # else check if the animal starts with the last letter of the last animal entered

    printString = ""
    if animal[0:1] != expected_first_letter:
        printString = animal[0:1].upper()+animal[1:] + " doesn't start with " + expected_first_letter
        return 1, printString
    if animal not in animals[expected_first_letter].keys():  # Invalid animal not present in animals directory
        printString = animal[0:1].upper()+animal[1:] + " is not an animal."
        if animal in birds[expected_first_letter].keys():    # but present in birds / fishes / reptiles etc other directories
            printString += " It's a bird!"
        if animal in insects[expected_first_letter].keys():
            printString += " It's an insect!"
        if animal in fishes[expected_first_letter].keys():
            printString += " It's a fish!"
        if animal in reptiles[expected_first_letter].keys():
            printString += " It's a reptile!"
        return 1, printString
    if animal in animals[expected_first_letter].keys():     # Animal is present in animals directory,
        if animals[expected_first_letter][animal] == 1 :    # but already used earlier
            printString = animal[0:1].upper()+ animal[1:] + " is already used in this game."
            return 1, printString
        else:
            updateAnimal(animal)                            # If valid animal entered, then mark the animal as used in animal database, and return 0
            return 0, ""

''' This is the main function. '''

if __name__ == '__main__':
        
    gameOn = True
    firstInstruction = True
    invalidEntryCount = 0
    last_letter = ""
    while gameOn:
        if firstInstruction:
            print("You type a name of an animal, I type another starting with your last letter, then you type another.")
            print("Who gives up first, looses.")
            print("Let's start!!")
            uAnimal = input("Enter name of an animal:")
            firstInstruction = False
            i,p = validateAnimal(uAnimal)
        
        else:
            if invalidEntryCount > 0:
                print("You can try ", 3 - invalidEntryCount, " more times, then you loose ..")
            if last_letter == "":
                uAnimal = input("Type name of an animal :")
            else:
                uAnimal = input("Type an animal starting with %s :" %last_letter)
            i,p = validateAnimal(uAnimal,last_letter)
        
        if p > "":
            print(p)
        if i == 0:                                              # if valid animal is entered by user, program plays the game
            invalidEntryCount = 0
            last_letter = uAnimal[-1:].lower()                  
            iAnimal = getAnimal(last_letter)
            if iAnimal == '':
                print("I give up, you win! ")
                gameOn = False
            else:
                print(iAnimal[0:1].upper() + iAnimal[1:].lower())
                last_letter = iAnimal[-1:].upper()
        else:
            invalidEntryCount += i                              # for invalid entries, user is given 3 chances to re-enter

        if invalidEntryCount >= 3:
            gameOn = False
            iAnimal = getAnimal(last_letter)
            if iAnimal == '':
                print("It's a tie ..")
            else:
                print("Don't you know ", iAnimal[0:1].upper()+iAnimal[1:].lower() , " ?? ")
                print("You loose, I win!!")
            
              
    
    
