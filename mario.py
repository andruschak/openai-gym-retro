import retro
import neat
import numpy as np
import cv2
import pickle

# load game, level (check dir for states), record each run
env = retro.make("SuperMarioBros-Nes", "Level1-1", record='bk2/')

imgarray = []

def eval_genomes(genomes, config):

    for genome_id, genome in genomes:
        
        # reset environment for each
        observ = env.reset()

        # load the default action sample - random action/button press
        action = env.action_space.sample()

        inx, iny, inc = env.observation_space.shape

        inx = int(inx/8)
        iny = int(iny/8)
        
        # create the RNN
        network = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        
        # tracking variables      
        current_max_fitness = 0
        fitness_current = 0
        frame = 0
        counter = 0
        done = False
       
        # see data.json in the game dir
        # do we care about time or lives?
        xscrollLo = 0
        xscrollLo_prev = 0
        xscrollHi = 0
        xscrollHi_prev = 0
        coins = 0
        coins_max = 0
        score = 0
        score_max = 0
        lives = 2
        time = 0
        scrolling = 0
        status = ""

        
        while not done:

            # render the environment on screen. comment out to speed up
            env.render()
            
            frame += 1
            
            # convert into grayscale
            observ = cv2.resize(observ, (inx, iny))
            observ = cv2.cvtColor(observ, cv2.COLOR_BGR2GRAY)
            observ = np.reshape(observ, (inx,iny))

            imgarray = np.ndarray.flatten(observ)

            nnOutput = network.activate(imgarray)
            
            # env.step takes the output of the neural network and returns 4 parameters
            # observ - object representing your observation of the environment
            # reward - a floating point number of the reward from the previous action
            # done - boolean value indicating whether or not to reset the environment
            # info - a dictionary containing data from the game variables defined in data.json (ex: info[coins])
            observ, reward, done, info = env.step(nnOutput)
            
            # extract x distance's traveled
            # note - because we are limited to 8bit, there are 2 counters for distance traveled 
            # xscrollHi increases by 1 every 255 xscrollLo x distance traveled
            xscrollLo = info['xscrollLo']
            xscrollHi = info['xscrollHi']

            # extract variables for bonus fitness
            coins = info['coins']
            score = info['score']

            # other variables
            lives = info['lives']
            time = info['time']
            scrolling = info['scrolling']
                        
            # run various checks for bonus fitness
            # if mario gets a coin add to fitness
            if coins > coins_max:
                fitness_current += 100
                coins_max = coins

            # if mario's score increases add to fitness 
            if score > score_max:
                fitness_current += 100
                score_max = score
                
            # need custom variable to check for powerup

            # if xscrollHi increases add to fitness
            # if xscrollHi = x? then mario completed the mission
            # buggy because lo wraps
            if xscrollLo > xscrollLo_prev:
                # bonus for each wrap on xLo increasing xHi
                if xscrollHi > xscrollHi_prev:
                    fitness_current += 1000
                    xscrollHi_prev = xscrollHi
                fitness_current += 10
                xscrollLo_prev = xscrollLo
                counter = 0
            else:
                counter += 1
                fitness_current -= 0.1
 
            # check for stalls, 
            # 1000 is approx ~49s game time, 800 is ~
            if counter == 800:
                status = "stalled"
                done = True  

            # check lives, if less than 2 mario died, set done to True
            if lives < 2:
                status = "dead"
                done = True  
            
            # done tripped, exit
            if done == True:
                print("Genome:", genome_id,", Fitness Achieved:", fitness_current,", xLo:", xscrollLo,", xHi:", xscrollHi,", time:", time,", score:", score,", coins:", coins,", status:", status)
                
            # total genome fitness for this round
            genome.fitness = fitness_current
                

# load the variables from config-neat.cfg
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, 'config-neat-mario.cfg')
# create pop based on loaded configuration file
pop = neat.Population(config)

# StdOutReporter(show_species_detail (bool)) – show additional details about each species in the population
pop.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
pop.add_reporter(stats)
# uncomment to create a checkpoint every x generations
# pop.add_reporter(neat.Checkpointer(5))

# if you've already done some training
# pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-5')

# kick off the process
winner = pop.run(eval_genomes)

# write winner to winner.pkl file
with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)