import app

class SqlOperations():
    def retrieveUploadedVideo(self):
        cur = app.conn.cursor()
        cur.execute(f"SELECT * FROM videoanalysisresults ORDER BY id ASC LIMIT 100")
        result = cur.fetchall()
        return result