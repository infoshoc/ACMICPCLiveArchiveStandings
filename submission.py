from datetime import datetime

class Submission:
    def __init__(self, problemID, problemDateTime):
        self.id = int(problemID)
        self.time = datetime.strptime(str(problemDateTime), '%Y-%m-%d %H:%M:%S')

    def getTime(self):
        return self.time

    def getProblemId(self):
        return self.id

if "__main__" == __name__:
    pass