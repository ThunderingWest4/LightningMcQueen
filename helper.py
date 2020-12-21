import neat

class Player():

    def __init__(self, genome):
        self.angle = 0
        self.speed = 0
        self.net = neat.nn.feed_forward.create(genome)