class Message():
    # sender = None -->  message sent by bot

    def __init__(self, sender, content):
        self.sender = sender
        self.content = content # includes the command
        self.body = "" # excludes the command

    def __str__(self):
        out = "SENDER : " + str(self.sender) + "\nCONTENT : " + str(self.content)
        return out
