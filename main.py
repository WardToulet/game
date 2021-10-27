from game import Game
from level import Level

if __name__ == '__main__':
    game = Game(
            width=1000, 
            height=1000, 
            tile_size=50, 
            levels=[ Level(f"leveldata/level{x}_data") for x in range(0, 8) ]
    )
    game.run()
