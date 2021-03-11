# Openai-gym-retro
Heavy work in progress - a semi organized brain dump

# Table of contents

# Part 1. What is this all about
Leveraging machine learning, specifically reinforcement learning, to train a bot to play classic emulated video games using Open-AI gym-retro. At the end of the day, I would like to understand how to make it play a couple different genre's - platformers (Mario and Sonic) and fighting games (Street Figher II).

Much of the heavy lifting is done for us by utilizing open source libraries and tutorials that can be found online (reference list at the bottom of the page). While I mainly build on what those have done before me, I add my own original contributions. 

This tutorial is for educational purposes only.

## Inspiration
There are several reasons I am interested in this project:

- To keep learning and continue programming (use it or lose it).

- The original [marI/O](https://www.youtube.com/watch?v=qv6UVOQ0F44) youtube video inspired me to learn about neuro-networks and the ability to apply them in the same way. 

- Since the release of open-ai's framework, I have also seen other examples of people using gym environments to model real life physics in order to train: 
  * [thrust vectoring rockets](https://github.com/EmbersArc/gym_rocketLander)
  * [rex the domestic robot](https://github.com/nicrusso7/rex-gym/blob/master/README.md).

- Take a look at my [arcade machine](https://github.com/andruschak/arcade-machine) build you will know I am a long time gamer. As a kid, I was lucky enough to have owned most of the nintendo/sega consoles at one time or another. 

- Finally, this project touches on so many cool topics; `classic video games`, `emulation`, `machine learning`, `gamegenie like memory manipulation`, `neuro-networks`, `evolution`, `biology`, `genome`, `computer vision`, `python3`, `linux on windows.` 

***

# Part 2. Definitions

### Reinforcement Learning (RL)
From wikipedia: "Reinforcement learning is an area of machine learning concerned with how software agents ought to take actions in an environment in order to maximize some notion of cumulative reward. Reinforcement learning is one of three basic machine learning paradigms, alongside supervised learning and unsupervised learning." 

### Recurrent Neural Network (RNN)
A recurrent neural network is a class of artificial neural networks where connections between nodes form a directed graph along a temporal sequence. This allows it to exhibit temporal dynamic behavior. Derived from feedforward neural networks, RNNs can use their internal state to process variable length sequences of inputs.

### Proximal Policy Optimization (PPO)
Useful in games with with frequent and incremental rewards where most of the difficulty comes from needed fast reaction times.

### Actor&Critic (A&C)
To do - for Fighting Games

### Biology Terms
To do
  - species 
  - genome 
  - evolution
  - homology
  - 


***

# Part 3. Environment

## Hardware
Microsoft Surface Laptop 3 - i7/16GB - Windows 10 Pro 1909 

## Software
* [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) allows us to run the linux environment inside Windows. This changed from v1 (ubuntu 18.04) to v2 during this project. It used to be launch bash and go. Now it is run as a container. I used ubuntu 20.04 as my linux distro for v2. 

* [chocolatey](https://chocolatey.org/) is a package manager for Windows. I use this to install most of my software and [XMING](http://www.straightrunning.com/XmingNotes/) is no different. It is an X Server for Windows. Allows us to render the emulator output. 

* [windows terminal](https://aka.ms/PowerShell-Release?tag=v7.1.1) improved windows terminal. Easiest way to interact with the powershell and the ubuntu container
 
* [python](www.python.org) the language we will be programming in. With WSL2 we are using python 3.8. On WSL1 it was 3.6.9.

## Libraries
### OpenAI Gym Retro
[OpenAI Gym Retro](https://openai.com/blog/gym-retro/) enables an interface between python and emulated video games. It sets up an environment for reinforcement learning and comes with integrations for ~1000 games. It uses various emulators that support the Libretro API.

Each game integration has files listing memory locations for in-game variables, reward functions based on those variables, episode end conditions, savestates at the beginning of levels and a file containing hashes of ROMs that work with these files.

ROMs are not included with gym-retro. The shasum's ~~generally~~ rarely match with those found inside The Internet Archive - NoIntro Rom collection. However, after you import, you can modify the rom.sha file to match the shasum of the file you imported (it will have been renamed to rom.nes).  

I highly encourage anyone reading this to check out the [Getting Started Guide](https://retro.readthedocs.io/en/latest/getting_started.html). It goes through this whole process in a lot more detail. 

Path `~/ai/env/lib/python3.8/site-packages/retro/data/stable/<games>`

### NeuroEvolution of Augmenting Topologies (NEAT)
[neat-python](https://github.com/CodeReclaimers/neat-python) is a genetic algorithm for the generation of evolving artificial neural networks. We can think of this as a system being modelled after natural evolution. 

Summarized from the [NEAT overview](https://neat-python.readthedocs.io/en/latest/neat_overview.html):
To evolve a solution to a problem, provide a fitness function which computes a single real number (increase in x_position for us) indicating the quality of an individual genome; i.e. the further the game character makes it through the level, the higher the fitness score is. The algorithm progresses through a user-specified number of generations (in our case ~30), with each generation being produced by reproduction and mutation of the most fit individuals of the previous generation.

These reproduction and mutation operations may add nodes and/or connections to genomes, so as the algorithm proceeds genomes (and the neural networks they produce) may become more and more complex. When the preset number of generations is reached, or when at least one individual (for a fitness criterion function of max; others are configurable) exceeds the user-specified fitness threshold, the algorithm terminates.

### OpenCV
[OpenCV](https://opencv.org/) is an open source computer vision library. It is amazing in it's own right. I have played with opencv a few times over the years - here are a few examples:
* [skeletal detection - Kinect/SDK](https://www.youtube.com/watch?v=bBsXQb-j9vk)
* [facial recognition](https://www.youtube.com/watch?v=onjW4iA1Ai4) 

In this case we will use it to transform each frame of the game into a lower resolution, grayscale image making it easier to process. 

## Windows Subsystem for Linux

Since my original work on this project, WSL went from v1 to v2. Instead of being "integrated" into the OS it now runs as a container. This completely changes several key components, such as networking. Because of this, we need to change how we interact with x-windows.  

### Windows Subsystem for Linux - WSL2

## Setting up the environment

windows
```
choco install vcxsrv
```

ubuntu wsl container
```
sudo hwclock --hctosys                # correct apt update error: “Release file is not yet valid”
sudo apt update && sudo apt upgrade
sudo apt install python3-venv
sudo apt install python3-pip
mkdir ~/ai
python3 -m venv ai                    # create a virtual environment
cd ~/ai
source env/bin/activate               # enter virtual env, the pip packages will only be installed here
pip3 install "pyglet<1.5"             # was required to be <1.5 for retro to install
pip3 install gym-retro
pip3 install neat-python
pip3 install opencv-python
```

### Windows Firewall
We need to add a rule or disable (bad idea) the Public Firewall for vcXsrv to recieve connections from the container. This is a big change from WSL1. 

### Running the simulation
Lets run a demo to see if everything is working. We will try and load an example agent (random button presses) to play Super Mario Bros Level 1-1. Since we are running this in windows we need to start our x-server app and export the linux DISPLAY.

windows
```
start vcxsrv with the following settings
<insert picture here>
```

ubuntu wsl container
```
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
python3 /examples/random_agent.py --game SuperMarioBros-Nes --state Level1-1

```

## Success!
It's a me, mario!

![random mariobros](https://github.com/andruschak/openai-gym-retro/raw/master/images/mario-random.gif "random mariobros")

***



# Part 4. Basic outline and concepts
Now that we have successfully installed and tested our environment, lets get some basic concepts down and then move onto code. For starters we will be using already included integrations. Later on, I would like to look at expanding on this section. Tweaking the reward function to incentivize the computer to take into account coin or rings for example.

## Concept
The premise here is simple. Mario will play over and over learning things as he goes. That knowledge will be passed down to future generations in the hopes they make better decisions and in turn make it further through the level.

To achieve that, we are going to:

1. create the environment (openai retro - integration/data.json/scenario.json)
2. step through the environment for each genome (opencv, neat - config and stats)
3. apply logic (neat)
  - reward for increased x distance (heading to the end of the level)
  - optional: add reward for increased score, coins, etc. Should make for a "better" run through
4. once reward has been reached, terminate

## Integrations
Setting up the environment for reinforcement learning. It enables the game be ran through via a python api. There are 3 conditions we need: start (location to begin), reward (fitness - keep going buddy!), and done (when to terminiate). For far more detail, check out the official [Game Integration Guide](https://retro.readthedocs.io/en/latest/integration.html).

### data.json
data.json contains references to memory locations for specific game attributes. As you can see by the SuperMarioBros-Nes example. These have been mapped out using retro integration tool. For more information on the variable types, check out this [Guide](https://retro.readthedocs.io/en/latest/integration.html#appendix-types)

By utilizing the various attributes in info[] I hope to make the bot more effective. For example, we can increase the fitness score when coins/rings are collected or slightly decrease the score when moving in the wrong direction. 

```
{
  "info": {
    "coins": {
      "address": 1886,
      "type": "|u1"
    },
    "levelHi": {
      "address": 1887,
      "type": "|i1"
    },
    "levelLo": {
      "address": 1884,
      "type": "|i1"
    },
    "lives": {
      "address": 1882,
      "type": "|i1"
    },
    "score": {
      "address": 2013,
      "type": ">n6"
    },
    "scrolling": {
      "address": 1912,
      "type": "|i1"
    },
    "time": {
      "address": 2040,
      "type": ">n3"
    },
    "xscrollHi": {
      "address": 1818,
      "type": "|u1"
    },
    "xscrollLo": {
      "address": 1820,
      "type": "|u1"
    }
  }
}
```

### scenario.json
The scenario.json file contains the done and reward game conditions based on the variables from data.json.

```
{
  "done": {
    "variables": {
      "lives": {
        "op": "equal",
        "reference": -1
      }
    }
  },
  "reward": {
    "variables": {
      "xscrollLo": {
        "reward": 1
      }
    }
  }
}
```

### Basic code outline
Basic code to load the game, create and render the environment. 


```
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

    total_reward = 0

    while True:
        # env.step returns 4 parameters
        # observ - object representing your observation of the environment
        # reward - a floating point number of the reward from the previous action
        # done - boolean value indicating whether or not to reset the environment
        # info - a dictionary containing data from the game variables defined in data.json (ex: info[coins])
        # action = env.action_space.sample() - do a random action
        # print(env.action_space.sample())
        observ, reward, done, info = env.step(env.action_space.sample())

        # add up the total rewards gained
        total_reward += reward
        
        # mario - unsigned single byte (8bit); xscrollLo wraps at 255 and increases xscrollHi by 1
        print("Reward: ", reward, "Total Reward: ", total_reward, "score:", info['score'], "levelLo:", info['levelLo'], "xscrollHi:", info['xscrollHi'], "xscrollLo:", info['xscrollLo'], "scrolling:", info['scrolling'])
        # sonic2 - unsigned double byte (16bit); makes it a lot easier to work with
        # print("Reward: ", reward, "Total Reward: ", total_reward, "screen_x_end:", info['screen_x_end'], "x:", info['x'], "y:", info['y'])
        
        # render the game. not displaying the screen will speed things up
        env.render()

        
        if done:
            obs = env.reset()
    env.close()

if __name__ == "__main__":
    main()

```


## Other tips & tricks
Here are a few tidbits I found from googling various topics and digging through the documentation.

### Replaying
If the record variable is set, we will save a zipped bk2 playback file for each environment rendered. You can replay this recording using the included watch.py 

`python3 watch.py --vid SuperMarioBros-Nes-Level1-1-000000.bk2`

### retro/examples
[interactive mode](https://github.com/openai/retro/blob/master/retro/examples/retro_interactive.py) will let you play the game using your keyboard. I havent tested.

[discreditizer](https://github.com/openai/retro/blob/master/retro/examples/discretizer.py) will let you can define your own set of button presses. I havent tested.

### console.json
You can look at the keybindings for the various emulators. The controller layouts are presented as a list of actions. Documentation is very light. Not sure exactly how this is mapped.

for ex: [0,0,1,0,0,0,0,1,1,1,0,0]

nes.json for example:
```
{
    "Nes": {
        "lib": "fceumm",
        "ext": ["nes"],
        "keybinds": ["Z", null, "TAB", "ENTER", "UP", "DOWN", "LEFT", "RIGHT", "X"],
        "buttons": ["B", null, "SELECT", "START", "UP", "DOWN", "LEFT", "RIGHT", "A"],
        "actions": [
            [[], ["UP"], ["DOWN"]],
            [[], ["LEFT"], ["RIGHT"]],
            [[], ["A"], ["B"], ["A", "B"]]
        ]
    }
}
```

Sample Input_keys.txt file extracted from one of the bk2 playbacks.

```

```


***

# Part 5. Adding machine learning into the mix

Now that we have our environment working as expected, its time to add in the machine learning component. 

### NEAT config 
The NEAT configuration file defines the evolutionary process for our bot. It uses old windows INI file style which is very easy to follow. I have tried to format and comment the file to make it easier to understand. You can read about it in much more detail on the official [NEAT config](https://neat-python.readthedocs.io/en/latest/config_file.html) file documentation.



```
# NEAT configuration file

[NEAT]
# fitness_criterion:    the function used to compute the termination criterion from the set of genome fitnesses (max, min, mean)
# fitness_threshold:	  in our case, when fitness_current meets this threshold the evolution process will terminate
#                       we can work inside this threshold with our game counters
# pop_size:             the amount of individuals genomes in each generation
# reset_on_extinction:  when all species become extinct; true: a new random one will appear, false: exception thrown
fitness_criterion     = max
fitness_threshold     = 100000
pop_size              = 30
reset_on_extinction   = True

[DefaultStagnation]
# species_fitness_func: the function used to compute species fitness (max, min, mean, median)
# max_stagnation:       species with no improvement in > number of generations are stagnant and removed (def: 15)
# species_elitism:      number of species that will be protected from stagnation; prevents extinction events (def: 2)
species_fitness_func = max
max_stagnation       = 50
species_elitism      = 2

[DefaultReproduction]
# elitism:              the number of most-fit individuals who will be preserved from one generation to the next (def: 0)
# survival_threshold:   the fraction for each species allowed to reproduce each generation (def: 0.2)
# min_species_size:     minimum number of genomes per species after reproduction (def: 2)     
elitism            = 2
survival_threshold = 0.3
min_species_size   = 2

[DefaultSpeciesSet]
# compatibility_threshold:  
compatibility_threshold = 2.5

[DefaultGenome]
# add more information
# node activation options
activation_default      = sigmoid
activation_mutate_rate  = 0.05
activation_options      = sigmoid gauss 
#abs clamped cube exp gauss hat identity inv log relu sigmoid sin softplus square tanh

# node aggregation options
aggregation_default     = random
aggregation_mutate_rate = 0.05
aggregation_options     = sum product min max mean median maxabs

# node bias options
bias_init_mean          = 0.05
bias_init_stdev         = 1.0
bias_max_value          = 30.0
bias_min_value          = -30.0
bias_mutate_power       = 0.5
bias_mutate_rate        = 0.7
bias_replace_rate       = 0.1

# genome compatibility options
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5

# connection add/remove rates
conn_add_prob           = 0.5
conn_delete_prob        = 0.1

# connection enable options
enabled_default         = True
enabled_mutate_rate     = 0.2

# feed_forward
feed_forward            = False
#initial_connection     = unconnected
initial_connection      = partial_nodirect 0.5

# node add/remove rates
node_add_prob           = 0.5
node_delete_prob        = 0.5

# network parameters
# need to be tweaked depending on the system being emulated
# num_inputs from the controller
# NES:          840
# SNES:         896
# Genesis       1120
num_hidden              = 0
num_inputs              = 1120
num_outputs             = 12

# node response options
response_init_mean      = 1.0
response_init_stdev     = 0.05
response_max_value      = 30.0
response_min_value      = -30.0
response_mutate_power   = 0.1
response_mutate_rate    = 0.75
response_replace_rate   = 0.1

# connection weight options
weight_init_mean        = 0.1
weight_init_stdev       = 1.0
weight_max_value        = 30
weight_min_value        = -30
weight_mutate_power     = 0.5
weight_mutate_rate      = 0.8
weight_replace_rate     = 0.1

```

### NEAT configuration

```
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, 'neat-config.cfg')
pop = neat.Population(config)
```

### Statistics and saving 
NEAT has a bunch of statistics we can report on. We also have the ability to save training checkpoints.

```
# StdOutReporter(show_species_detail (bool)) – show additional details about each species in the population
pop.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
pop.add_reporter(stats)
# uncomment to create a checkpoint every x generations
# pop.add_reporter(neat.Checkpointer(5))

# if you've already done some training
# pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-5')
```

example output:
```
Population's average fitness: 90.43333 stdev: 100.55535
Best fitness: 322.00000 - size: (12, 4297) - species 3 - id 83
Average adjusted fitness: 0.284
Mean genetic distance 2.236, standard deviation 0.575
Population of 30 members in 4 species:
   ID   age  size  fitness  adj fit  stag
  ====  ===  ====  =======  =======  ====
     1    2     2    186.0    0.116     2
     2    2     5    202.0    0.282     0
     3    2    14    322.0    0.313     0
     4    1     9    202.0    0.425     0
Total extinctions: 0
Generation time: 199.665 sec (165.241 average)
```

***

# Part 5. Platformers

Going to start here as these seem to be the easiest models to train.

## Super Mario Bros (NES)

Brainstorming
- only care about moving forward to the end. determined by increasing x distance
- add fitness bonus for reaching specific x distance?
- add fitness for each coin collected
- add fitness for an increase in score; collecting coins/power ups, killing mobs, other ways to increase? 
- add fitness when mario get a power up; mushroom, fireflower, star? like wise decrease fitness when lost
- decrease fitness for going the wrong way
- end turn if no movement for x frames
- others?

Notes
- 8bit architecture, limiting memory to 1byte chunks
- xscrollHi increases by 1 every 255 xscrollLo x distance travelled
- there appears to be a no reward zone at the start of the level

### Training runs

Simulation #1:
May 2020 - Results = Failure :: Mario never made it past this point in my initial training. After over 300 runs, all species stagnated and that triggered a mass extinction event. All training was lost. I modified the config-neat.cfg file afterwards to preserve at least 1 species (species_elitism)

![mario bane](https://github.com/andruschak/openai-gym-retro/raw/master/images/bane-of-marios-existence2.gif "mario bane")

Simulation #2
March 2021 - Results = Terminated :: I terminated the session after 777 generations and 3357 minutes (~55h). The last 25h mario moved one square. This run included additional points for score and coins. This perhaps complicated the learning by including additional variables? They always seem to get stuck at the same point. Further learning seems to dindle over time. Could be the neat-config variables?

![Time vs Generation](https://github.com/andruschak/openai-gym-retro/raw/master/images/timevsgeneration.png "Time vs Generation")
The time it took to run 30 genomes in each generation.
  - Interesting to see the rise at the start, dramatic fall and then average out. I would have thought that they time would increase as each generations genomes progressed further. But many runs where almost identical. Seems like not enough diversity or breeding?

![Fitness vs Generation](https://github.com/andruschak/openai-gym-retro/raw/master/images/fitnessvsgeneration.png "Fitness vs Generation")

How fitness grew over time
  - The jumps in the graph are the bonus fitness for increased score, collecting a coin or incrementing xscrollHi



***

## Sonic the Hedgehog 2 (Genesis)

Brainstorming
- possible to get stuck in a rocking motion - as seen in the gif
- backtracking might be a better strategy in some cases?
- rings can be gotten and lost. what about loss?
- add fitness for increased score?
- add fitness for collecting power ups. some wear off, some dont
- if sonic loses a life terminate? deduct fitness?
- what is the gamemode variable?

Notes
- 16bit architecture, memory is 2byte chunks, counters are easier to work with
- The screen_x variable provided to track sonics position. x didn't seem accurate from my testing
- The screen_x_end variable is the spinning signpost at the end (our target x distance)
- Sonic will rock in place depending on the obstacle in front of him. If no increase in x distance in y frames terminate

### Training runs

Simulation #1:
May 2020 - Results = Failure :: As with mario, sonic never completed his initial run. There was a bug in my original counter that did not take into account rocking for an extended period of distance within a given amount of time. This triggered the DONE event, however, sonic never completed the course.

![sonic bane](https://github.com/andruschak/openai-gym-retro/raw/master/images/bane-of-sonics-existence2.gif "sonic bane")

Simulation #2:
March 8 2021 - Results = Success! :: Sonic completed the run
   - Finished in 25 generations, 776s or ~5.38h
   - 2 genomes completed the level in the final generation
     - Genome: 665 , Fitness Achieved: 122320 , x: 10819 , screen_x: 10656 , screen_x_prev: 10656  score: 10 , rings: 6 , status:
     - Genome: 668 , Fitness Achieved: 122150 , x: 10817 , screen_x: 10656 , screen_x_prev: 10656  score: 20 , rings: 64 , status:


[![Sonic Bot](https://img.youtube.com/vi/wbVGff3ZeM/0.jpg)](https://www.youtube.com/watch?v=wbVGff3ZeM)


***

# Part 6. Fighting Games - Street Fighter II (SNES)

***

# Part 7. Reflection on what we've covered

### Challenges
Successfully playing games isnt always easy. Platformer games like Mario and Sonic can achieve success simply by increasing your x-coordinates until you reach a target. But what about games that require the player to solve unique puzzles or back track after finding a key later on?


***

### References

1. [MarI/O - Machine Learning for Video Games](https://www.youtube.com/watch?v=qv6UVOQ0F44)

2. [Lucasthompsons youtube tutorials](https://www.youtube.com/playlist?list=PLTWFMbPFsvz3CeozHfeuJIXWAJMkPtAdS)

3. [Lucasthompsons gitlab repo](https://gitlab.com/lucasrthompson/Sonic-Bot-In-OpenAI-and-NEAT)

4. [Gym Retro Documentation](https://retro.readthedocs.io/en/latest/getting_started.html)

5. [NEAT Documentation](https://neat-python.readthedocs.io/en/latest/)
