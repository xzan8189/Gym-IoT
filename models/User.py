class User:

    # Metodo costruttore
    def __init__(self, username: str, name: str, surname: str, password: str, registration_date: str, last_time_user_was_updated: str, sex: str, age: str, weight: str, height: str, calories_to_reach_today: str):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.registration_date = registration_date
        self.last_time_user_was_updated = last_time_user_was_updated
        self.sex = sex
        self.age = age
        self.weight = weight
        self.height = height
        self.calories_to_reach_today = calories_to_reach_today

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
    def getLast_time_user_was_updated(self):
        return self.last_time_user_was_updated
    def getSex(self):
        return self.sex
    def getAge(self):
        return self.age
    def getWeight(self):
        return self.weight
    def getHeight(self):
        return self.height
    def getCalories_lost_today(self):
        return self.calories_lost_today
    def getCalories_to_reach_today(self):
        return self.calories_to_reach_today

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
    def setLast_time_user_was_updated(self, last_time_user_was_updated):
        self.last_time_user_was_updated = last_time_user_was_updated
    def setSex(self, sex):
        self.sex = sex
    def setAge(self, age):
        self.age = age
    def setWeight(self, weight):
        self.weight = weight
    def setHeight(self, height):
        self.height = height
    def setCalories_lost_today(self, calories_lost_today):
        self.calories_lost_today = calories_lost_today
    def setCalories_to_reach_today(self, calories_to_reach_today):
        self.calories_to_reach_today = calories_to_reach_today

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
               f"Registration_date: {str(self.getRegistration_date())}, " \
               f"Last_time_user_was_updated: {self.getLast_time_user_was_updated()}" \
               f"Sex: {self.getSex()}, " \
               f"Age: {self.getAge()}, " \
               f"Weight: {self.getWeight()}, " \
               f"Height: {self.getHeight()}, " \
               f"Calories_to_reach_today: {self.getCalories_to_reach_today()}"