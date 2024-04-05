import itertools
import random

SUITS = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
RANKS = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def compare(self, other, use_suit=True):
        if use_suit:
            return (RANKS.index(self.rank), SUITS.index(self.suit)) > (RANKS.index(other.rank), SUITS.index(other.suit))
        else:
            return RANKS.index(self.rank) > RANKS.index(other.rank)

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit, rank in itertools.product(SUITS, RANKS)]
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, num_hands):
        hands = [[] for _ in range(num_hands)]
        for i, card in enumerate(self.cards):
            hands[i % num_hands].append(card)
        return hands

class Big2Game:
    def __init__(self):
        self.deck = Deck()
        self.players = [[] for _ in range(4)]
        self.current_starter = random.randint(0, 3)
        self.current_winner = None
        self.pass_count = 0
        self.current_combo = []
        self.current_combo_type = None
    
    def start(self):
        self.deck.shuffle()
        self.players = self.deck.deal(4)
        print("Game started. Dealing cards to players...")
        for i, hand in enumerate(self.players, start=1):
            hand.sort(key=lambda card: (RANKS.index(card.rank), SUITS.index(card.suit)))
            print(f"Player {i} hand: {' '.join(map(str, hand))}")
        self.game_loop()

    def game_loop(self):
        while not self.check_winner():
            print(f"\nPlayer {self.current_starter + 1}'s turn:")
            self.player_turn(self.current_starter)
            self.current_starter = (self.current_starter + 1) % 4
            if self.pass_count == 3:
                self.current_winner = (self.current_starter - 1) % 4
                self.pass_count = 0
                self.current_combo = []
                self.current_combo_type = None
        print(f"\nPlayer {self.check_winner()} wins the game!")

    def check_winner(self):
        for i, hand in enumerate(self.players):
            if not hand:
                return i + 1
        return None

    def player_turn(self, player_index):
        # Display the current combo on the table (if any)
        if self.current_combo:
            print(f"Current combo on the table: {', '.join(map(str, self.current_combo))}")
        else:
            print("No combo on the table. You're leading this round.")
        
        # Show the player's cards
        print(f"Your cards: {' '.join(map(str, self.players[player_index]))}")
        
        input_str = input("Enter your play (e.g., '5 of Diamonds') or 'pass': ").strip()
        if input_str == 'pass':
            self.pass_count += 1
            print(f"Player {player_index + 1} passed.")
            return
        try:
            card_str = input_str.split(', ')
            played_cards = [Card(suit, rank) for rank, suit in [carded.split(' of ') for carded in card_str]]
            valid_play, combo_type = self.is_valid_play(played_cards, player_index)
            if valid_play:
                for card in played_cards:
                    self.players[player_index].remove(card)  # Directly use the Card object here
                    print(f"Removed {card}")
                # Update the table combo after a successful play
                self.current_combo = played_cards
                self.current_combo_type = combo_type
                self.current_winner = player_index
                self.pass_count = 0
            else:
                print("Invalid play. Try again.")
                self.player_turn(player_index)
        except Exception as e:
            print("Error parsing cards. Please try again.")
            self.player_turn(player_index)



    def is_valid_play(self, cards, player_index):
        # First, sort the cards by rank and suit for easier comparison and validation
        cards.sort(key=lambda card: (RANKS.index(card.rank), SUITS.index(card.suit)))
        print('yuh')
        played_combo_type = self.combo_type(cards)
        print('yah')
        
        # Check if the cards form a valid combo
        if played_combo_type is None:
            print('played_combo_type is None')
            return False, None
        
        # If the player is the round's starter, any valid combo is allowed
        if self.current_winner is None or self.current_winner == player_index:
            print('current_winner')
            self.current_combo = cards
            self.current_combo_type = played_combo_type
            return True, played_combo_type
        
        # If not the starter, match the combo type and beat the current combo
        if played_combo_type != self.current_combo_type:
            print('not the starter')
            return False, None
        
        # Compare the highest card of the current play with the last play's highest card
        print('compare')
        highest_played_card = cards[-1]  # Cards are sorted, so the last card is the highest
        highest_current_combo_card = self.current_combo[-1]
        
        if not highest_played_card.compare(highest_current_combo_card):
            print('not highest_played_card')
            return False, None
        
        print('Update current combo')
        self.current_combo = cards  # Update current combo
        return True, played_combo_type

    def combo_type(self, cards):
        print('yeh')
        if len(cards) == 1:
            print('single')
            return 'single'
        elif len(cards) == 2 and cards[0].rank == cards[1].rank:
            print('pair')
            return 'pair'
        elif len(cards) == 3 and all(card.rank == cards[0].rank for card in cards):
            print('triple')
            return 'triple'
        elif len(cards) == 4 and all(card.rank == cards[0].rank for card in cards):
            print('quadruple')
            return 'quadruple'
        elif len(cards) >= 3 and self.is_consecutive_ranks(cards):
            print('straight')
            return 'straight'
        return None
    
    def is_consecutive_ranks(cards):
        print('is_consecutive_ranks')
        ranks = [RANKS.index(card.rank) for card in cards]
        print('RANKS.index(card.rank)')
        ranks.sort()
        return all(ranks[i] + 1 == ranks[i + 1] for i in range(len(ranks) - 1))

def main():
    game = Big2Game()
    game.start()

if __name__ == "__main__":
    main()
