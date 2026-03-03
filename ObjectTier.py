from DataTier import cameraData
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class cameraManager:
    def __init__(self, db):
        self.dataLayer = cameraData(db)

    def printData(self):
        result = self.dataLayer.createStats()
        print("  Number of Red Light Cameras:", f"{result[0]:,}")
        print("  Number of Speed Cameras:", f"{result[1]:,}")
        print("  Number of Red Light Camera Violation Entries:", f"{result[2]:,}")
        print("  Number of Speed Camera Violation Entries:", f"{result[3]:,}")
        print("  Range of Dates in the Database:", f"{result[4]:} - {result[5]}")
        print("  Total Number of Red Light Camera Violations:", f"{result[6]:,}")
        print("  Total Number of Speed Camera Violations:", f"{result[7]:,}")

    def option1(self):
        userInput = input("Enter the name of the intersection to find (wildcards _ and % allowed): ")
        result = self.dataLayer.intersectionSearch(userInput)

        if result:
            print()
            for row in result:
                print(f"{row[0]} : {row[1]}")
            print()
        else:
            print("\nNo intersections matching that name were found.\n")

    def option2(self):
        userInput = input("Enter the name of the intersection (no wildcards allowed):\n")
        result = self.dataLayer.intersectionCameras(userInput)

        red = []
        speed = []

        if not result: 
            print()
            print("No red light cameras found at that intersection.")
            print("No speed cameras found at that intersection.")
            print()
            return
        
        for Camera_ID, Address, camType in result:
            if camType == 'redCams':
                red.append((Camera_ID, Address))
            else:
                speed.append((Camera_ID, Address))
        
        print()
        if red:
            print("Red Light Cameras:")
            for Camera_ID, Address in red:
                print(f"   {Camera_ID}: {Address}")
            print()
        else:
            print("No red light cameras found at that intersection.")
            print()
        
        if speed:
            print("Speed Cameras:")
            for Camera_ID, Address in speed:
                print(f"   {Camera_ID}: {Address}")
            print()
        else:
            print("No speed cameras found at that intersection.")
            print()

    def option3(self):
        userInput = input("Enter the date that you would like to look at (format should be YYYY-MM-DD): ")
        result = self.dataLayer.numberOfViolations(userInput)

        if not result or len(result) < 2:
            print("\nNo violations on record for that date.")
            return
        
        if not result[0] or not result[1]:
            print("\nNo violations on record for that date.")
            return
        
        redViolations = result[0][0]  
        speedViolations = result[1][0]
        
        total = redViolations + speedViolations
        
        redPercentage = (redViolations / total) * 100
        speedPercentage = (speedViolations / total) * 100

        print("\nNumber of Red Light Violations:", f"{redViolations:,} ({redPercentage:.3f}%)")
        print("Number of Speed Violations:", f"{speedViolations:,} ({speedPercentage:.3f}%)")
        print("Total Number of Violations:", f"{total:,}")
        print()

    def option4(self):
        result = self.dataLayer.numberOfCamsPerIntersection()
        red = []
        speed = []

        totalRed = 0
        totalSpeed = 0

        for intersection, ID, numCams, camType in result:
            if camType == 'redCams':
                red.append((intersection, ID, numCams))
            else:
                speed.append((intersection, ID, numCams))

        for intersection, ID, numCams in red:
            totalRed += numCams

        for intersection, ID, numCams in speed:
            totalSpeed += numCams

        print("Number of Red Light Cameras at Each Intersection")
        for intersection, ID, numCams in red:
            print(f"  {intersection} ({ID}) : {numCams} ({(numCams / totalRed) * 100:.3f}%)")
        print()

        print("Number of Speed Cameras at Each Intersection")
        for intersection, ID, numCams in speed:
            print(f"  {intersection} ({ID}) : {numCams} ({(numCams / totalSpeed) * 100:.3f}%)")
        print()

    def option5(self):
        userInput = input("Enter the year that you would like to analyze: ")
        result = self.dataLayer.getViolationData(userInput)

        red = []
        speed = []

        for intersection, ID, totalVio, camType, total in result:
            if camType == 'redVio':
                red.append((intersection, ID, totalVio, total))
            else:
                speed.append((intersection, ID, totalVio, total))

        print(f"\nNumber of Red Light Violations at Each Intersection for {userInput}" )
        if red:
            for intersection, ID, totalVio, total in red:
                print(f"  {intersection} ({ID}) : {totalVio:,} ({(totalVio / total) * 100:,.3f}%)")
            print(f"Total Red Light Violations in {userInput} : {total:,}")
        else:
            print("No red light violations on record for that year.")
        print()

        print(f"Number of Speed Violations at Each Intersection for {userInput}" )
        if speed:
            for intersection, ID, totalVio, total in speed:
                print(f"  {intersection} ({ID}) : {totalVio:,} ({(totalVio / total) * 100:,.3f}%)")
            print(f"Total speed Violations in {userInput} : {total:,}")
        else:
            print("No speed violations on record for that year.")
        print()

    def option6(self):
        inputCameraID = input("Enter a camera ID: ")
        result = self.dataLayer.fetchViolations(inputCameraID)
        
        if not result:
            print("\nNo cameras matching that ID were found in the database.\n")
            return 

        print(f"\nYearly Violations for Camera {inputCameraID}")
        for violationYear, numViolations in result:
            print(f"{violationYear} : {numViolations:,}")
        print()

        plotInput = input("Plot? (y/n) ")
        print()
        if plotInput == 'y':
            x = [violationYear for violationYear, numViolations in result]
            y = [numViolations for violationYear, numViolations in result]
            plt.plot(x, y)
            plt.xlabel("Year")
            plt.ylabel("Number of Violations")
            plt.title(f"Yearly Violations for camera {inputCameraID}")
            plt.show()

    def option7(self):
        inputCameraID = input("Enter a camera ID: ")
        print()

        camCheck = self.dataLayer.cameraExists(inputCameraID)
        if not camCheck:
            print("\nNo cameras matching that ID were found in the database.\n")
            return

        inputYear = input("Enter a year: ")

        result = self.dataLayer.fetchMonthlyViolations(inputCameraID, inputYear)

        print(f"\nMonthly Violations for Camera {inputCameraID} in {inputYear}")
        for violationDate, totalViolations, month in result:
            print(f"{violationDate} : {totalViolations:,}")
        print()

        plotInput = input("Plot? (y/n) ")

        if plotInput == 'y':
            x = [month for vDate, totalVio, month in result]
            y = [totalVio for vDate, totalVio, month in result]
            plt.plot(x, y)
            plt.xlabel("Month")
            plt.ylabel("Number of Violations")
            plt.title(f"Monthly Violations for Camera {inputCameraID} ({inputYear})")
            plt.show()
        print()

    def option8(self):
        inputYear = input("Enter a year: ")

        result = self.dataLayer.fetchDailyViolationsByYear(inputYear)

        red = []
        speed = []

        for violationDate, totalViolations, camType in result:
            if camType == 'red':
                red.append((violationDate, totalViolations))
            else:
                speed.append((violationDate, totalViolations))

        print("\nRed Light Violations: ")
        if red:
            for violationDate, totalViolations in red[:5]:
                print(f"  {violationDate} {totalViolations}")
            for violationDate, totalViolations in red[-5:]:
                print(f"  {violationDate} {totalViolations}")

        print("\nSpeed Violations: ")
        if speed:
            for violationDate, totalViolations in speed[:5]:
                print(f"  {violationDate} {totalViolations}")
            for violationDate, totalViolations in speed[-5:]:
                print(f"  {violationDate} {totalViolations}")

        inputPlot = input("\nPlot? (y/n) ")

        if inputPlot == 'y':
            redDict = {date: violations for date, violations in red}
            speedDict = {date: violations for date, violations in speed}

            year = int(inputYear)
            startDate = datetime(year, 1, 1)
            endDate = datetime(year, 12, 31)

            allDates = []
            redY = []
            speedY = []

            currentDate = startDate
            dayNumber = 1

            while currentDate <= endDate:
                dateStr = currentDate.strftime('%Y-%m-%d')
                allDates.append(dayNumber)
                redY.append(redDict.get(dateStr, 0))
                speedY.append(speedDict.get(dateStr, 0))
                currentDate += timedelta(days=1)
                dayNumber += 1

            plt.plot(allDates, redY, color='red', label='Red Light Violations')
            plt.plot(allDates, speedY, color='orange', label='Speed Violations')
            plt.xlabel("Day of Year")
            plt.ylabel("Number of Violations")
            plt.title(f"Violations by Day for {inputYear}")
            plt.legend()
            plt.show()
        print()

    def option9(self):
        userInput = input("Enter a street name: ")

        result = self.dataLayer.fetchCamerasByStreet(userInput)

        if not result:
            print(f"\nThere are no cameras located on that street.\n")
            return

        red = []
        speed = []

        for Cam_ID, Address, Lat, Long, camType in result:
            if camType == 'RedCams':
                red.append((Cam_ID, Address, Lat, Long))
            else:
                speed.append((Cam_ID, Address, Lat, Long))

        print(f"\nList of Cameras Located on Street: {userInput}")
        print("   Red Light Cameras: ")
        for Cam_ID, Address, Lat, Long in red:
            print(f"      {Cam_ID} : {Address} ({Lat}, {Long})")

        print("   Speed Cameras: ")
        for Cam_ID, Address, Lat, Long in speed:
            print(f"      {Cam_ID} : {Address} ({Lat}, {Long})")

        print()

        plotInput = input("Plot? (y/n) ")
        if plotInput == 'y':
            redX = [Long for _, _, _, Long in red]
            redY = [Lat for _, _, Lat, _ in red]
            speedX = [Long for _, _, _, Long in speed]
            speedY = [Lat for _, _, Lat, _ in speed]

            image = plt.imread("Data/chicago.png")
            xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
            plt.imshow(image, extent=xydims)
            plt.title(f"Cameras on Street: {userInput}")

            if red:
                plt.plot(redX, redY, 'ro-', label='Red Light Cameras')

            if speed:
                plt.plot(speedX, speedY, color='orange', marker='o', linestyle='-', label='Speed Cameras')

            for Cam_ID, Address, Lat, Long in red:
                plt.annotate(Cam_ID, (Long, Lat))

            for Cam_ID, Address, Lat, Long in speed:
                plt.annotate(Cam_ID, (Long, Lat))

            plt.xlim([-87.9277, -87.5569])
            plt.ylim([41.7012, 42.0868])
            plt.legend()
            plt.show()
        print()
