__author__ = 'denislavrov'

# UNUSED FUNCTIONS !!!

def isAlphabetic(value):
    alphabeticCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return contains(alphabeticCharacters, value)


def isValidName(value):
    alphabeticCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ &-"
    return contains(alphabeticCharacters, value)


def isItemInList(value, list):
    for item in list:
        if item == value:
            return True
    return False


def isValidVerb(value):
    return isItemInList(value, VerbList)


def isValidNoun(value):
    return isItemInList(value, NounList)


def isValidItem(value):
    return isItemInList(value, ItemList)


# END IF UNUSED FUNCTIONS


def ASSERT(condition, message):
    if not condition:
        raise AssertionError(message + ":False")


def ASSERT_FALSE(condition, message):
    if not condition:
        raise AssertionError(message + ":True Failure")


def ASSERT_TRUE(condition, message):
    if not condition:
        raise AssertionError(message + ":False")


def TestDirectionsArray():
    lengthOfDirectionsArray = len(DirectionsArray)
    validvalues = 'NSEWUD'
    ASSERT(lengthOfDirectionsArray == 64, "The array length is correct?")
    for i in range(0, lengthOfDirectionsArray, 1):
        values = DirectionsArray[i]
        if not contains(validvalues, values):
            ASSERT(False, "The array contains invalid values" + values)
            return


def TestLocationsArray():
    lengthOfLocationsArray = len(LocationsArray)
    ASSERT(lengthOfLocationsArray == 64, "The total number of locations expected was correct")
    for i in range(0, lengthOfLocationsArray, 1):
        value = LocationsArray[i]
        if not isValidName(value):
            print(False, "The value is not alphabetic:" + value)
            return


def TestVerbsArray():
    lengthOfVerbList = len(VerbList)
    ASSERT(lengthOfVerbList == 25, "The size of the verb dictionary is incorrect")


def TestNounsArray():
    lengthOfNounsArray = len(NounList)
    ASSERT(lengthOfNounsArray == 12, "The size of the nouns dictionary is incorrect")


def TestItemsArray():
    lengthOfItemsArray = len(ItemList)
    ASSERT(lengthOfItemsArray == 18, "The size of the items dictionary is incorrect")


def TestParse():
    sentence = "GO NORTH"
    ASSERT(isMultiwordStatement(sentence), "Multiword?")
    verb = GetVerbFromSentence(sentence)
    noun = GetNounFromSentence(sentence)
    sentence = "SCORE"
    ASSERT(not isMultiwordStatement(sentence), "Multiword wrongly detected")


def TestChangeDirectionCharacter():
    ExpectedRoomsWithDirectionChanges = 3
    ActualRoomsWithDirectionChanges = 0
    lengthOfDirectionsArray = len(DirectionsArray)
    validvalues = 'NSEW'
    for i in range(0, lengthOfDirectionsArray, 1):
        values = DirectionsArray[i]
        if not contains(validvalues, values):
            ActualRoomsWithDirectionChanges += 1
    ASSERT(ExpectedRoomsWithDirectionChanges == ActualRoomsWithDirectionChanges,
           "Total Directions Changed Was Correct?")
    newDirection = changeDirectionCharacter("U", 20)
    ASSERT(newDirection == "N", "Changed Incorrectly")
    newDirection = changeDirectionCharacter("D", 20)
    ASSERT(newDirection == "W", "Changed Incorrectly")
    newDirection = changeDirectionCharacter("U", 22)
    ASSERT(newDirection == "W", "Changed Incorrectly")
    newDirection = changeDirectionCharacter("D", 22)
    ASSERT(newDirection == "S", "Changed Incorrectly")
    newDirection = changeDirectionCharacter("U", 36)
    ASSERT(newDirection == "S", "Changed Incorrectly")
    newDirection = changeDirectionCharacter("D", 36)
    ASSERT(newDirection == "N", "Changed Incorrectly")


def TestGo():
    newLocationID = Go("S", 0)
    ASSERT(newLocationID == 8, "Moved to Location Correctly")
    newLocationID = Go("S", newLocationID)
    ASSERT(newLocationID == 16, "Moved to Location Correctly")
    newLocationID = Go("W", newLocationID)
    ASSERT(newLocationID == 16, "Stayed in Location Correctly")
    newLocationID = Go("E", newLocationID)
    ASSERT(newLocationID == 16, "Stayed in Location Correctly")
    newLocationID = Go("S", newLocationID)
    ASSERT(newLocationID == 24, "Moved to Location Correctly")
    newLocationID = Go("N", newLocationID)
    ASSERT(newLocationID == 16, "Moved to Location Correctly")
    newLocationID = Go("N", newLocationID)
    ASSERT(newLocationID == 8, "Stayed in Location Correctly")
    newLocationID = Go("W", newLocationID)
    ASSERT(newLocationID == 8, "Stayed in Location Correctly")
    newLocationID = Go("E", newLocationID)
    ASSERT(newLocationID == 8, "Stayed in Location Correctly")
    newLocationID = Go("N", newLocationID)
    ASSERT(newLocationID == 0, "Moved to Location Correctly")
    newLocationID = Go("N", newLocationID)
    ASSERT(newLocationID == 0, "Stayed in Location Correctly")
    newLocationID = Go("W", newLocationID)
    ASSERT(newLocationID == 0, "Stayed in Location Correctly")
    newLocationID = Go("E", newLocationID)
    ASSERT(newLocationID == 1, "Moved to Location Correctly")
    newLocationID = Go("E", newLocationID)
    ASSERT(newLocationID == 2, "Moved to Location Correctly")
    newLocationID = Go("W", newLocationID)
    ASSERT(newLocationID == 1, "Moved to Location Correctly")


