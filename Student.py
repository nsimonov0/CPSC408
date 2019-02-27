class Student:
    def __init__(self, firstname, lastname, gpa, major, facultyadvisor):
        self.firstname = firstname
        self.lastname = lastname
        self.gpa = gpa
        self.major = major
        self.facultyadvisor = facultyadvisor

    def getFirstName(self):
        return self.firstname

    def getLastName(self):
        return self.lastname

    def getGpa(self):
        return self.gpa

    def getMajor(self):
        return self.major

    def getFacultyAdvisor(self):
        return self.facultyadvisor

    def getStudentTuple(self):
        return (self.getFirstName(), self.getLastName(), self.getGpa(), self.getMajor(), self.getFacultyAdvisor())