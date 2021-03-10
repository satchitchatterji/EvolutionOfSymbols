from genetic import Population

# population with 100 individuals, 4 traits each
p = Population(100, 4)
# initialize all traits to value 15
p.init_population(15)
# set targets for each trait
p.set_targets([10, 20, 15, 25])
# run 100 generations
p.run_generations(100)
# plot the history of the traits on a 2x2 grid
p.plot_history((2,2))