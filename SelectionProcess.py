import numpy as np
from scipy.stats import skewnorm

#passing a list of genomes
def rouletteSelect(genomes, exponent=1):
    """
    Implements roulette selection. The probability of a genome being chosen is proportional to its fitness ** exponent.
    Higher exponent shifts selection in favour of higher scores.
    Takes a list of genomes, returns the selected parent.
    """
    #calculating fitness score of each individual
    fitnessScores = [gene.fitness() ** exponent for gene in genomes]
    #sum of all fitnesses
    sumOfFitnessScores = np.sum(fitnessScores)
    #generate a random number between 0 and sum of fitnesses
    randFitnessScore = np.random.randint(0, sumOfFitnessScores)

    #starting from top of the population, keep adding fitnesses to the partial sum of fitnesses (P), till P > random fitness score
    partialSum = 0
    chosenGenome = None
    for genome in genomes:
        # the genome at which partial sum exceeds sum of all fitness is the selected parent.
        if partialSum < randFitnessScore:
            partialSum += genome.fitness() ** exponent
            chosenGenome = genome
    return chosenGenome

def rouletteSelection(genomes, n=20, exponent=1):
    """
    Implements roulette selection. The probability of a genome being chosen is proportional to its fitness.
    Takes a list of genomes, returns n top candidates.
    """
    genomes = list(genomes)
    parents = []
    for i in range(n):
        selection = rouletteSelect(genomes, exponent)
        genomes.remove(selection)
        parents.append(selection)
    return parents

def skewnessSelection(listofgenomes, n=20, skewness=30):
    '''
    So in theory this function needs fitness function to work. But i assume we will have a python list, full of sorted genomes
    And we choose the n best genomes. n is the % to keep. Returns list of survived.
    Negative skewness values are left skewed, positive values are right skewed.
    '''
    
    total = len(listofgenomes)   
    
    tokeep = ((total * n) // 100) #-1 because best one survives no matter what 
    
    listofgenomes = sorted(listofgenomes, key=lambda genome: genome.fitness())
    
    #survival.append(listofgenomes[0]) # best performer survives all the time listofgenaomes[1:]

    random = skewnorm.rvs(a=skewness, size=total)  #Skewnorm function
    random = np.clip(random, 0, None) # prevent negative probabilities
    random = random / random.sum() # Probabilities sum to 1
    random = sorted(random) # Align high weights to high fitnesses
    
    return np.random.choice(listofgenomes, size=tokeep, replace=False, p=random)