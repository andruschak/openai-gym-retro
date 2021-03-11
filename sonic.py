import retro
import neat
import numpy as np
import cv2
import pickle

# load game, level (check dir for states), record each run
env = retro.make("SonicTheHedgehog2-Genesis", "EmeraldHillZone.Act1", record='sonic-bk2/')

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
        x = 0
        x_prev = 0
        y = 0
        y_prev = 0
        lives = 0
        rings = 0
        score = 0
        screen_x = 0
        screen_x_prev = 0
        screen_y = 0
        screen_x_end = 0
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
            # use screen_x and screen_y, x and y did not produce the outputs I expected
            x = info['x']
            y = info['y']
            screen_x = info['screen_x']
            screen_y = info['screen_y']
            screen_x_end = info['screen_x_end']

            # extract variables for bonus fitness
            rings = info['rings']
            score = info['score']

            # other variables
            lives = info['lives']

            # run various checks for bonus fitness
            # if sonic collects a ring add to fitness
            #if rings > rings_max:
            #    fitness_current += 1000
            #    rings_max = rings
            
            # loses rings?
            # gain slowly, loose all instantly, do we need to penalize here? 
            # what about end turn on ring loss?

            # if sonics's score increases add to fitness 
            #if score > score_max:
            #    fitness_current += 250
            #    score_max = score
                
            # need custom variable to check for powerup?

            # check sonics forward progress
            if screen_x > screen_x_prev:
                fitness_current += 10
                current_max_fitness = fitness_current
                screen_x_prev = screen_x
                counter = 0
            else:
                counter += 1
                #fitness_current -= 0.1

            # restart if stalled for too long    
            if counter == 500:
                status = "stalled"
                done = True


            # level end has been reached. 10656 is the output of screen_x_end
            if screen_x > 10655:
                fitness_current += 100000
                done = True


            # check lives, if less than3 sonic died. will break if sonic recieves a free life
            if lives < 3:
                status = "died"
                done = True  
            
            # done tripped, exit
            if done == True:
                print("Genome:", genome_id,", Fitness Achieved:", fitness_current,", x:", x,", y:", y,", screen_x:", screen_x,", screen_y:", screen_y,", screen_x_prev:", screen_x_prev," score:", score,", rings:", rings,", status:", status)
            #    print("Genome:", genome_id,", Fitness Achieved:", fitness_current," score:", score,", rings:", rings,", status:", status)
                
            # total genome fitness for this round
            genome.fitness = fitness_current
                

# load the variables from config-neat.cfg
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, 'config-neat-sonic.cfg')
# create pop based on loaded configuration file
pop = neat.Population(config)

# StdOutReporter(show_species_detail (bool)) – show additional details about each species in the population
pop.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
pop.add_reporter(stats)
# uncomment to create a checkpoint every x generations
#pop.add_reporter(neat.Checkpointer(5))

# if you've already done some training
# pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-5')

# kick off the process
winner = pop.run(eval_genomes)

# write winner to winner.pkl file
with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)