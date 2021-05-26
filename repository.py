import app
import json
from pandas import DataFrame

class VideoSqlOperations():
    def retrieveUploadedVideo(self):
        cur = app.conn.cursor()
        cur.execute(f"SELECT * FROM videoanalysisresults")
        df = DataFrame(cur.fetchall())
        df.columns = [desc[0] for desc in cur.description]
        return df


    def insertNewRecordVideo(self,dispacelementxy,displacemenettime):
        query = f"INSERT INTO videodisplacementhistory(dispacelementxy, displacemenettime) VALUES({dispacelementxy}, {displacemenettime})"
        cur = app.conn.cursor()
        cur.execute(query)

    def retrieveUploadedVideoRecords(self):
        cur = app.conn.cursor()
        cur.execute(f"SELECT * FROM videoanalysisresults as va JOIN videodisplacementhistory as vd va.id = vd.videoanalysisid")
        df = DataFrame(cur.fetchall())
        df.columns = [desc[0] for desc in cur.description]
        return df



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
