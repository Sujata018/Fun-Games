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

# Database for animals

animals = { 'a':{"aardwolf":0,"aardvark":0,"albatross":0,"alpaca":0,"anemone":0,"anteater":0,"antelope":0,"ape":0,"armadillo":0,"axolotl":0,"aye-aye":0},
            'b':{"bandicoot":0,"barnacle":0,"barracuda":0,"bat":0,"bass":0,"bear":0,"beaver":0,"bison":0,"boar":0,"bobcat":0,"bullfrog":0},
            'c':{"caiman":0,"camel":0,"cpybara":0,"caracal":0,"cassowary":0,"cat":0,"cheetah":0,"chimpanzee":0,"chinchilla":0,"chipmunk":0,"coati":0,"cougar":0,"cow":0,"coyote":0},
            'd':{"deer":0,"dingo":0,"dog":0,"donkey":0,"dugong":0,"dolphin":0},
            'e':{"eland":0,"elephant":0,"elk":0},
            'f':{"ferret":0,"finch":0,"fossa":0,"fox":0,"frog":0},
            'g':{"gazelle":0,"goat":0,"groundhog":0,"guineapig":0},
            'h':{"hedgehog":0,"hippopotamus":0,"horse":0,"hyena":0},
            'i':{},
            'j':{},
            'k':{"koala":0},
            'l':{"leopard":0,"lion":0,"llama":0,"lynx":0},
            'm':{"meerkat":0,"mole":0,"moose":0,"mouse":0},
            'n':{},
            'o':{"orangutan":0,"orca":0},
            'p':{"panda":0,"panther":0,"pig":0,"polar-bear":0},
            'q':{},
            'r':{"rabbit":0,"raccoon":0,"reindeer":0,"robin":0,"rat":0},
            's':{"sea-lion":0,"seagull":0,"seahorse":0,"seal":0,"sea-otter":0,"sheep":0,"slug":0,"squirrel":0},
            't':{"tiger":0,"turtle":0, "tortoise":0},
            'u':{},
            'v':{},
            'w':{"wallaby":0,"walrus":0,"wasp":0,"weasel":0,"weaver":0,"whale":0,"wildcat":0,"wilddog":0,"wolf":0,"wolverine":0,"wombat":0},
            'x':{},
            'y':{},
            'z':{}
           }

# Database for birds

birds = { 'a':{"albatross":0},
            'b':{},
            'c':{"crane":0,"chicken":0},
            'd':{"dodo":0,"dove":0,"duck":0},
            'e':{"eagle":0,"echidnas":0,"emu":0},
            'f':{"flamingo":0, "falcon":0},
            'g':{},
            'h':{},
            'i':{},
            'j':{},
            'k':{},
            'l':{},
            'm':{},
            'n':{},
            'o':{},
            'p':{},
            'q':{},
            'r':{},
            's':{},
            't':{},
            'u':{},
            'v':{},
            'w':{},
            'x':{},
            'y':{},
            'z':{}
           }


# Database for insects

insects = {'a':{"ant":0},
            'b':{"beetle":0,"bee":0,"butterfly":0},
            'c':{"cockroach":0,"caterpillar":0, "centipede":0},
            'd':{"dragonfly":0},
            'e':{"earwig":0},
            'f':{"firefly":0, "flea":0,"fly":0},
            'g':{},
            'h':{},
            'i':{},
            'j':{},
            'k':{},
            'l':{},
            'm':{},
            'n':{},
            'o':{},
            'p':{},
            'q':{},
            'r':{},
            's':{},
            't':{},
            'u':{},
            'v':{},
            'w':{},
            'x':{},
            'y':{},
            'z':{}
           }

# Database for fishes

fishes = {  'a':{"angelfish":0},
            'b':{},
            'c':{"cuttlefish":0,"catfish":0,"clown":0},
            'd':{},
            'e':{"eel":0},
            'f':{"fish":0,"flounder":0},
            'g':{},
            'h':{},
            'i':{},
            'j':{},
            'k':{},
            'l':{},
            'm':{},
            'n':{},
            'o':{},
            'p':{},
            'q':{},
            'r':{},
            's':{},
            't':{},
            'u':{},
            'v':{},
            'w':{},
            'x':{},
            'y':{},
            'z':{}
           }


# Database for reptiles

reptiles ={ 'a':{"alligator":0,"anaconda":0},
            'b':{"boa":0},
            'c':{"crocodile":0,"cobra":0,"chameleon":0},
            'd':{},
            'e':{},
            'f':{},
            'g':{},
            'h':{},
            'i':{},
            'j':{},
            'k':{},
            'l':{},
            'm':{},
            'n':{},
            'o':{},
            'p':{},
            'q':{},
            'r':{},
            's':{},
            't':{},
            'u':{},
            'v':{},
            'w':{},
            'x':{},
            'y':{},
            'z':{}
    }

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
            print("You type an animal name, I type another starting with your last letter, then you type another.")
            print("Who gives up first, looses. Let's start!!")
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
            
              
    
    
