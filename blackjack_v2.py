"""
Blackjack Game
"""
import random

values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')


class Player:
    def __init__(self, bankroll):
        self.bankroll = bankroll
        self.hand = []
        self.total_value = 0
        self.aces = 0

    def hit(self, new_cards):
        self.hand.append(new_cards)
        self.total_value += new_cards.value

        if new_cards.rank == 'Ace':
            self.aces += 1

    def adjust_ace(self):
        while self.total_value > 21 and self.aces > 0:
            self.total_value -= 10
            self.aces -= 1
        return self.total_value

    def bet(self):
        """ Lets User place their bet, checks if it is possible"""
        while True:
            try:
                bet_value = int(input("Please place your bet"))
            except ValueError:
                print("Please try again")
            else:
                if bet_value > self.bankroll:
                    print("Sorry, you don't have enough money!")
                else:
                    self.bankroll = self.bankroll - bet_value
                    print(f"The bank roll has decreased by {bet_value} to {self.bankroll}")
                    global winnings
                    winnings = bet_value
                    return winnings

    def update_bankroll(self, bet_value):
        self.bankroll += (bet_value * 2)
        return self.bankroll

    def __str__(self):
        return f" The player has {self.bankroll} dollars with {self.hand} in hand"


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.all_cards = []
        # creating card objects from the suit and rank tuples
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        # this doesn't return anything
        random.shuffle(self.all_cards)

    def deal_one(self):
        # we remove one card from the list of all_cards
        return self.all_cards.pop()


""" All functions are below"""


def ask_hit():
    while True:
        try:
            result = input("Would you like to hit? Y or N").upper()
            if result == "Y":
                return True
            elif result == "N":
                return False
            else:
                print("Sorry I don't understand")
        except:
            print("error")


def check_win(Player, Dealer):
    if 21 >= Player.total_value > Dealer.total_value:
        return True
    else:
        return False


def check_bust(Player):
    return Player.total_value > 21


def show_some(player, dealer):
    print(f"You have {player.hand[0]} and a {player.hand[1]}")
    print(f"One of the Dealer's cards is {dealer.hand[0]}")


def current_cards(player):
    for card in player.hand:
        print(card)


def show_all(player, dealer):
    # print(f"You have {player.hand[0]} and a {player.hand[1]}")
    print(f"The Dealer had {dealer.hand[0]} and a {dealer.hand[1]}")


def replay():
    choice = "wrong"
    while choice not in ["Y", "N"]:
        choice = input("Keep playing? Y or N ").upper()

        if choice not in ["Y", "N"]:
            print("I don't understand, please choose Y or N")

    return choice == "Y"


""" Game Logic """

player = Player(100)
dealer = Player("N/A")
game_on = True
print("Welcome to Blackjack")
while game_on:
    if player.bankroll == 0:
        print("You have no more money!")
        break
    player.bet()
    print("\n" * 2)
    new_deck = Deck()
    new_deck.shuffle()
    player.hand = []
    dealer.hand = []
    for x in range(2):
        player.hit(new_deck.deal_one())
        dealer.hit(new_deck.deal_one())
    show_some(player, dealer)
    player.adjust_ace()
    print("\n")
    print(f" Your total value is {player.total_value}")
    while ask_hit():
        player.hit(new_deck.deal_one())
        print("\n" * 2)
        print(f"you drew a {player.hand[-1]}")
        player.adjust_ace()
        print(f" Your total is now {player.total_value}")
        if check_bust(player):
            print("You have gone bust!")
            if replay():
                break
            else:
                game_on = False
                break
    else:
        print("---------------------------------------------------------")
        print("\n")
        print("You chose to stand!")
        show_all(player, dealer)
        print(f" the dealer had a total of {dealer.total_value}")
        print("\n" * 2)
        print("The dealer will now play")
        if check_win(dealer, player):
            print("\n" * 2)
            print(f"The dealer has a total of {dealer.total_value} and has won!")
        while dealer.total_value < player.total_value:
            dealer.hit(new_deck.deal_one())
            print("\n" * 2)
            print(f"The dealer drew a {dealer.hand[-1]}")
            dealer.adjust_ace()
            print(f"The dealer's total is {dealer.total_value}")
            if check_bust(dealer):
                print("\n" * 2)
                print("The dealer is bust! You have won")
                player.update_bankroll(winnings)
                break
            if player.total_value == dealer.total_value:
                print("\n" * 2)
                print("its a tie!")
                break
        if check_win(dealer, player):
            print("\n" * 2)
            print("The dealer has won! You lose!")
        if replay():
            continue
        else:
            game_on = False
            break




# Shuffle cards - done
# let player place bet - done
# deal two cards to each person - done
# tell the player what cards he has - done
# tell the player one card of the dealer - done
# ask them if they want to hit or stay - done
# tell them if they bust - done
# if they dont bust, ask if they want to hit again
# 
# let the dealer play if the player stands
# someone wins or loses - done
# pay them out - done
# ask if they want to play again - done
