import sqlite3
import matplotlib.pyplot as plt

from ObjectTier import cameraManager

Data = cameraManager('Data/chicago-traffic-cameras.db')

def printDescript():
    print("Project 2: Chicago Traffic Camera Analysis")
    print("CS 341, Spring 2026")
    print()
    print("This application allows you to analyze various")
    print("aspects of the Chicago traffic camera database.")
    print()
    Data.printData()
    print()

def printMenu():
    print("Select a menu option: ")
    print("  1. Find an intersection by name")
    print("  2. Find all cameras at an intersection")
    print("  3. Percentage of violations for a specific date")
    print("  4. Number of cameras at each intersection")
    print("  5. Number of violations at each intersection, given a year")
    print("  6. Number of violations by year, given a camera ID")
    print("  7. Number of violations by month, given a camera ID and year")
    print("  8. Compare the number of red light and speed violations, given a year")
    print("  9. Find cameras located on a street")
    print("or x to exit the program.")
    choice = input("Your choice --> ")
    print()
    return choice

printDescript()

while True:
    choice = printMenu()

    match choice:
        case '1':
            Data.option1()
        case '2':
            Data.option2()
        case '3':        
            Data.option3()
        case '4':
            Data.option4()
        case '5':
            Data.option5()
        case '6':
            Data.option6()
        case '7':
            Data.option7()
        case '8':
            Data.option8()
        case '9':
            Data.option9()
        case 'x':
            print("Exiting program.")
            break
        case _:
            print("Error, unknown command, try again...\n")
