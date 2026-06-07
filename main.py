'''A command-line implementation of the classic Blackjack card game.'''

from random import shuffle

RANKS = (
    'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
    'Ten', 'Jack', 'Queen', 'King', 'Ace',
)
VALUES = {
    'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
    'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
    'Queen': 10, 'King': 10, 'Ace': 11,
}


class Card:
    '''Represents a single playing card with a rank and value.'''

    def __init__(self, rank: str):
        '''Initialize a card with a rank and its corresponding value.

        Args:
            rank: The rank of the card (e.g. 'Ace', 'King', 'Two').
        '''
        self.rank = rank
        self.value = VALUES[rank]

    def __str__(self) -> str:
        '''Return a string representation of the card.'''
        return f'Card: {self.rank}, Value: {self.value}'


class Deck:
    '''Represents a standard 52-card deck, with four cards of each rank.'''

    def __init__(self):
        '''Initialize a deck of 52 cards, four of each rank.'''
        self.cards = []
        for rank in RANKS:
            for _ in range(4):
                self.cards.append(Card(rank))


class Player:
    '''Represents a human player with a name, bankroll, and current hand.'''

    def __init__(self, name: str, bankroll: int):
        '''Initialize a player with a name and starting bankroll.
        
        Args:
            name: The player's name.
            bankroll: The player's starting bankroll in dollars.
        '''
        self.name = name
        self.bankroll = bankroll
        self.winnings = 0
        self.bet_amount = 0
        self.current_hand = []

    def __str__(self) -> str:
        '''Return a string representation of the player.'''
        return f'Player: {self.name} \nBankroll: ${self.bankroll:,}'


class Dealer:
    '''Represents the dealer, who manages the deck and plays against the player.'''
    
    def __init__(self, bankroll: int):
        '''Initialize the dealer with a starting bankroll and a fresh deck.

        Args:
            bankroll: The dealer's starting bankroll in dollars.
        '''
        self.name = 'Lauren'
        self.bankroll = bankroll
        self.winnings = 0
        self.current_hand = []
        self.deck = Deck()

    def shuffle_cards(self) -> None:
        '''Shuffle the cards in the deck in place.'''
        shuffle(self.deck.cards)

    def deal_a_card(self) -> Card:
        '''Removes and returns the top card from the deck.'''
        return self.deck.cards.pop(0)

    def __str__(self) -> str:
        '''Return a string representation of the dealer.'''
        return f'Dealer: {self.name} \nBankroll: ${self.bankroll:,}'


def get_bet_amount(player: Player) -> None:
    '''Prompt the player to place a bet and validate the input.

    Keeps prompting until the player enters a valid whole number
    that does not exceed their current bankroll.

    Args:
        player: The player placing the bet.
    '''
    while True:
        try:
            player.bet_amount = int(input(f'{player.name}, place your bet: '))
        except ValueError:
            print('Invalid input. Please enter a whole number.')
            continue
        if player.bet_amount > player.bankroll:
            print('You can\'t bet more than your current bankroll.')
            continue
        break


def get_choice() -> int:
    '''Prompt the player to choose to hit or stand and validate the input.

    Keeps prompting until the player enters either 1 (hit) or 2 (stand).

    Returns:
        1 if the player chooses to hit, 2 if the player chooses to stand.
    '''
    while True:
        try:
            choice = int(input('Choose 1 to hit or 2 to stand: '))
        except ValueError:
            print('Invalid input. Please enter 1 or 2.')
            continue
        if choice not in (1, 2):
            print('Invalid choice. Please enter 1 to hit or 2 to stand.')
            continue
        return choice


def calculate_hand(hand: list[Card]) -> int:
    '''Calculate the total value of a hand, adjusting for Aces.

    Aces are counted as 11 unless doing so would bust the hand,
    in which case they are counted as 1.

    Args:
        hand: A list of Card objects representing the hand.

    Returns:
        The total value of the hand.
    '''
    total = 0
    aces = 0
    for card in hand:
        total += card.value
        if card.rank == 'Ace':
            aces += 1
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


def update_bankroll_and_winnings(winner: Player | Dealer, loser: Player | Dealer, bet_amount: int) -> None:
    '''Update the bankroll and winnings of the winner and loser.

    Args:
        winner: The player or dealer who won the round.
        loser: The player or dealer who lost the round.
        bet_amount: The amount wagered in the round.
    '''
    winner.bankroll += bet_amount
    winner.winnings += bet_amount
    loser.bankroll -= bet_amount
    loser.winnings -= bet_amount


def display_cards(player: Player, dealer: Dealer) -> None:
    '''Display the player's cards and the dealer's first card.

    The dealer's second card is hidden.

    Args:
        player: The player whose cards are displayed.
        dealer: The dealer whose first card is displayed.
    '''
    print(f'{player.name}\'s cards: {player.current_hand[0].rank} and {player.current_hand[1].rank}')
    print(f'{dealer.name}\'s cards: {dealer.current_hand[0].rank} and Face Down')
    print()


def display_bankrolls(player: Player, dealer: Dealer) -> None:
    '''Display the current bankroll of the player and dealer.

    Args:
        player: The player whose bankroll is displayed.
        dealer: The dealer whose bankroll is displayed.
    '''
    print(f'{player.name}\'s bankroll: ${player.bankroll:,}')
    print(f'{dealer.name}\'s bankroll: ${dealer.bankroll:,}')
    print()


