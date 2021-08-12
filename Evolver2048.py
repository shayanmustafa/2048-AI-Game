from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
from game2048 import game2048

weightShapes = [(16, 8), (8,), (8, 4), (4,)]
weightSizes = [128, 8, 32, 4]

class Fitness:
	game = game2048()

	@staticmethod
	def makeChooseAction(model):
		"""Creates a chooseAction function for the 2048 game based on the input model"""
		return lambda actions, board: Fitness.modelChooseAction(actions, board, model)

	@staticmethod
	def modelChooseAction(actions, board, model):
		"""
		Run the model on the given board and determine the est available action.
		- actions is a 4-element boolean array indicating whether an action is available
		- board is a 4x4 element array indiating locations of tiles
		- model is the Keras model
		- return value is an integer [0,3] indicating preferred action
		This function relies on strictly-positive outputs from the model, such as with softmax
		"""
		# Keras is desgined to make multiple predictions at once, where each row is a single data point
		# Hence the input has data in the second dimension
		input = board.reshape(1,-1)
		# Run the NN on the given input as a 1d array
		# +1 so any valid option is chosen before any invalid
		output = np.squeeze(model(input)) + 1
		# Keep only values where actions are allowed
		output = output * actions
		# Return index of highest rated action
		return output.argmax()


	@staticmethod
	def fitness(model):
		chooseAction = Fitness.makeChooseAction(model)
		score, bestTile, moves = Fitness.game.play(chooseAction)
		
		return score

class Genome:
	"""
	A wrapper for genetic information.

	Create statically with genome = Genome.fromArray() or Genome.fromRandom()
	Genes are 172 element 1d numpy arrays
	Models are shape (16,8,4)

	Genomes will make models when required by ftiness()

	Test with genome.fitness()
	This stores the last computed fitness value and reuses it unless asked otherwise

	Get the genes as an array with genome.genes
	"""
	fitnessTrials = 1
	model = None

	def __init__(self):
		self.lastFitness = None

	@staticmethod
	def fromArray(array):
		"""Create a genome from a 1d array."""
		assert len(array) == 172, "Array is of invalid length"
		genome = Genome()
		genome.genes = array
		return genome
	
	@staticmethod
	def fromRandom():
		"""Create a genome with random weights in the range [-1,1]"""
		return Genome.fromArray(np.random.rand(172) * 2 - 1)
		
	@staticmethod
	def makeBlankModel():
		"""Return a Keras model from the contained array"""
		model = Sequential()
		model.add(Dense(8, input_shape=(16,)))
		model.add(Dense(4, activation="sigmoid"))
		return model
	
	def fitModel(self, model):
		"""Apply the weights from the genome to the given model"""
		l1w = self.genes[0:128].reshape(16,8)
		l1b = self.genes[128:136]
		l2w = self.genes[136:168].reshape(8,4)
		l2b = self.genes[168:172]
		model.set_weights([l1w,l1b,l2w,l2b])
		return model

	def toModel(self):
		"""Create and fit a model for this Genome"""
		return self.fitModel(Genome.makeBlankModel())

	def fitness(self, fitnessFunc=Fitness.fitness, forceTest=False):
		"""
		Get the last computed fitness of a genome.
		If forceTest is true then fitness is reevaluated even if it has been already.
		The model will play trials games and the fitness is its average score over all games.
		"""
		if Genome.model is None:
			Genome.model = Genome.makeBlankModel()
		if (self.lastFitness is None) or forceTest:
			model = self.fitModel(Genome.model)
			scores = [fitnessFunc(model) for _ in range(Genome.fitnessTrials)]
			self.lastFitness = sum(scores) // len (scores)
		return self.lastFitness

	def save(self, path="./genome.npy"):
		np.save(path, self.genes)
	
	@staticmethod
	def load(path="./genome.npy"):
		return Genome.fromArray(np.load(path))

class Mutator:
	"""
	A wrapper for reproduction and crossing between Genomes
	"""
	@staticmethod
	def crossover(genome1, genome2, rate=0.5):
		"""
		Crosses two genomes and returns a single child

		Each gene is inherited from gen2 with probability rate
		For low rate, children are similar to gen1
		"""
		genes1 = genome1.genes
		genes2 = genome2.genes
		mask = np.random.rand(172) > rate
		newGenes = np.where(mask, genes1, genes2)
		return Genome.fromArray(newGenes)
	
	@staticmethod
	def mutate(genome, rate=0.2, size=1):
		"""
		Returns a mutation on the given genome based on the given rate and size

		Rate is the fraction of genes that are mutated
		Size is the standard deviation of each mutation
		"""
		genes = genome.genes.copy()
		mask = np.random.rand(172) < rate
		numMuts = mask.sum()
		mutations = np.random.randn(numMuts) * size 
		genes[mask] += mutations
		return Genome.fromArray(genes)

# Testing code