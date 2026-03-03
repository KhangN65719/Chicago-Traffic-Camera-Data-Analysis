import sqlite3

class cameraData:
    def __init__(self, db):
        self.dbconn = sqlite3.connect(db)
        self.dbcursor = self.dbconn.cursor()

    def createStats(self):
        sql = """
            SELECT
            (SELECT COUNT(*) FROM RedCameras),
            (SELECT COUNT(*) FROM SpeedCameras),
            (SELECT COUNT(Num_Violations) FROM RedViolations),
            (SELECT COUNT(Num_Violations) FROM SpeedViolations),
            (SELECT MIN(Violation_Date)
                FROM(
                    SELECT Violation_Date FROM RedViolations
                    UNION
                    SELECT Violation_Date FROM SpeedViolations
                ) AS AllDates
            ),
            (SELECT MAX(Violation_Date)
                FROM(
                    SELECT Violation_Date FROM RedViolations
                    UNION
                    SELECT Violation_Date FROM SpeedViolations
                ) AS AllDates
            ),
            (SELECT SUM(Num_Violations) From RedViolations),
            (SELECT SUM(Num_Violations) From SpeedViolations);
        """
        self.dbcursor.execute(sql)
        return self.dbcursor.fetchone()
    
    def intersectionSearch(self, userInput):
        sql = """
            SELECT Intersection_ID, Intersection 
            FROM Intersections 
            WHERE Intersection LIKE ?
            ORDER BY Intersection ASC
        """
        self.dbcursor.execute(sql, (userInput,))
        return self.dbcursor.fetchall()

    def intersectionCameras(self, userInput):
        sql = """
            SELECT Camera_ID, Address, 'redCams'
            FROM RedCameras
            INNER JOIN Intersections
            ON RedCameras.Intersection_ID = Intersections.Intersection_ID 
            WHERE Intersection = ?
            UNION
            SELECT Camera_ID, Address, 'speedCams'
            FROM SpeedCameras
            INNER JOIN Intersections
            ON SpeedCameras.Intersection_ID = Intersections.Intersection_ID 
            WHERE Intersection = ?
            ORDER BY Camera_ID ASC
        """
        self.dbcursor.execute(sql, (userInput, userInput,))
        return self.dbcursor.fetchall()
    
    def numberOfViolations(self, userInput):
        sql = """
            SELECT SUM(Num_Violations)
            FROM RedViolations
            WHERE Violation_Date = ?
            UNION ALL
            SELECT SUM(Num_Violations)
            FROM SpeedViolations
            WHERE Violation_Date = ?
            GROUP BY Violation_Date
        """
        self.dbcursor.execute(sql, (userInput, userInput,))
        return self.dbcursor.fetchall()

    def numberOfCamsPerIntersection(self):
        sql = """
            SELECT Intersection, Intersections.Intersection_ID, COUNT(*) AS numCams, 'redCams'
            FROM Intersections
            INNER JOIN RedCameras 
            ON RedCameras.Intersection_ID = Intersections.Intersection_ID
            GROUP BY Intersection
            UNION ALL
            SELECT Intersection, Intersections.Intersection_ID, COUNT(*) AS numCams, 'speedCams'
            FROM Intersections
            INNER JOIN SpeedCameras 
            ON SpeedCameras.Intersection_ID = Intersections.Intersection_ID
            GROUP BY Intersection
            ORDER BY numCams DESC, Intersections.Intersection_ID DESC
        """
        self.dbcursor.execute(sql)
        return self.dbcursor.fetchall()
    
    def getViolationData(self, userInput):
        sql = """
            SELECT Intersection, Intersections.Intersection_ID, SUM(RedViolations.Num_Violations) AS totalVio, 
                'redVio', SUM(SUM(Num_Violations)) OVER() AS total 
            FROM Intersections
            INNER JOIN RedCameras
            ON Intersections.Intersection_ID = RedCameras.Intersection_ID
            INNER JOIN RedViolations 
            ON RedCameras.Camera_ID = RedViolations.Camera_ID 
            WHERE strftime('%Y', Violation_Date) = ?
            GROUP BY Intersection
            UNION ALL
            SELECT Intersection, Intersections.Intersection_ID, SUM(SpeedViolations.Num_Violations) AS totalVio, 
                'speedVio', SUM(SUM(Num_Violations)) OVER() AS total 
            FROM Intersections
            INNER JOIN SpeedCameras
            ON Intersections.Intersection_ID = SpeedCameras.Intersection_ID
            INNER JOIN SpeedViolations 
            ON SpeedCameras.Camera_ID = SpeedViolations.Camera_ID 
            WHERE strftime('%Y', Violation_Date) = ?
            GROUP BY Intersection
            ORDER BY totalVio DESC, Intersections.Intersection_ID DESC
        """
        self.dbcursor.execute(sql, (userInput, userInput,))
        return self.dbcursor.fetchall()
    
    def fetchViolations(self, inputCameraID):
        sql = """
            SELECT strftime('%Y', Violation_Date) AS Year, SUM(Num_Violations)
            FROM RedViolations
            WHERE Camera_ID = ?
            GROUP BY Year
            UNION
            SELECT strftime('%Y', Violation_Date) AS Year, SUM(Num_Violations)
            FROM SpeedViolations
            WHERE Camera_ID = ?
            GROUP BY Year
            ORDER BY Year ASC
        """
        self.dbcursor.execute(sql, (inputCameraID, inputCameraID,))
        return self.dbcursor.fetchall()

    def cameraExists(self, inputCameraID):
        """Check if a camera ID exists in either violation table."""
        sql = """
            SELECT Camera_ID
            FROM RedViolations
            WHERE Camera_ID = ?
            UNION 
            SELECT Camera_ID
            FROM SpeedViolations
            WHERE Camera_ID = ?
        """
        self.dbcursor.execute(sql, (inputCameraID, inputCameraID))
        return self.dbcursor.fetchall()

    def fetchMonthlyViolations(self, inputCameraID, inputYear):
        """Fetch monthly violation totals for a given camera ID and year."""
        sql = """
            SELECT strftime('%m/%Y', Violation_Date) AS monthYear, SUM(Num_Violations) AS Total, strftime('%m', Violation_Date) AS month
            FROM RedViolations
            WHERE Camera_ID = ? AND strftime('%Y', Violation_Date) = ?
            GROUP BY monthYear
            UNION ALL
            SELECT strftime('%m/%Y', Violation_Date) AS monthYear, SUM(Num_Violations) AS Total, strftime('%m', Violation_Date) AS month
            FROM SpeedViolations
            WHERE Camera_ID = ? AND strftime('%Y', Violation_Date) = ?
            GROUP BY monthYear
            ORDER BY monthYear ASC
        """
        self.dbcursor.execute(sql, (inputCameraID, inputYear, inputCameraID, inputYear,))
        return self.dbcursor.fetchall()

    def fetchDailyViolationsByYear(self, inputYear):
        """Fetch daily red and speed violation totals for a given year."""
        sql = """
            SELECT Violation_Date, SUM(Num_Violations), 'red'
            FROM RedViolations
            WHERE strftime('%Y', Violation_Date) = ?
            GROUP BY Violation_Date
            UNION ALL
            SELECT Violation_Date, SUM(Num_Violations), 'speed'
            FROM SpeedViolations
            WHERE strftime('%Y', Violation_Date) = ?
            GROUP BY Violation_Date
            ORDER BY Violation_Date ASC
        """
        self.dbcursor.execute(sql, (inputYear, inputYear,))
        return self.dbcursor.fetchall()

    def fetchCamerasByStreet(self, userInput):
        """Fetch all cameras (red and speed) whose address matches the given street name."""
        sql = """
            SELECT Camera_ID, Address, Latitude, Longitude, 'RedCams'
            FROM RedCameras
            WHERE Address LIKE ?
            UNION ALL
            SELECT Camera_ID, Address, Latitude, Longitude, 'SpeedCams'
            FROM SpeedCameras
            WHERE Address LIKE ?
            ORDER BY Camera_ID ASC
        """
        userInputWithWildcard = f"%{userInput}%"
        self.dbcursor.execute(sql, (userInputWithWildcard, userInputWithWildcard,))
        return self.dbcursor.fetchall()
