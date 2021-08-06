class Chat():
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def __str__(self):
        out = {
            "chat_name" : self.name,
            "members": self.members
        }
        return str(out)
