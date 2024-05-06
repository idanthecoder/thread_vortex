class User:
    def __init__(self, username: str, password: str, mail: str, age: int, gender: str, 
                 country: str, occupation: str, date_creation: str, description: str):
        self.username = username
        self.password = password
        self.mail = mail
        self.age = age
        self.gender = gender
        self.country = country
        self.occupation = occupation
        self.date_creation = date_creation
        self.description = description
    
    def edit_profile(self, age: int, gender: str, country: str, occupation: str, description: str):
        self.age = age
        self.gender = gender
        self.country = country
        self.occupation = occupation
        self.description = description
    
    def clone(self):
        cloned_user = User(self.username, None, self.mail, self.age, self.gender, self.country, self.occupation, self.date_creation, self.description)
        return cloned_user


#class Message:
#    def __init__(self, content: str, sender: User, date_published: str, conversation_id: int):
#        self.content = content
#        self.sender = sender
#        self.date_published = date_published
#        self.conversation_id = conversation_id

class Message:
    def __init__(self, content: str, sender: User, date_published: str):
        self.content = content
        self.sender = sender
        self.date_published = date_published

class MessageVServer:
    def __init__(self, content: str, date_published: str, sender_username: str, conversation_title: str):
        self.content = content
        self.date_published = date_published
        self.sender_username = sender_username
        self.conversation_title = conversation_title

class Conversation:
    def __init__(self, title: str, creator_username: int, creation_date: str, restrictions: str, message_lst: list[Message]=None):
        self.title = title
        self.creator_username = creator_username
        self.creation_date = creation_date
        self.restrictions = restrictions
        if message_lst is None:
            message_lst = []
        else:
            self.message_lst = message_lst

class ConversationVServer:
    def __init__(self, title: str, creator_username: str, creation_date: str, restrictions: str):
        self.title = title
        self.creator_username = creator_username
        self.creation_date = creation_date
        self.restrictions = restrictions



#class Conversation:
#    def __init__(self, id: int, creation_date: str, title: str, restrictions: list[str], message_lst: list[Message]=None):
#        if message_lst is None:
#            message_lst = []
#        else:
#            self.message_lst = message_lst
#        self.creation_date = creation_date
#        self.title = title
#        self.restrictions = restrictions