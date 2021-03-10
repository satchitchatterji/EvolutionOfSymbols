from genetic import Population

p = Population(100, 4)
p.init_population(15)

p.set_targets([10, 20, 15, 25])

p.run_generations(100)
p.plot_history((2,2))
