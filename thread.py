import threading
import time
from math import *

import matplotlib
from matplotlib import pyplot as plt
import matplotlib.animation as animation

import pygame
from PyQt5.QtWidgets import *
from pygame.locals import *
from pygame.key import *
from bob import Bob
from gui_v1 import Window
from map import Map
from world import World

BARRIER = threading.Barrier(2)
CONTINUE = True
PAUSE = False
SPEED = 2


def gui():
    """
    Affichage une fenêtre de paramétrage pour la simulation
    - output : (dict) le paramétrage
    """
    app = QApplication([])
    window = Window()
    app.exec_()

    mutations_flag = 0 # voir flag_bob_mutation.txt a remettre  #a zéro une fois que le window.memory-mutation est implementée
    if window.speed_mutation:
        mutations_flag += 1
    if window.mass_mutation:
        mutations_flag += 2
    if window.fov_mutation:
        mutations_flag += 4
    if window.memory_mutation:
        mutations_flag += 8

    return {"display_type": window.display_type,
            "number_of_ticks": int(window.nbTicks),
            "tick_duration" : int(window.tick_duration),
            "world_size": int(window.world_size),
            "population": int(window.population),
            "food_per_day": int(window.food_per_day),
            "speed": float(window.speed),
            "mass": float(window.mass),
            "fov": int(window.fov),
            "memory": int(window.memory),
            "mutations_flag": mutations_flag,
            "fullscreen": window.fullscreen,
            "resolution": window.resolution[:-1],
            "validation": window.validation,
            "graphic": window.graphic,
            "reproduction": window.reproduction_method,
            "keys": window.keyList
            }


def main(parametres):
    """
    Crée le monde et lance la simulation
    - input : (dict) le paramétrage de la simulation
    """
    # an open at the beginning to flush the file in case the last execution ended with an exception
    open('sample_data.txt', 'w').close()

    world = World(parametres["world_size"], parametres["food_per_day"], parametres["number_of_ticks"])
    Bob.init_param(parametres)

    # Create threads
    threads = [
        threading.Thread(target=simulation, args=(parametres["population"], world)),
    ]
    if(parametres["graphic"]):
        threads.append(threading.Thread(target=graphic_rendering, args=(world, parametres["display_type"])))

    for t in threads:
        t.start()
    # uncomment this to have a realtime graph
    # rt_graph()

    for t in threads:
        t.join()
    graph()
    print("end.")

    # an open at the end to flush it again
    open('sample_data.txt', 'w').close()

def cancel_IfNoGraphic():
    global CONTINUE
    input()
    CONTINUE = False


def graphic_rendering(w: World, vue):
    """
    Affiche un rendu graphique de la simulation
    """
    if(vue == "Top View : 2D"):
        display_world(w, list(w.get_list_bobs()))
    else:
        display_iso(w)
    print(f'exit from graphics rendering')

