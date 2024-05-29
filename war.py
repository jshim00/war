"""
This Python script simulates the card game war. 
We want to see how long a game of war takes on average given a set number of players each round (input) 
The game is over when one person usurps all 52 cards, and all other players have been eliminated. 

Hypothesis: 
If the game begins with 2 people, game should be over relatively quickly.
If the game begins with 10 people, game should take longer because 8 players will have to be eliminated and then we reach a game of 2 people. 

We can represent each card as an int. Numbered cards 2-10. Royal cards will be 11-14. 
Jack = 11, Queen = 12, King = 13, Ace = 14
Space-efficient! 

We need to represent each player in the game. 
This is because we need to track of how many cards each player has. 
We also need to keep track of how many players there are at all times; Once we reach the last man standing, game is over. 

Each player is randomly generated a hand from a deck of 52 cards. 

"""
import random 

class Player():
    def __init__(self,cards,eliminated=False):
        self.cards = cards # List of Int
        self.eliminated=eliminated 

class Game():
    def __init__(self,num_players):
        self.num_players = num_players # Keeps track of how many players are remaining

    def deal(self): # Instantiate players, create deck (dictionary), deal cards

        # Create a deck - shuffle it
        suit = list(range(2,15)) # list(range(SMALLEST,LARGEST+1))
        deck = suit + suit + suit + suit # unshuffled: 

        """
        deck = []
        for i in range(NUM_OF_SUITS):
            deck += suit 
        """

        num_of_cards = len(deck) 
        deck = random.sample(deck,num_of_cards)

        # Assign each player a hand 
        num_of_players = self.num_players
        hand_size = num_of_cards // num_of_players 
        players = []
        j = 0
        # print(num_of_cards)
        # print(deck)

        for i in range(num_of_players):
            ptr = j + hand_size 
            players.append(deck[j:ptr]) 
            # print(f"Player {i} has hand {players[i]}")
            j = ptr 

        # Check if we have cards remaining in the deck
        remainder = num_of_cards % hand_size
        if remainder != 0:
            cards_remaining = deck[-remainder:] 
            # print(f"There are {remainder} cards remaining in the deck: {cards_remaining}") 
            if remainder <= num_of_players: # This should always be true 
                for i in range(remainder):
                    players[i].append(cards_remaining[i])

            # for i in range(num_of_players):
            #     print(f"Player {i} now has hand {players[i]}") 

        # Returns a list of players
        return players 
    
    # Return the winner of the war 
    def war(self,contenders,players):
        n = len(contenders)  
        pile = [] # Goes to the winner
        cardpool = [] # Used to determine winner 

        while True:

            # Each player omits top 3 cards (face down) and places the 4th card face-up 
            for i in contenders:
                player = players[i] 
                if len(player) >= 4: # If the player has 4 cards or more 
                    pawns = player[:4] # Add first four cards to storage 
                    sword = player[3] # Place the third card 
                    players[i] = player[3:] # Remove all of these cards from the player 
                else: # If the player runs out of cards 
                    pawns = player # Add rest of player's hand 
                    sword = player[-1] # Place the last card  
                    players[i] = [] # Removes all cards -- empty list 
                
                pile.extend(pawns) # Pile the pawn cards together
                cardpool.append(sword) # Compute winner from this list 
            
            # If we do not have a winner, repeat 
            highest = max(cardpool) # Find the winner -- player with the highest value card 
            winners = [i for i in range(n) if cardpool[i]==highest] # Check if there is a tie  

            # winners = []
            # for i in contenders:
            #     player = players[i]




            if len(winners) == 1: # If there is a decisive winner, exit
                players[winners[0]].extend(pile) 
                players[winners[0]].extend(cardpool) 
                break
            else: # No decisive winner - WAR AGAIN w/ remaining contenders 
                pile.extend(cardpool) # Update burned pile
                cardpool = [] # Reset cardpool 
                contenders = winners 

                
        # print(pile)
        # print(cardpool) 
        return players 

    # Play one round of War. Determine winner. If tie, WAR. Update players hands accordingly. 
    def findWinner(self,players):
        n = len(players) 
        cardpool = [None]*n # store all of the cards here - goes to the winner 

        # Each player removes the top card from their hand and places it into the pool
        for i in range(n):
            top_card = players[i][0]
            cardpool[i] = top_card
            players[i].remove(top_card)
        
        highest = max(cardpool) # Find the winner -- player with the highest value card 
        winners = [i for i in range(n) if cardpool[i]==highest] # Check if there is a tie - where up to 4 players can have the highest value card 
        if len(winners) > 1: # Multiple winners - WAR 
            # print(f"I DECLARE WAR: {winners}") 
            # winner = winners[0] 
            return self.war(winners,players)
        else: # One decisive winner 
            # Update the winner's hand - populating with cardpool 
            players[winners[0]].extend(cardpool) 

        # print(cardpool)
        # print(f"The winner of the round is Player {winner} with card {highest}")

        # for i in range(n):
        #     num_of_cards = len(players[i])
        #     print(f"Player {i} now has {num_of_cards} cards") 

        return players 

    def playWar(self):
        players = self.deal() 
        rounds = 0 # Count the number of rounds 
        # result = self.findWinner(players)

        while self.num_players > 1: 
            # print(f"Round: {rounds}")
            hands = self.findWinner(players) 
            
            # Check for eliminated players 
            players = []
            for hand in hands: 
                if len(hand) == 0: 
                    self.num_players -= 1
                    # print(f"Someone was eliminated in round {rounds}") 
                else:
                    players.append(hand) 

            rounds+=1 
        
        print(f"This game took {rounds} rounds")

"""
"""

war = Game(num_players = 8)
war.playWar()

