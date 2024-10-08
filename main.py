import random

suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:

    def __init__(self):

        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_composition = ''
        for card in self.deck:
            deck_composition += '\n' + card.__str__()
        return "The deck has: " + deck_composition

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        #track aces in hand
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # if total value > 21, and I still have an ace
        # then change my ace to be 1 instead of 11
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chips:

    def __init__(self, total = 100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):

    while True:

        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print("You have to provide an integer. ")
        else:
            if chips.bet > chips.total:
                print("Sorry, you don't have enough cips! You have: {}".format(chips.total))
            else:
                break

def hit(deck, hand):

    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to hit or stand? Enter h or s: ")

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player stands. Dealer's turn.")
            playing = False

        else:
            print("Sorry, i did not understand, please enter h or s only!")
            continue
        break

def show_some(player, dealer):

    #show only one of the dealer's cards
    print("\n Dealer's hand: ")
    print("First card hidden!")
    print(dealer.cards[1])

    #show 2 of the player's cards
    print("\n Player's hand:")
    for card in player.cards:
        print(card)

def show_all(player, dealer):

    #show all the dealer's cards
    print("\n Dealer's hand:")
    for card in dealer.cards:
        print(card)

    #calculate and display value (e.g. J+K == 20)
    print(f"Value of dealer's hand is: {dealer.value}")

    #show all the player's cards
    print("\n Player's hand:")
    for card in player.cards:
        print(card)

    print(f"Value of player's hand is: {player.value}")

def player_busts(player, dealer, chips):
    print("BUST PLAYER!")
    chips.lose_bet()
def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()
def dealer_busts(player, dealer, chips):
    print("DEALER BUSTS!")
    chips.win_bet()
def dealer_wins(player, dealer, chips):
    print("DEALER WINS!")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and player tie! PUSH")

# STARTING THE GAME

while True:

    print("Welcome to Blackjack!")
    #create and shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #setup player's chips
    player_chips = Chips()

    #prompt player for bet
    take_bet(player_chips)

    #show cards but keep one dealer card hidden
    show_some(player_hand, dealer_hand)

    while playing: #recall this variable from hit_or_stand function

        #prompt for player to hit or stand
        hit_or_stand(deck, player_hand)

        #show cards (but keep on dealer card hidden)
        show_some(player_hand, dealer_hand)

        #if player's hand exceeds 21, run player_busts(_) and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    #if player hasn't busted, play dealer's hand until dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        #show all cards
        show_all(player_hand, dealer_hand)

        #run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    #inform player of their chips total
    print(f"\n Player total chips are at: {player_chips.total}")

    #ask to play again
    new_game = input("Would you like to play again? Enter y or n: ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break
