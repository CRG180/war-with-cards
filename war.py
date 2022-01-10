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

class Deck:
	def __init__(self):
		self.cards = []
		self.build()
		self.shuffle_deck()

	def build(self):
		for s in ['♠', '♦', '♥', '♣']:
			for v in range(1,15):
				self.cards.append(Card(s,v))

	def shuffle_deck(self):
		return random.shuffle(self.cards)

class Player:
	def __init__(self, cards, name):
		self.name = name
		self.cards = cards

	def add_card_to_pot(self,table,
						player_name = "Null",
						sim_mode = False,
						isActiveCard = False):

		card = self.cards.pop(0)
		table.pot.append(card)

		if (sim_mode == False) and (isActiveCard == True):
			print(player_name)
			print(card)
			return card
		else:
			return card

	def collect_cards_from_pot(self,table):
		self.cards.extend(table.pot)
		table.pot = []

	def card_count(self):
		return len(self.cards)

	def print_deck(self):
		'''function for trouble shooting'''
		return print(self.cards)

class Table:
	def __init__(self):
		self.pot = []

	def number_cards_on_table(self):
		'''method for trouble shooting'''
		return len(self.pot)

	def print_table(self):
		'''method for troubleshooting'''
		return print(self.pot)


class Game:
	def __init__(self,player1, player2,
				number_cards_face_down = 3,
				sim_mode = False):

		self.player1= player1
		self.player2 = player2
		self.table = Table()
		self.number_cards_face_down = number_cards_face_down
		self.sim_mode = sim_mode
		self.iterations = 0
		self.wars = 0
		self.game_lost_message = "None"
		self.number_of_cards_on_table = 0


	def war(self):
		game_won = False
		while game_won == False:
			self.iterations+=1

			active_card_player1 = self.player1.add_card_to_pot(
										table = self.table,
										player_name = self.player1.name,
										sim_mode = self.sim_mode,
										isActiveCard = True)

			active_card_player2 = self.player2.add_card_to_pot(
										table = self.table,
										player_name = self.player2.name,
										sim_mode = self.sim_mode,
										isActiveCard = True)


			if active_card_player1 > active_card_player2:
				self.player1.collect_cards_from_pot(self.table)
				if self.sim_mode == False:
					print(self.player1.name, "wins!")
				else:
					pass

			elif active_card_player1 < active_card_player2:
				self.player2.collect_cards_from_pot(self.table)

				if self.sim_mode == False:
					print(self.player2.name, "wins!")
				else:
					 pass

			else:
				if self.sim_mode == False:
					print("Let's play war!")
					input("Press Enter to contine...")
					clear()
				else:
					pass


				war = True
				while war ==True:
					self.wars+=1
					# Each iteration of war face card 1 to 3 are placed down first
					# If a player runs out of cards that player loses
					try:
						for _ in range(1, self.number_cards_face_down + 1):
							self.player1.add_card_to_pot(table = self.table)

						active_card_player1 = self.player1.add_card_to_pot(
												table = self.table,
												player_name = self.player1.name,
												sim_mode = self.sim_mode,
				 								isActiveCard = True)
					except:
						self.game_lost_message = self.player1.name + " has no more cards and has lost the game"
						self.number_of_cards_on_table = self.table.number_cards_on_table()
						self.player2.collect_cards_from_pot(self.table)

						if self.sim_mode == False:
							print(self.game_lost_message)
						else:
							pass

						game_won = True
						break

					try:
						for _ in range(1, self.number_cards_face_down + 1):
							self.player2.add_card_to_pot(self.table)

						active_card_player2 = self.player2.add_card_to_pot(
											table = self.table,
											player_name = self.player2.name,
											sim_mode = self.sim_mode,
											isActiveCard = True)

					except:
						self.game_lost_message = self.player2.name + " has no more cards and has lost the game"
						self.number_of_cards_on_table = self.table.number_cards_on_table()
						self.player1.collect_cards_from_pot(self.table)
						if self.sim_mode == False:
							print(self.game_lost_message)
						else:
							pass

						game_won = True
						break

					if active_card_player1 > active_card_player2:
						self.player1.collect_cards_from_pot(self.table)
						war = False
						if self.sim_mode == False:
							print(self.player1.name, "wins this bout of war!")
						else:
							pass

					elif active_card_player2 > active_card_player1:
						self.player2.collect_cards_from_pot(self.table)
						war = False
						if self.sim_mode == False:
							print(self.player2.name, "wins this bout of war!")
						else:
							pass

					else:
						if self.sim_mode == False:
							clear()
							print("The War Continues")
							#sleep(3)
							input("Press enter to contine...")
							clear()
						else:
							pass

			if self.sim_mode == False:
				print("\nThe score is:")
				print(self.player1.name, self.player1.card_count())
				print(self.player2.name, self.player2.card_count())
				print("Number of iterations:",self.iterations)
				print("Number of wars:",self.wars)
				input("\nPress Enter to contine...")
				clear()
				sleep(.1)

			else:
				pass

			if self.player1.card_count()== 0:
				game_won = True

			elif self.player1.card_count() == 0:
				game_won = True

			elif self.iterations >= 500_000:
				game_won = True

			else:
				pass

		if self.sim_mode == False:
			clear()
			print("\nThe Final score is:")
			print(self.player1.name, self.player1.card_count())
			print(self.player2.name, self.player2.card_count())
			print("Number of iterations:",self.iterations)
			print("Number of wars:",self.wars)

		else:
			pass

		return {"player1_name": self.player1.name,
		        "player2_name": self.player2.name,
		        "number_cards_face_down": self.number_cards_face_down,
		        "player1_score": self.player1.card_count(),
		        "player_2_score": self.player2.card_count(),
		        "number_iterations": self.iterations,
		        "number_of_wars": self.wars,
		        "game_lost_message": self.game_lost_message,
				"number_of_cards_on_table":self.number_of_cards_on_table}




def main():
	deck = Deck()
	# player1 = Player(deck.cards[0:26], input("Enter player 1's name: "))
	# player2 = Player(deck.cards[26:52], input("Enter Player 2's name: "))
	player1 = Player(deck.cards[0:26], "stu")
	player2 = Player(deck.cards[26:52], "charles")
	game_1 = Game(player1,player2, sim_mode = True)
	results=game_1.war()
	clear()
	for i in results.keys():
		print(i+": ",results[i])

if __name__ == "__main__":
    main()