def TestBoundaryOfMap():
    for i in range(0, 7, 1):
        ASSERT(contains("SEW", DirectionsArray[i]), "North Most Extends")
        ASSERT(contains("NEW", DirectionsArray[i + 57]), "South Most Extends")

    ASSERT(contains("SE", DirectionsArray[0]), "North West Corner")
    ASSERT(contains("SW", DirectionsArray[7]), "North East Corner")
    ASSERT(contains("NE", DirectionsArray[56]), "South West Corner")
    ASSERT(contains("NW", DirectionsArray[63]), "North East Corner")

    for i in range(8, 48, 8):
        ASSERT(contains("NSE", DirectionsArray[i]), "West Most Extends")
        ASSERT(contains("NSW", DirectionsArray[i + 7]), "East Most Extends")


def TestGoLonger():
    newLocationID = Go("GO SOUTH", 0)
    ASSERT(newLocationID == 8, "Moved to Location Correctly")
    newLocationID = Go("GO SOUTH", newLocationID)
    ASSERT(newLocationID == 16, "Moved to Location Correctly")
    newLocationID = Go("GO WEST", newLocationID)
    ASSERT(newLocationID == 16, "Stayed in Location Correctly")
    newLocationID = Go("GO EAST", newLocationID)
    ASSERT(newLocationID == 16, "Stayed in Location Correctly")
    newLocationID = Go("GO SOUTH", newLocationID)
    ASSERT(newLocationID == 24, "Moved to Location Correctly")
    newLocationID = Go("GO NORTH", newLocationID)
    ASSERT(newLocationID == 16, "Moved to Location Correctly")
    newLocationID = Go("GO NORTH", newLocationID)
    ASSERT(newLocationID == 8, "Stayed in Location Correctly")
    newLocationID = Go("GO WEST", newLocationID)
    ASSERT(newLocationID == 8, "Stayed in Location Correctly")
    newLocationID = Go("GO EAST", newLocationID)
    ASSERT(newLocationID == 8, "Stayed in Location Correctly")
    newLocationID = Go("GO NORTH", newLocationID)
    ASSERT(newLocationID == 0, "Moved to Location Correctly")
    newLocationID = Go("GO NORTH", newLocationID)
    ASSERT(newLocationID == 0, "Stayed in Location Correctly")
    newLocationID = Go("GO WEST", newLocationID)
    ASSERT(newLocationID == 0, "Stayed in Location Correctly")
    newLocationID = Go("GO EAST", newLocationID)
    ASSERT(newLocationID == 1, "Moved to Location Correctly")
    newLocationID = Go("GO EAST", newLocationID)
    ASSERT(newLocationID == 2, "Moved to Location Correctly")
    newLocationID = Go("GO WEST", newLocationID)
    ASSERT(newLocationID == 1, "Moved to Location Correctly")


def TestItemPositions():
    LengthOfItemsPositionArray = len(PositionOfItems)
    LengthOfItemsArray = len(ItemList)
    ASSERT(LengthOfItemsPositionArray == LengthOfItemsArray, "Item List And Item Position Lengths Match?")


def TestIsItemAvailableAtLocation():
    ASSERT(isItemAvailableAtLocation(0, 46) == True, "Item is supposed to be at this location")
    ASSERT(isItemAvailableAtLocation(0, 47) == False, "Item is not supposed to be at this location")
    ASSERT(isItemAvailableAtLocation(17, 100) == True, "Item is supposed to be at this location")
    ASSERT(isItemAvailableAtLocation(17, 33) == False, "Item is not supposed to be at this location")


def TestCarryingNothing():
    itemList = ""
    itemList = Carrying()
    ASSERT(len(itemList) == 0, "Item list is supposed to be empty")


def TestGetItem():
    ASSERT(isItemAvailableAtLocation(17, 100) == True, "Item is supposed to be in this location")
    GetItem(17, 100)
    ASSERT(isItemAvailableAtLocation(17, 32) == False, "Item is no longer in this location")
    strItemList = ""
    strItemList = Carrying()
    ASSERT(len(strItemList) != 0, "Items are now carried")
    DropItem(17, 32)
    strItemList = Carrying()
    ASSERT(len(strItemList) == 0, "Item dropped so now it is supposed to be empty again")


def TestGetScore():
    score = GetScore()
    ASSERT(score == 0, "The score is zero")
    for i in range(0, len(ItemList), 1):
        GetItem(i, PositionOfItems[i])
    ASSERT(GetScore() == 18, "The score is maximum")


def TestEndGame():
    expectedWinConditions = 1
    expectedNonWinConditions = (18 * 64) - 1
    actualWinConditions = 0
    actualNonWinConditions = 0
    for score in range(0, 18, 1):
        for location in range(0, 64, 1):
            if isEndOfGame(score, location):
                actualWinConditions += 1
            else:
                actualNonWinConditions += 1
    ASSERT(actualWinConditions == expectedWinConditions, "Total win conditions check")
    ASSERT(actualNonWinConditions == expectedNonWinConditions, "Total non-win conditions check")


def TestGame():
    TestDirectionsArray()
    TestLocationsArray()
    TestBoundaryOfMap()
    TestVerbsArray()
    TestNounsArray()
    TestItemsArray()
    TestParse()
    TestChangeDirectionCharacter()
    TestGo()
    TestGoLonger()
    TestItemPositions()
    TestIsItemAvailableAtLocation()
    TestCarryingNothing()
    TestGetItem()
    TestGetScore()
    TestEndGame()


# ############################################################################################################
# END TESTS                                                                                                 #
#############################################################################################################
