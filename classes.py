class User:
    def __init__(self, name: str, password: str, mail: str, age: int, birthdate, gender: str,
                 description: str, country, workplace, date_creation):
        self.name = name
        self.password = password
        self.mail = mail
        self.age = age
        self.birthdate = birthdate
        self.gender = gender
        self.description = description
        self.country = country
        self.workplace = workplace
        self.date_creation = date_creation


class Message:
    def __init__(self, content: str, sender: User, date_published: str, conversation_id):
        self.content = content
        self.seder = sender
        self.date_published = date_published
        self.conversation_id = conversation_id


class Conversation:
    def __init__(self, initialize_date, title, restrictions, message_lst=None):
        if message_lst is None:
            message_lst = []
        else:
            self.message_lst = message_lst
        self.initialize_date = initialize_date
        self.title = title
        self.restrictions = restrictions