# openai-gym-retro

## what is this all about?
Training an AI to beat classic video games using Open-AI gym-retro & NEAT

This project touches on so many cool topics; `classic video games`, `roms & emulation`, `AI`, `gamegenie like memory manipulation`, `neuro-networks`, `evolution`, `computer vision`, `python`, `linux on windows.` 

The original [MarI/O](https://www.youtube.com/watch?v=qv6UVOQ0F44) youtube video inspired me to learn about neuro-networks and the ability to apply them in the same way. Thankfully a lot of the heavy lifting has been done already.

I have also seen a few other examples of people using the Gym environment to model real life physics to train [thrust vectoring rockets](https://github.com/EmbersArc/gym_rocketLander) and [rex: domestic robot](https://github.com/nicrusso7/rex-gym/blob/master/README.md).

If you have looked at my [Arcade Machine](https://github.com/andruschak/arcade-machine) build you will know I am a long time gamer. As a kid, I was lucky enough to have owned most of the nintendo/sega consoles at one time or another. So many fond memories of many classic games. 

## hardware
Microsoft Surface Laptop 3 - i7/16GB - Windows 10 Pro 1909 

## software
### Windows Subsystem for Linux 
[WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) allows us to run the linux environment inside Windows. Launch bash and go. I used ubuntu 18.04 as my linux distro. 

[Chocolatey](https://chocolatey.org/) is a package manager for Windows. I use this to install most of my software and [XMING](http://www.straightrunning.com/XmingNotes/) is no different. It is an X Server for Windows. Allows us to render the emulator output. 


### OpenAI Gym Retro
[OpenAI Gym Retro](https://openai.com/blog/gym-retro/) lets you turn classic video games into Gym environments for reinforcement learning and comes with integrations for ~1000 games. It uses various emulators that support the Libretro API.

Each game integration has files listing memory locations for in-game variables, reward functions based on those variables, episode end conditions, savestates at the beginning of levels and a file containing hashes of ROMs that work with these files.

ROMs are not included with gym-retro. The shasum's generally match with those found inside The Internet Archive - NoIntro Rom collection. Just saying.

### NeuroEvolution of Augmenting Topologies (NEAT)
[neat-python](https://github.com/CodeReclaimers/neat-python) is a genetic algorithm for the generation of evolving artificial neural networks. Generally speaking, the algorithm is modelled after natural evolution. We start with an indiviual with no training and throughout generations of evolution and natural selection (breeding those individuals with the highest fitness score) hope to end up with one that can finish the level.  

Summarized from the [NEAT overview](https://neat-python.readthedocs.io/en/latest/neat_overview.html):
To evolve a solution to a problem, provide a fitness function which computes a single real number (increase in x_position for us) indicating the quality of an individual genome: better ability to solve the problem means a higher score. i.e. the further the game character makes it through the level, the higher the fitness score is. The algorithm progresses through a user-specified number of generations (in our case 30), with each generation being produced by reproduction and mutation of the most fit individuals of the previous generation.

The reproduction and mutation operations may add nodes and/or connections to genomes, so as the algorithm proceeds genomes (and the neural networks they produce) may become more and more complex. When the preset number of generations is reached, or when at least one individual (for a fitness criterion function of max; others are configurable) exceeds the user-specified fitness threshold, the algorithm terminates.

### OpenCV
[OpenCV](https://opencv.org/) is an open source computer vision library. It is amazing in it's own right. We will use it to transform each frame of the game into a lower resolution, grayscale image making it easier to process.



## setting up the environment

```
sudo apt-get update
sudo apt install python3-pip
sudo apt install python3-opencv // pip install resulted in core dump

pip3 install gym-retro
pip3 install neat-python
pip3 install opencv-python // did not work

```

## paths

### default path
`~/.local/lib/python3.6/site-packages/retro/data/stable/`

### verify the installation works correctly
`~/.local/lib/python3.6/site-packages/retro/examples/random_agent.py --game SonicTheHedgehog2-Genesis --state EmeraldHillZone.Act1`

## running the simulation

start xming

```
export DISPLAY=:0

```

## reflection on what we've covered

## references
[MarI/O - Machine Learning for Video Games](https://www.youtube.com/watch?v=qv6UVOQ0F44)
