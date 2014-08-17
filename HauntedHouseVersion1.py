import random
import sqlite_controller as SC


DirectionsArray = ['SE', 'WE', 'WE', 'SWE', 'WE', 'WE', 'SWE', 'WS',
                   'NS', 'SE', 'WE', 'NW', 'SE', 'W', 'NE', 'NSW',
                   'NS', 'NS', 'SE', 'WE', 'NWUD', 'SE', 'WSUD', 'NS',
                   'N', 'NS', 'NSE', 'WE', 'WE', 'NSW', 'NS', 'NS',
                   'S', 'NSE', 'NSW', 'S', 'NSUD', 'N', 'N', 'NS',
                   'NE', 'NW', 'NE', 'W', 'NSE', 'WE', 'W', 'NS',
                   'SE', 'NSW', 'E', 'WE', 'NW', 'S', 'SW', 'NW',
                   'NE', 'NWE', 'WE', 'WE', 'WE', 'NWE', 'NWE', 'W']

LocationsArray = \
    ['DARK CORNER', 'OVERGROWN GARDEN', 'BY LARGE WOODPILE', 'YARD BY RUBBISH',
     'WEEDPATCH', 'FOREST', 'THICK FOREST', 'BLASTED TREE',
     'CORNER OF HOUSE', 'ENTRANCE TO KITCHEN', 'KITCHEN & GRIMY COOKER', 'SCULLERY DOOR',
     'ROOM WITH INCHES OF DUST', 'REAR TURRET ROOM', 'CLEARING BY HOUSE', 'PATH',
     'SIDE OF HOUSE', 'BACK OF HALLWAY', 'DARK ALCOVE', 'SHALL DARK ROOM',
     'BOTTOM OF SPIRAL STAIRCASE', 'WIDE PASSAGE', 'SLIPPERY STEPS', 'CLIFFTOP',
     'NEAR CRUMBLING WALL', 'GLOOMY PASSAGE', 'POOL OF LIGHT', 'IMPRESSIVE VAULTED HALLWAY',
     'HALL BY THICK WOODEN DOOR', 'TROPHY ROOM', 'CELLAR WITH BARRED WINDOW', 'CLIFF PATH',
     'CUPBOARD WITH HANGING COAT', 'FRONT HALL', 'SITTING ROOM', 'SECRET ROOM',
     'STEEP MARBLE STAIRS', 'DINING ROOM', 'DEEP CELLAR WITH COFFIN', 'CLIFF PATH',
     'CLOSET', 'FRONT LOBBY', 'LIBRARY OF EVIL BOOKS', 'STUDY WITH DESK & HOLE IN WALL',
     'WEIRD COBWEBBY ROOM', 'VERY COLD CHAMBER', 'SPOOKY ROOM', 'CLIFF PATH BY MARSH',
     'RUBBLE-STREWN VERANDAH', 'FRONT PORCH', 'FRONT TOWER', 'SLOPING CORRIDOR',
     'UPPER GALLERY', 'MARSH BY WALL', 'MARSH', 'SOGGY PATH',
     'BY TWISTED RAILING', 'PATH THROUGH IRON GATE', 'BY RAILINGS', 'BENEATH FRONT TOWER',
     'DEBRIS FROM CRUMBLING FACADE', 'LARGE FALLEN BRICKWORK', 'ROTTING STONE ARCH', 'CRUMBLING CLIFFTOP']

VerbList = ['HELP', 'CARRYING?', 'GO', 'N', 'S', 'W', 'E', 'U', 'D',
            'GET', 'TAKE', 'OPEN', 'EXAMINE', 'READ', 'SAY',
            'DIG', 'SWING', 'CLIMB', 'LIGHT', 'UNLIGHT', 'SPRAY', 'USE', 'UNLOCK', 'DROP', 'SCORE']

NounList = ['NORTH', 'SOUTH', 'WEST', 'EAST', 'UP', 'DOWN',
            'DOOR', 'BATS', 'GHOSTS', 'X2ANFAR', 'SPELLS', 'WALL']

PropList = ['DRAWER', 'DESK', 'COAT', 'RUBBISH', 'COFFIN', 'BOOKS']

PositionOfProps = [43, 43, 32, 3, 38, 35]

ItemList = ['PAINTING', 'RING', 'MAGIC SPELLS', 'GOBLET', 'SCROLL', 'COINS', 'STATUE', 'CANDLESTICK', 'MATCHES',
            'VACUUM', 'BATTERIES', 'SHOVEL', 'AXE', 'ROPE', 'BOAT', 'AEROSOL', 'CANDLE', 'KEY']

