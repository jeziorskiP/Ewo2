import random
import numpy as np 

W = 0.5
c1 = 0.8
c2 = 0.9 

igrzyska = []

n_iterations = 200
target_error = 0.001
n_particles = 100

class Particle():
    def __init__(self):
        self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([0,0])
        self.subset = 0
        self.place = 0
        self.pair = 0

    def __str__(self):
        print("Position ", self.position, "  pbest ", self.pbest_position, " subset: ", self.subset)
    
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
        + particle.position[0] * particle.position[1] * particle.position[1]) +(2.625 - particle.position[0] + particle.position[0] * particle.position[1] \
        * particle.position[1] * particle.position[1]) * (2.625 - particle.position[0] + particle.position[0] * particle.position[1] * particle.position[1] \
        * particle.position[1])
    

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
    
    def div_swarm_per_sub(self, count):
        for particle in self.particles:
            sub_set = random.randint(0,count)         # 5 sub-sets
            particle.subset = sub_set
    
    def do_battle(self, n_subset):
        for i in range(0, n_subset):
            print("BITWA NR ", i)
            self.battle(i)
        
        print("ZACZYBAM IGRZYSKA")
        self.igrzyska(igrzyska)
        igrzyska.clear()
        
    
    #def move_particles_battle(self):
    # 3 wylosowane czastki dla jednego setu
    def battle(self, n_subset):
        global igrzyska
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
            #print(self.particles[ list[0][all] ].position)
            values.append(self.fitness(self.particles[ list[0][all] ]))
            list[1][all] = self.fitness(self.particles[ list[0][all] ])
        
        print("values")
        print(values)
        
        print("LIST")
        print(list)
        
        print("------")
        
        wartosc = np.amin(list, axis=1)
        
        print("wartosc ", wartosc[1], " indeks: ", wartosc[0])
        #winner = wartosc[0]
        
        result = np.where(list == wartosc[1]  )
        print("Index", result[1])
        
        winner = int( list[0][  result[1][0] ] )
        
        list = np.delete(list,result[1] , 1)
        print("LIST")
        print(list)
        print("KOniec")
        
        
        print("+++++++++")
        
         
        wartosc = np.amin(list, axis=1)
        
        print("wartosc ", wartosc[1])
        
        result = np.where(list == wartosc[1]  )
        
        winner2 = int (list[0][  result[1][0] ] )
        print("Index", result[1])
        list = np.delete(list,result[1] , 1)
        print("LIST")
        print(list)
        print("KOniec")
        
        
        winner3 = int(list[0][0])
        
        print("WINNERZY")
        print(winner)
        print(winner2)
        print(winner3)
        
        print("WINNERZY")
        
        print("Aktualizuje")
        self.move_particles_Battle(winner,winner2, winner3)
        
        igrzyska.append(winner)
        
        print(igrzyska)
        
        
        
    def igrzyska(self, igrzyska):
        cnt = 0
        list = [[0]*3 for _ in [0]*2]
        while cnt<3:
            position = random.randint(0, len(self.particles)-1)
            print("Posi",position)
            if(position in igrzyska and position not in list[0]):
                list[0][cnt] = position
                list[1][cnt] = self.fitness(self.particles[position])
                cnt = cnt +1  
          
        print("LIST")
        print(list)
        
        print("------")
        
        wartosc = np.amin(list, axis=1)
        
        print("wartosc ", wartosc[1], " indeks: ", wartosc[0])
        #winner = wartosc[0]
        
        result = np.where(list == wartosc[1]  )
        print("Index", result[1])
        
        winner = int( list[0][  result[1][0] ] )
        
        list = np.delete(list,result[1] , 1)
        print("LIST")
        print(list)
        print("KOniec")
        
        
        print("+++++++++")
        
         
        wartosc = np.amin(list, axis=1)
        
        print("wartosc ", wartosc[1])
        
        result = np.where(list == wartosc[1]  )
        
        winner2 = int (list[0][  result[1][0] ] )
        print("Index", result[1])
        list = np.delete(list,result[1] , 1)
        print("LIST")
        print(list)
        print("KOniec")
        
        
        winner3 = int(list[0][0])
        
        print("WINNERZY IGRZYSK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("WINNERZY")
        print(winner)
        print(winner2)
        print(winner3)
        
        print("WINNERZY")
        
        print("Aktualizuje")
        self.move_particles_Battle(winner,winner2, winner3)
        
        
        
        
    def move_particles_Battle(self, winner, second, third):
            
            
            new_velocity2 = self.velocity2(winner, second)
                            
            self.particles[second].velocity = new_velocity2
            self.particles[second].move() 
            
            new_velocity3 = self.velocity3(winner, second, third)
                            
            self.particles[third].velocity = new_velocity2
            self.particles[third].move() 
        
        
        
    # 2 miejsce
    def velocity2(self, winner, second):
        return(self.particles[second].velocity) * (c1*random.random()) +\
                            (random.random()*c2) * (self.particles[winner].position - self.particles[second].position)

    # 3 miejsce                     
    def velocity3(self, winner, second, third):
        return (self.particles[third].velocity) * (random.random()) +\
                            (random.random()) * (self.particles[winner].position - self.particles[third].position) +\
                            (random.random()) * (self.particles[second].position - self.particles[third].position)

        """
        for particle in self.particles:
            print(particle.subset)
        """   
        
# ---------------------------------------------------------------------------------------
# CSO

    def mean(self):
        cnt = 0
        X1 = 0
        X2 = 0
        for particle in self.particles:
            # A[cnt][0] = particle.position[0]
            # A[cnt][1] = particle.position[1]
            X1 = X1 + particle.position[0]
            X2 = X2 + particle.position[1]
            cnt = cnt + 1 
        A =  np.array([0,0], dtype = np.double)
        A[0] = X1/cnt
        A[1] = X2/cnt
        print("TABLICA ", A)
        return A
        
    def move_particles_CSO(self, winner, looser):
    
            new_velocity = self.velocityCSO(winner, looser)
            self.particles[looser].velocity = new_velocity
            self.particles[looser].move()
            
    def CSO(self):
        p=0
        cnt = int( len(self.particles) / 2 )
        print(cnt)
        list = [[0]*2 for _ in [0]*cnt]
        while(cnt>0):
            position = random.randint(0, len(self.particles)-1)
            print("wylosowane 1: ", position)
            if(position not in list):
                print("w warunku")
                list[cnt-1][0] = position
                print(list[cnt-1][0] )
                while(p==0):
                    position = random.randint(0, len(self.particles)-1)
                    
                    print("wylosowane 2: ", position)
                    if(position not in list):
                        list[cnt-1][1] = position
                        p = 1
                        cnt = cnt - 1
            p = 0
        print(list) 
        
        
        for i in range(0, len(list)-1):
            poz1 = list[i][0]
            poz2 = list[i][1]
            print("POZYCJA 1",poz1)
            print(self.particles[poz1].position)
            Y1 = self.fitness(self.particles[poz1])
            Y2 = self.fitness(self.particles[poz2])
            if(Y1 < Y2):    #Y1 zywciezca!
                #aktualizacja Y2
                self.move_particles_CSO(list[i][0],list[i][1])
            else:
                self.move_particles_CSO(list[i][1],list[i][0])
                
              
        #cnt = int( len(self.particles) / 2 )

    # 3 miejsce
    def velocityCSO(self, winner, looser):
        return  (self.particles[looser].velocity) * (random.random()) +\
                            (random.random()) * (self.particles[winner].position - self.particles[looser].position) +\
                            (random.random()) * (self.mean() - self.particles[looser].position)  
        

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

    #search_space.move_particles()
    
    search_space.div_swarm_per_sub(5)
    search_space.do_battle(5)
    
    #search_space.battle(5)
    #search_space.CSO()
    print("dddd")
    #search_space.mean()
    iteration += 1
    
print("The best solution is: ", search_space.gbest_position, " in n_iterations: ", iteration)
#print("The best solution is: ", search_space.fitness(search_space.gbest_position), " in n_iterations: ", iteration)