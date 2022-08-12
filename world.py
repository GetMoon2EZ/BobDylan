from random import randint
from bob import Bob


class Square:
    def __init__(self, x, y):
        self.population = set()
        self.x = x
        self.y = y
        self.food = 0

    def insert_bob(self, b: Bob):
        """
        Insert un bob dans la case et change la position du bob
        """
        self.population.add(b)
        b.setPosition(self.x, self.y)

    def remove_bob(self, b: Bob):
        """
        Supprime le bob de la case
        """
        return self.population.remove(b)

    def get_population(self, b:Bob=None):
        """
        Renvoit l'ensemble des bob de la case
        si b != None : on enlève le bob de l'ensemble
        """
        if b != None:
            return self.population - {b}
        return self.population

    def set_population(self, bobs):
        """
        Change la population de la case
        - input :
            - (set) : l'ensemble des bobs
        """
        self.population = bobs
        
    def clear_food(self):
        """
        Supprime la nourriture de la case
        """
        self.food = 0


class World:
    def __init__(self, n, foods_per_day, ticks_per_day):
        self.map = [[Square(x, y) for x in range(n)] for y in range(n)]
        self.size = n
        self.f = foods_per_day
        self.d = ticks_per_day
        self.bob_dylans = set()
        self.food_coordinate = {}
        self.ticks = 0  # current number of ticks
        self.days = 0
        self.reproduction = 3 #Cette ligne ne sert a rien ???????

    def get_random_coordinate(self):
        """
        Renvoi une position aléatoire dans le monde
        - output : tuple de 2 int
        """
        return (randint(0, self.size - 1), randint(0, self.size - 1))

    def get_list_bobs(self):
        """
        Renvoi la liste des bobs du monde
        """
        return self.bob_dylans

    def set_list_bobs(self, bobs):
        """
        Change la liste des bobs du monde
        """
        self.bob_dylans = bobs

    def insert_bob(self, x, y, b: Bob):
        """
        Insert un bob à la case (x, y)
        """
        self.map[y][x].insert_bob(b)
        self.bob_dylans.add(b)

    def remove_bob(self, b: Bob):
        """
        Supprime le bob du monde
        """
        pos = b.getPosition()
        try:
            self.map[pos[1]][pos[0]].remove_bob(b)
            self.bob_dylans.remove(b)
        except:
            print(f"-- ERROR remove bob at {pos[0]} {pos[1]}")

    def move_bob(self, b: Bob, last_pos):
        """
        Déplace le bob de last_pos à sa nouvelle position
        """
        # if b in self.map[last_pos[1]][last_pos[0]].population:
        sqr = self.get_square(last_pos[0], last_pos[1])
        if b in sqr.population:
            sqr.remove_bob(b)
        (x, y) = b.getPosition()
        self.get_square(x, y).insert_bob(b)
        # self.map[y][x].insert_bob(b)

    # somehow it's map[y][x] that gives the correct square

    def get_list_food(self):
        """
        Renvoi la liste des positions de nourriture
        """
        return self.food_coordinate

    def spawn_food(self):
        """
        Fait apparaitre de la nourriture dans le monde
        """
        def addOrCreate(pos, qt):
            if pos in self.food_coordinate:
                self.food_coordinate[pos] += qt
            else:
                self.food_coordinate[pos] = qt

        daily_food = self.f
        while daily_food >= 5:
            # print(f"f: {daily_food} {daily_food // self.size}")
            qt = randint(1, max(daily_food, daily_food // (self.size**2/5)) // 3)  # on vient de changer ça pour mieux repartir la nourriture
            (fx, fy) = self.get_random_coordinate()
            daily_food -= qt
            self.get_square(fx,fy).food += qt
            addOrCreate((fx, fy), qt)

        if daily_food > 0:
            (fx, fy) = self.get_random_coordinate()
            self.get_square(fx,fy).food += qt
            addOrCreate((fx, fy), daily_food)

    def number_of_bob(self):
        """
        Renvoi la taille de la population
        """
        return len(self.bob_dylans)

    def get_square(self, x, y):
        """
        Renvoi la case à la position (x,y)
        """
        return self.map[y][x]

    def get_square_of_bob(self, b: Bob):
        """
        Renvoi la case où se situe le bob
        """
        (x, y) = b.getPosition()
        return self.get_square(x, y)

    def clear_food(self):
        """
        Supprime toute la nourriture du monde
        """
        for (x,y) in self.food_coordinate.keys():
            self.get_square(x, y).clear_food()
        self.food_coordinate.clear()

    def get_bobs_by_velocity(self):
        """
        Renvoi la liste des bobs trié par leur vitesse décroissante
        """
        return sorted(self.get_list_bobs(), key=lambda bob: -bob.velocity)

    def is_there_food_here(self,x,y):
        # return [self.get_list_food()[i] for i in range (0,len(self.get_list_food())) if x and y in self.get_list_food()[i]]
        return (x,y) in self.food_coordinate #[el for el in self.get_list_food() if el[0] == x and el[1] == y]
        # to_be_returned=[]
        # for i in range(0,len(self.get_list_food())):
        #     if x and y in self.get_list_food()[i]:
        #         print(self.get_list_food()[i])
        #         to_be_returned.append(self.get_list_food()[i])
        # return(to_be_returned)

    def eat_food(self, sqr, qt):
        """
        eat qt food at the (x,y) position
        """
        # print(f"bob is eating {qt} food at ({sqr.x},{sqr.y})")
        sqr.food = round(sqr.food - qt, 2)
        # if self.food_coordinate[(sqr.x, sqr.y)] > qt:
        #     self.food_coordinate[(sqr.x, sqr.y)] = round(self.food_coordinate[(sqr.x, sqr.y)] - qt, 2)
        # else:
        #     del self.food_coordinate[(sqr.x, sqr.y)]
        if sqr.food < 0.1:
            # print("deleting food records...")
            # print(f"food is here: {self.food_coordinate[(sqr.x, sqr.y)]}")
            if (sqr.x, sqr.y) in self.food_coordinate:
                del self.food_coordinate[(sqr.x, sqr.y)]
        else:
            self.food_coordinate[(sqr.x, sqr.y)] = sqr.food

        # for i in range(len(self.food_coordinate)):
        #     if(self.food_coordinate[i][0] == sqr.x and self.food_coordinate[i][1] == sqr.y):
        #         if self.food_coordinate[i][2]-qt > 0 :
        #             self.food_coordinate[i] = (sqr.x, sqr.y, self.food_coordinate[i][2]-qt)
        #         else:
        #             del self.food_coordinate[i]
        #         return