PositionOfItems = [46, 38, 35, 50, 13, 18, 28, 42, 10, 25, 26, 4, 2, 7, 47, 60, 100, 100]

visitedLocations = [0, ]

LocationID = 0

Parameters = {
    'SAVE_CURRENT': False,
    'DATABASE': 'new.db',

}

#############################################################################################################
# HELPER FUNCTIONS                                                                                          #
#############################################################################################################


def contains(validValues, values):
    validCount = 0
    lengthValues = len(values)
    for letter in validValues:
        for character in values:
            if letter == character:
                validCount = validCount + 1
    return validCount == lengthValues


def containsLetter(letter, values):
    for character in values:
        if letter == character:
            return True
    return False


def isMultiwordStatement(value):
    return value.find(" ") != -1


def isItemAvailableAtLocation(ItemID, LocationID):
    return PositionOfItems[ItemID] == LocationID


def isItemInInventory(name):
    return isItemAvailableAtLocation(getItemID(name), -1)


def changePositionOfItem(ItemID, newLocationID):
    PositionOfItems[ItemID] = newLocationID


#############################################################################################
# GAME LOGIC                                                                                #
#############################################################################################

def display_position_setting(locationID):
    if locationID == 0:
        show_dungeon_master()


def getVerbFromSentence(sentence):
    if not isMultiwordStatement(sentence):
        return sentence
    locationOfSpace = sentence.find(" ")
    return sentence[:locationOfSpace]


def getNounFromSentence(sentence):
    if not isMultiwordStatement(sentence):
        return ""
    locationOfSpace = sentence.find(" ") + 1
    return sentence[locationOfSpace:]


def getItemID(item):
    for ItemID in range(0, len(ItemList), 1):
        if item == ItemList[ItemID]:
            return ItemID
    return -1


def changeDirectionCharacter(directioncharacter, locationID):
    if locationID == 20 and directioncharacter == 'U':
        directioncharacter = 'N'
    elif locationID == 20 and directioncharacter == 'D':
        directioncharacter = 'W'
    elif locationID == 22 and directioncharacter == 'U':
        directioncharacter = 'W'
    elif locationID == 22 and directioncharacter == 'D':
        directioncharacter = 'S'
    elif locationID == 36 and directioncharacter == 'U':
        directioncharacter = 'S'
    elif locationID == 36 and directioncharacter == 'D':
        directioncharacter = 'N'
    return directioncharacter


def isMovementAvailable(directioncharacter, LocationID):
    return DirectionsArray[LocationID].find(directioncharacter) >= 0


def isMovementVerb(verb, noun):
    return verb == 'N' or verb == 'S' or verb == 'E' or verb == 'W' or verb == 'U' or verb == 'D' or verb == 'GO'


def getMovementDirection(statement):
    verb = getVerbFromSentence(statement)
    noun = getNounFromSentence(statement)
    if len(verb) == 1:
        return verb
    if verb == 'GO':
        return noun[:1]
    return ''


def isEndOfGame(score, locationID):
    return score == 17 and locationID == 57


def getScore():
    score = 0
    for i in range(0, len(PositionOfItems), 1):
        if isItemAvailableAtLocation(i, -1):
            score += 1
    return score


#############################################################################################
# END GAME LOGIC                                                                            #
#############################################################################################

#############################################################################################
# BEGIN PRESENTATION LOGIC                                                                  #
#############################################################################################

def show_dungeon_master():
    print('\n', end='')
    print("""Hello my son, I'm the housekeeper!\n
Your task here is to find all of these items:
%s
And find the path through an iron gate.
          """ % (', '.join(ItemList)))


def displayGameName():
    print("========Haunted House=========")


def displayPosition(LocationID):
    print("YOU ARE LOCATED IN A ", LocationsArray[LocationID])


def displayItemsAtPosition(LocationID):
    if itemsAvailableAtPosition(LocationID):
        print("YOU CAN SEE THE FOLLOWING ITEMS AT THIS LOCATION: ", listItemsAtPosition(LocationID))


def displayVisibleExitsAtPosition(LocationID):
    exits = DirectionsArray[LocationID]
    exits_buffer = []
    if 'S' in exits:
        exits_buffer.append('South')
    if 'N' in exits:
        exits_buffer.append('North')
    if 'E' in exits:
        exits_buffer.append('East')
    if 'W' in exits:
        exits_buffer.append('West')

    print('Visible exits are:', ' and '.join(exits_buffer))


