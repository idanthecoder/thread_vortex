class User:
    """
    A structure-like class that describes a user and how it is saved in the ORM database. 

    Attributes:
        username (str): Username (unique to each one).
        password (str): Password.
        mail (str): A valid mail address (unique to each one).
        age (str): Age (numerical).
        gender (str): Gender.
        country (str): Country.
        occupation (str): Occupation.
        date_creation (str): The date the profile was created.
        description (str): Description of the user.
    """
    
    def __init__(self, username: str, password: str, mail: str, age: str, gender: str, 
                 country: str, occupation: str, date_creation: str, description: str):
        """
        The constructor for User class.

        Args:
            username (str): Username (unique to each one).
            password (str): Password.
            mail (str): A valid mail address (unique to each one).
            age (str): Age (numerical).
            gender (str): Gender.
            country (str): Country.
            occupation (str): Occupation.
            date_creation (str): The date the profile was created.
            description (str): Description of the user.
        """
        
        self.username = username
        self.password = password
        self.mail = mail
        self.age = age
        self.gender = gender
        self.country = country
        self.occupation = occupation
        self.date_creation = date_creation
        self.description = description
    
    def edit_profile(self, age: str, gender: str, country: str, occupation: str, description: str):
        """
        Change attributes that the user can edit.

        Args:
            age (str): Age (numerical).
            gender (str): Gender.
            country (str): Country.
            occupation (str): Occupation.
            description (str): Description of the user.
        """ 
        self.age = age
        self.gender = gender
        self.country = country
        self.occupation = occupation
        self.description = description
    
    def clone(self):
        """
        Return another instance of the same user.

        Returns:
            User: A clone of the self user.
        """
        cloned_user = User(self.username, None, self.mail, self.age, self.gender, self.country, self.occupation, self.date_creation, self.description)
        return cloned_user

class MessageStruct:
    """
    A structure-like class that describes a message and how it is saved in the ORM database. 

    Attributes:
        content (str): The content of the message.
        date_published (str): The date the message was published.
        sender_username (str): The username of the sender.
        conversation_title (str): The title of the conversation that this message was sent in.
        id (int, optional): The id in the database. Defaults to None.
    """
    
    def __init__(self, content: str, date_published: str, sender_username: str, conversation_title: str, id=None):
        """
        The constructor for MessageStruct class.

        Args:
            content (str): The content of the message.
            date_published (str): The date the message was published.
            sender_username (str): The username of the sender.
            conversation_title (str): The title of the conversation that this message was sent in.
            id (int, optional): The id in the database. Defaults to None.
        """
        
        self.content = content
        self.date_published = date_published
        self.sender_username = sender_username
        self.conversation_title = conversation_title
        self.id = id


class ConversationStruct:
    """
    A structure-like class that describes a conversation and how it is saved in the ORM database. 

    Attributes:
        title (str): The title of the conversation,
        creator_username (str): The username of the conversation's creator,
        creation_date (str): The date in which the conversation was created.
        restrictions (str): The access restrictions of the conversation (18+ or nothing).
    """
    
    def __init__(self, title: str, creator_username: str, creation_date: str, restrictions: str):
        """
        The constructor for ConversationStruct class.

        Args:
            title (str): The title of the conversation,
            creator_username (str): The username of the conversation's creator,
            creation_date (str): The date in which the conversation was created.
            restrictions (str): The access restrictions of the conversation (18+ or nothing).
        """
        
        self.title = title
        self.creator_username = creator_username
        self.creation_date = creation_date
        self.restrictions = restrictions


class UsersMessagesVotes:
    """
    A structure-like class that describes a message vote of a user and how it is saved in the ORM database. 

    Attributes:
        username (str): The username of the voter.
        message_id (int): The id of the message that the user voted on.
        vote (int): The vote of the user (1:upvote, -1:downvote, 0:user regretted voting - no vote)
    """
    
    def __init__(self, username, message_id, vote):
        """
        The constructor for UsersMessagesVotes class.

        Args:
            username (str): The username of the voter.
            message_id (int): The id of the message that the user voted on.
            vote (int): The vote status (1:upvote, -1:downvote, 0:user regretted voting - no vote)
        """
        
        self.username = username
        self.message_id = message_id
        self.vote = vote


class UsersConversationsPins:
    """
    A structure-like class that describes a conversation pin of a user and how it is saved in the ORM database. 

    Attributes:
        username (str): The username of the user who pinned the conversation.
        conversation_title (str): The conversation title of the conversation that this user has pinned.
        pin (int): The pin status (1:pinned, 0:user regretted pinning - unpinned)
    """
    
    def __init__(self, username, conversation_title, pin):
        """
        The constructor for UsersConversationsPins class.

        Args:
            username (str): The username of the user who pinned the conversation.
            conversation_title (str): The conversation title of the conversation that this user has pinned.
            pin (int): The pin status (1:pinned, 0:user regretted pinning - unpinned)
        """
        
        self.username = username
        self.conversation_title = conversation_title
        self.pin = pin