def main() -> None:
    '''Entry point for the Blackjack game.'''
    player = Player('Yousef', 10000)
    dealer = Dealer(10000)
    print()

    continue_game = True
    while continue_game:
        dealer.shuffle_cards()

        # Continue playing until the deck doesn't have enough cards to start a new game
        while len(dealer.deck.cards) >= 4:
            get_bet_amount(player)

            # Add two cards to each player's hand at the start of every game
            for _ in range(2):
                player.current_hand.append(dealer.deal_a_card())
                dealer.current_hand.append(dealer.deal_a_card())

            # Display the player's and dealer's cards
            display_cards(player, dealer)

            # Evaluate player and dealer hands
            player_hand_value = calculate_hand(player.current_hand)
            dealer_hand_value = calculate_hand(dealer.current_hand)

            if player_hand_value == 21 or dealer_hand_value == 21:  # Check for blackjack
                if player_hand_value == 21 and dealer_hand_value != 21:  # Player win with blackjack
                    print(f'{player.name} won with a blackjack!')
                    update_bankroll_and_winnings(player, dealer, player.bet_amount)
                elif player_hand_value == 21 and dealer_hand_value == 21:  # Tie with blackjack
                    print('Tie with blackjack!')
                elif dealer_hand_value == 21 and player_hand_value != 21:  # Dealer win with blackjack
                    print(f'{dealer.name} won with a blackjack!')
                    update_bankroll_and_winnings(dealer, player, player.bet_amount)

                display_bankrolls(player, dealer)
                player.current_hand.clear()
                dealer.current_hand.clear()
                continue

            choice = get_choice()

            # If the player chooses to hit, add a card to his current hand
            if choice == 1:
                outcome = ''
                while choice == 1:  # While the player chooses to hit
                    dealt_card = dealer.deal_a_card()
                    player.current_hand.append(dealt_card)
                    player_hand_value = calculate_hand(player.current_hand)
                    if dealt_card.rank[0] in ('A', 'E'):
                        print(f'{player.name} drew an {dealt_card.rank}.')
                    else:
                        print(f'{player.name} drew a {dealt_card.rank}.')

                    if player_hand_value == 21:  # Player win
                        print(f'{player.name} won with {player_hand_value}! {dealer.name} had {dealer_hand_value}.')
                        update_bankroll_and_winnings(player, dealer, player.bet_amount)
                        outcome = 'win'
                    elif player_hand_value > 21: # Player bust
                        print(f'{player.name} bust with {player_hand_value}! {dealer.name} won!')
                        update_bankroll_and_winnings(dealer, player, player.bet_amount)
                        outcome = 'bust'
                    else:
                        choice = get_choice()

                    if outcome:
                        display_bankrolls(player, dealer)
                        player.current_hand.clear()
                        dealer.current_hand.clear()
                        break

            # If the player chooses to stand, the dealer will hit until his hand value is at least 17, 
            # then evaluate the winner
            elif choice == 2:
                while dealer_hand_value < 17:
                    dealt_card = dealer.deal_a_card()
                    dealer.current_hand.append(dealt_card)
                    dealer_hand_value = calculate_hand(dealer.current_hand)
                    if dealt_card.rank[0] in ('A', 'E'):
                        print(f'{dealer.name} drew an {dealt_card.rank}.')
                    else:
                        print(f'{dealer.name} drew a {dealt_card.rank}.')

                if dealer_hand_value > 21:  # Dealer bust
                    print(f'{dealer.name} bust with {dealer_hand_value}! {player.name} won!')
                    update_bankroll_and_winnings(player, dealer, player.bet_amount)
                elif dealer_hand_value > player_hand_value:  # Dealer win
                    print(f'{dealer.name} won with {dealer_hand_value}! {player.name} had {player_hand_value}.')
                    update_bankroll_and_winnings(dealer, player, player.bet_amount)
                elif player_hand_value > dealer_hand_value:  # Player win
                    print(f'{player.name} won with {player_hand_value}! {dealer.name} had {dealer_hand_value}.')
                    update_bankroll_and_winnings(player, dealer, player.bet_amount)
                else:  # Tie
                    print(f'Tie! {player.name} and {dealer.name} both had {player_hand_value}.')

                display_bankrolls(player, dealer)
                player.current_hand.clear()
                dealer.current_hand.clear()

            # End the game if either the dealer or player runs out of money
            if player.bankroll < 1:
                print(f'{player.name} has run out of money! {dealer.name} wins! GAME OVER!')
                continue_game = False
                break
            elif dealer.bankroll < 1:
                print(f'{dealer.name} has run out of money! {player.name} wins! GAME OVER!')
                continue_game = False
                break

            # If the deck has between one and four cards, determine the winner and end the game
            if len(dealer.deck.cards) < 4:
                print('There are not enough cards in the deck to continue playing!')
                if dealer.winnings > player.winnings:
                    print(f'{dealer.name}\'s winnings: ${dealer.winnings:,} \n{dealer.name} wins!')
                else:
                    print(f'{player.name}\'s winnings: ${player.winnings:,} \n{player.name} wins!')
                continue_game = False


if __name__ == '__main__':
    main()