def displayListOfVerbs():
    print(VerbList)


def displayHelpMessage():
    print("I UNDERSTAND THE FOLLOWING WORDS:")
    displayListOfVerbs()


def displayMoveFromTo(LocationID, newLocationID):
    if LocationID != newLocationID:
        print("YOU MOVED FROM " + LocationsArray[LocationID] + " TO " + LocationsArray[newLocationID])
    else:
        print("YOU ARE UNABLE TO MOVE IN THAT DIRECTION")


def displayGetItemMessage(successful, noun):
    if successful:
        print("YOU ARE NOW CARRYING A ", noun)
    else:
        print("SORRY YOU CANNOT TAKE A ", noun)


def displayInventory(strInventory):
    if len(strInventory) == 0:
        strInventory = "NOTHING"
    print("YOU ARE CARRYING:" + strInventory)


def displayScore(score):
    print("YOUR CURRENT SCORE IS:", score)


def displayTheDoorIsLockedMessage():
    print("THE DOOR IS LOCKED")


def displayOpenDoorMessage():
    print("THE DOOR IS NOW OPEN! REVEALLING A NEW EXIT!")


def displayYouDugAHole():
    print("YOU DIG A HOLE")


def displayWhatWith():
    print("YOU HAVE NOTHING TO DIG WITH")


def getActionStatement():
    return input("WHAT DO YOU WANT TO DO NEXT?").upper()


def displayDropMessage(dropped, item):
    if dropped:
        print("YOU HAVE DROPPED THE ", item)
    else:
        print("YOU CANNOT DROP THAT WHICH YOU DO NOT POSSESS")


def displayDigAttempt(DigMessageType):
    if DigMessageType == 1:
        print("YOU DIG AROUND THE ROOM. THE BARS BECOME LOOSE. A NEW EXIT!")
    elif DigMessageType == 2:
        print("YOU DIG A LITTLE HOLE.")
    else:
        print("WHAT WITH?")


def displayAttemptOpenDoor(opened, LocationID):
    if opened:
        displayOpenDoorMessage()

    else:
        displayTheDoorIsLockedMessage()


def examineCoat(LocationID):
    if LocationID == 32 and isItemAvailableAtLocation(getItemID("Key"), 100):
        PositionOfItems[getItemID("KEY")] = 32
        return 1
    elif LocationID == 32 and not isItemAvailableAtLocation(getItemID("Key"), 100):
        return 2
    return 99


def examineDrawer(LocationID):
    if LocationID == 43 and isItemInInventory("KEY"):
        return 3
    elif LocationID == 43 and not isItemInInventory("KEY"):
        return 4
    return 99


def examineRubbish(LocationID):
    if LocationID == 3:
        return 5
    return 99


def examineWall(LocationID):
    if LocationID == 43:
        LocationsArray[LocationID] = "STUDY WITH DESK"
        DirectionsArray[LocationID] = "NW"
        return 6
    return 7


def examineDoor(LocationID):
    if LocationID == 28 and isItemInInventory("KEY"):
        DirectionsArray[LocationID] = "SEW"
        return 8
    elif LocationID == 28 and not isItemInInventory("KEY"):
        return 9
    return 88


def doExamine(LocationID, noun):
    if noun == "COAT":
        return examineCoat(LocationID)
    if noun == "DRAWER":
        return examineDrawer(LocationID)
    if noun == "RUBBISH":
        return examineRubbish(LocationID)
    if noun == "WALL":
        return examineWall(LocationID)
    if noun == "DOOR":
        return examineDoor(LocationID)

    return 99


def displayExamineMessage(MessageID, noun):
    if MessageID == 1:
        print("YOU EXAMINE THE COAT AND FIND A KEY IN THE POCKET")
    elif MessageID == 2:
        print("IT\'S A DIRTY OLD COAT")
    elif MessageID == 3:
        print("YOU UNLOCK THE DRAWER AND FIND IT IS EMPTY")
    elif MessageID == 4:
        print("UNFORTUNATELY THE DRAWER IS LOCKED")
    elif MessageID == 5:
        print("THE RUBBISH IS FILTHY")
    elif MessageID == 6:
        print("YOU LOOK AT THE WALL AND DISCOVER IT IS FALSE!\nYOU DISCOVER A NEW EXIT")
    elif MessageID == 7:
        print("NO INTERESTING WALLS HERE")
    elif MessageID == 8:
        print("YOU UNLOCK THE DOOR AND DISCOVER A NEW LOCATION!")
    elif MessageID == 9:
        print("UNFORTUNATELY THE DOOR IS LOCKED")

    elif MessageID == 88:
        print("NO INTERESTING " + noun + "HERE...")
    elif MessageID == 99:
        print("WHAT " + noun + "?")


