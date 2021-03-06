'''
Eric Goodwin
09-17-2018
Python 3.7.0
PyCharm IDE
CS 4500 Introduction to the Software Profession
External Files created - H3goodwinOutfile.txt
Program creates this file with output data.  data is same as what
is displayed on the screen running of the program.



Resources Used:
https://docs.python.org/3/library
https://thispointer.com/python-how-to-check-if-an-item-exists-in-list-search-by-value-or-condition/
https://www.geeksforgeeks.org/sum-function-python/
https://www.tutorialspoint.com/python/list_max.htm
http://treyhunner.com/2016/04/how-to-loop-with-indexes-in-python/
https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space
https://stackoverflow.com/questions/10660435/pythonic-way-to-create-a-long-multi-line-string
https://www.programiz.com/python-programming/methods/list/clear
https://www.tutorialspoint.com/python/list_min.htm



Requirements (from HW2 Specification):
Simulate dice roll to determine direction - DONE
Account for invalid moves as a move as if jumping in place - DONE
Map moves to dice result - DONE
Encode movements on tuple - DONE
Print results to Screen - DONE
Print results to output file - DONE
Format out of output line - EX: 5, 4, 5, 6, 7.  Period signifies end of the line - DONE
Calculate statistics - total moves, average dots on a node, which node has max dots - DONE

Note - this version of the pyramid game is an extension of HW2
Keeping code from HW2 intact in order to test against same dice rolls for autogenerated nodes



Design:
Use a list of tuples to represent each location on the pyramid.  Each location to be encoded with data for number
of visits (dots) as well as valid moves. Invalid moves will be marked as None in the tuple.
use a variable, currentlocation, to hold where the player is currently at.  Starts at one.
Use if check to see if a move is valid
if move is valid, update currentlocation to the new location and record a visit.
if the move is not valid, currentlocation remains the same and update that location with a new visit
maintain another list of how often a location is visited.
game continues until a 0 is no longer detected in the tracker list.
one the game ends, compute statistics and display.

made a couple of design decisions-
I count the initial start of the game as a visit
I also added a pause in the execution so the use can "see" the locations being added to the visit list

Use git for version control.

New Features for HW3:
User can specify a number of leves to the pyramid between 2 and 25 levels. - DONE
Program checks for valid input and if incorrect, prints error message and reprompts.  repeats until valid input given -DONE
User can specify number of times to run the simulation between 10 and 50. - DPNE
Program checks for valid input  and if incorrect, prints error message and reprompts. repeats until valid input given - DONE
add total sim statistics - DONE

add feature to turn off on screen reporting of nodes visited -DONE

Development:

'''

# for the random number generator
import random

# program creates this file if not already created
outputFile = open("HW3goodwinOutfile.txt", "w")

introMessage = """Dice Rolling Simulation - 
User to make three selections at the start of the simulation.
Select yes or no to turn on or off verbose mode.  Verbose mode will display on screen a list of all nodes visted.
Select number of levels of the pyramid between 2 and 25.
Select number of times to run the simulation between 10 and 50.
Program simulates navigating of a pyramid of integers using a four sided die.
Number of the die indicates direction to travel on the pyramid.  If there is a valid location to travel to
then the location is updated and that location is marked as visited.  Every visit is recorded.
If a move is not valid, counts as another visit at the current location.
Game continues until all locations are visited.
When game terminates, vital statistics are reported."""

print(introMessage + "\n")
outputFile.write(introMessage + "\n\n")

# next section continually prompts until user selects yes or no for verbose mode.  verbose mode will show all
# visited location.  input is made not cast sensitive by using .lower method
# once valid entry is received, break from the while loop and proceed
# verbose mode off prevents display visited nodes from both screen and output file.  clarified in class
verboseModeAnswerNotValid = True
verbose = False
while verboseModeAnswerNotValid:
    verboseMode = input("Display all visited nodes (yes/no)?")
    verboseMode = verboseMode.lower()

    if verboseMode == 'yes':
        verbose = True
        verboseModeAnswerNotValid = False
        break
    if verboseMode == 'no':
        verbose = False
        verboseModeAnswerNotValid = False
        break
    if verboseMode is not {'yes', 'no'}: # if user input is not part of this set, loop while loop repeats until selected
        verboseModeAnswerNotValid = True


# follow section purpose is to obtain number of levels from the user.
numberOfLevelsIsNotValid = True  # controls while loop.  must become false to break the loop
numLevels = 2  # declare number of levels.  minimum is 2 levels

