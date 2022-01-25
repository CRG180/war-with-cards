import random
import os
from subprocess import call
from time import sleep


def clear():
	_ = call('clear' if os.name =='posix' else 'cls')

class Card:
	"""docstring for Card"""
	def __init__(self, suit, value):
		self.suit = suit
		self.value =  value
		self.face_text = str(value)
		self.face()

	def face(self):
		if self.value == 11:
			self.face_text= "J"
		elif self.value == 12:
			self.face_text = "Q"
		elif self.value == 13:
			self.face_text = "k"
		elif self.value == 14:
			self.face_text = "A"
		else:
			self.face_text = str(self.value)

	def __str__(self):

		card = (
        '┌─────────┐\n'
        '│{}       │\n'
        '│         │\n'
        '│         │\n'
        '│    {}   │\n'
        '│         │\n'
        '│         │\n'
        '│       {}│\n'
        '└─────────┘\n'
	    ).format(
	        format(self.face_text, ' <2'),
	        format(self.suit, ' <2'),
	        format(self.face_text, ' <2')
	    )
		return card

	def __repr__(self):
		return self.face_text + self.suit


	def __gt__(self, other):
		if(self.value > other.value):
			return True
		else:
			return False

	def __lt__(self, other):
		if(self.value < other.value):
			return True
		else:
			return False

	def __eq__(self, other):
		if(self.value == other.value):
			return True
		else:
			return False


class Deck(list):
	def __init__(self):
		super().__init__(Card(s,v) for s in ['♠', '♦', '♥', '♣']
		for v in range(2,15))
		random.shuffle(self)

class Player:
	def __init__(self, name):
		self.name = name
		self.hand = []
		self.captured =[]
		self.player_message = ""

	@property
	def outOfCards(self):
		if len(self.hand) == 0 and len(self.captured) == 0:
			return True
		else:
			return False
	@property
	def totalCards(self):
		return len(self.hand) + len(self.captured)

	def build_hand(self):
		random.shuffle(self.captured)
		while len(self.captured) >0:
			self.hand.append(self.captured.pop(0))


	def add_cards_to_table(self,
	                      table,
						  nCardsAdd = 1,
	 					  simMode = True,
						  ):
		activeCard = "_"
		if self.outOfCards or self.totalCards < nCardsAdd:
			if simMode:
				self.player_message = f"{self.name} is out of cards." \
				 f" {self.name} has {self.totalCards}" \
				 f" cards but needs {nCardsAdd}"
			self.hand = []
			self.captured = [] # This is the reason why we don't always see 52 cards at the end
			return Card('♠', 0)

		elif len(self.hand) == 0 or len(self.hand) < nCardsAdd:
			self.build_hand() # build hand if out of cards, get captured cards
		else:
			pass

		for i in range(0,nCardsAdd):
			if i == 0:
				activeCard = self.hand[i]
			else:
				pass
			table.append(self.hand.pop(0))
		return activeCard

	def collect_cards_from_table(self, table):
		while len(table) > 0:
			self.captured.append(table.pop(0))
		#print(self.name, "collecting from the pot")

	def __repr__(self):
		return f"{self.name}--{self.totalCards}"


class Table(list):
	def __init__(self):
		super().__init__()

class Game:
	def __init__(self,playerList,
				numberCardsFaceDown = 4,
				simMode = False):
		self.playerList = playerList
		self.numberCardsFaceDown = numberCardsFaceDown
		self.table = []
		self.numberIters = 0
		self.numberWarIters = 0

	def deal_cards(self):
		deck = Deck() # maybe add more decks if more than x players
		#Shuffle the order in which the cards get dealt
		playerIndexShuffle = [i for i in range(len(self.playerList))]
		random.shuffle(playerIndexShuffle)
		while len(deck) > 0:
			for i in playerIndexShuffle:
				try:
					self.playerList[i].hand.append(deck.pop(0))
				except:
					pass

	def no_war(self):
		self.numberIters+=1
		activeCardlist =[]
		for player in self.playerList:
			activeCardlist.append(player.add_cards_to_table(self.table))

		maxCardValue = max(activeCardlist)
		maxCardIndex = [index for index, val in enumerate(activeCardlist) if val == maxCardValue]

		if len(maxCardIndex) > 1 and maxCardValue.value > 0:
			self.war(maxCardIndex)
			return False
		#draw
		elif sum(card.value for card in activeCardlist) == 0:
			return True #Game is over, not sure if this is possible

		#all but one player has cards, a person has been defeated
		elif [player.totalCards for player in self.playerList].count(0) == len(self.playerList) -1:
			return True # Games is over

		else:
			self.playerList[maxCardIndex[0]].collect_cards_from_table(self.table)
			return False # game continues

	def war(self, maxCardIndex):
		self.numberWarIters+=1
		warPlayerList = [self.playerList[i] for i in maxCardIndex]
		activeCardlist = []
		for player in warPlayerList:
			activeCardlist.append(player.add_cards_to_table(self.table ,self.numberCardsFaceDown))

		maxCardValue = max(activeCardlist)
		maxCardIndex = [index for index, val in enumerate(activeCardlist) if val == maxCardValue]

		if len(maxCardIndex) >1 and maxCardValue.value > 0:
			self.war(maxCardIndex) # Has occured multiable times

		else: # a player has won the war
			warPlayerList[maxCardIndex[0]].collect_cards_from_table(self.table)
			# goes back to regular game

def main():
	playerList = [Player("Stu"), Player("Charles"), Player("Sally Jo"),Player("Clara")]
	game = Game(playerList = playerList)
	game.deal_cards()
	gameWinner = False

	while gameWinner == False:
		gameWinner = game.no_war()

	winnerTotals = [player.totalCards for player in playerList]
	winnerValue = max(winnerTotals)
	winnerIndex = winnerTotals.index(winnerValue)
	playerList[winnerIndex].collect_cards_from_table(game.table)

	for player in playerList:
		player.build_hand()

	for player in playerList:
		print(f"{player.name} ---Total cards {player.totalCards}" )

	print(f"The game played {game.numberIters} iterarations.")
	print(f"War happend {game.numberWarIters} iterarations.")


if __name__ == "__main__":

	main()

	# playerList = [Player("Stu"), Player("Charles"), Player("Sally Jo"),Player("Clara")]
	# game = Game(playerList = playerList)
	# game.deal_cards()
	# gameWinner = False
	#
	# while gameWinner == False:
	# 	gameWinner = game.no_war()
	#
	# winnerTotals = [player.totalCards for player in playerList]
	# winnerValue = max(winnerTotals)
	# winnerIndex = winnerTotals.index(winnerValue)
	# playerList[winnerIndex].collect_cards_from_table(game.table)
	#
	# for player in playerList:
	# 	player.build_hand()
	#
	# for player in playerList:
	# 	print(f"{player.name} ---Total cards {player.totalCards}" )
	#
	# print(f"The game played {game.numberIters} iterarations.")
	# print(f"War happend {game.numberWarIters} iterarations.")
