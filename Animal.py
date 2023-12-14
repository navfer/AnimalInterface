class Animal:
    headings = ['ID', 'Name', 'Owner', 'Phone', 'Age', 'Pos']
    fields = {
        '-ID-': 'Animal ID:',
        '-Name-': 'Animal Name:',
        '-Owner-': 'Owner:',
        '-Phone-': 'Phone:',
        '-Age-': 'Age:',
        '-PosFile-': 'Position into File'
    }

    def __init__(self, ID, name, owner, phone, age, posFile):   #Constructor
        self.ID = ID
        self.name = name
        self.owner = owner
        self.phone = phone
        self.age = age
        self.posFile = posFile
        self.erased = False

    def __eq__(self, oA):   #Equals method
        return oA.posFile == self.posFile

    def __str__(self):  #ToString method
        return str(self.ID) + str(self.name) + str(self.owner) + str(self.phone) + str(self.age) + str(self.posFile)

    def animalInPos(self, pos):
        return self.posFile == pos

    def setAnimal(self, name, owner, phone, age):
        self.name = name
        self.owner = owner
        self.phone = phone
        self.age = age

