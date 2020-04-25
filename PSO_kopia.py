import random
import numpy as np 

W = 0.5
c1 = 0.8
c2 = 0.9 

n_iterations = 200#int(input("Inform the number of iterations: "))
target_error = 0.001#float(input("Inform the target error: "))
n_particles = 100#int(input("Inform the number of particles: "))

class Particle():
    def __init__(self):
        self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([0,0])
        self.subset = 0
        self.place = 0

    def __str__(self):
        print("I am at ", self.position, " meu pbest is ", self.pbest_position, " subset: ", self.subset)
    
    def move(self):
        self.position = self.position + self.velocity
        

        


class Space():

    def __init__(self, target, target_error, n_particles):
        self.target = target
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.random()*50, random.random()*50])
        #self.subset = 0
        self.place = 0

    def print_particles(self):
        for particle in self.particles:
            particle.__str__()
   
    def fitness(self, particle):
        #return particle.position[0] ** 2 + particle.position[1] ** 2 + 1
        return (1.5 - particle.position[0] + particle.position[0] * particle.position[1]) * (1.5 - particle.position[0] + particle.position[0]* particle.position[1]) \
        +(2.25 - particle.position[0] + particle.position[0] * particle.position[1] * particle.position[1]) * (2.25 - particle.position[0] \
        + particle.position[0] * particle.position[1] * particle.position[1]) +(2.625 - particle.position[0] + particle.position[0] * particle.position[1] * particle.position[1] * particle.position[1]) * (2.625 - particle.position[0] + particle.position[0] * particle.position[1] * particle.position[1] * particle.position[1])
    

    def set_pbest(self):
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
    
    def div_swarm_per_sub(self):
        for particle in self.particles:
            sub_set = random.randint(0,5)         # 5 sub-sets
            particle.subset = sub_set
    
    #def move_particles_battle(self):
    # 3 wylosowane czastki dla jednego setu
    def battle(self, n_subset):
        print("BATTLE")
        cnt = 0
        #list  = [3][3]
        #list = [[0]*cols for _ in [0]*rows]
        list = [[0]*3 for _ in [0]*2]
        
        while(cnt <3):
            position = random.randint(0, len(self.particles)-1)
            print("Posi",position)
            if(self.particles[position].subset == n_subset and position not in list[0]):
                #list.append(position)
                list[0][cnt] = position
                cnt = cnt +1
        print("Liczba" ,cnt)
        print(list)
        values = []
        print("LISTA:")
        print(list)
        for all in range(0,3):
            print("wewnatrz ", list[0][all])
            values.append(self.fitness(self.particles[ list[0][all] ]))
            list[1][all] = self.fitness(self.particles[ list[0][all] ])
        
        print("values")
        print(values)
        
        print("LIST")
        print(list)
        
        
        print("------")
        
        wartosc = np.amin(list, axis=1)
        
        print("wartosc ", wartosc[1], " indeks: ", wartosc[0])
        
        self.particles[ wartosc[0] ].place = 1 # zwyciezca
        
        
        
        
        
        
        
    # predkosc 2 miejsce
    def velocity2(self, winner, second):
        new_velocity = (particle.velocity) * (c1*random.random()) +\
                            (random.random()*c2) * (self.particles[winner].position - self.particles[second].position)
                            
    def velocity3(self, winner, second, third):
        new_velocity = (particle.velocity) * (random.random()) +\
                            (random.random()) * (self.particles[winner].position - self.particles[third].position) +\
                            (random.random()) * (self.particles[second].position - self.particles[third].position)

        """
        for particle in self.particles:
            print(particle.subset)
        """   
        
        
            

search_space = Space(1, target_error, n_particles)
particles_vector = [Particle() for _ in range(search_space.n_particles)]
search_space.particles = particles_vector
search_space.print_particles()

iteration = 0
while(iteration < n_iterations):
    search_space.set_pbest()    
    search_space.set_gbest()
    print("GBest", search_space.gbest_position)
    if(abs(search_space.gbest_value - search_space.target) <= search_space.target_error):
        break

    search_space.move_particles()
    search_space.div_swarm_per_sub()
    """
    for particle in search_space.particles:
        print(particle.subset)
    """
    search_space.particles[5].pbest_position
    search_space.battle(5)
    iteration += 1
    
print("The best solution is: ", search_space.gbest_position, " in n_iterations: ", iteration)
#print("The best solution is: ", search_space.fitness(search_space.gbest_position), " in n_iterations: ", iteration)