def simulation(p: int, world: World):
    """
    Lance la simulation
    - input :
        - p (int) : la taille initiale de la population
        - world (object) : le monde on s'effectue la simulation
    """
    print('running simulation......')
    population_generator(p, world)
    # print(world.number_of_bob())
    world.spawn_food()
    ticks = 0
    days = 0
    global CONTINUE
    global PAUSE
    global SPEED
    # Bob action
    while CONTINUE:
        if not PAUSE:
            world.ticks=ticks
            world.days=days
            bobs = set()
            bobs_counter = 0
            for bo in world.get_bobs_by_velocity():
                if not bo.dead:
                    # print(f'bob with {bo.velocity} move')
                    # print('----')
                    movement_points = bo.velocity
                    while movement_points > 0:
                        # print(f'bob still has {movement_points} gas')
                        # print()
                        energy_multiplier = 0 if (movement_points < 1 and bo.velocity > 1) else 1

                        sqr = world.get_square_of_bob(bo)

                        # gathering_data
                        # bob can evaluate all squares in his fov and then decide which square has the most food and
                        # which has the biggest enemy
                        """
                        x, y = bo.getPosition()
                        for i in range(-bo.fov, bo.fov + 1):
                            for j in range(abs(i) - bo.fov, bo.fov - abs(i) + 1):
                                x_fov = (x + i) % 10
                                y_fov = (y + j) % 10
                                s_fov = world.get_square(x_fov, y_fov)
                                bo.evaluate_square_in_fov(s_fov)
                        """
                                # print(f'Bob is evaluating square {x_fov} {y_fov} with {s_fov.food} food')
                        # if bo.perception["food"]["flag"] == 1:
                        #     print(f'bob has decided that the biggest source of food is at: {bo.perception["food"]["x"]} {bo.perception["food"]["y"]} which has {bo.perception["food"]["value"]}')
                        #     print(f'therefore bob will go to {bo.perception["food"]["x"]} {bo.perception["food"]["y"]}')
                        # else:
                        #     print('bob see no food :Feelsbadman:')

                        if sqr.food > 0 and movement_points >= 1:
                            # # qt eating can't be more than the square have and than bob can eat
                            # qt_food = min(sqr.food, floor(bo.max_energy - bo.energy))
                            # if qt_food > 0:
                            #     world.eat_food(sqr, qt_food)
                            #     bo.energy += qt_food
                            # im gonna reimplement your eatfood dude
                            if (bo.energy + sqr.food) >= 200:
                                qt_food = round(200 - bo.energy, 2)
                                bo.energy = 200 # this ensures that he'll reproduce
                            else:
                                qt_food = sqr.food
                                bo.energy = round(bo.energy + qt_food, 2)
                            world.eat_food(sqr, qt_food)

                        sqr_pop = set()
                        tmp_pop = sqr.get_population(bo)
                        for bo2 in tmp_pop:  # on parcourt les autres bobs
                            # eat
                            if bo.mass != 0 and (bo2.mass / bo.mass) < 2 / 3:    #apparemment un division par zéro peut se produire ici
                                # i corrected the formula
                                ori_energy = bo.energy
                                bo.energy = round(bo.energy + 0.5 * bo2.energy * ( 1 - (bo2.mass / bo.mass) ), 2)
                                bo.energy = bo.energy if bo.energy < 200 else 200
                                print(f'bob with {bo.mass} just ate {bo2} with {bo2.mass} mass and gained {round(bo.energy - ori_energy, 2)} gas !')
                                bo2.dead = True
                                bo2.energy = 0
                                # sqr.remove_bob(bo2)

                            # sex
                            if parametres["reproduction"] in (2,3) and bo2.energy >= 150 and bo.energy >= 150:
                                b = Bob.born(bo, bo2, parametres["mutations_flag"])
                                bobs.add(b)
                                sqr_pop.add(b)
                                bo.energy -= 100
                                bo2.energy -= 100
                                print('a new bob is born at', sqr.x , sqr.y)

                        # alone sex
                        if parametres["reproduction"] in (1,3) and bo.energy >= 200:
                            b = Bob.born(bo, None, parametres["mutations_flag"])
                            bobs.add(b)
                            sqr_pop.add(b)
                            bo.energy -= 150
                            print(f'a new bob is born at {sqr.x} {sqr.y}; alone sex')

                        # bo.mutation(parametres["mutations_flag"])
                        for new_bobs in sqr_pop:
                            sqr.insert_bob(new_bobs)
                        # sqr.set_population(sqr_pop)
                        # bobs_counter += len(sqr_pop)
                        # print(sqr_pop, sqr.get_population())

                        if bo.energy > 0:
                            if sqr.food == 0:
                                # last_pos = bo.sentient_action(world.size, energy_multiplier,world)
                                last_pos = bo.sentient_action_rework(energy_multiplier, world)
                                bo.clear_perception()
                            else:
                                last_pos = (bo.x, bo.y)
                                # fix long decimal energy bug
                                bo.energy = round(bo.energy - 0.5, 2)

                            world.move_bob(bo, last_pos)
                            bobs.add(bo)
                        
                        else:
                            print(f'a bob just died at {bo.getPosition()}. He has {bo.energy}')
                            if bo in world.get_square_of_bob(bo).population:
                                world.get_square_of_bob(bo).remove_bob(bo)

                        movement_points = round(movement_points - 1, 2)
                    
                else:
                    if bo in world.get_square_of_bob(bo).population:
                        print("removed for being eaten, tough luck")
                        world.get_square_of_bob(bo).remove_bob(bo)


            world.set_list_bobs(bobs)

            for x in range(0, world.size):
                for y in range(0, world.size):
                    bobs_counter += len(world.get_square(x, y).population)

            print(f'there are currently: {len(bobs)} global or {bobs_counter} sum of all squares bobs in our world')

            ticks += 1
            if ticks >= world.d:
                ticks = 0
                days += 1

                # to avoid division by zero
                if world.number_of_bob() > 0:
                    f = open("sample_data.txt","a")
                    x = world.days
                    y = round((sum([bo.mass for bo in world.get_list_bobs()]) / world.number_of_bob()),2)
                    z = round((sum([bo.velocity for bo in world.get_list_bobs()]) / world.number_of_bob()),2)
                    f.write(f'{x},{y},{z}\n')
                    f.close()

                # spawn food
                world.clear_food()
                world.spawn_food()
                # print('DAY', days)
                # print(world.number_of_bob(), 'in the world right now')
        if(parametres["graphic"]):
            BARRIER.wait()
        time.sleep( 0.1 )