# this while loop continues until a valid int in range of 2 to 25 is received.
while numberOfLevelsIsNotValid:
    numLevels = input("Enter integer between 2 and 25 for number of levels")

    # Check if input is a valid int
    if numLevels.isdigit():
        # check if the int is in the range of 2 to 25
        if int(numLevels) in range(2, 26):
            numberOfLevelsIsNotValid = False
        else:
            print("Invalid number of levels")
            numberOfLevelsIsNotValid = True
    else:
        print("Integer not entered.")
        numberOfLevelsIsNotValid = True

print("You entered " + numLevels + " levels for the pyramid")

numberOfTimesSimRanIsNotValid = True  # controls the while loop.  must become false to break the loop
numTimesRan = 10  # declare number of times sim is ran.  default is 10

while numberOfTimesSimRanIsNotValid:
    numTimesRan = input("Enter number of times to run the simulation between 10 and 50:")

    # Check if input is a valid int
    if numTimesRan.isdigit():
        #check if the int is in the range of 10 to 50
        if int(numTimesRan) in range(10, 51):
            numberOfTimesSimRanIsNotValid = False
        else:
            print("Invalid number of times")
            numberOfTimesSimRanIsNotValid = True

    else:
        print("Integer not entered.")
        numberOfTimesSimRanIsNotValid = True

# print("You entered " + numTimesRan + " to run the sim")


# list declarations for recording statistics
allMoves = [0] * int(numTimesRan)
maxMoves = [0] * int(numTimesRan)

# calculate number of nodes
numNodes = int((int(numLevels) * (int(numLevels) + 1)) / 2)
# create gameDotTrackerV2. uses the number of nodes to create the list.  add 1 because lists are index starting at 0
gameDotTrackerV2 = [0] * (numNodes + 1)

# create gameBoard for Version 2 of pyramid. uses the number of nodes to create the list.  add 1 because lists are
# index starting at 0
gameBoardLocationV2 = [0, 0, 0, 0, 0] * (numNodes + 1)

# game boards for both version 1 and version follow the same encoding rules
#
# gameBoardLocation contains the game data for each position on the board.
# Encoding is as follows:
# index 0 - dot counter
# ended up not using the index 0 and opted for a separate list for the tracking of dots.  left in code for future use
# index 1 - Valid Upper Left Movement
# index 2 - Valid Lower Left Movement
# index 3 - Valid Upper Right Movement
# index 4 - Valid Lower Right Movement
# index of gameBoardLocation corresponds to a location on the pyramid.
# Example: gameBoardLocation[1] refers to position 1

# generate gameBoardLocationV2 size

# populate nodes

# gameBoardLocationV2[0] not used for this project.  initializing as in version 1
gameBoardLocationV2[0] = [0, None, None, None, None]
# level 1 and  level 2 are required. setting these as special cases.  they will not generate automatically
# same values as in version 1

for level in range(1, (int(numLevels) + 1)):
    # levels 1 and 2 are special cases and declared implicitly
    if level == 1:
        gameBoardLocationV2[1] = [0, None, 2, None, 3]  # dot count starts at 0, valid moves are lower left, lower right

    if level == 2:
        gameBoardLocationV2[2] = [0, None, 4, 1, 5]
        gameBoardLocationV2[3] = [0, 1, 5, None, 6]


    # generates the nodes for all the rows in the game board that are not row 1, 2 or the terminating row
    if level >= 3 and level < int(numLevels):

        # determine the rightMostNode
        rightMostNode = int((int(level) * (int(level) + 1) / 2))
        # determine the leftMostNode
        leftMostNode = int(rightMostNode) - (int(level) - 1)

        # populate right most node's valid locations into the list
        gameBoardLocationV2[rightMostNode] = [0, rightMostNode - int(level), rightMostNode + int(level), None,
                                              rightMostNode + int(level) + 1]

        # populate left most node's valid location into the list
        gameBoardLocationV2[leftMostNode] = [0, None, leftMostNode + int(level), leftMostNode - int(level) + 1,
                                             leftMostNode + int(level) + 1]


        # purpose of the following for loop is to generate the internal nodes and the valid moves for each of the
        # internal nodes.  start at the left most node and continue to the right most node
        # skips the calculation for left and right most nodes as they are defined as special cases
        # results validated against the version 1 of the hard encoded list from HW 1
        y = leftMostNode
        for internalNode in range(leftMostNode, rightMostNode + 1):
            if internalNode != leftMostNode and internalNode != rightMostNode:
                gameBoardLocationV2[internalNode] = [0, internalNode - int(level), internalNode + int(level), internalNode - int(level) + 1,
                                          internalNode + int(level) + 1]

    if level == int(numLevels):

        # determine the rightMostNode
        rightMostNode = int((int(numLevels) * (int(numLevels) + 1) / 2))
        print("right most node is: " + str(rightMostNode))
        # determine the leftMostNode
        leftMostNode = int(rightMostNode) - (int(numLevels) - 1)
        print("Left most node is: " + str(leftMostNode))

        # populate valid moves in the rightMostNode and leftMostNode
        gameBoardLocationV2[rightMostNode] = [0, rightMostNode - int(numLevels), None, None, None]
        gameBoardLocationV2[leftMostNode] = [0, None, None, leftMostNode - int(numLevels) + 1, None]

        # begin building internal nodes at the leftmostnode
        internalNode = leftMostNode
        for internalNode in range(leftMostNode, rightMostNode + 1):
            if internalNode != leftMostNode and internalNode != rightMostNode:
                gameBoardLocationV2[internalNode] = [0, internalNode - int(numLevels), None, internalNode - int(numLevels) + 1, None]



