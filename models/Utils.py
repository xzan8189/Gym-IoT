from models.User import User

class Utils:

    # Per lo User
    @staticmethod
    def dictUser_to_object(dict_user: dict) -> User:
        user = User(
            username=dict_user['Item']['username'],
            name=dict_user['Item']['name'],
            surname=dict_user['Item']['surname'],
            password=dict_user['Item']['password'],
            registration_date=dict_user['Item']['registration_date']
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