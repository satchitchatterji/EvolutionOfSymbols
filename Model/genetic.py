import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
# This class implements a population of individuals with an arbitrary number
# of traits, whose individuals can reproduce. Thus far, clonal reproduction
# with selection and mutation has been implemented.

class Population:

	########## INITIALIZATION ##########
	def __init__(self, npop, ntraits):
		# basic constructor
		self.population = np.zeros((npop, ntraits))

		self.fitness_function = self.targetted_fitness_gaus
		self.fitness_targets = np.zeros((ntraits))
		self.total_fitnesses = np.zeros((npop))
		self.trait_fitnesses = np.zeros((npop, ntraits))

		self.reproduction = "clonal"
		self.record_history = True
		self.history = []
		
	def init_random(self):
		# all traits are random in the range [0, 1]
		self.population = np.random.random(self.population.shape)

	def init_num(self, num):
		# all traits are set to (float) num
		self.population = np.full(self.population.shape, num)

	def init_population(self, init='random', arr=None):
		# traits can be initialized randomly, to the same value 
		# or based on an array of shape == (population.shape)
		if arr is not None:
			self.population = arr
		elif init == 'random':
			self.init_random()
		elif type(init) in [int, float]:
			self.init_num(init)
		else:
			print("Init type undefined, reverting to zeros")
		
		if self.record_history:
			self.history.append(self.population)

	########## FITNESS ##########
	
	def set_targets(self, arr):
		# set targets for each trait
		arr=np.array(arr)
		if self.fitness_targets.shape != arr.shape:
			print(f"Incorrect shapes: got {arr.shape}, expected {self.fitness_targets.shape}")
			return
		self.fitness_targets = arr

	def targetted_fitness_gaus(self, sigma = 1):
		# for each trait, the fitness is the normal probability
		# of attaining the trait value with a mean of the target
		for ind in range(len(self.population)):
			for trait_idx in range(len(self.population[ind])):
				trait_val = self.population[ind][trait_idx]
				self.trait_fitnesses[ind][trait_idx] = norm.pdf(trait_val, 
																loc = self.fitness_targets[trait_idx], 
																scale = sigma)
	
	def targetted_fitness_lin(self, s = 0.1):
		# for each trait, the fitness linearly decreases wrt the
		# the target, shifted upwards by an arbitrary value to ensure
		# non-negativity, set to the max of each trait
		mu = np.max(self.population.T)
		self.trait_fitnesses = np.abs(s*mu)-np.abs(s*np.add(self.fitness_targets, -self.population))


	def equal_fitness(self):
		# set all fitnesses equal to one another (no selection)
		self.trait_fitnesses = np.full(self.population.shape, 1)

	def direct_fitness(self):
		# the values of the traits are fitness values
		# makes no semantic sense, just for debugging
		self.trait_fitnesses = self.population.copy()


	def calc_total_fitness(self):
		# calculates fitness of each individual
		self.fitness_function()
		self.total_fitnesses = sum(self.trait_fitnesses.T)

	def max_fitness(self):
		# get max fitness of individual
		return max(self.total_fitnesses)

	def mean_fitness(self):
		# get min fitness of individual
		return np.mean(self.total_fitnesses)

	########## MUTATION ##########

	def mutate_traits(self, rate = 0.02, mu = 0, sigma = 2):
		# mutates traits on the basis of a chance (rate)
		# adds a gaussian random if trait is chosen to be mutated
		# this function can be made faster by better vectorization
		# chance is calculated per trait per individual
		to_mutate = np.round(np.random.random(self.population.shape)+rate-0.5)
		changes = np.random.normal(mu, sigma, self.population.shape)
		mutations = np.multiply(to_mutate, changes)
		self.population = np.add(mutations, self.population)

	########## REPRODUCTION ##########

	# Fitness proportionate selection
	def roulette_wheel(self):
		return self.total_fitnesses/sum(self.total_fitnesses)
	
	def choose_parents_indices(self, nparents=1):
		# choose parents probabilistically, on the basis of 
		# fitness, n=1 == clone of parent (crossover to be added)
		next_gen = []
		probs = self.roulette_wheel()
		# for each i of the next gen,
		# 	choose each parent
		for i in range(len(self.population)):
			next_gen.append([])
			for j in range(nparents):
				child_index = np.random.choice(len(self.population), p=probs)
				next_gen[i].append(child_index)

		return next_gen

	def renew_population_exact(self):
		# copy this generation over with mutations
		self.mutate_traits()
	
	def renew_population_clonal(self):
		# create next generation of individuals, probabilistically
		# with respect to each parent's fitness value
		self.calc_total_fitness()
		next_gen_indices = self.choose_parents_indices(nparents=1)
		next_gen = np.zeros(self.population.shape)

		for i in range(len(next_gen_indices)):
			next_gen[i]= self.population[next_gen_indices[i][0]]

		self.population = next_gen
		self.mutate_traits()
	
	def next_gen(self):
		# get next generation, and record it
		if self.reproduction == "clonal":
			self.renew_population_clonal()
		elif self.reproduction == "exact":
			self.renew_population_exact()
		else:
			print("No reproduction mode specified")
		
		if self.record_history:
			self.history.append(self.population)

	def run_generations(self, gens):
		# run next_gen gens number of times
		for _ in range(gens):
			self.next_gen()


	########## PLOTTING ##########

	def plot_single(self, trait=0):
		# simple single plot for the trait-th value
		hist = np.transpose(np.array(self.history), axes=(2,1,0))
		for p in hist[trait]:
			plt.plot(p)
		plt.title(f'Trait {trait}')
		plt.grid()
		plt.show()

	def plot_history(self, args):
		# plot history of traits on different
		# subplots over time.
		# args should contain an nxm matrix
		# to decide layout of the plots
		# if there is only one trait, plot it
		if args == (1,1):
			args = 0;
		if type(args) == int:
			try:
				self.plot_single(args)
			except IndexError:
				print(f"No such trait {args} exists, cannot plot!")
			return

		# else, create subplots for each trait
		fig, axs = plt.subplots(*args)
		axs = axs.ravel()
		hist = np.transpose(np.array(self.history), axes=(2,1,0))
		
		for t in range(len(hist)):
			trait = hist[t]
			for pop in (trait):
				axs[t].plot(pop)
			axs[t].set_title(f"Trait {t}")
			axs[t].grid()

		plt.show()