# this code used to validate gameboard generation
# for z in range(1, int(numNodes) + 1):
#    print("Location: " + str(z) + " is " + str(gameBoardLocationV2[z]))


'''
left this code so i could validate the results of the generated lists.  the above code if ran with 6 levels generates 
identical list to the below encoding

# gameBoardLocation encoding
gameBoardLocation[0] = [0, None, None, None, None]  # unused for this project
gameBoardLocation[1] = [0, None, 2, None, 3]  # dot count starts at 0, valid moves are lower left, lower right
gameBoardLocation[2] = [0, None, 4, 1, 5]
gameBoardLocation[3] = [0, 1, 5, None, 6]
gameBoardLocation[4] = [0, None, 7, 2, 8]
gameBoardLocation[5] = [0, 2, 8, 3, 9]
gameBoardLocation[6] = [0, 3, 9, None, 10]
gameBoardLocation[7] = [0, None, 11, 4, 12]
gameBoardLocation[8] = [0, 4, 12, 5, 13]
gameBoardLocation[9] = [0, 5, 13, 6, 14]
gameBoardLocation[10] = [0, 6, 14, None, 15]
gameBoardLocation[11] = [0, None, 16, 7, 17]
gameBoardLocation[12] = [0, 7, 17, 8, 18]
gameBoardLocation[13] = [0, 8, 18, 9, 19]
gameBoardLocation[14] = [0, 9, 19, 10, 20]
gameBoardLocation[15] = [0, 10, 20, None, 21]
gameBoardLocation[16] = [0, None, None, 11, None]
gameBoardLocation[17] = [0, 11, None, 12, None]
gameBoardLocation[18] = [0, 12, None, 13, None]
gameBoardLocation[19] = [0, 13, None, 14, None]
gameBoardLocation[20] = [0, 14, None, 15, None]
gameBoardLocation[21] = [0, 15, None, None, None]
# end encoding of gameboard V1
'''






