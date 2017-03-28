class Team:
    def __init__(self, users):
        self.users = tuple(users)

    def getSubmissions(self):
        teamSubmissions = list()

        for user in self.users:
            userSubmissions = user.updateSubmissions()
            teamSubmissions += userSubmissions
        return teamSubmissions

    def getUsers(self):
        return self.users

    #TODO: cache
    def getName(self):
        return ' & '.join(map(lambda user: user.getUserName(), self.getUsers()))