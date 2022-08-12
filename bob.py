from random import choice, uniform,randrange, random, randint

the_mighty_magic_number = 69420
avoid_memory = 0.5
remember_food = 1
def to_shine_or_not_to_shine():
    return (randrange(69000,70000)==the_mighty_magic_number)

names = ["Gabe", "Luc", "Nathan", "Thanh", "Esteban", "Florian", "Romain", "Mr Hugot", "Mr Berthome", "Ross", "Dylan", "Square Pants", "Ricardo", "Aniki", "Dylan Dylan Dylan Dylan", "BY", "LinkinPark", "Yoda", "Anakin", "Highground", "Lightsaber", "Whoosh", "Bruce U", "CaptainAlex", "Pepe", "KEKW", "MC Donald", "KFC", "Wake me up inside", "Green", "JOJO", "DIO", "The World", "Morane"]

class Bob:
    DEFAULT_MASS = 1
    DEFAULT_MASS_MUTATION_RATE = 0.5
    DEFAULT_VELOCITY = 1
    DEFAULT_VELOCITY_MUTATION_RATE = 0.1
    DEFAULT_FIELD_OF_VIEW = 3
    DEFAULT_ENERGY = 100
    DEFAULT_SHINY = False
    DEFAULT_MEMORY_TOKEN = 1

    def __init__(self, pos_x, pos_y, energy_level, velocity, mass, field_of_view, shiny, memory):
        self.x = pos_x
        self.y = pos_y
        self.energy = energy_level
        self.max_energy = 200
        self.velocity = velocity
        self.mass = mass
        self.fov = field_of_view
        self.perception = {"enemy": {"flag": 0, "size": 0, "x": 0, "y": 0}, "food": {"flag": 0, "value": 0, "x": 0, "y": 0}}
        self.memorytoken = memory #c'est ça qu'il faut changer dans le gui#
        self.orient = 'E'
        self.shiny = shiny
        self.dead = False
        self.name = "BOB " + names[randint(0,len(names)-1)]

        self.memory= {"flag": 0, "points": self.memorytoken, "avoid" : [], "remember" : []}
        # location to avoid will be a tuple (x, y)
        # food location will be a tuple (x, y, value)
        # 0 means he is not remembering any food
        # vice versa
        # point tracks the memory space our bob has left

    @staticmethod
    def init_param(parametres):
        """
        Change les attributs static par défaut par les valeurs contenues dans parametres (pris en paramètres)
        @param sont les parametres d'un bob, passés dans le tableau paramtres, 
        """
        Bob.DEFAULT_MASS = parametres["mass"]
        Bob.DEFAULT_VELOCITY = parametres["speed"]
        Bob.DEFAULT_FIELD_OF_VIEW = parametres["fov"]
        Bob.DEFAULT_MEMORY_TOKEN=parametres["memory"]

    @staticmethod
    def create_default_bob():
        """
        Crée un Bob à partir des attributs par défaut
        """
        return Bob(-1, -1, Bob.DEFAULT_ENERGY, Bob.DEFAULT_VELOCITY, Bob.DEFAULT_MASS, Bob.DEFAULT_FIELD_OF_VIEW, Bob.DEFAULT_SHINY,Bob.DEFAULT_MEMORY_TOKEN)

    @staticmethod
    def born(b1, b2=None, flag=0):
        """
        Crée un bob à partir de 1 ou 2 bobs parents
        flag représente les mutations possibles pour l'enfant
        on va ici utiliser une string binaire pour differencier les cas, etant les mutations activées par l'uitlisateur
        @param bob parents
        @return attributs du nouveau bob
        """
        if to_shine_or_not_to_shine():
            print("YOUR BOB IS FUCKING SHINY FAM")
            shiny = True
        else :
            shiny = Bob.DEFAULT_SHINY
        bin_flag = f"{flag:b}"  # int traduit en str binaire

        generic_velocity = b1.velocity if b2 == None else ( b1.velocity + b2.velocity ) / 2
        if bin_flag[choice([-1,0,1])-1] == "0":  # pas de mutation de vitesse
            speed = Bob.DEFAULT_VELOCITY
        else:
            speed = round(uniform(generic_velocity - Bob.DEFAULT_VELOCITY_MUTATION_RATE,
                            generic_velocity + Bob.DEFAULT_VELOCITY_MUTATION_RATE), 2)

        if len(bin_flag) >= 2 and bin_flag[-1] == "1": 
            mass = b1.mass if b2 == None else (b1.mass + b2.mass) / 2
            mass = round(uniform(mass - Bob.DEFAULT_MASS_MUTATION_RATE, mass + Bob.DEFAULT_MASS_MUTATION_RATE),2)
        else:
            mass = Bob.DEFAULT_MASS
       
       
                 #print("le bob",self.index,"a vu sa masse augmenté de :",add_masse)
        if len(bin_flag)>=3 and bin_flag[-3]=="1":
                
            fov= b1.fov if b2 == None else (b1.fov + b2.fov) / 2
            fov = round(uniform(fov - Bob.DEFAULT_FIELD_OF_VIEW, fov + Bob.DEFAULT_FIELD_OF_VIEW),2)
            #print("le bob",self.index,"a vu son FOV changé à :",self.fov)
        else:
            fov=Bob.DEFAULT_FIELD_OF_VIEW

        if len(bin_flag)>=4 and bin_flag[-4]=="1":
                
            memory= b1.memorytoken if b2 == None else (b1.memorytoken + b2.memorytoken) / 2
            # Test your code before pushing please
            tmp = 0 if b2 == None else b2.memorytoken 
            memory = max(0,round((b1.memorytoken+tmp)/2) + choice([-1,0,1]))
            # print("sa memoire a été changée à", memory)
        else: 
            memory = Bob.DEFAULT_MEMORY_TOKEN
            # print("la memoire est une flemmarde")
        # print(f'new x-man has {speed} speed and {mass} mass and {memory}')
        pos = b1.getPosition()
        return Bob(pos[0], pos[1], Bob.DEFAULT_ENERGY, speed, mass, 3, shiny, memory)

    # Allow bobs to evaluate food and enemy in a square
    def evaluate_square_in_fov(self, sqr):
        """methode qui sert a regarder les cases autour du bob pour de la nourriture ou pour un bob trop grand qu'il doit fuir.
        @param attributs du bob et attibuts du square. 
        """
        if sqr.food > self.perception["food"]["value"]:
            self.perception["food"]["flag"] = 1
            self.perception["food"]["value"] = sqr.food
            self.perception["food"]["x"] = sqr.x
            self.perception["food"]["y"] = sqr.y

        for b_fov in sqr.get_population():
            if b_fov.mass > self.mass * 1.5 and b_fov.mass > self.perception["enemy"]["size"]:
                self.perception["enemy"]["flag"] = 1
                self.perception["enemy"]["size"] = b_fov.mass
                self.perception["enemy"]["x"] = sqr.x
                self.perception["enemy"]["y"] = sqr.y

    def sentient_action(self, n, energy_multiplier,world):
        """
        fonctions qui va gerer les deplacements, prends en compte les elements en memoire, les elements en vue.
        @param bob, avec n la taille du monde( pour gerer la circularité de la carte, energy_multiplier sert a gerer les deplacement non entier sur les cases( du a la celerité non-entière) et world n'est autre que la classe world.
        @return la position precedante, pour pouvoir gerer les orientations des bobs.
        """
        if self.perception["enemy"]["flag"] == 1:   # bug ! If this condition is verified, previous_foodlist isn't initialized then when it's called it doesn't exist locally anymore causing the game to crash
            # avoiding enemy
            # using the same idea of dx and dy
            dx = self.perception["enemy"]["x"] - self.x
            dy = self.perception["enemy"]["y"] - self.y

            if dx != 0:
                dx = -int(dx / abs(dx))
            if dy != 0:
                dy = -int(dy / abs(dy))

            flow_control = choice([1, 0])
        else:
            last_pos = (self.x, self.y)
            previous_foodlist=self.foodcheck(world,self.x,self.y)
            self.locationmemoryentry()
            dx = self.perception["food"]["x"] - self.x
            dy = self.perception["food"]["y"] - self.y

            if dx != 0:
                dx = int(dx / abs(dx))
            if dy != 0:
                dy = int(dy / abs(dy))
            # dx, dy tell bob which direction to advance to reach the target
            flow_control = choice([1, 0])
            # random if no target

            if self.perception["food"]["flag"] == 0: #si on est dans le cas où on a pas de nourriture en vue

                if len(self.memory["remember"]) > 0: #si on est dans le cas où il avait vu de la nourriture qu'il ne vboie plus la maintenant

                    self.memory["remember"].sort(key=lambda list:list[2], reverse=True)
                    #print(self.memory["remember"])
                    dx = (self.memory["remember"][0][0][0]) - self.x
                    dy = (self.memory["remember"][0][0][1]) - self.y
                    if dx != 0:
                        dx = int(dx / abs(dx))
                    if dy != 0:
                        dy = int(dy / abs(dy))
                    # dx, dy tell bob which direction to advance to reach the target

                else : #si vraiment on est dans le cas ou le bob ne voit pas de nourriture et en plus ! il n'apas de location où il y avait de la nourriture en memoire
                    # print(f'no target')
                    dx = choice([-1, 0, 1])
                    dy = choice([-1, 0, 1])
            else:
                # normal case
                # redundant code for case (1, 0) and (0, 1) because i can't think of anything else lol
                if abs(dx) == 1 and dy == 0:
                    flow_control = 1  # 1 means we will change self.x

                if dx == 0 and abs(dy) == 1:
                    flow_control = 0  # 0 means we will change self.y

        self.x = (self.x + dx * flow_control) % n
        self.y = (self.y + dy * (1 - flow_control)) % n
        # print(f'our bob is at {last_pos}')
        # print(f'our bob is going to {self.perception["food"]["x"]} {self.perception["food"]["y"]}')
        # print(f'By following the direction of ({dx}, {dy})')
        # print()

        next_foodlist=self.foodcheck(world,self.x,self.y)

        # Here i think we can just check if the distance from our new position to a food source is greater than our fov
        food_to_enter_in_memory = [item for item in previous_foodlist if item not in next_foodlist]

        self.list_food_in_memory(food_to_enter_in_memory)


        self.energy -= energy_multiplier *(0.5 * self.mass * (self.velocity ** 2)+0.2*self.fov+0.2*self.memorytoken)
        return last_pos

    def sentient_action_rework(self, energy_multiplier, world):
        # since we are handling multiple squares around our bob i would say we have no option but to make world a parameter

        # an action occur at the end of our bob's turn, he will evaluate the squares in his fov, then depends on the situation
        # he will decide where to go (more precisely the next square that he will go to)
        # that means first clearing his perception from the previous turn

        self.clear_perception()
        # print(f'----- new tick -----')
        # print(f'at this state our bob has {self.memory["points"]} memory points')
        # print(f'bob is at {self.x} {self.y}')
        # print(f'he can see a distance of {self.fov} around him')
        # print(f'his avoid mem {self.memory["avoid"]}')
        # print(f'--------------')
        # print(f'food mem {self.memory["remember"]}')

        fov_food = []
        for i in range(-self.fov, self.fov + 1):
            for j in range(abs(i) - self.fov, self.fov - abs(i) + 1):
                x_fov = (self.x + i) % world.size # this shoud be world.size, it will be fucked up when we use bigger worlds
                y_fov = (self.y + j) % world.size
                s_fov = world.get_square(x_fov, y_fov)
                if self.memory["flag"] == 1:
                    for x, y, val in self.memory["remember"]:
                        if x == x_fov and y == y_fov:
                            # print(f'a food in bobs memory is now in his fov, now he will clear his memory of that food')
                            self.clear_memory(1, (x, y, val))
                if s_fov.food > 0:
                    fov_food.append( (x_fov, y_fov, s_fov.food) )
                # we can't put evaluation function in side the if because we also need to check for enemies
                self.evaluate_square_in_fov(s_fov)
        # evaluate square in fov should give us the list of food that is not in bob's perception
        # (foods that are ignored) so we can put one of them in memory after he moves
        # this is almost the same with nathan's foodcheck function
        ignored_food = [(x, y, val) for (x, y, val) in fov_food if x != self.perception["food"]["x"] and y != self.perception["food"]["y"]]
        # probably need some changes to this because memory and perception are not using the same data format
        ignored_food.sort(key=lambda f : -f[2])
        # print(f' these are the foods that are getting ignored {ignored_food}')

        # Clear bob's memory if any of the squares he remembers is in his fov
        """
        This cause an unexpected bug when our bob is near the world's edge he will not erase the food on the other side from his memory
        if self.memory["flag"] == 1:
            for x, y, val in self.memory["remember"]:
                if abs(x - self.x) + abs(y - self.y) < self.fov:
                    print(f'a food in bobs memory is now in his fov, now he will clear his memory of that food')
                    self.clear_memory(1, (x, y, val))
        """
        # Our bob always run if there is an enemy
        # dx and dy are therefore definite for the whole action
        if self.perception["enemy"]["flag"] == 1:
            # avoiding enemy
            # using the same idea of dx and dy
            dx = self.perception["enemy"]["x"] - self.x
            dy = self.perception["enemy"]["y"] - self.y

            # we want to run at the opposite direction of our biggest enemy
            if dx != 0:
                dx = -int(dx / abs(dx))
            if dy != 0:
                dy = -int(dy / abs(dy))
        else:
            # If he sees no enemy
            # time for food hunting
            if self.perception["food"]["flag"] == 1:
                # our bob will go to his targeted food
                # print(f'bob saw a square with {self.perception["food"]["value"]} food so he will go to {self.perception["food"]["x"]} {self.perception["food"]["y"]}')
                dx = self.perception["food"]["x"] - self.x
                dy = self.perception["food"]["y"] - self.y

                # Team fortress 2 the quick fix
                dx = -dx if abs(dx) * 2 > world.size else dx
                dy = -dy if abs(dy) * 2 > world.size else dy

            elif self.memory["flag"] == 1:
                # if not he will check what he remembers
                # first item in the list will be the oldest source that he can remember
                # we'll go with that for now
                x, y, value = self.memory["remember"][0]
                # print(f'bob doesnt see any food around him')
                # print(f'but he remembered a square with {value} food so he will go to {x} {y}')
                # print(f'bob is at {self.x} {self.y}')
                dx = x - self.x
                dy = y - self.y
                # Team fortress 2 the quick fix part 2
                dx = -dx if abs(dx) * 2 > world.size else dx
                dy = -dy if abs(dy) * 2 > world.size else dy
                # print(f"his distance to cover {dx} {dy}")

            elif self.memory["avoid"]:
                x, y = self.memory["avoid"][-1]
                adx = x - self.x
                ady = y - self.y
                # print(f'no food in sight no food in mind')
                # print(f'at least i remembered where i was: {x} {y}')
                # print(f'so i should avoid moving in the direction of {adx} {ady}')
                # if not then he checks if he remember where he was last turn
                # self.memory["avoid"] is false if it is an empty list
                # another bug
                # since if dx = adx and dy != ady flow control may randomly choose dx as the next movement
                # we don't want that so
                dx = choice([d_x for d_x in [-1, 0, 1] if d_x != adx])
                dy = choice([d_y for d_y in [-1, 0, 1] if d_y != ady])
                # print(f'therefore, i will move in the direction of {dx} {dy}')

            else:
                # print(f'bob see no food, remembered no food and is dumb')
                # print(f'so he go random places')
                # i guess at this point we'll just go with da flow
                dx = choice([-1, 0, 1])
                # to make sure that our bob will move lol
                # i'm so sorry this is so stupid but i just realized it today xD (4/12/2019)
                # >> always write comments kids
                dy = choice([-1, 0, 1]) if dx != 0 else choice([-1, 1])

            # now we reduce dx and dy so that we don't have to do it for every case
            # >> "yeah, this is big brain time"
            if dx not in [-1, 0, 1]:
                dx = int(dx / abs(dx))
            if dy not in [-1, 0, 1]:
                dy = int(dy / abs(dy))

        # print(f"our bob will finally move in the direction of {dx} {dy}")
        # reducing dx and dy to unit vectors allows us to use them directly to move our bob while keeping the right direction

        # 1 means we'll move along dx
        # 0 means we'll move along dy
        flow_control = choice([1, 0])
        # now that we have our dx and dy we can handle special cases where dx = 0 or dy = 0
        # that means no random bullshit we can't escape our destiny (movement is fixed)
        # this is to prevent bob from not moving (flow_control = 1 and dx = 0 for example)
        if abs(dx) == 1 and dy == 0:
            flow_control = 1  # 1 means we will change self.x
        if dx == 0 and abs(dy) == 1:
            flow_control = 0  # 0 means we will change self.y

        # last position for moving our bob through squares
        last_pos = (self.x, self.y)
        self.x = (self.x + dx * flow_control) % world.size
        self.y = (self.y + dy * (1 - flow_control)) % world.size
        # % world.size makes our bob appear on the other side

        # now we will check if any of the food went outside our fov
        # and if it's the case we will try to put that location in our memory
        for x, y, val in ignored_food:
            # list is already sorted in descending order
            if abs(x - self.x) + abs(y - self.y) > self.fov:
                # print(f'our bob has moved too far from a food source, he should put it in his memory if possible')
                # print(f'our bob is at {self.x} {self.y}')
                # print(f'the food is at {x} {y}')
                # we miss a food let's try to put it in memory
                if self.memory["points"] >= 1:
                    # since remembering food always take priority, i considered remembering
                    # a food location costs 1 points, and remembering where we were costs nothing
                    # but it depends on our remaining points
                    for i in range(2):
                        # make some space
                        self.clear_memory(0, None)
                    self.remember_food_location( (x, y, val) )

        # at the end of the action bob will try to put the remaining memory points to use by remembering where he was
        self.remember_location(last_pos)

        de = energy_multiplier * (0.5 * self.mass * (self.velocity ** 2) + 0.2 * self.fov + 0.2 * self.memorytoken)
        # print(f"our bob now losing {de} energy")
        self.energy = round((self.energy - de), 2)
        # print(f"his new energy level is {self.energy}")
        self.orient=self.orientation(last_pos[0],last_pos[1])
        #print(self.orient)
        return last_pos

    def remember_location(self, last_pos):
        # this function is made at 11pm so i will check it tomorrow
        n = len( self.memory["avoid"] )
        if self.memory["points"] > 0:
            if n == 2 * self.memory["points"]:
                self.memory["avoid"].pop(0)
            self.memory["avoid"].append(last_pos)

    def remember_food_location(self, fv):
        # this method will only be called if memory space is available
        self.memory["flag"] = 1
        self.memory["points"] -= 1
        self.memory["remember"].append(fv)
        # print(f'bob just remembered a location that he want to revisit later {fv}')


    def clear_perception(self):
        self.perception["food"]["flag"] = 0
        self.perception["food"]["value"] = 0
        self.perception["food"]["x"] = 0
        self.perception["food"]["y"] = 0

    def clear_memory(self, flag, m):
        if flag == 1:
            # print(f'food mem getting removed {m}')
            x, y, val = m
            self.memory["remember"].remove( (x, y, val) )
            self.memory["points"] += 1
            if self.memory["points"] == self.memorytoken:
                self.memory["flag"] = 0
        else:
            if self.memory["avoid"]:
                self.memory["avoid"].pop(0)

    def mutation(self, flags=0):
        proba = 0.1
        proba2=0.3
        bin_flag = f"{flags:b}"
        #print(bin_flag)
        if bin_flag[-1]==1 and random() >= proba:  # default = true pour la velocity, false pour la masse
            self.velocity += uniform(-1,1)
            #print("le bob",self.index,"a vu sa velocity augmenté de :",add_velocity)
        if len(bin_flag)>=2 and bin_flag[-2]==1 and random() >= proba:
                test = uniform(-1,1)
                if test<self.mass:
                    self.mass += test
                else:
                    self.mass = 0.01
                #print("le bob",self.index,"a vu sa masse augmenté de :",add_masse)
        if len(bin_flag)>=3 and bin_flag[-3]==1 and random() >= proba:
                self.fov += uniform(-1,1)
                #print("le bob",self.index,"a vu son FOV changé à :",self.fov)
        if len(bin_flag)>=4 and bin_flag[-4]==1 and random() >= proba2:
                self.memorytoken += choie([-1,0,1])
                # print(self.memorytoken)
                # print("le bob",self.index,"a vu sa memoire (token) changé à :",self.memorytoken)


    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getPosition(self):
        return self.x, self.y

    def getEnergy(self):
        return self.energy

    def getMass(self):
        return self.mass/self.DEFAULT_MASS

    def locationmemoryentry(self): #enter the location in memory if possible
        if self.memoryallowance(avoid_memory):
            self.memory["avoid"].append((self.x,self.y))
        elif not self.memoryallowance(avoid_memory) and len(self.memory["avoid"])>=1:
            self.memory["avoid"]=self.memory["avoid"][:1]
            self.memory["avoid"].append((self.x,self.y))

    def foodmemoryentry(self, x, y, value): #enter the food in memory if possible
        self.memory["remember"].sort(key=lambda list:list[2], reverse=True)
        if self.memoryallowance(remember_food):
            #print(f'{x} {y} {value} {[x,y,value]} will be added to {self.memory["remember"]}')
            self.memory["remember"].append([x,y,value])
            #print(f'which will result in {self.memory["remember"]}')
            #print()
        elif not self.memoryallowance(remember_food) and len(self.memory["avoid"])>=2:
            self.memory["avoid"]=self.memory["avoid"][:2]
            self.memory["remember"].append([x,y,value])
            #print(self.memory["remember"])

        elif not self.memoryallowance(remember_food) and len(self.memory["avoid"])<2:
            if self.memory["remember"][len(self.memory["remember"])-1][2]<value:
                self.memory["remember"]=self.memory["remember"][:len(self.memory["remember"])-1]
                self.memory["remember"].append([x,y,value])
                #print(self.memory["remember"])


    def list_food_in_memory(self,food): #this function basically calls the foodmemoryentry function for all the food that has to be called, the fooid thatr used to be in the perception redius but is no more.
        food.sort(key=lambda list:(list[2]), reverse=True) #we possibly don't need this one as the list is sorted in the sentient_action function
        for i in range (0,len(food)):
            self.foodmemoryentry(food[i][0],food[i][1],food[i][2])

    def foodcheck(self,world,x,y): #checks all the food in the redius, the center being put as parameters. returns the list of the food
        foodlist=[]
        food=[]
        for i in range(-self.fov, self.fov + 1):
            for j in range(abs(i) - self.fov, self.fov - abs(i) + 1):
                x_fov = (x + i) % 10
                y_fov = (y + j) % 10
                food=world.is_there_food_here(x_fov,y_fov)
                if len(food) == 3:
                    foodlist.append(food)
        return foodlist

    def memoryallowance(self, size): #chekcs wether the entered parameter is permitted to be put in memory (if the memory is not full)
        return ((len(self.memory["avoid"])*0.5 + len(self.memory["remember"])+size)<self.memorytoken)



    def orientation(self,x,y):
        """
        Retourne l'orientation du bob pour changer le sprite du meme bob
        bo: selfb (objet)
        """

        if y-self.y==0:
            if x-self.x==1:
                return 'W'
            else:
                return 'E'
        elif y-self.y==1:
            return 'N'
        else:
            return 'S'
            

    def getOrientation(self):
        return self.orient

    def getShiny(self):
        return self.shiny

