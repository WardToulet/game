import pickle

from world import World

class Level: 
    def __init__(self, level_data_path):
        self.level_data_path = level_data_path

    def load_world(self, tile_size):
        pickle_in = open(self.level_data_path, 'rb')
        world_data = pickle.load(pickle_in)

        return World(world_data, tile_size)