def displayMagicMessage(LocationID, newLocationID):
    print("YOU UTTER WORDS OF DARK MAGIC... X2ANFAR!")
    print("YOU DISAPPEAR AND REAPPEAR IN ANOTHER LOCATION...")
    print("YOU WERE IN " + LocationsArray[LocationID])
    print("YOU ARE NOW IN " + LocationsArray[newLocationID])


def printableInts(value):
    if (value < 10):
        return " " + str(value)
    return str(value)


def displayMap():
    Line1 = ""
    Line2 = ""
    Line3 = ""

    for Index in range(0, 64, 1):
        currentValues = DirectionsArray[Index]

        if Index in visitedLocations:  # ++

            if containsLetter("N", currentValues):  ### here
                Line1 += "+  +"
            else:
                Line1 += "+--+"

            if containsLetter("W", currentValues):
                Line2 += (" ") + ('**' if Index is LocationID else printableInts(Index))
            else:
                Line2 += ("|") + ('**' if Index is LocationID else printableInts(Index))

            if containsLetter("E", currentValues):
                Line2 += (" ")
            else:
                Line2 += ("|")

            if containsLetter("S", currentValues):
                Line3 += "+  +"
            else:
                Line3 += "+--+"  # here tabbed right
        else:  # +++++
            Line1 += '    '
            Line2 += '    '
            Line3 += '    '

        if (Index + 1) % 8 == 0:
            print(Line1)
            print(Line2)
            print(Line3)
            Line1 = ""
            Line2 = ""
            Line3 = ""


#############################################################################################
# END PRESENTATION LOGIC                                                                    #
#############################################################################################



def carrying():
    strItems = ""
    for i in range(0, len(PositionOfItems), 1):
        if PositionOfItems[i] == -1:
            strItems = strItems + " " + ItemList[i]
    return strItems


def dig(LocationID):
    if LocationID == 30 and isItemInInventory("SHOVEL"):
        DirectionsArray[LocationID] = "SEW"
        LocationsArray[30] = 'HOLE IN WALL'
        return 1
    elif isItemInInventory("SHOVEL"):
        return 2
    return 3


def listItemsAtPosition(LocationID):
    strItems = ""
    for i in range(0, len(PositionOfItems), 1):
        if PositionOfItems[i] == LocationID:
            strItems = strItems + " " + ItemList[i]
    return strItems


def itemsAvailableAtPosition(LocationID):
    for i in range(0, len(PositionOfItems), 1):
        if PositionOfItems[i] == LocationID:
            return True
    return False


def goMagic(LocationID):
    newLocationID = LocationID
    while (newLocationID == LocationID):
        newLocationID = random.randint(0, 63)

    return newLocationID


def go(statement, LocationID):
    directioncharacter = getMovementDirection(statement)
    if isMovementAvailable(directioncharacter, LocationID):
        directioncharacter = changeDirectionCharacter(directioncharacter, LocationID)
        if directioncharacter == 'N':
            LocationID -= 8
        elif directioncharacter == 'S':
            LocationID += 8
        elif directioncharacter == 'W':
            LocationID -= 1
        elif directioncharacter == 'E':
            LocationID += 1

    return LocationID


def getItem(ItemID, LocationID):
    if isItemAvailableAtLocation(ItemID, LocationID):
        changePositionOfItem(ItemID, -1)
        return True
    return False


def dropItem(ItemID, LocationID):
    if isItemAvailableAtLocation(ItemID, -1):
        changePositionOfItem(ItemID, LocationID)
        return True
    return False


def openDoor(LocationID):
    if LocationID == 28 and isItemInInventory("KEY"):
        DirectionsArray[LocationID] = "SEW"
        return True
    return False


def shell():  # function that facilitates an interactive python shell
    while 1:
        useri = input("#!>")  # continuously ask for user input
        if useri == 'exit':  # exit, exits the shell
            break
        else:
            try:
                exec(useri)  # try to execute user input if it fails, just print there was an error.
            except:
                pass


