import random


class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __str__(self):
        return f"{self.color} {self.number}"


class Deck:
    def __init__(self):
        self.cards = []
        colors = ["red", "green", "blue", "yellow"]
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "skip", "reverse", "draw two"]
        for color in colors:
            for number in numbers:
                self.cards.append(Card(color, number))
                if number != "0":
                    self.cards.append(Card(color, number))

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop(0)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.deal())

    def play(self, number, game_pile):
        if number >= 0 or number < len(self.hand):
            #self.hand.pop(number)
            game_pile.append(self.hand.pop(number))
            return True
        return False

    def has_won(self):
        return len(self.hand) == 0

    def __str__(self):
        return self.name


class Game:
    def __init__(self, player_names):
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self.game_pile = []
        self.current_player_index = 0
        self.direction = 1

    def next_player(self):
        self.current_player_index = self.current_player_index + self.direction
        self.current_player_index = self.current_player_index % len(self.players)
        # int(self.current_player_index)

    def play_card(self, index):
        while index < -2 or index >= len(self.players[self.current_player_index].hand):
            index = int(input("choose a valid index or enter -1 to draw card: "))
        if index == -1:
            self.players[self.current_player_index].draw(self.deck)
            print(f"you got --> {len(self.players[self.current_player_index].hand)-1}: {self.players[self.current_player_index].hand[-1]}")
            if self.players[self.current_player_index].hand[-1] != self.game_pile[-1].color and self.players[self.current_player_index].hand[-1] != self.game_pile[-1].number and self.players[self.current_player_index].hand[-1].number not in ["wild", "draw four"]:
                self.next_player()
                return
            elif self.players[self.current_player_index].hand[-1] == self.game_pile[-1].color or self.players[self.current_player_index].hand[-1] == self.game_pile[-1].number or self.players[self.current_player_index].hand[-1].number in ["wild", "draw four"]:
                index = int(input("Which card? "))
        card = self.players[self.current_player_index].hand[index]
        while card.color != self.game_pile[-1].color and card.number != self.game_pile[-1].number and card.number not in ["wild", "draw four"]:
            index = int(input("choose a valid index: "))
            card = self.players[self.current_player_index].hand[index]
        self.players[self.current_player_index].play(index, self.game_pile)
        card = self.players[self.current_player_index].hand[index]
        # self.players[self.current_player_index].play(index, self.game_pile)
        if card.number == "skip":
            self.next_player()
            self.next_player()
        elif card.number == "reverse":
            self.direction *= -1
            self.next_player()
        elif card.number == "draw two":
            self.next_player()
            self.players[self.current_player_index].draw(self.deck)
            self.players[self.current_player_index].draw(self.deck)
            self.next_player()
        elif card.number == "draw four":
            self.next_player()
            self.players[self.current_player_index].draw(self.deck)
            self.players[self.current_player_index].draw(self.deck)
            self.players[self.current_player_index].draw(self.deck)
            self.players[self.current_player_index].draw(self.deck)
            self.next_player()
        else:
            self.next_player()
        

    def start(self):
        for player in self.players:
            player.draw(self.deck)
            player.draw(self.deck)
            player.draw(self.deck)
            player.draw(self.deck)
            player.draw(self.deck)
            player.draw(self.deck)
            player.draw(self.deck)
        self.game_pile.append(self.deck.deal())
        while self.game_pile[-1].number in ["skip", "reverse", "draw two", "wild", "draw four"]:
            self.game_pile.append(self.deck.deal())
    
    def winner(self):
        for player in self.players:
            if player.has_won():
                return player
        return False

game = Game(["Alice", "Bob", "Charlie", "Diana"])
game.start()
length = len(game.players)
while not game.winner():
    print(game.players[game.current_player_index].name)
    print(f"Current card: {game.game_pile[-1]}")
    for i, card in enumerate(game.players[game.current_player_index].hand):
        print(f"{i}: {card}")
    game.play_card(int(input("Which card? ")))
    if len(game.deck.cards) == 0:
        game.deck.cards = game.game_pile[:-1]
        game.deck.shuffle()
        game.game_pile = [game.game_pile[-1]]
        print("shuffled")
print(f"{game.winner()} won!")

    


