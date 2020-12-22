import neat
from sim_runner import *
import pygame

# got walls after drawing using ray-tracing code from github, going to be set map for genetic

# techwithtim helped a ton with this (through tutorials), specifically his flappy bird one
# https://github.com/techwithtim/NEAT-Flappy-Bird/blob/master/flappy_bird.py 

# Load configuration.
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        'config-feedforward.txt')

# Create the population, which is the top-level object for a NEAT run.
p = neat.Population(config)

# Add a stdout reporter to show progress in the terminal.
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
#p.add_reporter(neat.Checkpointer(5))

# Run for up to 100 generations.
winner = p.run(eval_genomes, 100)

# show final stats
print('\nBest genome:\n{!s}'.format(winner))