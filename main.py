from user import User, listOfHandlesToListOfUserId
from team import Team
from datetime import datetime
import tkinter

updateTimeoutSeconds = 30*1000

def tryToSetUserIds(teams):
    handles = list()
    for team in teams:
        for user in team.getUsers():
            if not user.hasUserId():
                handles.append(user.getHandle())

    userids = listOfHandlesToListOfUserId(handles)

    for team in teams:
        for user in team.getUsers():
            if not user.hasUserId():
                userid = userids.pop(0)

                if not (userid is None):
                    user.setUserId(userid)
                else:
                    print('User with handle %s still not found' % user.getHandle())

def teamsToNumberOfSolvedPenaltyTeamNameProblem2SubmissionTime(teams):
    # TODO: ugly code - rewrite
    numberOfSolvedPenaltyTeamNameProblem2submissionTime = list()
    for team in teams:
        teamSubmissions = team.getSubmissions()

        problemId2SubmissionTime = dict()

        for submission in teamSubmissions:
            if submission.getProblemId() not in problemId2SubmissionTime or \
                            submission.getTime() < problemId2SubmissionTime[submission.getProblemId()]:
                problemId2SubmissionTime[submission.getProblemId()] = submission.getTime()

        numberOfSolved = len(problemId2SubmissionTime)
        penalty = sum(
            map(lambda submissionTime: (problemId2SubmissionTime[submissionTime] - startContestTime).seconds / 60,
                problemId2SubmissionTime))
        numberOfSolvedPenaltyTeamNameProblem2submissionTime.append(
            (numberOfSolved, penalty, team.getName(), problemId2SubmissionTime))

    numberOfSolvedPenaltyTeamNameProblem2submissionTime = list(reversed(sorted(
        numberOfSolvedPenaltyTeamNameProblem2submissionTime)))

    return numberOfSolvedPenaltyTeamNameProblem2submissionTime

def numberOfSolvedPenaltyTeamNameProblem2submissionTime2table(problemIds, numberOfSolvedPenaltyTeamNameProblem2submissionTime):
    table = [['' for c in range(1 + len(problemIds))] for r in range(1 + len(teams))]

    for r in range(1 + len(teams)):
        for c in range(1 + len(problemIds)):
            if 0 == r and 0 == c:
                text = ''
            elif 0 == r:
                text = str(problemIds[c - 1])
            elif 0 == c:
                text = numberOfSolvedPenaltyTeamNameProblem2submissionTime[r - 1][2]
            else:
                if problemIds[c - 1] in numberOfSolvedPenaltyTeamNameProblem2submissionTime[r - 1][3]:
                    text = '%0.2f m' % ((numberOfSolvedPenaltyTeamNameProblem2submissionTime[r - 1][3][
                                             problemIds[c - 1]] - startContestTime).seconds / 60)
                else:
                    text = '-'

            table[r][c] = text

    return table

def writeToHTML(table, outputFileName='standings.html'):
    def wrapRow(row):
        return '<tr>%s</tr>' % row

    def wrapCell(cell):
        return '<td>%s</td>' % cell

    html = '<meta http-equiv="refresh" content="%d"><table>\n%s\n</table>' % (updateTimeoutSeconds, '\n'.join(map(wrapRow,
        [
            '\n'.join(map(wrapCell, table[row]))
                for row in range(len(table))
        ]
    )))

    with open(outputFileName, 'w') as fileHandler:
        fileHandler.write(html)

    return html

class Standings(tkinter.Tk):
    def __init__(self, teams, problemIds, startContestTime, finishContestTime, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.teams = tuple(teams)
        self.problemIds = problemIds
        self.startContestTime = startContestTime
        self.finishContestTime = finishContestTime
        self.updateTable()

    def updateTable(self):
        tryToSetUserIds(self.teams)

        numberOfSolvedPenaltyTeamNameProblem2submissionTime = \
            teamsToNumberOfSolvedPenaltyTeamNameProblem2SubmissionTime(teams)

        table = numberOfSolvedPenaltyTeamNameProblem2submissionTime2table(problemIds, numberOfSolvedPenaltyTeamNameProblem2submissionTime)

        #TODO: update instead of create if possible
        for r in range(len(table)):
            for c in range(len(table[r])):
                tkinter.Label(
                    self,
                    text=table[r][c],
                    borderwidth=1
                ).grid(
                    row=r,
                    column=c
                )

        writeToHTML(table)

        self.after(updateTimeoutSeconds, self.updateTable)

if "__main__" == __name__:
    teams = [
        Team((
            User(name='Volodymyr', handle='infoshoc'),
            User(name='Artem', handle='a.shtefan'),
        )),
        Team((
            User(name='Denis', handle='denyswitchof'),
            User(name='Alex', handle='RandoMize'),
        )),
        Team((
            User(name='Vasya Pupkin', handle='infoshoc42'), #Fake one
        ))
    ]
    problemIds = [4976, 4977, 6884, 7275]
    #TODO: fix timezone. Currently need to convert from +3 to +0 (-3)
    startContestTime = datetime.strptime(r'2017-03-27 13:30:00','%Y-%m-%d %H:%M:%S')
    finishContestTime = datetime.strptime(r'2017-03-27 15:30:00','%Y-%m-%d %H:%M:%S')


    root = Standings(teams, problemIds, startContestTime, finishContestTime)
    root.mainloop()