from urllib.request import urlopen
import re
from submission import Submission

def listOfHandlesToListOfUserId(handles):
    if (0 == len(handles)):
        return list()

    html = urlopen(r'https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=20&page=show_authorsrank&limit=100000&limitstart=0').read()

    unmatchedHandlesNumber = len(handles)
    userids = [None] * len(handles)

    for index in range(len(handles)):
        handle = handles[index]
        #TODO: compile
        match = re.search(b'<td align="center"><a href=".*userid=(\d+)">' + handle.encode('utf-8') + b'</a></td>', html)

        if match:
            userids[index] = int(match.group(1))
            unmatchedHandlesNumber -= 1

            if 0 == unmatchedHandlesNumber:
                return userids

    return userids

class User:
#public
    def __init__(self, name, handle = None, userid = None):
        self.handle = str(handle)
        self.userid = None if userid is None else int(userid)
        self.name = str(name)

    def getSubmissions(self):
        return self.submissions

    def hasUserId(self):
        return not (self.userid is None)

    def getHandle(self):
        return self.handle

    def getUserName(self):
        return self.name

    def setUserId(self, userid):
        self.userid = userid

    def updateSubmissions(self):
        if self.userid is None:
            return list()

        html = self.getUserStatisticsHTML()
        self.updateSolvedProblems(html)

        return self.submissions

#private
    def getUserStatisticsPageURL(self):
        return 'https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&page=show_authorstats&userid=%d' % self.userid

    def getUserStatisticsHTML(self):
        return urlopen(self.getUserStatisticsPageURL()).read() #TODO: read only relevant part

    def updateSolvedProblems(self, html):
        #TODO: compile
        submissionPattern = b'\t<tr class="sectiontableentry\d+">\n' \
                            b'\t<td align="center"><a href="[^"]*">(\d+)</a></td>\n' \
                            b'\t<td align="center">\d+</td>\n' \
                            b'\t<td align="center">\d+</td>\n' \
                            b'\t<td align="center">([^<]*)</td>\n' \
                            b'\t<td align="center">[^<]*</td>\n\t'
        tablePattern = b'<div class="contentheading">Solved problems</div>\n\t<table border="0" cellspacing="0" cellpadding="4" style="width:70%" align="center">\n\t<tr class="sectiontableheader"><th align="center">Problem</th><th align="center">Ranking</th><th align="center">Submission</th><th align="center">Date</th><th align="center">Run time</th></tr>\n\t' \
                       b'(' + submissionPattern + b')*' \
                                                  b'\t</table>'
        tableHTML = re.search(tablePattern, html).group(0)

        self.submissions = list()
        for match in re.finditer(submissionPattern, tableHTML):
            self.submissions.append(Submission(match.group(1).decode('utf-8'), match.group(2).decode('utf-8')))

if "__main__" == __name__:
    assert [213094, 96768] == listOfHandlesToListOfUserId(['a.shtefan', 'infoshoc'])

    pass