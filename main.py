import os
import sys
import sqlite3

import database
import menuCommands

# Main program code

# TODO: change the options to work like terminal commands,
#       make it so that you can choose which database to use, and pass the
#       cursor for that database to the different functions. add functions to
#       init a new database...
exitProgram = False
if len(sys.argv) != 2 :
    print("Please enter database that you would like to open as a " \
          "console argument")
    exitProgram = True
else :
    tmpStr = sys.argv[1].split("/")
    dirStr = ""
    for index in range(0,len(tmpStr)-1) :
        dirStr += tmpStr[index] + "/"
    if os.path.isdir(dirStr) == False :
        print("Path to database doesn't exist")
        exitProgram = True
    else :
        if os.path.isfile(sys.argv[1]) == False :
            database.create_database(sys.argv[1])
        conn = sqlite3.connect(sys.argv[1])
        cur = conn.cursor()

while exitProgram == False :
    print(menuCommands.introString)
    userInput = input("Selection: ")
    if userInput == "1" :
        # Execute code for adding a new ticker
        print("\n")
        print("Adding new stock for tracking")
        foundStock = False
        while foundStock == False :
            print("Enter 'quit' to exit to main menu")
            userInput = input("New stock: ")
            if userInput == "quit" :
                break
            else :
                foundStock = database.track_stock(userInput,conn)


    elif userInput == "2" :
        # Execute code for removing a tracked ticker
        print("\n")
        print("Removing stock from tracking")
        foundStock = False
        while foundStock == False :
            print("Enter 'quit' to exit to main menu")
            userInput = input("Remove stock: ")
            if userInput == "quit" :
                break
            else :
                foundStock = database.untrack_stock(userInput,conn)

    elif userInput == "3" :
        # Execute code for listing all currently tracked tickers
        print("3")

    elif userInput == "4" :
        # Execute code for listing all the tickers that can be tracked
        print("4")

    elif userInput == "5" :
        # Execute code for updating all the information for the tracked tickers
        print("5")

    elif userInput == "6" :
        # Exit
        exitProgram = True
    else :
        print("Incorrect selection. Please try again.")
print("Quiting Stock Ticker Tracker")