def nag_user(statement, answers):
    while 1:
        ui = input(statement + '[' + ', '.join(answers) + "]: ").lower()
        if ui in answers:
            return ui


def save():
    if nag_user('Would you like to set up a new database or use existing', ['new', 'existing']) == 'new':
        SC.createdb()
    else:
        SC.switchdb()

    inventory = []
    for itemID, item in enumerate(ItemList):
        if PositionOfItems[itemID] == -1:
            inventory.append(itemID)

    SC.save(inventory, visitedLocations)
    Parameters['SAVE_CURRENT'] = True


def load():
    SC.switchdb()
    savename = input("Please enter a valid savename:")
    if SC.userexists(savename):
        inventory = SC.readinv(savename)
        for litem in inventory:
            for itemID, item in enumerate(ItemList):
                if itemID == litem:
                    PositionOfItems[itemID] = -1

        global visitedLocations
        visitedLocations = SC.readloc(savename)
        global LocationID
        LocationID = visitedLocations[len(visitedLocations) - 1]
        Parameters['SAVE_CURRENT'] = True
    else:
        print("That save name is not valid, Try one of these:\n%s" % '\n'.join(SC.readusers()))


def processStatement(statement):
    global LocationID

    verb = getVerbFromSentence(statement)
    noun = getNounFromSentence(statement)

    if verb == "HELP":
        displayHelpMessage()

    elif verb == "SCORE" or ((verb == 'SHOW' or verb == 'LIST') and noun == 'SCORE'):
        displayScore(getScore())

    elif verb == "CARRYING" or verb == "CARRYING?" or verb == "INVENTORY" or verb == "INV":
        displayInventory(carrying())

    elif verb == "GET" or verb == "TAKE" or verb == 'PICKUP':
        displayGetItemMessage(getItem(getItemID(noun), LocationID), noun)
        Parameters['SAVE_CURRENT'] = False

    elif ((verb == "OPEN" or verb == "UNLOCK") and noun == "DOOR") or (verb == "USE" and noun == "KEY"):
        displayAttemptOpenDoor(openDoor(LocationID), LocationID)

    elif verb == "DIG" or (verb == "USE" and noun == "SHOVEL"):
        displayDigAttempt(dig(LocationID))

    elif verb == "DROP" or verb == 'PUT':
        displayDropMessage(dropItem(getItemID(noun), LocationID), noun)
        Parameters['SAVE_CURRENT'] = False

    elif verb == "EXAMINE":
        displayExamineMessage(doExamine(LocationID, noun), noun)

    elif verb == "SAY" and noun == "X2ANFAR":
        newLocationID = goMagic(LocationID)
        displayMagicMessage(LocationID, newLocationID)
        LocationID = newLocationID
        Parameters['SAVE_CURRENT'] = False

    elif (verb == "SHOW" or verb == 'LIST') and noun == "MAP":
        displayMap()

    elif verb == 'SHOW' and noun == 'SHELL':
        shell()

    elif verb == 'SAVE':
        save()

    elif verb == 'LOAD':
        load()

    elif verb == "EXIT" or verb == "QUIT":
        while 1:
            if not Parameters['SAVE_CURRENT']:
                ui = input("Game isn't saved all progress will be lost, Would you like to save?\n" \
                           + "[save, exit, cancel]: ").lower()
            else:
                print("Your game is saved you are good to go.")
                exit()

            if ui == 'exit':
                exit()
            elif ui == 'save':
                save()
                exit()
            elif ui == 'cancel':
                break

    elif isMovementVerb(verb, noun):
        newLocationID = go(statement, LocationID)

        visitedLocations.append(newLocationID)  # +++

        displayMoveFromTo(LocationID, newLocationID)
        LocationID = newLocationID
        Parameters['SAVE_CURRENT'] = False

    print("LocationID=", LocationID)

    return LocationID


def game():
    global LocationID
    while not isEndOfGame(LocationID, getScore()):
        displayGameName()
        displayPosition(LocationID)
        displayItemsAtPosition(LocationID)
        displayVisibleExitsAtPosition(LocationID)

        display_position_setting(LocationID)  # +++

        statement = getActionStatement()
        LocationID = processStatement(statement)


try:
    game()
except KeyboardInterrupt:
    print("\nWHY !?!?!?!? WHY !?!?!? Y U KILL ME !?!?")
    exit(0)

