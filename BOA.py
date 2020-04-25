import random
import numpy as np 

W = 0.5
c1 = 0.8
c2 = 0.9 

a = random.random()
c = random.random()
p = 0.7

bestFrag = 0

n_iterations = 200
target_error = 0.001
n_particles = 100

class Particle():
    def __init__(self):
        self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([0,0])
        self.fitnessVal = float('inf')
        self.fragrance = float('inf')


    def __str__(self):
        print("Position: ", self.position, " pbest is ", self.pbest_position)
    
    def move(self):
        self.position = self.position + self.velocity
        

class Space():

    def __init__(self, target, target_error, n_particles):
        self.target = target
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gbest_frag = float('inf')
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.random()*50, random.random()*50])


    def print_particles(self):
        for particle in self.particles:
            particle.__str__()
   
    def fitness(self, particle):
        #return particle.position[0] ** 2 + particle.position[1] ** 2 + 1
        return (1.5 - particle.position[0] + particle.position[0] * particle.position[1]) * (1.5 - particle.position[0] + particle.position[0]* particle.position[1]) \
        +(2.25 - particle.position[0] + particle.position[0] * particle.position[1] * particle.position[1]) * (2.25 - particle.position[0] \
        + particle.position[0] * particle.position[1] * particle.position[1]) +(2.625 - particle.position[0] + particle.position[0] * particle.position[1] * particle.position[1] * particle.position[1]) * (2.625 - particle.position[0] + particle.position[0] * particle.position[1] * particle.position[1] * particle.position[1])
    

    def set_pbest(self):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for particle in self.particles:
            fitness_cadidate = self.fitness(particle)
            if(particle.pbest_value > fitness_cadidate):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position
                
            

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = self.fitness(particle)
            if(self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position

    def move_particles(self):
        for particle in self.particles:
            global W
            new_velocity = (W*particle.velocity) + (c1*random.random()) * (particle.pbest_position - particle.position) + \
                            (random.random()*c2) * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            particle.move()
    
    def calcFragrance(self):
        for particle in self.particles:
            inside = ( particle.fitnessVal / c )
            particle.fragrance = pow(inside, 1/a)
    
    def calcFitness(self):
        for particle in self.particles:
            particle.fitnessVal = self.fitness(particle)
    
    def calcEq1(self):
        self.calcFitness()
        self.calcFragrance()
    
    def setBest(self):
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for particle in self.particles:
            if self.gbest_value > particle.fitnessVal:
                self.gbest_value = particle.fitnessVal
                self.gbest_position = particle.position
                self.gbest_frag = particle.fragrance
                #print("Zmieniam")
    
    def moveEq2(self, particle, r):
        particle.position = particle.position + (r*r * self.gbest_position - particle.position) * particle.fragrance
    
    def moveEq3(self, particle, r):
        max = len(self.particles) -1
        end = 0
        while end == 0:
            end = 1
            pos1 = random.randint(0,max)
            pos2 = random.randint(0,max)
            if(pos1 != pos2):
                end = 0
         
        particle.position = particle.position  + (r*r * self.particles[pos1].position - self.particles[pos2].position ) * particle.fragrance
    
    def Move(self):
        for particle in self.particles:
            r = random.random()
            if(r < p):
                self.moveEq2(particle,r)
            else:
                self.moveEq3(particle,r)
                    

    def Work(self):
        self.calcEq1() # fitness + fragrance
        self.setBest() # find best
        self.Move()    # move
            
            

search_space = Space(1, target_error, n_particles)
particles_vector = [Particle() for _ in range(search_space.n_particles)]
search_space.particles = particles_vector
search_space.print_particles()

iteration = 0
while(iteration < n_iterations):
    search_space.Work()
    #search_space.set_pbest()    
    #search_space.set_gbest()
    print("GBest", search_space.gbest_position)
    if(abs(search_space.gbest_value - search_space.target) <= search_space.target_error):
        break

    #search_space.move_particles()
    #search_space.div_swarm_per_sub()

    #search_space.particles[5].pbest_position
    #search_space.battle(5)
    iteration += 1
    
print("The best solution is: ", search_space.gbest_position, " in n_iterations: ", iteration)
#print("The best solution is: ", search_space.fitness(search_space.gbest_position), " in n_iterations: ", iteration)