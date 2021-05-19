import app

class VideoSqlOperations():
    def retrieveUploadedVideo(self):
        cur = app.conn.cursor()
        cur.execute(f"SELECT * FROM videoanalysisresults ORDER BY id ASC LIMIT 100")
        result = cur.fetchall()
        return result

class SensorSqlOperations():
    def insertNewRecord(self,userid,uploaddate):
        query = f"INSERT INTO uploadsensordata(userid, uploaddate) VALUES({userid}, {uploaddate})"
        cur = app.conn.cursor()
        cur.execute(query)

    def fetchSensorRecords(self):
        query = f"SELECT * FROM uploadsensordata"
        cur = app.conn.cursor()
        result = cur.fetchall()
        return result

    def insertTimedData(self,uploadsensorid, x , y, displacementtime):
        displacementxyz = "" + x + "," + y
        query = f"INSERT INTO sensordisplacementhistory(uploadsensorid, displacementxyz, displacementtime)" \
                f"VALUES({uploadsensorid}, {displacementxyz}, {displacementtime})"
        cur = app.conn.cursor()
        cur.execute(query)

    def fetchTimedData(self, uploadsensorid):
        query = f"SELECT * FROM sensordisplacementhistory WHERE uploadsensorid = {uploadsensorid}"
        cur = app.conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result
