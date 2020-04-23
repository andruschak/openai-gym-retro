# openai-gym-retro

# 1. what is this all about
Leveraging machine learning, specifically reinforcement learning, to train the computer to play classic emulated video games using Open-AI gym-retro. At the end of the day, I would like to understand how to make it play a couple different genre's - platformers (Mario and Sonic) and fighting games (Street Figher II).

## inspiration
There are several reasons I am interested in this project:

The original [marI/O](https://www.youtube.com/watch?v=qv6UVOQ0F44) youtube video inspired me to learn about neuro-networks and the ability to apply them in the same way. Much of the heavy lifting is done for us by utilizing open source libraries and tutorials that can be found online (reference list at the bottom of the page). While I mainly build on what those have done before me, I try and add my own original contributions in the form of tweaks to environment configs and rewards as well as comparisons of different approaches.

Since the release of open-ai's framework, I have also seen other examples of people using gym environments to model real life physics in order to train [thrust vectoring rockets](https://github.com/EmbersArc/gym_rocketLander) and [rex the domestic robot](https://github.com/nicrusso7/rex-gym/blob/master/README.md).

If you have looked at my [arcade machine](https://github.com/andruschak/arcade-machine) build you will know I am a long time gamer. As a kid, I was lucky enough to have owned most of the nintendo/sega consoles at one time or another. 

To keep learning and programming. Expand

Finally, this project touches on so many cool topics; `classic video games`, `emulation`, `machine learning`, `gamegenie like memory manipulation`, `neuro-networks`, `evolution`, `computer vision`, `python3`, `linux on windows.` 

***

# 2. definitions 

### reinforcement learning (RL)
From wikipedia: "Reinforcement learning is an area of machine learning concerned with how software agents ought to take actions in an environment in order to maximize some notion of cumulative reward. Reinforcement learning is one of three basic machine learning paradigms, alongside supervised learning and unsupervised learning."

### NEAT
### Recurrent Neural Network (RNN)
A recurrent neural network is a class of artificial neural networks where connections between nodes form a directed graph along a temporal sequence. This allows it to exhibit temporal dynamic behavior. Derived from feedforward neural networks, RNNs can use their internal state to process variable length sequences of inputs.

### Proximal Policy Optimization (PPO)
Useful in games with with frequent and incremental rewards where most of the difficulty comes from needed fast reaction times.

### Actor&Critic (A&C)

***

# 3. environment

## hardware
Microsoft Surface Laptop 3 - i7/16GB - Windows 10 Pro 1909 

## software
### Windows Subsystem for Linux 
[WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) allows us to run the linux environment inside Windows. Launch bash and go. I used ubuntu 18.04 as my linux distro. 

[chocolatey](https://chocolatey.org/) is a package manager for Windows. I use this to install most of my software and [XMING](http://www.straightrunning.com/XmingNotes/) is no different. It is an X Server for Windows. Allows us to render the emulator output. 

### python 3.6.9
[python](www.python.org) the language we will be programming in. This came included in the wsl ubuntu environment we installed

### OpenAI Gym Retro
[OpenAI Gym Retro](https://openai.com/blog/gym-retro/) enables an interface between python and emulated video games. It sets up an environment for reinforcement learning and comes with integrations for ~1000 games. It uses various emulators that support the Libretro API.

Each game integration has files listing memory locations for in-game variables, reward functions based on those variables, episode end conditions, savestates at the beginning of levels and a file containing hashes of ROMs that work with these files.

ROMs are not included with gym-retro. The shasum's ~~generally~~ rarely match with those found inside The Internet Archive - NoIntro Rom collection. However, after you import, you can modify the rom.sha file to match the shasum of the file you imported (it will have been renamed to rom.nes).  

### NeuroEvolution of Augmenting Topologies (NEAT)
[neat-python](https://github.com/CodeReclaimers/neat-python) is a genetic algorithm for the generation of evolving artificial neural networks. We can think of this as as a system being modelled after natural evolution. 

Summarized from the [NEAT overview](https://neat-python.readthedocs.io/en/latest/neat_overview.html):
To evolve a solution to a problem, provide a fitness function which computes a single real number (increase in x_position for us) indicating the quality of an individual genome: better ability to solve the problem means a higher score. i.e. the further the game character makes it through the level, the higher the fitness score is. The algorithm progresses through a user-specified number of generations (in our case ~30), with each generation being produced by reproduction and mutation of the most fit individuals of the previous generation.

The reproduction and mutation operations may add nodes and/or connections to genomes, so as the algorithm proceeds genomes (and the neural networks they produce) may become more and more complex. When the preset number of generations is reached, or when at least one individual (for a fitness criterion function of max; others are configurable) exceeds the user-specified fitness threshold, the algorithm terminates.

### OpenCV
[OpenCV](https://opencv.org/) is an open source computer vision library. It is amazing in it's own right. I have played with opencv a few times over the years - [skeletal detection - Kinect/SDK](https://www.youtube.com/watch?v=bBsXQb-j9vk) and [facial recognition](https://www.youtube.com/watch?v=onjW4iA1Ai4) 

In this case we will use it to transform each frame of the game into a lower resolution, grayscale image making it easier to process. 

***

## setting up the environment

windows
```
choco install xming
```

ubuntu wsl (windows subsystem for linux)
```
sudo apt-get update
sudo apt install python3-pip
sudo apt install python3-opencv // pip install resulted in core dump

pip3 install gym-retro
pip3 install neat-python
pip3 install opencv-python // did not work, resulted in segfaults
```

### default paths for retro
`/.local/lib/python3.6/site-packages/retro`

### import roms
`/retro/scripts/python3 import_path.py /path/to/rom/file/nes/`


### running the simulation
Lets run a demo to see if everything is working. We will try and load an example agent (random button presses) to play Super Mario Bros Level 1-1. Since we are running this in windows we need to start our x-server app and export the linux DISPLAY.

windows
```
start xming
```

ubuntu wsl
```
export DISPLAY=:0.0
python3 /examples/random_agent.py --game SuperMarioBros-Nes --state Level1-1

```

## success!
it's a me, mario!

![random mariobros](https://github.com/andruschak/openai-gym-retro/raw/master/images/mario-random.gif "random mariobros")

***

# 4. basic outline and concepts
Now that we have successfully installed our environment, lets get some basic concepts down and then move onto code.

## getting started
I highly suggest checking out the [Getting Started](https://retro.readthedocs.io/en/latest/getting_started.html) guide for retro.

## integrations

### data.json

### scenario.json

### basic code outline - example/random_agent.py 


```
import retro

def main():
    env = retro.make(game='SuperMarioBros-Nes')
    obs = env.reset()
    while True:
        obs, rew, done, info = env.step(env.action_space.sample())
        env.render()
        if done:
            obs = env.reset()
    env.close()


if __name__ == "__main__":
    main()

```

### pickling 

### saving

### replaying

***

# 5. Platformers - Super Mario Bros (NES) & Sonic the Hedgehog 2 (Genesis)

### feed-forward

***

# 6. Fighting Games - Street Fighter II (SNES)

***

# X. reflection on what we've covered

### challenges
Successfully playing games isnt always easy. Platformer games like Mario and Sonic can achieve success simply by increasing your x-coordinates until you reach a target. But what about games that require the player to solve unique puzzles or back track after finding a key later on?


***

### references
[MarI/O - Machine Learning for Video Games](https://www.youtube.com/watch?v=qv6UVOQ0F44)

[Wikipedia](www.wikipedia.org)