runTimes = 0
# sim will repeat based on user input
for runTimes in range(1, int(numTimesRan) + 1):
    # stillPlaying controls if the game is continuing to play.  Once all locations have been visited once, stillPlaying
    # will change to false and terminate the game
    stillPlaying = True

    gameDotTrackerV2.clear()  # clear out the current dotTracker to make it ready for next run of the sim

    # i start the 0 location as 1 so that the game can end if no 0s are found in the list.  this requires an adjustment of
    # -1 to the game statistics
    gameDotTrackerV2 = [0] * (numNodes + 1)
    gameDotTrackerV2[0] = 1
    # i opted to count the start of the game as a visit to location 1.  remove this initialization to not have the start
    # counted as a visit
    gameDotTrackerV2[1] = 1
    diceRoll = 0
    currentLocation = 1  # game starts location 1.
    if verbose == True:
        print("Game Location: " + str(currentLocation), end='')
        outputFile.write("Game Location: " + str(currentLocation))

    while stillPlaying:

        # simulate a dice rolling by generating random value 1 to 4. Each value represents a direction to move as follows:
        # 1 = Upper Left, 2 = Lower Left, 3 = Upper Right, 4 = Lower Right
        diceRoll = random.randint(1, 4)
        # added this sleep so I could watch the program execute instead of instantly complete.
        # adjust this value to slow/down speed up the simulation
        # commented out as not a requirement of this assignment.  uncomment out to restore delay
        # time.sleep(0.015)

    # this section checks to see if the location selected by the dice roll is valid.  if so, updates the visit counter and
    # changes current location to the new location on the gameboard.
    # if the move is not valid, increments the counter for the currentlocation
        if gameBoardLocationV2[currentLocation][diceRoll] is not None:
            currentLocation = gameBoardLocationV2[currentLocation][diceRoll]
            # for progam efficieny, commenting out the dottracking in the location tuple since this isn't used in the final
            # calculations.  left for future use.
            # gameBoardLocation[currentLocation][0] += 1
            gameDotTrackerV2[currentLocation] += 1
            if verbose == True:
                print(",", end='')
                print(str(currentLocation), end='')
                outputFile.write("," + str(currentLocation))
            # commented code below allows for more verbose description of what is occurring in game
            # print("Move valid.  New Location is " + str(currentLocation) + ". Incrementing count. Location " + str(currentLocation) +
            # " has been visited " + str(gameBoardLocation[currentLocation][0]) + " times")
        else:
            # commented code below allows for more verbose description of what is occurring in game
            # print("Unable to move.  Incrementing count for location " + str(currentLocation))
            currentLocation = currentLocation
            gameDotTrackerV2[currentLocation] += 1
            # for progam efficieny, commenting out the dottracking in the location tuple since this isn't used in the final
            # calculations.  left for future use.
            # gameBoardLocation[currentLocation][0] += 1
            if verbose == True:
                print(",", end='')
                print(str(currentLocation), end='')
                outputFile.write("," + str(currentLocation))

    # this code checks to see if 0 does not exist in the gameDotTracker array.  If not, stillPlaying changes to False and the game ends
        if 0 not in gameDotTrackerV2:
            stillPlaying = False
            if verbose == True:
                print(".")
                outputFile.write(".\n")


    # Reporting statistics

    print("\nGame Statistics for game: " + str(runTimes))
    outputFile.write("\nGame Statistics for game: " + str(runTimes) + "\n\n")

    # need to adjust off 1 move from totalMoves in each calculation due to the unused element 0 in gameDotTracker being
    # initalized to 1.

    # stores the total moves for each run of the sim
    totalMoves: int = sum(gameDotTrackerV2)
    # need to adjust off 1 move from each recorded moves due to the setting of the 0 index to 1
    allMoves[runTimes - 1] = (totalMoves - 1)

    print("Total moves to complete the game: " + str(totalMoves - 1))
    outputFile.write("Total moves to complete the game: " + str(totalMoves - 1) + "\n")
    print("Average visits per location: " + str((totalMoves - 1)/21))
    outputFile.write("Average visits per location: " + str((totalMoves - 1)/21) + "\n")

    # find the maximum of dots on any one location
    maxDots = max(gameDotTrackerV2)
    maxMoves[runTimes - 1] = maxDots

    print("Maximum visits to any one location: " + str(maxDots) + "\n\n")
    outputFile.write("Maximum visits to any one location: " + str(maxDots) + "\n\n\n")

# Grand Total Statistics
print("Total Simulation Statistics\n")
outputFile.write("Total Simulation Statistics\n")

grandTotalMoves: int = sum(allMoves)
print("Minimum moves required to a complete a sim was: " + str(min(allMoves)))
outputFile.write("Minimum moves required to complete a sim was: " + str(min(allMoves)) + "\n")

print("Maximum moves required to complete a sim was: " + str(max(allMoves)))
outputFile.write("Maximum moves required to complete a sim was: " + str(max(allMoves)) + "\n")


# print("Grand total of all moves: " + str(grandTotalMoves))
# outputFile.write("Grand total of all moves to complete the sim: " + str(grandTotalMoves) + "\n")
averageMovesToCompleteTheSims = grandTotalMoves / int(numTimesRan)
print("Average number of moves to complete each sim: " + str(averageMovesToCompleteTheSims))
outputFile.write("Average number of moves to complete each sim: " + str(averageMovesToCompleteTheSims) + "\n")

print("Minimum max moves is: " + str(min(maxMoves)))
outputFile.write("Minimum max moves is: " + str(min(maxMoves)) + "\n")

print("Maximum max moves is: " + str(max(maxMoves)))
outputFile.write("Maximum max moves is: " + str(max(maxMoves)) + "\n")

averageMaxMoves = (sum(maxMoves) / int(numTimesRan))
print("Average number of max moves: " + str(averageMaxMoves))
outputFile.write("Average number of max moves: " + str(averageMaxMoves) + "\n")


# close the file being written
outputFile.close()


# testing
# used defined dice rolls to determine if currentlocation changed to expected location
# displayed gameDotTracker to be able to confirm dot summing and max dots to verify index
# git used for version control.
# tested upper and lower boundries for number of levels and number of times to run sim
# tested to validate user input is an int
# validated the generation of levels against original encoding.
# tested verbose on and off.  results as expected










