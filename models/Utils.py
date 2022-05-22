from models.User import User
import datetime

class Utils:

    # Per lo User

    # Kcal che deve perdere il cliente giornalmente
    @staticmethod
    def calculate_calorie_deficit(sex: str, weight: float, height: float, age: int) -> float:
        # Mifflin-St. Jeor equation
        if (sex == 'F'): # for Females
            return (10 * weight) + (6.25 * height) - (5 * age) - 161
        elif (sex == 'M'): # for Fales
            return (10 * weight) + (6.25 * height) - (5 * age) + 5

    @staticmethod
    def calculate_monthly_target_percentage(user: dict) -> int:
        workouts_per_week = 3 # quante volte va in palestra, ma negli sviluppi futuri si potrebbe modificare questo parametro a piacimento
        number_of_weeks = 4  # sarebbero le settimane del mese

        calories_lost = float(user['gym']['data']['calories_lost'])
        calories_to_reach_monthly = float(user['gym']['data']['calories_to_reach_today']) * (
                    workouts_per_week * number_of_weeks)

        print(f'calculate_monthly_target_percentage: {calories_lost} * 100 / {calories_to_reach_monthly} = {int(calories_lost * 100 / calories_to_reach_monthly)}%')
        return int(calories_lost * 100 / calories_to_reach_monthly)

    @staticmethod
    def dictUser_to_object(dict_user: dict) -> User:
        user = User(
            username=dict_user['Item']['username'],
            name=dict_user['Item']['name'],
            surname=dict_user['Item']['surname'],
            password=dict_user['Item']['password'],
            registration_date=dict_user['Item']['registration_date'],
            sex=dict_user['Item']['info']['sex'],
            age=dict_user['Item']['info']['age'],
            weight=dict_user['Item']['info']['weight'],
            height=dict_user['Item']['info']['height'],
            calories_to_reach_today=dict_user['Item']['gym']['data']['calories_to_reach_today']
        )

        return user

    @staticmethod
    def objectUser_to_dict(obj_user: User) -> dict:
        new_customer = {
            'username': obj_user.getUsername(),
            'name': obj_user.getName(),
            'surname': obj_user.getSurname(),
            'password': obj_user.getPassword(),
            'registration_date': obj_user.getRegistration_date()
        }

        return new_customer

    @staticmethod
    def create_objectUser_to_dict(obj_user: User) -> dict:
        new_customer = {
            'username': obj_user.getUsername(),
            'name': obj_user.getName(),
            'surname': obj_user.getSurname(),
            'password': obj_user.getPassword(),
            'registration_date': obj_user.getRegistration_date(),
            'last_time_user_was_updated': obj_user.getLast_time_user_was_updated(),
            'info': {
                "sex": obj_user.getSex(),
                "age": obj_user.getAge(),
                "weight": f'{obj_user.getWeight()}',
                "height": f'{obj_user.getHeight()}'
            },
            'gym': {
                "calories": {
                    str(datetime.datetime.now().year): ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                },
                "machines": {
                    "name_machine": ["Cyclette", "Tapis_roulant", "Elliptical_bike", "Spin_bike"],
                    "time_spent": ["0", "0", "0", "0"],
                    "calories_spent": ["0", "0", "0", "0"]
                },
                "data": {
                    "calories_lost": "0",
                    "calories_lost_today": "0",
                    "calories_to_reach_today": f'{obj_user.getCalories_to_reach_today()}'
                }
            }
        }

        return new_customer
