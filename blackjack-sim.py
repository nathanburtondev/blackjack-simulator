import random

# Global Constant
MIN_BALANCE = 1
MAX_BALANCE = 1000
MIN_DECKS = 1
MAX_DECKS = 6

# Card Definitions
VALUES = list(range(2, 15))
SUITS = ["Clubs", "Diamonds", "Spades", "Hearts"]

FACE_CARDS = {
    11: 'J',
    12: 'Q',
    13: 'K',
    14: 'A',
}

SUIT_SYMBOLS = {
    'Hearts': '♥',
    'Diamonds': '♦',
    'Clubs': '♣',
    'Spades': '♠'
}

class Card:
    """Represents a single playing card."""
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        
    def __repr__(self):
        display_value = FACE_CARDS.get(self.value, self.value)
        if display_value == 10:
            display_value = '10' 
        display_suit = SUIT_SYMBOLS.get(self.suit, self.suit)
        return f"{display_value}{display_suit}"
        
    def get_ascii_art_lines(self):
        """Returns a list of strings for ASCII art representation of the card."""
        display_value = FACE_CARDS.get(self.value, self.value)
        if display_value == 10:
            display_value = '10' 
        display_suit = SUIT_SYMBOLS.get(self.suit, self.suit)

        card_art = [
            "┌─────────┐",
            f"│ {str(display_value):<2}      │", 
            "│         │",
            f"│    {display_suit}    │",
            "│         │",
            f"│      {str(display_value):>2} │",
            "└─────────┘"
        ]
        return card_art

    

