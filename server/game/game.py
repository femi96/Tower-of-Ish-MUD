import time


class GameResponse():
    """
    Class for response messages from Game

    Contains list of usernames to send response too, and message to send
    """

    def __init__(self, usernames, message):
        if type(usernames) == str:
            self.usernames = [usernames]
        else:
            self.usernames = usernames
        self.message = message

    def __iter__(self):
        for username in self.usernames:
            yield (username, self.message)


class Game():
    """
    Class for game
    """

    def __init__(self):
        self.name = "The Garden"
        self.time = time.time()
        self.clock = 0

    def input(self, username, message):
        """
        Apply an input to this game

        Returns a list of game updates to broadcast
        """

        # Parse message, apply as appropriate
        msg_tokens = self.tokenize(message)

        # Help
        if msg_tokens[0].lower() in {"h", "help"}:
            return [GameResponse(username, "Type help or h for help")]

        # Say
        if msg_tokens[0].lower() in {"s", "say"}:
            pass

        return [GameResponse(username, "Unknown input")]

    def tokenize(self, message):
        return message.split(" ")

    def update(self):
        new_time = time.time()
        delta_time = new_time - self.time
        self.time = new_time

        responses = []

        self.clock += delta_time
        if self.clock > 60:
            print("A minute has passed")
            self.clock -= 4
            for username in ["Femi"]:
                responses.append(
                    GameResponse(username, "A minute has passed")
                )

        return responses


class Item():
    """
    Base class for items
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return "{}\n=====\n{}\n".format(self.name, self.description)


class Weapon(Item):
    """
    Base class for weapons, sub class of items
    """

    def __init__(self, name, description, damage):
        self.damage = damage
        super().__init__(name, description)

    def __str__(self):
        return "{}\n=====\n{}\n".format(self.name, self.description)


class Character():

    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.inventory = Inventory()

    def is_alive(self):
        return self.hp > 0


class Inventory():

    def __init__(self):
        self.item_list = []

    def add_item(self, item):
        self.item_list.append(item)


class Room():

    def __init__(self):
        self.contents_list = []

if __name__ == '__main__':
    pass
