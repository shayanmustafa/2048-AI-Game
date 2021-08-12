import numpy as np

directionToAxis = np.array([
	(0,1),
	(1,-1),
	(0,-1),
	(1,1)
])

class game2048():
	def __init__(self, rngSeed=2048):
		self.rng = np.random.default_rng(rngSeed)
		self.showSteps = False
		self.actions = np.array([True,True,True,True])

	def newGame(self):
		self.board :np.ndarray = np.zeros((4,4), dtype=int)
		self.actions = np.array([True,True,True,True])
		self.score = 0
		# Start with 2 random tiles
		self.placeRandomTile()
		self.placeRandomTile()
	
	def pickRandomEmpty(self):
		empties = np.argwhere(self.board == 0)
		return tuple(self.rng.choice(empties))

	def placeRandomTile(self):
		idx = self.pickRandomEmpty()
		tile = (self.rng.random() > 0.9) * 2 + 2
		self.board[idx] = tile

	def action(self, direction):
		# directions are 0,1,2,3 for up, right, down, left
		assert self.actions[direction], f"Attempted to take action {direction} when {self.actions} were available"
		# Translate direction into row/column and towards start/end
		axis, orientation = directionToAxis[direction]
		self.board = np.apply_along_axis(self.moveRow, axis, self.board, orientation=orientation)
		self.placeRandomTile()

		return self.board

	def moveRow(self, row, orientation):
		# +1 collapse towards the beginning of the row, -1 collapse to end
		# Method is collapse all tiles to start, merge adjacent tiles, collapse again
		newRow = row[::orientation].copy()
		newRow = self.collapseRow(newRow)
		newRow = self.mergeRow(newRow)
		newRow = self.collapseRow(newRow)

		return newRow[::orientation]

	def collapseRow(self, row):
		# nonzero returns a one element tuple
		nzIndices = np.nonzero(row)[0]
		newRow = np.zeros(len(row), dtype=int)
		# Add all nonzero values to the start of the array
		newRow[:len(nzIndices)] += row[nzIndices]
		return newRow

	def mergeRow(self, row):
		newRow = row.copy()
		# I don't know if it's possible to vectorise this bc each value relies on the previous one
		# Don't merge last index
		for i in range(len(row)-1):
			# If two tiles have same value
			if newRow[i] == newRow[i+1]:
				# Merge them into the tile of lower index
				newRow[i] = 2 * newRow[i]
				newRow[i+1] = 0
				# Add score equal to value of merged tile
				self.score += newRow[i]
		return newRow
	
	def possibleActions(self):
		# Return an array of whether each action is possible
		# This is a 4-element boolean array where each element indicates whether that action is available
		return np.array([self.actionPossible(direction) for direction in range(4)])
		
	def actionPossible(self, direction):
		axis, orientation = directionToAxis[direction]
		rowsMoveable = np.apply_along_axis(self.rowMovePossible, axis, self.board, orientation=orientation)
		return rowsMoveable.any()

	def rowMovePossible(self, row, orientation):
		possible = False
		checkRow = row[::orientation]
		# Ensure there are nonzero values
		nzIndices = np.nonzero(checkRow)[0]
		if nzIndices.size > 0:
			# Test if the furthest nonzero from start is further away than minimum so can move
			possible = np.max(nzIndices) >= len(nzIndices)
			# If no fillable zeros, check for merges
			if not possible:
				# Test if any consecutive nonzeros are equal so can merge
				# ediff1d returns a length n-1 array of differences between consecutive values
				nzValues = checkRow[nzIndices]
				possible = (np.ediff1d(nzValues) == 0).any()
		return possible

	def play(self, chooseAction, showSteps=False):
		self.newGame()
		actionsTaken = 0
		if showSteps: print(self.board)
		while self.actions.any():
			action = chooseAction(self.actions, self.board)
			self.action(action)
			actionsTaken += 1
			self.actions = self.possibleActions()
			if showSteps: print(self.board)
		return self.score, self.board.max(), actionsTaken

# Testing Code
"""
game = game2048()

def chooseRandomAction(actions, board):
	return np.random.choice(np.nonzero(actions)[0])

score, bestTile, moves = game.play(chooseRandomAction, True)

print(f"Score: {score} Best Tile: {bestTile} Moves: {moves}")
"""