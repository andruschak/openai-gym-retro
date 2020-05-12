import argparse
import retro

# SuperMarioBros-Nes
# SonicTheHedgehog2-Genesis
parser = argparse.ArgumentParser()
parser.add_argument('--game', default='SuperMarioBros-Nes', help='the name or path for the game to run')
parser.add_argument('--state', help='the initial state file to load, minus the extension')
parser.add_argument('--record', '-r', action='store_true', help='record bk2 movies')
args = parser.parse_args()

def main():
    env = retro.make(args.game, args.state or retro.State.DEFAULT, record=args.record)
    obs = env.reset()
    while True:
        # env.step returns 4 parameters
        # observ - object representing your observation of the environment
        # reward - a floating point number of the reward from the previous action
        # done - boolean value indicating whether or not to reset the environment
        # info - a dictionary containing data from the game variables defined in data.json (ex: info[coins])
        # action = env.action_space.sample() - do a random action
        # action = [0,0,1,0,0,0,0,1,1,1,0,0] - mapping out possible actions? need more info
        # print(env.action_space.sample())
        observ, reward, done, info = env.step(env.action_space.sample())
        print("Reward: ", reward)
        # mario - unsigned single byte (8bit); xscrollLo wraps at 255 and increases xscrollHi by 1
        print("score:", info['score'], "levelLo:", info['levelLo'], "xscrollHi:", info['xscrollHi'], "xscrollLo:", info['xscrollLo'], "scrolling:", info['scrolling'])
        # sonic2 - unsigned double byte (16bit); makes it a lot easier to work with
        # print("screen_x_end:", info['screen_x_end'], "x:", info['x'], "y:", info['y'])
        env.render()
        if done:
            obs = env.reset()
    env.close()


if __name__ == "__main__":
    main()
