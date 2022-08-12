from random import choice
import pygame
from pygame.locals import *
from world import World


# la liste des couleurs possibles pour les cases du terrain
listColorBackground = ["#4a763f", "#558449", "#5c904e", "#416637", "#4a753d", "#679f58", "#68a159", "#49743c",
                       "#466e3b", "#619653", "#49723c", "#609452", "#446839"]

# la liste des couleurs possibles pour les cases du terrain lorsqu'un shiny passe dessus
listColorBackgroundBoss = ["#3F4575", "#485082", "#4E578E", "#373D66", "#3C4472", "#58619E", "#5963A0", "#3B4372",
                       "#3B416D", "#525B93", "#3B4470", "#525B93", "#383F66"]

RED = (255, 0, 0)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
color_stat= GREY
color_speed= GREY

class Map:
    def __init__(self, n, fullscreen, resolution):
        pygame.init()
        try:
            resolution = int(resolution)
            self.screen_w = int(resolution*16/9)
            self.screen_h = resolution
            print("the type of resolution is int")
        except:   
            infoObject = pygame.display.Info()
            self.screen_w = infoObject.current_w
            self.screen_h = int(self.screen_w*9/16)
            print("the type of resolution is str")
        self.zoom = 1
        self.didWeZoom = 0
        self.move_x = 0
        self.move_y = 0
        self.n = n
        self.listColor = [[pygame.Color(choice(listColorBackground)) for j in range(n)] for i in range(n)]
        self.font = pygame.font.SysFont("comicsansms", 24)
        self.SPEED_font = pygame.font.SysFont("comicsansms", 72)
        if fullscreen:
            self.DISPLAYSURF = pygame.display.set_mode((self.screen_w, self.screen_h),
                                                       FULLSCREEN)  # set the display mode, window title and FPS clock
        else:
            self.DISPLAYSURF = pygame.display.set_mode((self.screen_w, self.screen_h))

        # Create a transparent status surface
        self.STATSURF = pygame.surface.Surface( (self.screen_w, self.screen_h) )
        self.STATSURF.set_colorkey( BLACK )

        pygame.display.set_caption('Map Rendering Demo')
        self.w = pygame.image.load('Resources/wallpaperbobross.png').convert_alpha()
        self.w2 = pygame.image.load('Resources/wallpaperbobross2.png').convert_alpha()
        self.wall = pygame.transform.scale(self.w, (self.screen_w,self.screen_h))
        self.wall2 = pygame.transform.scale(self.w2, (self.screen_w,self.screen_h))
        self.cdr = pygame.image.load('Resources/cadre.png').convert_alpha()
        self.bob_n = pygame.image.load('Resources/bob/bob_n.png').convert_alpha()
        self.bob_s = pygame.image.load('Resources/bob/bob_s.png').convert_alpha()
        self.bob_e = pygame.image.load('Resources/bob/bob_e.png').convert_alpha()
        self.bob_w = pygame.image.load('Resources/bob/bob_w.png').convert_alpha()
        self.bob_shiny_n = pygame.image.load('Resources/bob/bob_shiny_n.png').convert_alpha()
        self.bob_shiny_s = pygame.image.load('Resources/bob/bob_shiny_s.png').convert_alpha()
        self.bob_shiny_e = pygame.image.load('Resources/bob/bob_shiny_e.png').convert_alpha()
        self.bob_shiny_w = pygame.image.load('Resources/bob/bob_shiny_w.png').convert_alpha()


        # self.bobSprit = pygame.transform.scale(bob_e, (800 // self.n, 1000 // self.n))
        self.food = pygame.image.load('Resources/steak.png').convert_alpha()

        self.initSizeTiles()

        self.numberDictDnB = {}
        for i in range(10):
            img = pygame.image.load(f'Resources/numbers/{i}.png').convert_alpha()
            self.numberDictDnB[i] = pygame.transform.scale(img, (round(self.screen_w*0.00833333333), round(self.screen_h*0.01851851851))) #(16,20)


        self.numberDictTime = {}
        for i in range(7):
            img = pygame.image.load(f'Resources/time/{i}.png').convert_alpha()
            self.numberDictTime[i]= pygame.transform.scale(img, (round(self.screen_w*0.04166666666), round(self.screen_h*0.11447811447))) #(80, 80*17//11)

        self.numberDictZoom = {}
        for i in range(1,22):
            img = pygame.image.load(f'Resources/zoom/{i}.png').convert_alpha()
            self.numberDictZoom[i]= pygame.transform.scale(img, (round(self.screen_w*0.01510416666), round(self.screen_h*0.11447811447))) #(29, 29*23//4)

        self.numberDictX = {}
        for i in range(1,22):
            img = pygame.image.load(f'Resources/xnumbers/{i}.png').convert_alpha()
            self.numberDictX[i]= pygame.transform.scale(img, (round(self.screen_w*0.03125), round(self.screen_h*0.02287581699))) #(60, 60*7//17)

        bobs = pygame.image.load('Resources/time/bobs.png').convert_alpha()
        self.bSprit = pygame.transform.scale(bobs, (round(self.screen_w*0.04092261904), round(self.screen_h*0.02037037037))) #(22*25//7, 22)
        days = pygame.image.load('Resources/time/days.png').convert_alpha()
        self.dSprit = pygame.transform.scale(days, (round(self.screen_w*0.03392857142), round(self.screen_h*0.02222222222))) #(24*19//7, 24)
        vtss = pygame.image.load('Resources/speed/Speed.png').convert_alpha()
        self.sSprit = pygame.transform.scale(vtss, (round(self.screen_w*0.06), round(self.screen_h*0.03)))


        self.rotateTime = self.numberDictTime[6]  # This will reference our rotated image.
        self.rect = self.rotateTime.get_rect().move((0,0))
        self.angle = 0


    def initSizeTiles(self):
        self.TILEWIDTH = (self.screen_w*self.zoom / self.n)  # holds the tile width and height
        self.TILEHEIGHT = self.TILEWIDTH / 2
        self.TILEHEIGHT_HALF = self.TILEHEIGHT / 2
        self.TILEWIDTH_HALF = self.TILEWIDTH / 2
        self.foodSprit = pygame.transform.scale(self.food, (round(self.screen_w*0.20833333333*self.zoom // self.n), round(self.screen_h*0.46296296296*self.zoom // self.n))) #(400,500)

        self.numberDict = {}
        for i in range(10):
            img = pygame.image.load(f'Resources/numbers/{i}.png').convert_alpha()
            self.numberDict[i] = pygame.transform.scale(img, (round(self.screen_w*0.05208333333*self.zoom // self.n), round(self.screen_h*0.11574074074*self.zoom // self.n))) #(100,125)

        self.numberDictLife = {}
        for i in range(21):
            img = pygame.image.load(f'Resources/life/{i}.png').convert_alpha()
            self.numberDictLife[i] = pygame.transform.scale(img, (round(self.screen_w*0.55729166666*self.zoom // self.n), round(self.screen_h*0.13888888888*self.zoom // self.n)))


    def numberFood(self, nb):
        i = 0
        while nb > 0:
            u = int(nb % 10)
            self.DISPLAYSURF.blit(self.numberDict[u], (
                self.centered_x + self.TILEWIDTH_HALF * (0.95 - i * 0.15),
                self.centered_y - self.TILEHEIGHT_HALF * 1 / 5))
            nb //= 10
            i += 1

    def number(self, nb, line):
        if nb==0:
            self.DISPLAYSURF.blit(self.numberDictDnB[0], (round(self.screen_w*(0.09375+line*0.0078125)), round(self.screen_h*(0.00555555555+line*0.09259259259)))) #(180 + line * 15, 6 + line * 100)
        i = 0
        digits=int(nb)
        while digits > 0:
            digits //= 10
            i += 1
        while nb > 0:
            u = int(nb % 10)
            self.DISPLAYSURF.blit(self.numberDictDnB[u], (round(self.screen_w*(0.08333333333+line*0.0078125+i*0.01041666666)), round(self.screen_h*(0.00555555555+line*0.09259259259)))) #(160+i*20+line*15, 6+line*100)
            nb //= 10
            i += -1

    def life(self, energy, mass):
        if energy>=0 and mass >=0:
            i = int(energy / 10)
            self.DISPLAYSURF.blit(self.numberDictLife[i], (
            int(self.centered_x + self.TILEWIDTH_HALF / 3), int(self.centered_y - (2.5 * mass ** (1 / 3)) * self.TILEHEIGHT_HALF)))


    def positionnement(self, x, y):
        cart_x = x * self.TILEWIDTH_HALF
        cart_y = y * 2 * self.TILEHEIGHT_HALF
        iso_x = (cart_x - cart_y)
        iso_y = (cart_x + cart_y) / 2
        self.centered_x = (self.DISPLAYSURF.get_rect().centerx + iso_x - self.TILEWIDTH_HALF)+self.move_x
        self.centered_y = (self.DISPLAYSURF.get_rect().centery / 5 + iso_y + (0.54629629629*self.screen_h)//self.n + self.n//(0.09259259259*self.screen_h))+self.move_y #590_100

    def check_zone(self, x, y):
        for i in range(self.n):
            for j in range(self.n):
                self.positionnement(i, j)
                if (x - self.centered_x - self.TILEWIDTH_HALF) ** 2 + (y - self.centered_y) ** 2 <= (self.TILEHEIGHT_HALF * 3 / 4) ** 2:
                    return i, j
        return (-1, -1)

    def status(self, sqr):
        bobs = sqr.population
        self.STATSURF.fill( BLACK )
        # print("status is called")
        if bobs:
            # print("we have bobs in this square")
            self.positionnement(sqr.x, sqr.y)
            tmpx, tmpy = (self.centered_x, self.centered_y)
            # print(tmpx, tmpy)
            for b in bobs:
                nstr = f"{b.name}"
                nw, nh = self.font.size(nstr)
                nf = self.font.render(nstr, True, color_stat)
                self.STATSURF.blit(nf, (tmpx, tmpy))
                tmpy = tmpy + nh

                hstr = f"health: {b.energy}"
                hw, hh = self.font.size(hstr)
                hf = self.font.render(hstr, True, color_stat)
                self.STATSURF.blit(hf, (tmpx, tmpy))
                tmpy = tmpy + hh

                sstr = f"speed: {b.velocity}"
                sw, sh = self.font.size(sstr)
                sf = self.font.render(sstr, True, color_stat)
                self.STATSURF.blit(sf, (tmpx, tmpy))
                tmpy = tmpy + sh

                mstr = f"mass: {b.mass}"
                mw, mh = self.font.size(mstr)
                mf = self.font.render(mstr, True, color_stat)
                self.STATSURF.blit(mf, (tmpx, tmpy))
                tmpy = tmpy + mh

                fstr = f"fov: {b.fov}"
                fw, fh = self.font.size(fstr)
                ff = self.font.render(fstr, True, color_stat)
                self.STATSURF.blit(ff, (tmpx, tmpy))
                tmpy = tmpy + fh

    def speed_status(self, speed):
        spdstr = f"{int(speed/2)}X speed"
        spdw, spdh = self.SPEED_font.size(spdstr)
        spdf = self.SPEED_font.render(spdstr, True, color_speed)
        self.STATSURF.fill( BLACK, (250, 0, spdw, spdh) )
        self.STATSURF.blit(spdf, (250, 0))

        # pygame.draw.rect(self.STATSURF, (0, 0, 100), (self.centered_x, self.centered_y, 200, 200) )
        # self.STATSURF.blit(texts[0], (self.centered_x, self.centered_y))

    def printSpeedStatus(self, speed):
        self.DISPLAYSURF.blit(self.sSprit,(int(self.screen_w*0.921875), round(6))) #(1920-150, 6)
        self.DISPLAYSURF.blit(self.numberDictX[int(speed/2)],(int(self.screen_w*0.890625), round(6))) #(1920-210, 6)

    def start(self):
        # print("values", self.bobSprit, bob_e)
        if (self.didWeZoom):
            self.DISPLAYSURF.blit(self.wall2, (0,0))
            if (self.zoom <= 8):
                self.cadre = pygame.transform.scale(self.cdr, (self.screen_w*self.zoom,round(self.screen_h*0.55555555555*self.zoom))) #1920/600
                self.positionnement(0, self.n)
                self.DISPLAYSURF.blit(self.cadre, (self.centered_x + self.TILEWIDTH_HALF, self.centered_y - self.TILEHEIGHT_HALF * 5/4))
        else:
            self.DISPLAYSURF.blit(self.wall, (0,0))
        for x in range(self.n):
            for y in range(self.n):
                self.positionnement(x, y)
                pygame.draw.polygon(self.DISPLAYSURF, self.listColor[x][y], [(self.centered_x, self.centered_y), (
                    self.centered_x + self.TILEWIDTH_HALF, self.centered_y - self.TILEHEIGHT_HALF),
                                                                             (self.centered_x + self.TILEWIDTH,
                                                                              self.centered_y),
                                                                             (self.centered_x + self.TILEWIDTH_HALF,
                                                                              self.centered_y + self.TILEHEIGHT_HALF)])



    '''def printBob(self, m): #comment récuperer l'energie d'un bob à partir de world et non des bobs?
        for lines in m:
            for sqr in lines:
                if sqr.population > 0:
                    x = sqr.x
                    y = sqr.y
                    self.positionnement(x,y)
                    self.DISPLAYSURF.blit(self.bobSprit,(self.centered_x + self.TILEWIDTH_HALF / 2, self.centered_y - 2 * self.TILEHEIGHT_HALF))
                    self.life(energy)'''


    def bobSize(self, size, orientation):
        if (orientation=='N'):
            self.bobSprit = pygame.transform.scale(self.bob_n, (
                int((0.41666666666*self.screen_w * (size ** (1 / 3)))*self.zoom // self.n), round((0.92592592592*self.screen_h * (size ** (1 / 3)))*self.zoom // self.n))) #800_1000
        elif (orientation=='S'):
            self.bobSprit = pygame.transform.scale(self.bob_s, (
                int((0.41666666666*self.screen_w * (size ** (1 / 3)))*self.zoom // self.n), round((0.92592592592*self.screen_h * (size ** (1 / 3)))*self.zoom // self.n)))
        elif (orientation=='E'):
            self.bobSprit = pygame.transform.scale(self.bob_e, (
                int((0.41666666666*self.screen_w * (size ** (1 / 3)))*self.zoom // self.n), round((0.92592592592*self.screen_h * (size ** (1 / 3)))*self.zoom // self.n)))
        elif (orientation=='W'):
            self.bobSprit = pygame.transform.scale(self.bob_w, (
                int((0.41666666666*self.screen_w * (size ** (1 / 3)))*self.zoom // self.n), round((0.92592592592*self.screen_h * (size ** (1 / 3)))*self.zoom // self.n)))
        if size <= 1:
            self.DISPLAYSURF.blit(self.bobSprit, (
                self.centered_x + (self.TILEWIDTH_HALF * size ** (1 / 3)) / (0.7 + (size - 0.1) * 10 / 1.3) + (0.20833333333*self.screen_w * size)*self.zoom // self.n, self.centered_y - 2 * self.TILEHEIGHT_HALF * (size ** (1 / 3)))) #400
        else:
            self.DISPLAYSURF.blit(self.bobSprit, (
                self.centered_x + (self.TILEWIDTH_HALF * size ** (1 / 3)) / (0.7 + (size - 0.1) * 10 / 1.3) + (0.20833333333*self.screen_w - 39 * size) // self.n, self.centered_y - 2 * self.TILEHEIGHT_HALF * (size ** (1 / 3))))

    def bobSize_shiny(self, size, orientation): 
        if (orientation=='N'):
            self.bobSprit = pygame.transform.scale(self.bob_shiny_n, (
                int((0.41666666666*self.screen_w * (size ** (1 / 3)))*self.zoom // self.n), round((0.92592592592*self.screen_h * (size ** (1 / 3)))*self.zoom // self.n))) #800_1000
        elif (orientation=='S'):
            self.bobSprit = pygame.transform.scale(self.bob_shiny_s, (
                int((0.41666666666*self.screen_w * (size ** (1 / 3)))*self.zoom // self.n), round((0.92592592592*self.screen_h * (size ** (1 / 3)))*self.zoom // self.n)))
        elif (orientation=='E'):
            self.bobSprit = pygame.transform.scale(self.bob_shiny_e, (
                int((0.41666666666*self.screen_w * (size ** (1 / 3)))*self.zoom // self.n), round((0.92592592592*self.screen_h * (size ** (1 / 3)))*self.zoom // self.n)))
        elif (orientation=='W'):
            self.bobSprit = pygame.transform.scale(self.bob_shiny_w, (
                int((0.41666666666*self.screen_w * (size ** (1 / 3)))*self.zoom // self.n), round((0.92592592592*self.screen_h * (size ** (1 / 3)))*self.zoom // self.n)))
        if size <= 1:
            self.DISPLAYSURF.blit(self.bobSprit, (
                self.centered_x + (self.TILEWIDTH_HALF * size ** (1 / 3)) / (0.7 + (size - 0.1) * 10 / 1.3) + (0.20833333333*self.screen_w * size)*self.zoom // self.n, self.centered_y - 2 * self.TILEHEIGHT_HALF * (size ** (1 / 3)))) #400

        else:
            self.DISPLAYSURF.blit(self.bobSprit, (
                self.centered_x + (self.TILEWIDTH_HALF * size ** (1 / 3)) / (0.7 + (size - 0.1) * 10 / 1.3) + (0.20833333333*self.screen_w - 39 * size) // self.n, self.centered_y - 2 * self.TILEHEIGHT_HALF * (size ** (1 / 3))))


    # def printBob(self, w):
    #     for x in range(self.n):
    #         for y in range(self.n):
    #             sqr = w.get_square(x, y)
    #             bobs = sqr.get_population()
    #             if bobs:
    #                 for bob in bobs: 
    #                     energy = bob.getEnergy()
    #                     mass = bob.getMass()
    #                     orientation=bob.getOrientation()
    #                     shiny=bob.getShiny()
    #                     self.positionnement(x, y)
    #                     # print("size :", mass)
    #                     if shiny and mass>=0:
    #                         self.bobSize_shiny(mass,orientation)
    #                         self.listColor[x][y] = pygame.Color(choice(listColorBackgroundBoss))
    #                     elif mass>=0:
    #                         self.bobSize(mass,orientation)
    #                     self.life(energy, mass)

    def printBob(self, listBob):
        for bob in listBob:
            (x, y) = bob.getPosition()
            energy = bob.getEnergy()
            mass = bob.getMass()
            orientation=bob.getOrientation()
            shiny=bob.getShiny()
            self.positionnement(x, y)
            # print("size :", mass)
            if shiny and mass>=0:
                self.bobSize_shiny(mass,orientation)
                self.listColor[x][y] = pygame.Color(choice(listColorBackgroundBoss))
            elif mass>=0:
                self.bobSize(mass,orientation)
            self.life(energy, mass)

    def printFood(self, foods):
        for pos in foods:
            self.positionnement(pos[0], pos[1])
            self.DISPLAYSURF.blit(self.foodSprit,
                          (self.centered_x + self.TILEWIDTH_HALF * 4 / 5, self.centered_y - self.TILEHEIGHT_HALF * 4 / 5))
            self.numberFood(foods[pos])
        # for lines in m:
        #     for sqr in lines:
        #         if sqr.food > 0:
        #             x = sqr.x
        #             y = sqr.y
        #             self.positionnement(x, y)
        #             self.DISPLAYSURF.blit(self.foodSprit,
        #                           (self.centered_x + self.TILEWIDTH_HALF * 4 / 5, self.centered_y - self.TILEHEIGHT_HALF * 4 / 5))
        #             self.numberFood(sqr.food)

    def time(self, w):
        if (w.d>=6):
            unit=int(w.d/6)
            frame=int(w.ticks/unit)
            if (frame==6):
                self.rot = pygame.transform.rotate(self.rotateTime, self.angle)
                self.angle += 30 % 180
                self.DISPLAYSURF.blit(self.rot,(round(0.00625*self.screen_w), round(0.00555555555*self.screen_h))) #(12, 6)
            elif 0<=frame<=5 :
                self.DISPLAYSURF.blit(self.numberDictTime[frame],(round(0.00625*self.screen_w), round(0.00555555555*self.screen_h))) #(12, 6)
            else :
                self.DISPLAYSURF.blit(self.numberDictTime[0],(round(0.00625*self.screen_w), round(0.00555555555*self.screen_h)))
            self.DISPLAYSURF.blit(self.dSprit,(round(0.05208333333*self.screen_w), round(0.00555555555*self.screen_h))) #(100, 6)
            self.DISPLAYSURF.blit(self.bSprit,(round(0.05208333333*self.screen_w), round(0.09722222222*self.screen_h))) #(100, 105)
            self.number(w.days, 0)
            self.number(w.number_of_bob(), 1)


        else :
            self.DISPLAYSURF.blit(self.dSprit,(round(0.02604166666*self.screen_w), round(0.00555555555*self.screen_h))) #(50, 6)
            self.DISPLAYSURF.blit(self.bSprit,(round(0.02604166666*self.screen_w), round(0.09722222222*self.screen_h))) #(50, 105)
            self.number(w.days, 0)
            self.number(w.number_of_bob(), 1)

    def printZoom(self):
        self.DISPLAYSURF.blit(self.numberDictZoom[self.zoom],(round(0.00625*self.screen_w), round(0.14814814814*self.screen_h))) #(12, 160)
        self.DISPLAYSURF.blit(self.numberDictX[self.zoom],(round(0.02604166666*self.screen_w), round(0.21296296296*self.screen_h))) #(50, 230)
        
