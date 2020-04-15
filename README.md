# openai-gym-retro
Training models to beat classic video games inside Open-AI gym-retro

# what is this all about?
If you have looked at my Arcade Machine build you will know I am a long time gamer. As a kid, I had NES, SNES, Ever since watching the original MarI/O video I have wanted to learn about neuronetworks and the ability to apply them in the same way.

# software
### Windows Subsystem for Linux 
[WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) allows us to run the linux environment inside Windows.

[Chocolatey](https://chocolatey.org/) is a package manager for Windows. Used to install [XMING](http://www.straightrunning.com/XmingNotes/) an X Server for Windows. Allows us to render the emulator output. 


### OpenAI Gym Retro
[OpenAI Gym Retro](https://openai.com/blog/gym-retro/) lets you turn classic video games into Gym environments for reinforcement learning and comes with integrations for ~1000 games. It uses various emulators that support the Libretro API.

Each game integration has files listing memory locations for in-game variables, reward functions based on those variables, episode end conditions, savestates at the beginning of levels and a file containing hashes of ROMs that work with these files.

ROMs are not included with gym-retro. The shasum's generally match with those found inside The Internet Archive - NoIntro Rom collection. Juat saying.

### NeuroEvolution of Augmenting Topologies (NEAT)
[neat-python](https://github.com/CodeReclaimers/neat-python) is a genetic algorithm for the generation of evolving artificial neural networks. Generally speaking, the algorithm is modelled after natural evolution. 

From the [NEAT overview](https://neat-python.readthedocs.io/en/latest/neat_overview.html):
To evolve a solution to a problem, the user must provide a fitness function which computes a single real number indicating the quality of an individual genome: better ability to solve the problem means a higher score. The algorithm progresses through a user-specified number of generations, with each generation being produced by reproduction (either sexual or asexual) and mutation of the most fit individuals of the previous generation.

The reproduction and mutation operations may add nodes and/or connections to genomes, so as the algorithm proceeds genomes (and the neural networks they produce) may become more and more complex. When the preset number of generations is reached, or when at least one individual (for a fitness criterion function of max; others are configurable) exceeds the user-specified fitness threshold, the algorithm terminates.

### OpenCV
[OpenCV](https://opencv.org/) is an open source computer vision library. It is amazing in it's own right. We will use it to transform each frame of the game into a lower resolution, grayscale image making it easier to process.



# setup the environment
We will be using python3

...
sudo apt-get update
sudo apt install python3-pip
sudo apt install python3-opencv // pip install resulted in core dump

pip3 install gym-retro
pip3 install neat-python
pip3 install opencv-python // did not work

...

# paths

### default path
~/.local/lib/python3.6/site-packages/retro/data/stable/

### verify the installation works correctly
~/.local/lib/python3.6/site-packages/retro/examples/random_agent.py --game SonicTheHedgehog2-Genesis --state EmeraldHillZone.Act1

# running the simulation

start xming

...
export DISPLAY=:0

...

# references
[MarI/O - Machine Learning for Video Games](https://www.youtube.com/watch?v=qv6UVOQ0F44)
