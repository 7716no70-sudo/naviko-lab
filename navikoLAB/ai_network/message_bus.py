class MessageBus:

    def __init__(self):
        self.messages = []

    def send(self, sender, receiver, message):

        self.messages.append({
            "from": sender,
            "to": receiver,
            "message": message
        })

    def get(self):
        return self.messages