def population_generator(nb: int, w: World):
    """
    Insert nb Bob aléatoirement dans le monde w
    """
    for i in range(nb):
        pos = w.get_random_coordinate()
        w.insert_bob(pos[0], pos[1], Bob.create_default_bob())


def display_iso(w: World):
    """
    Affiche un rendu isométrique du monde
    - input :
        - w (object) : le monde
    """
    m = Map(w.size, parametres["fullscreen"], parametres["resolution"])
    print('its rendering something...')
    global CONTINUE
    global PAUSE
    global SPEED
    speed = parametres["tick_duration"]
    # m = Map(w.size, parametres["fullscreen"])
    m.start()
    m.printFood(w.get_list_food())
    m.printBob(w.get_list_bobs())
    clock = pygame.time.Clock()

    while CONTINUE:
        BARRIER.wait()

        
        m.DISPLAYSURF.fill((0, 0, 0))
        m.start()
        m.printFood(w.get_list_food())
        m.printBob(w.get_list_bobs())
        m.time(w)
        m.printZoom()

        #m.speed_status(SPEED)
        m.printSpeedStatus(SPEED)

        m.DISPLAYSURF.blit(m.STATSURF, (0, 0))
        # print("zoom:",m.zoom)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and PAUSE:
                # print('game is PAUSED')
                mx, my = event.pos
                s_x, s_y = m.check_zone(mx, my)
                if s_x != -1 and s_y != -1:
                    m.status(w.get_square(s_x, s_y))
                    sqr = w.get_square(s_x, s_y)
                    # print(f"you clicked on square {s_x} {s_y} or {sqr.x} {sqr.y}")
                    bobs = sqr.get_population()
                    # print(f'{bobs}')
                    # if bobs:
                    #     print(f'this square has {len(bobs)} bobs ')
                    #     for b in bobs:
                    #         print('-------------')
                    #         print(f'health: {b.energy}')
                    #         print(f'speed: {b.velocity}')
                    #         print(f'mass: {b.mass}')
                    #         print(f'fov: {b.fov}')
                    #         print(f'memory points: {b.memorytoken}')
                    #         print(f'shiny {b.shiny}')

            k=pygame.key.get_pressed()

            if (k[parametres["keys"][4]]):
                BARRIER.wait()
                PAUSE = not PAUSE
                m.STATSURF.fill( (0, 0, 0) )
            if (k[parametres["keys"][2]]):

                SPEED = SPEED - 2
                if SPEED <= 0:
                    SPEED = 2
                # print(SPEED)
            if (k[parametres["keys"][3]]):

                SPEED = SPEED + 2
                if SPEED > 8:
                    SPEED = 8
                # print(SPEED)
            if(k[K_ESCAPE] or k[K_q]):
                CONTINUE = False
                pygame.quit()
            # For the key binding, every symbol seems to be equal to the same integer in Pygame and QT
            # For the letters, QT throws the CAPS version (between 65 and 90) whereas Pygame uses min values (between 97 and 122)
            # For any other key, QT uses weird numbers (around 16777000 to 16777999) while Pygame uses more reasonable numbers (around 200 to 300)
            #           But the key aren't in the same order ex : Pygame        Qt
            #                                               left    276      16777234
            #                                               right   275      16777236
            #                                                up     273      16777235
            #                                               down    274      16777237
            # We might wanna use a conversion table for these weird values or find a library if it exists
            # For other symbols, letters and numbers, a quick addition should do the trick
            # print(K_LEFT, K_RIGHT, K_UP, K_DOWN) # Used for key mapping

            if (k[parametres["keys"][0]] and m.zoom<21):
                m.zoom += 1
                m.initSizeTiles()
                m.didWeZoom +=1
            elif (k[parametres["keys"][1]] and m.zoom>1):
                m.zoom -= 1
                if m.zoom == 1:
                    m.move_x = 0
                    m.move_y = 0
                m.initSizeTiles()
                m.didWeZoom -=1
            elif (k[parametres["keys"][5]] and m.move_x<=1000*m.zoom):
                if m.zoom >1:
                    m.move_x += (10/m.zoom)*m.n
                    m.initSizeTiles()
            elif (k[parametres["keys"][6]] and -1000*m.zoom<=m.move_x):
                if m.zoom >1:
                    m.move_x -= (10/m.zoom)*m.n
                    m.initSizeTiles()
            elif (k[parametres["keys"][7]] and m.move_y<=100*m.zoom):
                if m.zoom >1:
                    m.move_y += (10/m.zoom)*m.n
                    m.initSizeTiles()
            elif (k[parametres["keys"][8]] and -850*m.zoom<=m.move_y):
                if m.zoom >1:
                    m.move_y -= (10/m.zoom)*m.n
                    m.initSizeTiles()

        time.sleep(speed / (1000 * SPEED) ) # durée de la frame (en seconde)