class BlackjackGame:
    """Manages the state and logic for a Blackjack game."""
    def __init__(self):
        self.balance = 0
        self.deck_count = 0
        self.live_deck = []
        self.player_hands = [[]]
        self.dealer_hand = []
        self.current_bet = 0
        self.initial_deck_size = 0 # To track for reshuffling
        self.player_hand_bets = [self.current_bet]

    def generate_cards(self):
        """Generates a single, unshuffled deck of Card objects."""
        cards = []
        for value in VALUES:
            for suit in SUITS:
                # The Card class itself will handle the value/suit mapping during __repr__
                cards.append(Card(value, suit)) 
        return cards

    def reset_round_state(self):
        """Resets hands and bets for the start of a new round."""
        self.player_hands = [[]] # Player starts with one empty hand
        self.dealer_hand = []     # Dealer's hand is empty
        self.player_hand_bets = [] # Clear all bets
        # self.current_bet = 0 # Reset current_bet if it's used to store the initial bet size
        # (Or it will be set again when the next bet is placed)
        # self.check_and_reshuffle_deck() 

    def deal_card(self):
        """Removes and returns the top card from the live deck."""
        if not self.live_deck:
            print("One moment! Reshuffling!")
            self.reshuffle_deck() # Call reshuffle method if deck is empty
            print("Deck reshuffled!")


        if self.live_deck: # Check again after potential reshuffle
            return self.live_deck.pop(0)
        else:
            print("Error: Deck is still empty after reshuffle attempt.")
            return None
            
    def print_hand_ascii_art(self, hand, name="Hand", hide_first_card=False):
        """
        Prints a list of Card objects horizontally as ASCII art.
        This method belongs in the BlackjackGame class.
        """
        if not hand:
            print(f"\n{name}: Empty")
            return

        all_card_lines = []
        for i, card in enumerate(hand): # 'card' here is an actual Card object
            if hide_first_card and i == 0:
                # Create a generic "hidden card" ASCII art
                hidden_card_art = [
                    "┌─────────┐",
                    "│░░░░░░░░░│",
                    "│░░░░░░░░░│",
                    "│░░░░░░░░░│",
                    "│░░░░░░░░░│",
                    "│░░░░░░░░░│",
                    "└─────────┘"
                ]
                all_card_lines.append(hidden_card_art)
            else:
                # Call the get_ascii_art_lines method ON THE Card object
                all_card_lines.append(card.get_ascii_art_lines())

        # Now, print collected lines horizontally
        # Assuming all card arts have the same number of lines (7)
        if not all_card_lines: # Safety check if somehow it's empty after loop
            return 

        num_lines_per_card = len(all_card_lines[0]) # Get number of lines from the first card's art

        print(f"\n{name}:")
        for line_idx in range(num_lines_per_card):
            line_output_parts = []
            for card_lines in all_card_lines: # card_lines is the list of 7 lines for one card
                line_output_parts.append(card_lines[line_idx])
            print(" ".join(line_output_parts)) # Join lines with a space for separation


    def reshuffle_deck(self):
        """Regenerates and shuffles the live deck based on deck_count."""
        generated_base_deck = self.generate_cards()
        self.live_deck = []
        for _ in range(self.deck_count):
            for card in generated_base_deck:
                self.live_deck.append(Card(card.value, card.suit))
        random.shuffle(self.live_deck)
        self.initial_deck_size = len(self.live_deck) # Update initial deck size

    def print_hand_basic(self, hand, name="Hand"):
        """Prints a list of Card objects without brackets, using their __repr__ method."""
        if not hand:
            print(f"{name}: Empty")
            return
        print(f"{name}: {', '.join(str(card) for card in hand)}")

    def get_starting_balance(self):
        """Prompts user for starting balance and sets it."""
        while True:
            print(f"\n Enter a Number between {MIN_BALANCE}-{MAX_BALANCE}")
            deposit_str = input("\n Set your starting balance: ")
            try:
                deposit = int(deposit_str)
                if MIN_BALANCE <= deposit <= MAX_BALANCE: 
                    self.balance = deposit
                    break
                else:
                    print(f"The Number entered was not between {MIN_BALANCE}-{MAX_BALANCE}. Please Try Again.")
            except ValueError:
                print("Invalid input. Please enter a valid integer for the starting balance.")

    def set_deck_count(self):
        """Prompts user for deck count, generates and shuffles the deck."""
        while True:
            print(f"\nEnter a deck count between {MIN_DECKS}-{MAX_DECKS}")
            deck_count_str = input("\n Set the amount of decks used: ")
            try:
                deck_count = int(deck_count_str)
                if MIN_DECKS <= deck_count <= MAX_DECKS:
                    self.deck_count = deck_count
                    self.reshuffle_deck() # Generate and shuffle the deck
                    print(f"\n Deck count set to {self.deck_count} decks. Live deck contains {len(self.live_deck)} cards.")
                    break
                else:
                    print (f"\n The number entered was not {MIN_DECKS}-{MAX_DECKS} please try again")
            except ValueError:
                print("\n Invalid input. Please enter a valid integer for the deck count.")

    def calculate_hand_value(self, hand, return_soft_total_str=False):
        """
        Calculates the total value of a hand, handling Aces.
        Aces are initially counted as 11. If the total exceeds 21,
        and there's an Ace, its value is reduced to 1 until the total
        is 21 or less.

        Args:
            hand (list): A list of Card objects.
            return_soft_total_str (bool): If True, returns a string like "7/18"
                                         for soft totals. Otherwise returns
                                         a single integer value.
        """

        value = 0
        num_aces = 0
        for card in hand:
            if card.value == 11 or card.value == 12 or card.value == 13:
                value += 10
            elif card.value == 14:
                value += 11
                num_aces += 1
            else:
                value += card.value
        
        
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
            
        return value

    def calculate_card_value(self, card, return_soft_total_str=False):
        value = 0 
        num_aces = 0 
        if card.value == 11 or card.value == 12 or card.value == 13:
            value += 10
        elif card.value == 14:
            value += 11
            num_aces += 1 
        else:
            value += card.value
        while value > 21 and num_aces > 0:
            value -= 10 
            num_aces -= 1
            
        return value

    def check_blackjack(self, hand):
        if len(hand) == 2:
            
            if self.calculate_hand_value(hand) == 21:
                return True
        return False

    def determine_winner(self):
        dealer_score = self.calculate_hand_value(self.dealer_hand)

        print(f"\n--- Dealer's Hand ---")
        self.print_hand_ascii_art(self.dealer_hand, "Dealer's Hand", hide_first_card=False)
        print(f"Dealer's Total: {dealer_score}")

        for i, player_hand in enumerate(self.player_hands): # Iterate through each player's hand
            print(f"\n--- Results for Player's Hand {i + 1} ---")
            self.print_hand_ascii_art(player_hand, f"Player's Hand {i + 1}", hide_first_card=False)
            player_score = self.calculate_hand_value(player_hand)
            player_has_blackjack = self.check_blackjack(player_hand)
            dealer_has_blackjack = self.check_blackjack(self.dealer_hand)
            current_hand_bet = self.player_hand_bets[i] # Access the bet for this specific hand

            # 1. Check for Blackjacks first for *this* player hand
            if player_has_blackjack and dealer_has_blackjack:
                print("Both have Blackjack! It's a Push.")
                # Bet is returned to player (no net change)
                self.balance += current_hand_bet
            elif player_has_blackjack:
                print("Blackjack! You win!")
                # Typical 3:2 payout. Adjust balance based on the bet for this specific hand.
                self.balance += current_hand_bet * 2.5 # Original bet + 1.5x winnings
            elif dealer_has_blackjack:
                print("Dealer has Blackjack! You lose.")
                # Bet for this hand is lost. Assuming it's already deducted from balance.
            
            # 2. Check for Busts (if no Blackjacks)
            elif player_score > 21:
                print("Player busts! You lose.")
                # Bet for this hand is lost. Assuming it's already deducted from balance.
            elif dealer_score > 21:
                print("Dealer busts! You win!")
                # Player gets original bet back plus winnings.
                self.balance += current_hand_bet * 2 

            # 3. Compare scores if no Blackjacks or Busts
            elif player_score > dealer_score:
                print("You win!")
                # Player gets original bet back plus winnings.
                self.balance += current_hand_bet * 2
            elif dealer_score > player_score:
                print("Dealer wins!")
                # Bet for this hand is lost. Assuming it's already deducted from balance.
            else: # Scores are equal
                self.balance += current_hand_bet
                print("It's a Push!")
                # Bet is returned to player (no net change)
        

    def play_players_turn(self):
        # Ensure the player starts with at least one hand.
        if not self.player_hands:
            self.player_hands.append([])  # Start with an empty hand if none exist

        # Iterate through each hand the player currently has.
        # We use a while loop with an index to handle potential splitting, which modifies the list length.
        hand_index = 0
        while hand_index < len(self.player_hands):
            current_hand = self.player_hands[hand_index]
            print(f"\n--- Player's Hand {hand_index + 1} ---")
            self.print_hand_ascii_art(current_hand, f"Player's Hand {hand_index + 1}", hide_first_card=False)
            print(f"Player's Total: {self.calculate_hand_value(current_hand)}")

            while True:
                hand_value = self.calculate_hand_value(current_hand)
                # Determine available actions based on hand and game rules.
                options = ["Hit: 1 or H", "Stand: 2 or S"]
                
                # Allow Doubling only on the initial hand (2 cards).
                # Check that the hand is a player's first hand, meaning its length is 2.
                # The index check ensures this applies only to the first hand in the player's hands list initially.
                if len(current_hand) == 2:
                    options.append("Double: 3 or D")
                
                # Allow Splitting only if the hand is an initial two-card hand
                # with two cards of the same value.
                if (len(current_hand) == 2 and 
                    self.calculate_card_value(current_hand[0]) == self.calculate_card_value(current_hand[1])): 
                    options.append("Split: 4 or Sp")
                if len(current_hand) >= 2 and self.calculate_card_value(self.dealer_hand[0]) is not None:
                    dealer_upcard = self.dealer_hand[1]
                    # Make sure you have a valid dealer upcard before simulating
                    if dealer_upcard:
                        odds = self.simulate_odds(current_hand, dealer_upcard, self.live_deck)
                        print("\n--- Strategic Odds (based on 1000 simulations) ---")
                        for decision, percentages in odds.items():
                            print(f"Decision: {decision.capitalize()} -> Win: {percentages['win_percentage']:.2f}% | Lose: {percentages['lose_percentage']:.2f}% | Push: {percentages['push_percentage']:.2f}%")
                        print("-----------------------------------------------------")
                hit_stand_input = input(f"\n{'\n'.join(options)}\n\nHand {hand_index + 1}'s Turn\n\nHit or Stand: ").lower()

                if hit_stand_input in ["s", "2"]:
                    break  # End turn for this hand
                elif hit_stand_input in ["h", "1"]:
                    current_hand.append(self.deal_card())
                    self.print_hand_ascii_art(current_hand, f"Player's Hand {hand_index + 1}", hide_first_card=False)
                    print(f"Player's Total: {self.calculate_hand_value(current_hand)}")
                    if self.calculate_hand_value(current_hand) > 21:
                        print("Bust!")
                        break  # End turn for this hand if busted
                elif hit_stand_input in ["d", "3"] and len(current_hand) == 2: # Double down allowed only on initial two cards
                    # Ensure enough balance before allowing double down
                    if self.balance >= self.player_hand_bets[hand_index]:
                        self.balance -= self.player_hand_bets[hand_index]  # Deduct the additional bet
                        self.player_hand_bets[hand_index] *= 2  # Double the bet for this hand
                        current_hand.append(self.deal_card())
                        self.print_hand_ascii_art(current_hand, f"Player's Hand {hand_index + 1}", hide_first_card=False)
                        print(f"Player's Total: {self.calculate_hand_value(current_hand)}")
                        if self.calculate_hand_value(current_hand) > 21:
                            print("Bust!")
                        break  # Double down ends the turn for this hand
                    else:
                        print("Not enough balance to double down.")
                elif hit_stand_input in ["sp", "4"] and len(current_hand) == 2 and self.calculate_card_value(current_hand[0]) == self.calculate_card_value(current_hand[1]):
                    # Create two new hands from the split.
                    new_hand1 = [current_hand.pop(0), self.deal_card()]  # Deal a new card for the first hand
                    new_hand2 = [current_hand.pop(0), self.deal_card()]  # Deal a new card for the second hand

                    # Add the new hands to the player's hands.
                    self.player_hands.insert(hand_index + 1, new_hand2)  # Insert at next position
                    self.player_hands[hand_index] = new_hand1
                    self.player_hand_bets.insert(hand_index + 1, self.current_bet) # Add bet for the new hand
                    current_hand = self.player_hands[hand_index]
                    # Place the additional bet for the second hand.
                    # Ensure enough balance before allowing split
                    if self.balance >= self.current_bet:
                        self.balance -= self.current_bet  
                        # Bet is doubled to cover both hands implicitly if current_bet is per-hand

                        print(f"\nPlayer split their hand. Two new hands created!")
                        self.print_hand_ascii_art(new_hand1, f"Player's Hand {hand_index + 1}", hide_first_card=False)
                        print(f"Player's Total: {self.calculate_hand_value(new_hand1)}")
                        self.print_hand_ascii_art(new_hand2, f"Player's Hand {hand_index + 2}", hide_first_card=False)
                        print(f"Player's Total: {self.calculate_hand_value(new_hand2)}")
                        
                    else:
                        print("Not enough balance to split.")
                        # Revert changes if split not allowed due to balance
                        current_hand.append(new_hand1[0])
                        current_hand.append(new_hand2[0])
                        self.player_hands.pop(hand_index + 1)
                        self.player_hands[hand_index] = current_hand
                else:
                    print("Input the correct option to proceed")
            hand_index += 1 # Move to the next hand

        # After all hands are played, proceed to the dealer's turn.
        self.play_dealers_turn()
        self.reset_round_state()


    def play_dealers_turn(self):
        while True:
            dealer_total = self.calculate_hand_value(self.dealer_hand)
            # Check if all player hands have busted
            active_player_hands = [hand for hand in self.player_hands if self.calculate_hand_value(hand) <= 21]
        
            # If no active player hands, skip dealer's turn and go straight to determining winner
            if not active_player_hands:
                print("\nAll player hands have busted. Skipping dealer's turn.")
                self.determine_winner()
                return
            elif dealer_total < 17:
                self.dealer_hand.append(self.deal_card())
                self.print_hand_ascii_art(self.dealer_hand, "Dealer's Cards", hide_first_card=False)
                dealer_new_total = self.calculate_hand_value(self.dealer_hand)
                if dealer_new_total > 21:
                    self.determine_winner()
                    return
            elif dealer_total >= 17:
                self.print_hand_ascii_art(self.dealer_hand, "Dealer's Cards", hide_first_card=False)
                self.determine_winner()
                return
                
    def play_again(self):    
        print(f"Your Balance: {self.balance} | Your Current Bet: {self.current_bet} | Current Deck size: {self.deck_count}\n")
        
        while True: # Loop until valid 'y' or 'n' input is received
            play_again_input = input("Play again : Y (yes) or N (no)\nAnother Hand: ").lower()
            if play_again_input == "y":
                # Only proceed to bet setting if 'y' is entered
                while True: # Loop until a valid bet is received
                    current_bet_str = input('Set your bet amount: ')
                    try:
                        requested_bet = int(current_bet_str)
                        if requested_bet <= self.balance and requested_bet > 0:
                            self.current_bet = requested_bet
                            self.player_hand_bets = [self.current_bet] # Reset bets for new round
                            return True # Exit both loops, play again
                        else:
                            print(f"Your bet must be more than 0 and less than or equal to your balance: {self.balance}")
                    except ValueError:
                        print("Invalid input. Please enter only valid integers for your bet.")
            elif play_again_input == "n":
                return False # Exit both loops, do not play again
            else:
                print("Incorrect input. Please enter 'Y' or 'N'.")
    
    def play_game(self):
        """Handles betting and initial card dealing for a round."""
        print("\nWelcome to your table! Set your bet and type 'deal' when you would like to begin.")
        print(f"\n Your balance is: {self.balance} and you are playing with {self.deck_count} decks.")
        
        while True:
            current_bet_str = input('\n Set your bet amount: ')
            try:
                requested_bet = int(current_bet_str)
                if requested_bet <= self.balance and requested_bet > 0:
                    self.current_bet = requested_bet
                    self.player_hand_bets = [self.current_bet]
                    break
                else:
                    print(f"\n Your bet must be more than 0 and less than or equal to your balance: {self.balance}")
            except ValueError:
                print("\n Invalid input. Please enter only valid integers.")
        should_repeat = True        
        while should_repeat:
            deal_status = input("\n Enter 'D' to deal a hand or 'E' to exit the table: ")
            
            if deal_status.lower() == "d":
                if self.balance < self.current_bet:
                    print("\n You don't have enough balance to place this bet. Please set a lower bet or exit.")
                    continue 

                self.balance -= self.current_bet
                print(f"\n Bet of {self.current_bet} placed. Your new balance: {self.balance}")
                
                self.player_hands.clear()
                self.dealer_hand.clear()
                self.player_hands = [[]]
                self.dealer_hand = [] # Reset dealer's hand too

                self.player_hands[0].append(self.deal_card())  # Deal 1st card to player's first hand
                self.dealer_hand.append(self.deal_card())       # Deal 1st card to dealer's hand
                self.player_hands[0].append(self.deal_card())  # Deal 2nd card to player's first hand
                self.dealer_hand.append(self.deal_card())       # Deal 2nd card to dealer's hand
                
                if self.dealer_hand:
                    
                    self.print_hand_ascii_art(self.dealer_hand, "Dealer's Up Card", hide_first_card=True)
                    # Print dealer's UP CARD total
                    print(f"Dealer's Up Card Total: {self.calculate_hand_value([self.dealer_hand[1]])}\n")
                else:
                    print("Dealer's Hand: Empty")
            
                # Display player's initial hand with ASCII art
                self.print_hand_ascii_art(self.player_hands[0], "Player's Hand")
                print(f"Player's Total: {self.calculate_hand_value(self.player_hands[0], return_soft_total_str=True)}")

                
                #function to check for blackjacks

                for i, player_hand in enumerate(self.player_hands): # Iterate through each player's hand
                    player_blackjack = self.check_blackjack(player_hand)
                    dealer_blackjack = self.check_blackjack(self.dealer_hand)
                
                if player_blackjack or dealer_blackjack:
                    print("\n--- Initial Blackjack Check ---")
                    self.print_hand_ascii_art(self.dealer_hand, "Dealer's Cards", hide_first_card=False)
                    self.determine_winner()
                    self.reset_round_state()
                    if self.play_again():
                        continue
                    else: 
                        break
                
                #If no immediate blackjack
                print("\n--- No immediate Blackjack. Starting player's turn ---")
                 # function to handle the player's turn (hit/stand loop)
                self.play_players_turn()
                self.play_again()

            elif deal_status.lower() == "e":
                print("Exiting table.")
                return 
            else:
                print("Invalid input. Please enter 'D' or 'E'.")
    def simulate_odds(self, player_hand, dealer_upcard, deck_state, num_simulations=1000):
        # Dictionary to store the results for each possible decision
        results = {
            "hit": {"win": 0, "lose": 0, "push": 0},
            "stand": {"win": 0, "lose": 0, "push": 0},
            "double": {"win": 0, "lose": 0, "push": 0},
        }

        
        # --- Simulate for 'stand' decision ---
        for _ in range(num_simulations):
            sim_deck = deck_state[:]  # Create a copy of the deck
            random.shuffle(sim_deck)
            
            sim_dealer_hand = [dealer_upcard, sim_deck.pop(0)]
            
            # Simulate dealer's turn
            while self.calculate_hand_value(sim_dealer_hand) < 17:
                if not sim_deck: break # Handle empty deck
                sim_dealer_hand.append(sim_deck.pop(0))
            
            # Determine outcome for 'stand'
            outcome = self.determine_simulation_outcome(player_hand, sim_dealer_hand)
            results["stand"][outcome] += 1
            
        # --- Simulate for 'hit' decision ---
        # NOTE: This is a simplified simulation. A more advanced one would consider
        # further hits after the initial one based on strategy.
        for _ in range(num_simulations):
            sim_deck = deck_state[:]
            random.shuffle(sim_deck)
            
            # Simulate one hit for the player
            sim_player_hand = player_hand[:]
            if not sim_deck: break
            sim_player_hand.append(sim_deck.pop(0))
            
            # Check for bust immediately
            if self.calculate_hand_value(sim_player_hand) > 21:
                results["hit"]["lose"] += 1
                continue
            
            if self.calculate_hand_value(sim_player_hand) <= 11:
                if not sim_deck: continue
                sim_dealer_hand.append(sim_deck.pop(0))
                
            elif 12 <= self.calculate_hand_value(sim_player_hand) <= 16:
                if self.calculate_card_value(dealer_upcard) >= 7:
                    if not sim_deck: continue
                    sim_player_hand.append(sim_deck.pop(0))
                    
            # Play out the rest of the dealer's hand
            sim_dealer_hand = [dealer_upcard, sim_deck.pop(0)]
            while self.calculate_hand_value(sim_dealer_hand) < 17:
                if not sim_deck: break
                sim_dealer_hand.append(sim_deck.pop(0))
                
            # Determine outcome for 'hit'
            outcome = self.determine_simulation_outcome(sim_player_hand, sim_dealer_hand)
            results["hit"][outcome] += 1
            
        # --- Simulate for 'double' decision ---
        for _ in range(num_simulations):
            sim_deck = deck_state[:]
            random.shuffle(sim_deck)
            
            sim_player_hand = player_hand[:]
            if not sim_deck: break
            sim_player_hand.append(sim_deck.pop(0))
            
            # Check for bust immediately after doubling
            if self.calculate_hand_value(sim_player_hand) > 21:
                results["double"]["lose"] += 1
                continue
            
            # Play out the rest of the dealer's hand
            sim_dealer_hand = [dealer_upcard, sim_deck.pop(0)]
            while self.calculate_hand_value(sim_dealer_hand) < 17:
                if not sim_deck: break
                sim_dealer_hand.append(sim_deck.pop(0))
                
            # Determine outcome for 'double'
            outcome = self.determine_simulation_outcome(sim_player_hand, sim_dealer_hand)
            results["double"][outcome] += 1
        
        # Format and return the results as win percentages
        formatted_results = {}
        for decision, outcome_counts in results.items():
            total_outcomes = sum(outcome_counts.values())
            if total_outcomes == 0:
                formatted_results[decision] = {"win_percentage": 0, "lose_percentage": 0, "push_percentage": 0}
            else:
                formatted_results[decision] = {
                    "win_percentage": (outcome_counts["win"] / total_outcomes) * 100,
                    "lose_percentage": (outcome_counts["lose"] / total_outcomes) * 100,
                    "push_percentage": (outcome_counts["push"] / total_outcomes) * 100
                }
        
        return formatted_results

    def determine_simulation_outcome(self, player_hand, dealer_hand):
        player_score = self.calculate_hand_value(player_hand)
        dealer_score = self.calculate_hand_value(dealer_hand)
        
        if player_score > 21: return "lose"
        if dealer_score > 21: return "win"
        if player_score > dealer_score: return "win"
        if dealer_score > player_score: return "lose"
        return "push"   
        
        
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*30)
    print("      Blackjack Simulator")
    print("="*30)
    print("1. Play Game")
    print("2. Set Deck Count") # Added for explicit option
    print("3. View Rules")
    print("4. Exit")
    print("="*30, "\n")

def main():
    """Main game loop and entry point."""
    game = BlackjackGame() # Create an instance of the game


    while True:
        display_menu()
        choice = input("Enter your command: ").lower()

        if choice == "1" or choice == "play": # Allow numerical or text input
            game.get_starting_balance()
            game.set_deck_count()
            if not game.live_deck:
                print("Deck is not set up. Please set deck count first (Option 2).")
                continue
            game.play_game() # This will handle betting and initial deal
            print(f"Returning to menu. Current Balance: {game.balance}")

        elif choice == "2" or choice == "set deck count":
            game.set_deck_count()

        elif choice == "3" or choice == "view rules":
            print("\nBlackjack Rules:")
            print("- Goal: Get as close to 21 without going over.")
            print("- Face cards (J, Q, K) are worth 10.")
            print("- Aces (A) can be 1 or 11 (decided by player/rules).")
            print("- If you go over 21, you 'bust' and lose.")
            print("- Dealer must hit until their hand is 17 or greater.")
            print("- Push: Player and Dealer have the same score.")

        elif choice == "4" or choice == "exit":
            print("Exiting Blackjack Simulator. Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()