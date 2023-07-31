class Board:
    def __init__(self, size):
        self.start = 1
        self.end = self.start + size - 1
        self.size = size

# -----
import random

class Dice:
    def __init__(self, minValue, maxValue):
        self.minValue = minValue
        self.maxValue = maxValue
        self.currentValue = minValue

    def roll(self):
        self.currentValue = random.randint(self.minValue, self.maxValue + 1)
        return self.currentValue


import random

class Game:
    def __init__(self, numberOfLadders, numberOfSnakes, boardSize):
        self.numberOfLadders = numberOfLadders
        self.numberOfSnakes = numberOfSnakes
        self.players = []
        self.snakes = []
        self.ladders = []
        self.board = Board(boardSize)
        self.dice = Dice(1, 6, 2)
        self.initBoard()

    def initBoard(self):
        slSet = set()
        for i in range(self.numberOfSnakes):
            while True:
                snakeStart = random.randint(self.board.getStart(), self.board.getSize())
                snakeEnd = random.randint(self.board.getStart(), self.board.getSize())
                if snakeEnd >= snakeStart:
                    continue
                startEndPair = str(snakeStart) + str(snakeEnd)
                if startEndPair not in slSet:
                    snake = Snake(snakeStart, snakeEnd)
                    self.snakes.append(snake)
                    slSet.add(startEndPair)
                    break
        for i in range(self.numberOfLadders):
            while True:
                ladderStart = random.randint(self.board.getStart(), self.board.getSize())
                ladderEnd = random.randint(self.board.getStart(), self.board.getSize())
                if ladderEnd <= ladderStart:
                    continue
                startEndPair = str(ladderStart) + str(ladderEnd)
                if startEndPair not in slSet:
                    ladder = Ladder(ladderStart, ladderEnd)
                    self.ladders.append(ladder)
                    slSet.add(startEndPair)
                    break

    def addPlayer(self, player):
        self.players.append(player)

    def playGame(self):
        while True:
            player = self.players.pop(0)
            val = self.dice.roll()
            newPosition = player.getPosition() + val
            if newPosition > self.board.getEnd():
                player.setPosition(player.getPosition())
                self.players.append(player)
            else:
                player.setPosition(self.getNewPosition(newPosition))
                if player.getPosition() == self.board.getEnd():
                    player.setWon(True)
                    print("Player " + player.getName() + " Won.")
                else:
                    print("Setting " + player.getName() + "'s new position to " + player.getPosition())
                    self.players.append(player)
            if len(self.players) < 2:
                break

    def getNewPosition(self, newPosition):
        for snake in self.snakes:
            if snake.getHead() == newPosition:
                print("Snake Bit")
                return snake.getTail()
        for ladder in self.ladders:
            if ladder.getStart() == newPosition:
                print("Climbed ladder")
                return ladder.getEnd()
        return newPosition


# ---
class Ladder:
    def __init__(self, start, end):
        self.start = start
        self.end = end


# ---
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.won = False

# ---
class Snake:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

# -- 
# from gb.snakeladder.model import Game
# from gb.snakeladder.model import Player

boardSize = int(input("Enter board Size: "))
numberOfPlayers = int(input("Enter number of players: "))
numSnakes = int(input("Enter number of snakes: "))
numLadders = int(input("Enter number of ladders: "))

game = Game(numLadders, numSnakes, boardSize)
for i in range(numberOfPlayers):
    pName = input("Enter player name: ")
    player = Player(pName)
    game.addPlayer(player)

game.playGame()

