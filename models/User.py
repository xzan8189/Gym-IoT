class User:

    # Metodo costruttore
    def __init__(self, username: str, name: str, surname: str, password: str, registration_date: str):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.registration_date = registration_date

    # Getter
    def getUsername(self):
        return self.username
    def getName(self):
        return self.name
    def getSurname(self):
        return self.surname
    def getPassword(self):
        return self.password
    def getRegistration_date(self):
        return self.registration_date

    # Setter
    def setUsername(self, username):
        self.username = username
    def setName(self, name):
        self.name = name
    def setSurname(self, surname):
        self.surname = surname
    def setPassword(self, password):
        self.password = password
    def setRegistration_date(self, registration_date):
        self.registration_date = registration_date

    # Metodi d'appoggio

    # Metodi sovrascritti
    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.username == o.surname and self.name == o.name and self.surname == o.surname and self.password == o.password and self.registration_date == o.registration_date

    def __str__(self):
        return f"Username: {self.getUsername()}, " \
               f"Name: {self.getName()}, " \
               f"Surname: {str(self.getSurname())}, " \
               f"Password: {str(self.getPassword())}, " \
               f"Registration_date: {str(self.getRegistration_date())}"