def display_world(w: World, b: list):
    """
    Affiche un rendu simplifié du monde
    - input :
        - w (object) : le monde
        - b (list) : la liste des Bobs
    """
    global CONTINUE

    pygame.init()
    screen_size = 10*w.size
    screen = pygame.display.set_mode((screen_size, screen_size))
    bob_size = 5
    dr = 10

    def draw_food(sqr):
        col = (0, 128, 0)
        pygame.draw.rect(screen, col, pygame.Rect(sqr.x * dr, sqr.y * dr, dr, dr))

    def draw_bob(bo: Bob):
        # (255 - 100) / mutation rate = 1550
        # bob will be more green ( -> yellow because green + red = yellow) if they are faster
        # and less green (more red) if they are slower than average
        col = (255, ( 100 + (bo.velocity - 1) * 1550 ) % 255, 60)
        pygame.draw.rect(screen, col, pygame.Rect(bo.x * dr, bo.y * dr, bob_size, bob_size))

    def draw_population():
        for l_sqr in w.map:
            for sqr in l_sqr:

                if sqr.food > 0:
                    draw_food(sqr)

                for bo in sqr.population:
                    # print(type(bo))
                    draw_bob(bo)

    clock = pygame.time.Clock()

    while CONTINUE:
        BARRIER.wait()
        screen.fill((69, 69, 69))
        draw_population()
        pygame.display.flip()
        clock.tick(60)
        # for event in pygame.event.get():
        #     if event.type == QUIT or (event.type == KEYUP and event.key in (K_ESCAPE, K_q)):
        #         CONTINUE = False
        #         BARRIER.wait()



# Graphs, because we all love graphs
# "Look at this photoGRAPH"
# fun fact: rt stands for real time
def rt_graph():
    fig = plt.figure()
    aii= fig.add_subplot(1,1,1)

    def animate(i):
        pullData = open("sample_data.txt","r").read()
        dataArray = pullData.split('\n')
        xar = []
        yar = []
        for eachLine in dataArray:
            if len(eachLine)>1:
                x,y = eachLine.split(',')
                xar.append(float(x))
                yar.append(float(y))
        ax1.clear()
        ax1.plot(xar,yar)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

# i think we can plot the graph at the end because to make the program easier to handle
def graph():

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    pullData = open("sample_data.txt","r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    y2ar = []

    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y,z = eachLine.split(',')
            xar.append(float(x))
            yar.append(float(y))
            y2ar.append(float(z))
    ax1.clear()
    ax1.plot(xar,yar, label='Average mass')
    ax1.plot(xar,y2ar, label='Average velocity')

    legend = ax1.legend(loc='upper center', shadow=True, fontsize='medium')

    plt.xlabel('Days')

    plt.show()

if __name__ == '__main__':
    parametres = gui()
    # print(parametres["resolution"]) # TEST
    if parametres["validation"]:
        main(parametres)
    else:
        print("Program interrupted")
