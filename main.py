import requests
from bs4 import BeautifulSoup

# Main program code

# TODO: change the options to work like terminal commands
introString = """
Stock Ticker Tracker (v0.1)
Current Actions:
    (1) Add new tracked ticker
    (2) Remove tracked ticker
    (3) List tracked tickers
    (4) List all tickers
    (5) Update all tracked tickers
    (6) Update single tracked ticker
    (7) Exit"""
exitProgram = False
while exitProgram == False :
    print(introString)
    userInput = input("Selection: ")
    if userInput == "1" :
        # Execute code for adding a new ticker
        print("\n")
        print("Adding new ticker for tracking")
        userInput = input("New ticker: ")
        # Check whether the ticker exists, and if it's already tracked


    elif userInput == "2" :
        # Execute code for removing a tracked ticker
        print("2")

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
        # Execute code for updating information for a single tracked ticker
        print("6")

    elif userInput == "7" :
        # Exit
        exitProgram = True
    else :
        print("Incorrect selection. Please try again.")
print("Quiting Stock Ticker Tracker")

def add_new_ticker (*args) :
    print("\nAdding a new ticker for tracking")
    userInput = input("Stock Ticker or Name: ")

    # Check whether the input ticker/name is contained in the current database

