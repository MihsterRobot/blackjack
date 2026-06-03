"""Blackjack card game."""
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
    def __init__(self, rank):
        self.rank = rank
        self.value = VALUES[rank]

    def __str__(self):
        return f'Card: {self.rank}, Value: {self.value}'


class Deck:
    def __init__(self):
        self.cards = []
        for rank in RANKS:
            for _ in range(4):
                created_card = Card(rank)
                self.cards.append(created_card)


class Player:
    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = bankroll
        self.winnings = 0
        self.bet_amount = 0
        self.current_hand = []

    def __str__(self):
        return f'Player: {self.name} \nBankroll: ${self.bankroll:,}'


class Dealer:
    def __init__(self, bankroll):
        self.name = 'Dealer'
        self.bankroll = bankroll
        self.winnings = 0
        self.current_hand = []
        self.deck = Deck()

    def shuffle_cards(self):
        shuffle(self.deck.cards)

    def deal_a_card(self):
        """Deal a card off the top of the deck."""
        return self.deck.cards.pop(0)

    def __str__(self):
        return f'Player: {self.name} \nBankroll: ${self.bankroll:,}'


def update_bankroll_and_winnings(winner: Player | Dealer, loser: Player | Dealer, bet_amount: int) -> None:
    winner.bankroll += bet_amount
    winner.winnings += bet_amount
    loser.bankroll -= bet_amount
    loser.winnings -= bet_amount


def calculate_hand(hand: list[Card]) -> int:
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


# FIXME: Consider whether the parameter name `dealer` shadows the outer `dealer` variable. 
# It won't cause a bug here since it's a function parameter, 
# but it's worth being deliberate about it.
def display_cards(player: Player, dealer: Dealer) -> None:
    print(f"{player.name}'s cards: {player.current_hand[0].rank} and {player.current_hand[1].rank}")
    print(f"{dealer.name}'s cards: {dealer.current_hand[0].rank} and Face Down")
    print()


def main() -> None:
    player = Player('Yousef', 10000)
    dealer = Dealer(10000)
    print()

    continue_game = True
    while continue_game:
        dealer.shuffle_cards()

        # Continue playing until the deck doesn't have enough cards to start a new game
        while len(dealer.deck.cards) > 3:
            # Ask the player to place a bet
            player.bet_amount = int(input(f'{player.name}, place your bet: '))

            # Input validation for bet
            while player.bet_amount > player.bankroll:
                print("You don't have enough money to place this bet.")
                player.bet_amount = int(input(f'{player.name}, place your bet: '))

            # Add two cards to each player's hand at the start of every game
            for _ in range(2):
                player.current_hand.append(dealer.deal_a_card())
                dealer.current_hand.append(dealer.deal_a_card())

            # Display the player's and dealer's cards
            display_cards(player, dealer)

            # Evaluate player and dealer hands
            player_hand_value = calculate_hand(player.current_hand)
            dealer_hand_value = calculate_hand(dealer.current_hand)

            # Ask the player to hit or stand
            choice = int(input('Choose 1 to hit or 2 to stand: '))

            # If the player chooses to hit, add a card to his current hand
            if choice == 1:
                # While the player chooses to hit
                while choice == 1:
                    dealt_card = dealer.deal_a_card()
                    player.current_hand.append(dealt_card)
                    player_hand_value = calculate_hand(player.current_hand)
                    if dealt_card.rank[0] in ('A', 'E'):
                        print(f'{player.name} drew an {dealt_card.rank}.')
                    else:
                        print(f'{player.name} drew a {dealt_card.rank}.')

                    outcome = ''
                    if player_hand_value == 21:  # Player win
                        print(f'{player.name} won with {player_hand_value}! {dealer.name} had {dealer_hand_value}.')
                        update_bankroll_and_winnings(player, dealer, player.bet_amount)
                        outcome = 'win'
                    elif player_hand_value > 21: # Player bust
                        print(f'{player.name} bust with {player_hand_value}! {dealer.name} won!')
                        update_bankroll_and_winnings(dealer, player, player.bet_amount)
                        outcome = 'bust'
                    else:
                        choice = int(input('Choose 1 to hit or 2 to stand: '))

                    if outcome:
                        print(f"{player.name}'s bankroll: ${player.bankroll:,}")
                        print(f"{dealer.name}'s bankroll: ${dealer.bankroll:,}")
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

                print(f"{player.name}'s bankroll: ${player.bankroll:,}")
                print(f"{dealer.name}'s bankroll: ${dealer.bankroll:,}")
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

            # If there are only four cards left in the deck, deal both players two cards,
            # evaluate the last play, determine a winner based on winnings, and end the game
            if len(dealer.deck.cards) == 4:
                print('There are four cards left in the deck!')

                # Ask the player to place a bet
                player.bet_amount = int(input(f'{player.name}, place your bet: '))
                # Input validation for bet
                while player.bet_amount > player.bankroll:
                    print("You don't have enough money to place this bet.")
                    player.bet_amount = int(input(f'{player.name}, place your bet: '))

                # Deal two cards each to the player and dealer
                for _ in range(2):
                    player.current_hand.append(dealer.deal_a_card())
                    dealer.current_hand.append(dealer.deal_a_card())

                # Display the player's and dealer's cards
                display_cards(player, dealer)
                
                # Evaluate player and dealer hands
                player_hand_value = calculate_hand(player.current_hand)
                dealer_hand_value = calculate_hand(dealer.current_hand)

                if player_hand_value == dealer_hand_value:
                    print('Tie!')
                # Player win
                elif player_hand_value > dealer_hand_value:
                    print(f'{player.name} won with {player_hand_value}! {dealer.name} had {dealer_hand_value}.')
                    update_bankroll_and_winnings(player, dealer, player.bet_amount)
                # Dealer win
                else:
                    print(f'{dealer.name} won with {dealer_hand_value}! {player.name} had {player_hand_value}.')
                    update_bankroll_and_winnings(dealer, player, player.bet_amount)

                if dealer.winnings > player.winnings:
                    print(f"{dealer.name}'s winnings: ${dealer.winnings:,} \n{dealer.name} wins!")
                else:
                    print(f"{player.name}'s winnings: ${player.winnings:,} \n{player.name} wins!")

                print('The deck is empty! GAME OVER!')
                continue_game = False

            # If the deck has between one and four cards, determine the winner and end the game
            if len(dealer.deck.cards) in range(1, 4):
                print('There are not enough cards in the deck to continue playing!')

                if dealer.winnings > player.winnings:
                    print(f"{dealer.name}'s winnings: ${dealer.winnings:,} \n{dealer.name} wins!")
                else:
                    print(f"{player.name}'s winnings: ${player.winnings:,} \n{player.name} wins!")

                continue_game = False


if __name__ == '__main__':
    main()
