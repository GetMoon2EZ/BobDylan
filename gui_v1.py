from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QImage,QPalette, QBrush
import csv
from key_solver import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        reader=self.readConfig()
        self.title = "Welcome To The Game"
        self.width = 1000
        self.height = 800
        self.top = (1080-self.height)/2
        self.left = (1920-self.width)/2

        # Initializing every settings according to the "conf.cfg" file
        # If any value has been manually set to an invalid format, it should get caught and a default value will then be attributed

        try:
            self.nbTicks = int(next(reader))
        except:
            self.nbTicks = 100
        try:
            self.tick_duration = int(next(reader))
        except:
            self.tick_duration = 10
        try:
            self.world_size = int(next(reader))
        except:
            self.world_size = 100
        try:
            self.population = int(next(reader))
        except:
            self.population = 25
        try:
            self.food_per_day = int(next(reader))
        except:
            self.food_per_day = 1000
        try:
            self.speed = float(next(reader))
        except:
            self.speed = 1
        try:
            self.mass = float(next(reader))
        except:
            self.mass = 1
        try:
            self.fov = int(next(reader))
        except:
            self.fov = 3

        self.speed_mutation = (next(reader)=="True")
        self.mass_mutation = (next(reader)=="True")
        self.fov_mutation = (next(reader)=="True")

        try:
            self.reproduction_method = int(next(reader))
        except:
            self.reproduction_method = 0

        try:
            self.memory = int(next(reader))
        except:
            self.memory = 0
        if next(reader)=="True":
            self.memory_mutation = True
        else:
            self.memory_mutation = False

        if next(reader)=="False":
            self.graphic = False
        else:
            self.graphic = True
        if next(reader)=="Top View : 2D":
            self.display_type = "Top View : 2D"
        else:
            self.display_type = "Isometric : 2.5D"
        if next(reader)=="False":
            self.fullscreen = False
        else:
            self.fullscreen = True
        saved_resolution = next(reader)
        if saved_resolution in ["Auto","1080p","720p","480p","240p"]:
            self.resolution = saved_resolution
        else:
            self.resolution = "Auto"

        next(reader)        #Skipping Over the explanation line

        self.keyDictionnary={"zoom_in": 0, "zoom_out":1, "slow_time":2, "speed_up_time":3, "pause_game":4,"move_left":5, "move_right":6, "move_up":7, "move_down":8}
        self.defaultKeys=[ord('I'),ord('O'),ord('A'),ord('D'),Qt.Key_Space, Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]
        self.defaultKeysLabel=["I", "O", "A", "D", "Space", "Left Arrow", "Right Arrow", "Up Arrow", "Down Arrow"]

        self.keyList=[]
        for i in range(9): #Filling up the list with the memorized key ("_" by default)
            try:
                self.keyList.append(int(next(reader)))
            except:
                self.keyList.append(self.defaultKeys[i])

        next(reader)

        # print(Qt.Key_F1)  # Used for key mapping

        self.currentWindow = 1 #Variable to know in which window the user currently is
        self.validation = False
        self.init_window()
        self.initFirstWindow()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.currentWindow==2:
                self.onValidationClick()
            else:
                self.initSecondWindow()
        if event.key() == Qt.Key_Escape:
            if self.currentWindow==2:
                self.initFirstWindow()
            else:
                self.onQuitClick()


    def init_window(self):
        self.layout = []       # Pur all the widgets that are in the 2nd page in this list (for page switch purposes)
        self.layoutLandingPage = []  # Put all the widgets that are in the landing page in this list (for page switch purposes)
        self.layoutLabel = []  # Put all the labels in this list (for language switch purposes)
        self.buttonList = []   # All the press button shall be put in this list so that the language change can work
        self.buttonKeyBindList=[]
        self.tabList = []      # All the tabs shall be put in this list so that the language change can work
        self.comboBoxList = [] # All the comboBox shall be put in this list so that the language change can work
        self.groupList=[]      # All the groups shall be put in this list (for language switch AND page switch puposes)
        self.setFixedSize(self.width, self.height)      #Set the size of the window
        self.move(self.left, self.top)      #window displayed windowed 1920 x 1080
        #size=QDesktopWidget().screenGeometry(-1)
        #self.setGeometry(self.top, self.left, size.width(), size.height())  # window displayed in windowed mode (but at screen size)
        #self.setWindowState(Qt.WindowFullScreen)                                    # window displayed in fullscreen

        ##################################################################################

        #sélection de langue ?                      Si on l'implémente je pensais faire comme ça
        #comboBox => différentes langues
        #On récupère l'index, on a une liste contenant les listes de tous les label dans chacune des langues puis on récupère la bonne liste avec l'indice de la combobox
        # Ex : langage=[["title", "population", "world size"],["titre", "population", "taille du monde"], [titulo, "poblation", "tamaño del mundo"]]
        #       self.labeltitle=QLabel(langage[indice_combobox][0]) etc ...
        # Il faudrait peut-être récupérer l'indice pour la simulation pour écrire "jour" au lieux de "day" par exemple

        # Problèmes éventuels : le texte sera plus ou moins long en fonction de la langue, faudrait mieux gérer les positions des widgets adjacents
        # Problème résolu thx to layouts
        self.language=[]

        english=["Settings", "Number of ticks per day :","Tick duration :", "Population :","Number of food per day :", "Speed mutation : ", "Initial speed :", "How to play", "World Size :","Graphic display :",
        "Display type :", "Display mode :", "Resolution :", "Mass mutation : ", "Initial mass :", "Bob's default FOV :","tiles", "FOV mutation : ", "Reproduction method : ", "Memory mutation : ", "Memory Capacity : ",
        "Current key", "Default Key", "Zoom +", "Zoom -", "Slow Time", "Speed Up Time", "Pause Game", "Move Left", "Move Right", "Move Up", "Move Down",
        "Play !", "Back", "Quit", "Let's Go !",
        "World Settings","Bob Properties","Display", "Controls",
        "Ticks Parameters", "Population Parameters", "Food Parameters", "Speed Parameters", "World Parameters",  "Display Parameters",  "Mass Parameters", "FOV Parameters", "Reproduction Parameters", "Memory Parameters",
        "Isometric : 2.5D", "Top View 2D", "Fullscreen", "Windowed", "None", "Solo", "Duo", "Solo & Duo"]

        french=["Paramètres", "Nombre de ticks par jour :", "Durée d'un tick :", "Population :", "Nombre de nourriture par jour :", "Mutation de la vitesse :", "Vitesse initiale :", "Comment jouer", "Taille du monde :", "Affichage graphique :",
        "Type d'affichage :", "Mode d'affichage :","Résolution :", "Mutation de la masse :", "Masse initiale :", "FOV par défaut :", "cases", "Mutation du FOV :", "Méthode de reproduction :", "Mutation de la mémoire : ", "Capacité mémorielle : ",
        "Touche actuelle", "Touche par défaut", "Zoom +", "Zoom -", "Ralentir le temps", "Accélérer le temps", "Pauser le jeu", "Aller à Gauche", "Aller à Droite", "Avancer", "Reculer",
        "Jouer !", "Retour", "Quitter", "Allons-y !",
        "Paramètres du monde","Propriétés des Bobs","Affichage","Contrôles",
        "Réglages des Ticks", "Réglages de la Population", "Réglages de la Nourriture", "Réglages de la Vitesse", "Réglages du Monde", "Paramètres d'Affichage", "Réglages de la masse", "Réglages du FOV", "Réglages de la Reproduction", "Réglages de la mémoire",
        "Isométrique : 2.5D", "Vue du dessus : 2D", "Plein Écran", "Fenêtré", "Aucune", "Solo", "Duo", "Solo & Duo"]

        spanish=["Configuración", "Número de ticks por día :", "Duración del tick :", "Población :", "Número de alimentos por día :", "Mutación de la velocidad :", "Velocidad inicial :", "Cómo jugar" , "Tamaño mundial :", "Pantalla gráfica :",
        "Tipo de visualización :", "Modo de visualización :","Resolución :", "Mutación de la masa :", "Masa inicial :", "FOV predeterminado de Bob :", "mosaicos", "Mutación del FOV :", "Método de reproducción :", "Mutación de la memoria : ", "Capacidad de memoria : ",
        "Tecla actual", "Tecla predeterminada", "Zoom +", "Zoom -", "Ralentización del Tiempo", "Aceleración del Tiempo", "Pausa del juego", "Ir a la izquierda", "Ir a la derecha" , "Avanzar", "Retroceder",
        "Jugar", "Volver", "Salir", "¡Vamos!",
        "Configuración del mundo", "Propiedades de Bob", "Pantalla","Controles",
        "Parámetros de Tick", "Parámetros de población", "Parámetros de alimentos", "Parámetros de velocidad", "Parámetros mundiales", "Parámetros de visualización", "Parámetros de masa", "Parámetros de FOV", "Parámetros de reproducción","Parámetros de memoria",
        "Isométrico: 2.5D", "Vista superior: 2D", "Pantalla completa", "Ventana", "Ninguno", "Solo", "Duo", "Solo & Duo"]

        boblanguage=["Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob",
        "Bob", "Bob", "Bob", "Bob", "Bob", "Bob","Bob", "Bob", "Bob", "Bob", "Bob", "Bob","Bob","Bob",
        "Bob","Bob","Bob","Bob !",
        "Bob","Bob","Bob","Bob",
        "Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob",
        "Bob","Bob","Bob","Bob","Bob","Bob","Bob","Bob"]


        self.language.append(english)
        self.language.append(french)
        self.language.append(spanish)
        self.language.append(boblanguage)

        self.comboBoxLanguage=QComboBox(self)
        self.comboBoxLanguage.move(875,750)

        ukFlagPixmap = QtGui.QPixmap("Resources/GUI/Flags/uk_flag.svg")
        ukFlag = QtGui.QIcon(ukFlagPixmap)
        self.comboBoxLanguage.addItem(ukFlag, "English")

        frFlagPixmap = QtGui.QPixmap("Resources/GUI/Flags/fr_flag.png")
        frFlag = QtGui.QIcon(frFlagPixmap)
        self.comboBoxLanguage.addItem(frFlag, "Français")

        spFlagPixmap = QtGui.QPixmap("Resources/GUI/Flags/sp_flag.png")
        spFlag = QtGui.QIcon(spFlagPixmap)
        self.comboBoxLanguage.addItem(spFlag, "Español")

        bobFlagPixmap = QtGui.QPixmap("Resources/GUI/Flags/bob_flag.png")
        bobFlag =QtGui.QIcon(bobFlagPixmap)
        self.comboBoxLanguage.addItem(bobFlag, "Bob")
        self.comboBoxLanguage.currentTextChanged.connect(self.switchLanguage)

        ##################################################################################              Title initialization

        parametersWidth = 500
        parametersHeight = 100
        positionParametersX = (self.width/2) - (parametersWidth/2)
        positionParametersY = 10
        self.labelTitle=QLabel("Settings",self)
        self.labelTitle.setFont(QtGui.QFont('Arial', 50))
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.labelTitle.setGeometry(positionParametersX,positionParametersY,parametersWidth, parametersHeight)
        #self.labelTitle.setStyleSheet("color : #ff3030;")
        self.layoutLabel.append(self.labelTitle)


        ##################################################################################              Number of Ticks per day / Initial Tick duration

        self.ticksParameters=TicksParameters(self)
        self.groupTicks=GroupBox(self, "Ticks Parameters", [self.ticksParameters.labelNbTicks,0,0], [self.ticksParameters.lineEditNbTicks,0,1],
        [self.ticksParameters.labelTickDuration,1,0], [self.ticksParameters.lineEditTickDuration,1,1], [self.ticksParameters.labelTickDurationUnit,1,2])
        self.groupList.append(self.groupTicks)


        ##################################################################################              Initial Population

        self.populationParameters=PopulationParameters(self)
        self.groupPopulation=GroupBox(self, "Population Parameters",
        [self.populationParameters.sliderPopulationMinimum,0,0],[self.populationParameters.sliderPopulation,0,1],[self.populationParameters.sliderPopulationMaximum,0,2],
        [self.populationParameters.labelPopulation,1,0], [self.populationParameters.lineEditPopulation,1,1])
        self.groupList.append(self.groupPopulation)
        ##################################################################################              Number of food per day

        self.foodParameters=FoodParameters(self)
        self.groupFood = GroupBox(self, "Food Parameters", [self.foodParameters.labelNbFood,0,0], [self.foodParameters.lineEditNbFood,0,1])
        self.groupList.append(self.groupFood)

        ##################################################################################              Initial Speed + Speed mutation toggle

        self.speedParameters=SpeedParameters(self)
        self.groupSpeed=GroupBox(self,"Speed Parameters", [self.speedParameters.labelSpeed,0,0],
        [self.speedParameters.checkBoxSpeed,0,1],[self.speedParameters.labelSpeedInit,1,0],[self.speedParameters.lineEditSpeedInit,1,1])
        self.groupList.append(self.groupSpeed)

        ###################################################################################            "Play", "Quit", "Back" and "Let Go !" buttons initialisation

        validationHeight = 50
        validationWidth = 200
        positionValidationX = (self.width/2) - (validationWidth/2)
        positionValidationY = self.height-60
        playWidth = 300
        playHeight = 100
        positionPlayX = (self.width-playWidth)/2
        positionPlayY = (self.height-(playHeight)-50)

        self.playButton=QPushButton("Play !",self)
        self.playButton.setFont(QtGui.QFont('Arial', 35))
        self.playButton.setGeometry(positionPlayX, positionPlayY, playWidth, playHeight)
        self.playButton.clicked.connect(self.initSecondWindow)
        self.layoutLandingPage.append(self.playButton)
        self.buttonList.append(self.playButton)

        positionBackButtonX=50
        positionBackButtonY=self.height-60
        self.backButton = QPushButton('Back', self)
        self.backButton.setGeometry(positionBackButtonX,positionBackButtonY,validationWidth,validationHeight)
        self.backButton.clicked.connect(self.initFirstWindow)
        self.layout.append(self.backButton)
        self.buttonList.append(self.backButton)

        positionQuitButtonX=50
        positionQuitButtonY=self.height-115
        quitWidth = 100
        quitHeight = 50
        self.quitButton = QPushButton('Quit', self)
        self.quitButton.setGeometry(positionQuitButtonX,positionQuitButtonY,quitWidth,quitHeight)
        self.quitButton.clicked.connect(self.onQuitClick)
        self.layoutLandingPage.append(self.quitButton)
        self.buttonList.append(self.quitButton)

        self.validationButton = QPushButton("Let's Go !", self)
        self.validationButton.setGeometry(positionValidationX, positionValidationY,validationWidth,validationHeight)
        self.layout.append(self.validationButton)
        self.validationButton.clicked.connect(self.onValidationClick)
        self.layout.append(self.validationButton)
        self.buttonList.append(self.validationButton)



        ##################################################################################                  Help button initialisation

        positionHelpX=self.width-50
        positionHelpY=10
        self.helpButton = QPushButton("?", self)
        self.helpButton.setGeometry(positionHelpX,positionHelpY,40,25)
        self.layout.append(self.helpButton)
        self.helpButton.clicked.connect(self.needHelp)

        self.labelHelp = QLabel("How to play", self)
        self.labelHelp.setGeometry(positionHelpX-130,positionHelpY+4,125,25)
        self.labelHelp.setAlignment(Qt.AlignRight)
        self.layoutLabel.append(self.labelHelp)

        ##################################################################################                  World Size Parameters

        self.worldSizeParameters=WorldSizeParameters(self)

        self.groupWorldSize=GroupBox(self,"World Parameters",
        [self.worldSizeParameters.sliderWorldSizeMinimum,0,0],[self.worldSizeParameters.sliderWorldSizeMaximum,0,2],[self.worldSizeParameters.sliderWorldSize,0,1],
        [self.worldSizeParameters.labelWorldSize,1,0],[self.worldSizeParameters.lineEditWorldSize,1,1])

        self.groupList.append(self.groupWorldSize)

        ###################################################################################                 Graphic Display

        self.displayParameters= DisplayParameters(self)

        self.groupDisplay=GroupBox(self, "Display Parameters", [self.displayParameters.labelGraphic,0,0],
        [self.displayParameters.checkBoxGraphic,0,1],[self.displayParameters.labelDisplayType,1,0],[self.displayParameters.comboBoxDisplayType,1,1],
        [self.displayParameters.labelFullscreen,2,0],[self.displayParameters.comboBoxFullscreen,2,1],[self.displayParameters.labelResolution,3,0],
        [self.displayParameters.comboBoxResolution,3,1])

        self.groupList.append(self.groupDisplay)

        ###################################################################################                 Mass Parameters

        self.massParameters=MassParameters(self)

        self.groupMass=GroupBox(self, "Mass Parameters",[self.massParameters.labelMass,0,0],
        [self.massParameters.checkBoxMass,0,1], [self.massParameters.labelMassInit,1,0], [self.massParameters.lineEditMassInit,1,1])

        self.groupList.append(self.groupMass)

        ###################################################################################                 FOV Parameters

        self.fovParameters = FOVParameters(self)

        self.groupFOV = GroupBox(self, "FOV Parameters", [self.fovParameters.labelFOVMutation,0,0],
        [self.fovParameters.checkBoxFOV,0,1],[self.fovParameters.labelFOV,1,0],[self.fovParameters.lineEditFOV,1,1],[self.fovParameters.labelFOVTiles,1,2])

        self.groupList.append(self.groupFOV)

        ###################################################################################                 Reproduction Method


        self.reproductionParameters = ReproductionParameters(self)

        self.groupReproduction = GroupBox(self, "Reproduction Parameters",
        [self.reproductionParameters.labelReproduction,0,0],[self.reproductionParameters.comboBoxReproduction,0,1])

        self.groupList.append(self.groupReproduction)

        ##################################################################################                  Memory Parameters

        self.memoryParameters = MemoryParameters(self)

        self.groupMemory = GroupBox(self, "Memory Parameters",
        [self.memoryParameters.labelMemoryMutation,0,0], [self.memoryParameters.checkBoxMemory,0,1], [self.memoryParameters.labelMemory,1,0], [self.memoryParameters.lineEditMemory,1,1])

        self.groupList.append(self.groupMemory)

        ###################################################################################                 Tabs Initialisation
        layouttest=QGridLayout()
        layouttest.addWidget(self.groupWorldSize,0,0)
        layouttest.addWidget(self.groupPopulation,1,0)

        self.setStyle(ProxyStyle())
        self.tab=TabWidget(self)
        self.tab.setGeometry(40,125,900,600)

        self.firsttabWidget=WidgetforTab(self,[layouttest,0,0,1,2], [self.groupFood,2,0], [self.groupTicks,2,1])
        self.tab.addTab(self.firsttabWidget, "World Settings")
        self.tabList.append(self.firsttabWidget)

        self.secondTabWidget=WidgetforTab(self, None,[self.groupMass,0,0],[self.groupSpeed,0,1], [self.groupFOV,1,0],[self.groupReproduction,1,1], [self.groupMemory,2,0])
        self.tab.addTab(self.secondTabWidget, "Bob Properties")
        self.tabList.append(self.secondTabWidget)

        self.thirdTabWidget=WidgetforTab(self, None, [self.groupDisplay,0,0])
        self.tab.addTab(self.thirdTabWidget, "Display")
        self.tabList.append(self.thirdTabWidget)

        self.keys = KeyBinding(self)
        self.widgetKeybind = WidgetforTab(self, [self.keys.layoutKeybind,0,0,1,1])
        self.zoomIn=WidgetforTab(self, [self.keys.zoomIn.keyLayout,0,0,1,1])
        self.zoomOut=WidgetforTab(self, [self.keys.zoomOut.keyLayout,0,0,1,1])
        self.slowTime=WidgetforTab(self, [self.keys.slowTime.keyLayout,0,0,1,1])
        self.speedUpTime=WidgetforTab(self, [self.keys.speedUpTime.keyLayout,0,0,1,1])
        self.pauseGame=WidgetforTab(self, [self.keys.pauseGame.keyLayout,0,0,1,1])
        self.moveLeft=WidgetforTab(self, [self.keys.moveLeft.keyLayout,0,0,1,1])
        self.moveRight=WidgetforTab(self, [self.keys.moveRight.keyLayout,0,0,1,1])
        self.moveUp=WidgetforTab(self, [self.keys.moveUp.keyLayout,0,0,1,1])
        self.moveDown=WidgetforTab(self, [self.keys.moveDown.keyLayout,0,0,1,1])

        self.fourthTabWidget=WidgetforTab(self, None,[self.widgetKeybind,0,0], [self.zoomIn, 1, 0],[self.zoomOut,2,0], [self.slowTime,3,0],
        [self.speedUpTime,4,0], [self.pauseGame,5,0], [self.moveLeft,6,0], [self.moveRight,7,0], [self.moveUp,8,0], [self.moveDown,9,0])
        self.tab.addTab(self.fourthTabWidget, "Controls")
        self.tabList.append(self.fourthTabWidget)

        ###################################################################################                 Window Initialisation

        self.setWindowTitle(self.title)
        self.show()

    #########################################################################################################
    #                                                                                                       #
    #                                              Methods                                                  #
    #                                                                                                       #
    #########################################################################################################

    def initFirstWindow(self):
        for i in self.layout:
            i.hide()
        for i in self.layoutLabel:
            i.hide()
        for i in self.layoutLandingPage:
            i.show()
        self.tab.hide()

        oImage=QImage("Resources/GUI/Backgrounds/background_resized.png")
        sImage = oImage.scaled(QSize(self.width,self.height))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette2)

        self.currentWindow=1

    def initSecondWindow(self):
        for i in self.layout:
            i.show()
        for i in self.layoutLabel:
            i.show()
        for i in self.layoutLandingPage:
            i.hide()
        self.tab.show()

        oImage=QImage("Resources/GUI/Backgrounds/background-test.png")
        sImage = oImage.scaled(QSize(self.width,self.height))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.currentWindow=2

        if self.graphic:
            self.displayParameters.checkBoxGraphic.setCheckState(Qt.Checked)
        else:
            self.displayParameters.checkBoxGraphic.setCheckState(Qt.Unchecked)
        self.displayParameters.displayTypeSelection()

    def switchLanguage(self):
        j=0
        tabIndex=1
        currentTab=self.tab.currentIndex()
        # currentLanguage=self.comboBoxLanguage.currentIndex()
        for i in self.layoutLabel:
            i.setText(self.language[self.comboBoxLanguage.currentIndex()][j])
            j+=1
        for i in self.buttonList:
            i.setText(self.language[self.comboBoxLanguage.currentIndex()][j])
            j+=1
        for i in self.tabList:
            self.tab.removeTab(tabIndex)
            self.tab.insertTab(tabIndex, i, self.language[self.comboBoxLanguage.currentIndex()][j])
            tabIndex+=1
            j+=1
        self.tab.setCurrentIndex(currentTab) #On remet l'affichage a l'ancien Index, ce qui permet de rester sur un tab tout en changeant de langue
        for i in self.groupList:
            i.setTitle(self.language[self.comboBoxLanguage.currentIndex()][j])
            j+=1
        for i in self.comboBoxList:
            numberOfItems=i.count()
            for x in range(numberOfItems):
                i.setItemText(x, self.language[self.comboBoxLanguage.currentIndex()][j])
                j+=1

    def needHelp(self):
        help = QMessageBox(self)
        help.setStandardButtons(QMessageBox.Ok)
        if (self.comboBoxLanguage.currentIndex()==0):
            help.setWindowTitle("How to play ?")
            help.setText("Welcome to Bob's Bizarre Adventure, here's how to play :\n\nYou can tweak the diferent parameters in this window then click \"Let's Go !\" once you are done.\nThe game will then launch the simulation in which you will be able to see Bobs in their natural habitat...")
        elif (self.comboBoxLanguage.currentIndex()==1):
            help.setWindowTitle("Comment jouer ?")
            help.setText("Bienvenue dans Bob's Bizarre Adventure, voici comment jouer :\n\nVous pouvez modifier les différents paramètres se trouvant dans cette fenêtre puis cliquez sur \"Allons-y !\" pour lancer la simulation.\nLe jeu commencera alors la simulation dans laquelle vous pourrez admirer les Bobs dans leur habitat naturel...")
        elif (self.comboBoxLanguage.currentIndex()==2):
            help.setWindowTitle("¿ Cómo jugar ?")
            help.setText("Bienvenido a Bob's Bizarre Adventure, así es cómo se juega:\n\nPuedes modificar los diferentes parámetros en esta ventana y luego hacer clic en\"¡Vamos!\"Una vez que hayas terminado.\nEl juego iniciará la simulación en la que podrás poder ver a Bobs en su hábitat natural ... ")
        elif (self.comboBoxLanguage.currentIndex()==3):
            help.setWindowTitle("Bob ?")
            help.setText("Bob bob bob'bob bob bob, bob bob bob bob bob :\n\nBob bob bob bob bob bob bob bob bob bob bob\"Bob !\" bob bob bob bob.\nBob bob bob bob bob bob bob bob bob bob bob bob bob bob bob bob Bobs bob bob bob bob...")
        help.show()

    def writeConfig(self):
        file=open("config.cfg", "w", newline='')
        writer = csv.writer(file, delimiter='=',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Number of Ticks per day ', str(self.nbTicks)])
        writer.writerow(['Tick duration ', str(self.tick_duration)])
        writer.writerow(['World Size ', str(self.world_size)])
        writer.writerow(['Population ', str(self.population)])
        writer.writerow(['Number of food per day ', str(self.food_per_day)])
        writer.writerow(['Initial Speed ', str(self.speed)])
        writer.writerow(['Initial Mass ', str(self.mass)])
        writer.writerow(['Initial FOV ', str(self.fov)])
        writer.writerow(['Speed Mutation ', str(self.speed_mutation)])
        writer.writerow(['Mass Mutation ', str(self.mass_mutation)])
        writer.writerow(['FOV Mutation ', str(self.fov_mutation)])
        writer.writerow(['Reproduction Method (0 = None, 1 = Solo, 2 = Duo, 3 = Solo & Duo)', str(self.reproduction_method)])
        writer.writerow(['Initial Memory ', str(self.memory)])
        writer.writerow(['Memory Mutation ', str(self.memory_mutation)])
        writer.writerow(['Graphic Display (True = On) ', str(self.graphic)])
        writer.writerow(['Type of Display ', str(self.display_type)])
        writer.writerow(['Fullscreen ', str(self.fullscreen)])
        writer.writerow(['Resolution ', str(self.resolution)])
        writer.writerow(['---- Keybinding, ascii exquivalent of the maj key (ex: A Key = 65) ----'])
        writer.writerow(['Zoom in ', str(self.keyList[0])])
        writer.writerow(['Zoom Out ', str(self.keyList[1])])
        writer.writerow(['Slow Down Time ', str(self.keyList[2])])
        writer.writerow(['Speed Up Time ', str(self.keyList[3])])
        writer.writerow(['Pause Game ', str(self.keyList[4])])
        writer.writerow(['Move Left ', str(self.keyList[5])])
        writer.writerow(['Move Right ', str(self.keyList[6])])
        writer.writerow(['Move Up ', str(self.keyList[7])])
        writer.writerow(['Move Down ', str(self.keyList[8])])
        writer.writerow([' '])
        writer.writerow(['DO NOT CHANGE THE ORDER OF THE VALUES ! But you can still modify them manually'])
        file.close()

    def readConfig(self):
        file=open("config.cfg", "a+")
        file.close()
        file=open("config.cfg", "r")
        reader=csv.reader(file, delimiter='=', quotechar='|')
        reader
        for i in reader:
            try:
                yield i[1]
            except:
                yield "No Value"
        file.close()
        while True:
            try:
                yield "Void"
            except GeneratorExit:
                # print("Exiting")
                return

    def onQuitClick(self):
        quit = QMessageBox(self)
        quit.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        if (self.comboBoxLanguage.currentIndex()==0):
            quit.setWindowTitle("Quit")
            quit.setText("Do you really want to leave ?")
        elif (self.comboBoxLanguage.currentIndex()==1):
            quit.setWindowTitle("Quitter")
            quit.setText("Êtes-vous sur de vouloir quitter ?")
        elif (self.comboBoxLanguage.currentIndex()==2):
            quit.setWindowTitle("Dejar")
            quit.setText("¡ Hola amigo !\n¿ Donde esta la biblioteca ?")
        elif (self.comboBoxLanguage.currentIndex()==3):
            quit.setWindowTitle("Bob")
            quit.setText("Bob bob bob bob bob bob ?")
        quit.show()
        ret = quit.exec()
        if ret == QMessageBox.Yes:
            self.close()

    def onValidationClick(self):
        self.validation=False
        integers = [str(i) for i in range(10)]
        self.errorWindow = QMessageBox(self)
        self.errorWindow.setWindowTitle("ERROR")
        self.errorWindow.setStandardButtons(QMessageBox.Ok)
        string = ""
        try:
            population=int(self.populationParameters.lineEditPopulation.text())
            if population<1 or population>1000:
                string += "Population must be a positive integer between 1 and 1000\n"
        except:
            string += "Population must be a positive integer between 1 and 1000\n"
        try:
            nb_food=int(self.foodParameters.lineEditNbFood.text())
            if nb_food<0:
                string += "The number of food per day must be a positive integer\n"
        except:
            string += "The number of food per day must be a positive interger\n"
        try:
            speed=float(self.speedParameters.lineEditSpeedInit.text())#(self.lineEditSpeedInit.text())
            if speed<0:
                string += "Initial speed must be a positive number\n"
        except:
            string += "Initial speed must be a positive number\n"
        try:
            fov=int(self.fovParameters.lineEditFOV.text())
            if fov<0:
                string += "Initial FOV must be a positive integer\n"
        except:
            string += "Initial FOV must be a positive integer\n"
        try:
            mass=float(self.massParameters.lineEditMassInit.text())
            if mass<=0:
                string += "Initial mass must be a strictly positive number\n"
        except:
            string += "Initial mass must be a strictly positive number\n"
        try:
            nbTicks=int(self.nbTicks)
            if nbTicks<1:
                string += "The number of ticks per day must be a positive integer (non null)\n"
        except:
            string += "The number of ticks per day must be a positive integer (non null)\n"
        try:
            memory = int(self.memory)
            if memory < 0:
                string += "The memory must be a positive or null integer\n"
        except:
            string += "The memory must be a positive or null integer\n"
        try:
            tickduration = int(self.tick_duration)
            if tickduration < 1:
                string += "Wow there cowboy, you can't be THAT fast, only tick durations above 1 ms are allowed here.\n"
        except:
            string += "Tick duration must be an integer greater than 1\n"
        if any(i not in integers for i in self.worldSizeParameters.lineEditWorldSize.text()) or (self.world_size<10) or (self.world_size>1000):
            string += "World Size must be a positive integer between 10 and 1000\n"
        if string!="":
            self.errorWindow.setText(string)
            self.errorWindow.show()
        else:
            self.validation=True
            self.writeConfig()
            self.keyList=qtKeyToPygameKey(self.keyList)
            self.close()


class GroupBox(QGroupBox):
    def __init__(self, parentwidget, boxTitle, *widgets):
        super().__init__()
        self.setParent(parentwidget)
        self.setTitle(boxTitle)
        self.widget_list=[]
        while widgets:
            widget, *widgets=widgets
            self.widget_list.append(widget)
        self.fillGroupBox()

        self.show()

    def fillGroupBox(self):
        self.layout=QGridLayout()
        for i in self.widget_list:
            self.layout.addWidget(i[0], i[1],i[2])
        self.layout.rowStretch(0)
        self.setLayout(self.layout)

class SpeedParameters():
    def __init__(self,widgetsParent):
        self.parent=widgetsParent
        self.createWidgets()

    def createWidgets(self):
        self.labelSpeed = QLabel("Speed mutation : ", self.parent)
        self.parent.layoutLabel.append(self.labelSpeed)

        self.checkBoxSpeed = QCheckBox(self.parent)
        if self.parent.speed_mutation:
            self.checkBoxSpeed.setCheckState(Qt.Checked)
        else:
            self.checkBoxSpeed.setCheckState(Qt.Unchecked)
        #self.parent.layout.append(self.checkBoxSpeed)
        self.checkBoxSpeed.stateChanged.connect(self.speedMutationState)

        self.labelSpeedInit = QLabel("Initial speed :", self.parent)
        self.parent.layoutLabel.append(self.labelSpeedInit)

        self.lineEditSpeedInit = QLineEdit(str(self.parent.speed),self.parent)
        self.lineEditSpeedInit.textChanged.connect(self.getLineEditSpeedValue)

    def speedMutationState(self):
        self.parent.speed_mutation = (self.checkBoxSpeed.checkState() != 0)
        #print(self.parent.speed_mutation) #To Test if speed_mutation updates correcly

    def getLineEditSpeedValue(self):
        self.parent.speed = self.lineEditSpeedInit.text()
        #print(self.parent.speed)  # test to check that self.speed contains the correct value

class WorldSizeParameters():
    def __init__(self,widgetsParent):
        self.parent=widgetsParent
        self.createWidgets()

    def createWidgets(self):
        self.lineEditWorldSize = QLineEdit(str(self.parent.world_size),self.parent)  # boîte de texte à valeur modifiable

        self.labelWorldSize= QLabel("World Size :", self.parent)  # "nom" du slider
        self.parent.layoutLabel.append(self.labelWorldSize)

        self.sliderWorldSize = QSlider(Qt.Horizontal, self.parent)  # définiton du slider
        self.sliderWorldSize.setMinimum(10)
        self.sliderWorldSize.setMaximum(1000)
        self.sliderWorldSize.setTickPosition(QSlider.TicksAbove)
        self.sliderWorldSize.setTickInterval(25)
        self.sliderWorldSize.setValue(int(self.parent.world_size))
        self.sliderWorldSize.valueChanged.connect(self.getSliderWorldSizeValue)

        self.sliderWorldSizeMinimum=QLabel("10",self.parent)
        self.sliderWorldSizeMinimum.setAlignment(Qt.AlignRight)
        self.sliderWorldSizeMaximum=QLabel("1000",self.parent)

        self.lineEditWorldSize.textChanged.connect(self.getLineEditWorldSizeValue)

    def getSliderWorldSizeValue(self):
        worldsize= str(self.sliderWorldSize.value())
        self.parent.world_size = self.sliderWorldSize.value()
        self.lineEditWorldSize.setText(worldsize)

    def getLineEditWorldSizeValue(self):
        integers = [str(i) for i in range(10)]
        worldsize = self.lineEditWorldSize.text()
        if worldsize != '' and all(i in integers for i in worldsize):
            self.parent.world_size = int(worldsize)
            self.sliderWorldSize.setValue(self.parent.world_size)

class PopulationParameters():
    def __init__(self, widgetsParent):
        self.parent=widgetsParent
        self.createWidgets()

    def createWidgets(self):
        self.lineEditPopulation = QLineEdit(str(self.parent.population),self.parent)  # boîte de texte à valeur modifiable

        self.labelPopulation = QLabel("Population :", self.parent)  # "nom" du slider
        self.parent.layoutLabel.append(self.labelPopulation)

        self.sliderPopulation = QSlider(Qt.Horizontal, self.parent)  # définiton du slider
        self.sliderPopulation.setMinimum(1)
        self.sliderPopulation.setMaximum(1000)
        self.sliderPopulation.setTickPosition(QSlider.TicksAbove)
        self.sliderPopulation.setTickInterval(25)
        self.sliderPopulation.setValue(int(self.parent.population))
        self.sliderPopulation.valueChanged.connect(self.getSliderPopulationValue)
        self.lineEditPopulation.textChanged.connect(self.getLineEditPopulationValue)

        self.sliderPopulationMinimum=QLabel("1",self.parent)
        self.sliderPopulationMinimum.setAlignment(Qt.AlignRight)
        self.sliderPopulationMaximum=QLabel("1000",self.parent)

    def getSliderPopulationValue(self):
        population = str(self.sliderPopulation.value())
        self.parent.population = self.sliderPopulation.value()
        self.lineEditPopulation.setText(population)
        # print(self.parent.population)  # test to check if self.population contains the correct value

    def getLineEditPopulationValue(self):
        integers = [str(i) for i in range(10)]
        population = self.lineEditPopulation.text()
        if population != '' and all(i in integers for i in population):
            self.parent.population = int(population)
            self.sliderPopulation.setValue(self.parent.population)
        # print(self.parent.population)  # test to check if self.population contains the correct value

class MassParameters():
    def __init__(self, widgetsParent):
        self.parent=widgetsParent
        self.createWidgets()

    def createWidgets(self):
        self.labelMass = QLabel("Mass mutation : ", self.parent)
        self.parent.layoutLabel.append(self.labelMass)

        self.checkBoxMass = QCheckBox(self.parent)
        if self.parent.mass_mutation:
            self.checkBoxMass.setCheckState(Qt.Checked)
        else:
            self.checkBoxMass.setCheckState(Qt.Unchecked)
        self.checkBoxMass.stateChanged.connect(self.massMutationState)

        self.labelMassInit = QLabel("Initial mass :", self.parent)
        self.parent.layoutLabel.append(self.labelMassInit)

        self.lineEditMassInit = QLineEdit(str(self.parent.mass),self.parent)
        self.lineEditMassInit.textChanged.connect(self.getLineEditMassValue)

    def massMutationState(self):
        self.parent.mass_mutation = (self.checkBoxMass.checkState() != 0)
        #print(self.parent.mass_mutation) #To Test if mass_mutation updates correcly

    def getLineEditMassValue(self):
        self.parent.mass = self.lineEditMassInit.text()
        #print(self.parent.mass)  # test to check that self.mass contains the correct value

class FOVParameters():
    def __init__(self, widgetsParent):
        self.parent=widgetsParent
        self.createWidgets()

    def createWidgets(self):
        self.labelFOV=QLabel("Bob's default FOV :",self.parent)
        self.parent.layoutLabel.append(self.labelFOV)

        self.labelFOVTiles=QLabel("tiles", self.parent)
        self.parent.layoutLabel.append(self.labelFOVTiles)

        self.lineEditFOV=QLineEdit(self.parent)
        self.lineEditFOV.setText(str(self.parent.fov))
        self.lineEditFOV.textChanged.connect(self.getLineEditFOVValue)

        self.labelFOVMutation = QLabel("FOV mutation : ", self.parent)
        self.parent.layoutLabel.append(self.labelFOVMutation)

        self.checkBoxFOV = QCheckBox(self.parent)
        if self.parent.fov_mutation:
            self.checkBoxFOV.setCheckState(Qt.Checked)
        else:
            self.checkBoxFOV.setCheckState(Qt.Unchecked)
        self.checkBoxFOV.stateChanged.connect(self.fovMutationState)

    def fovMutationState(self):
        self.parent.fov_mutation = (self.checkBoxFOV.checkState() != 0)
        #print(self.parent.fov_mutation) #To Test if fov_mutation updates correcly

    def getLineEditFOVValue(self):
        self.parent.fov=self.lineEditFOV.text()

class ReproductionParameters():
    def __init__(self,widgetsParent):
        self.parent=widgetsParent
        self.createWidgets()

    def createWidgets(self):
        self.labelReproduction=QLabel("Reproduction method :",self.parent)
        self.parent.layoutLabel.append(self.labelReproduction)

        self.comboBoxReproduction=QComboBox(self.parent)
        self.comboBoxReproduction.addItem("None")
        self.comboBoxReproduction.addItem("Solo")
        self.comboBoxReproduction.addItem("Duo")
        self.comboBoxReproduction.addItem("Solo & Duo")
        self.comboBoxReproduction.setCurrentIndex(self.parent.reproduction_method)
        self.comboBoxReproduction.currentTextChanged.connect(self.reproductionMethodChange)
        self.parent.comboBoxList.append(self.comboBoxReproduction)

    def reproductionMethodChange(self):
        self.parent.reproduction_method=self.comboBoxReproduction.currentIndex()
        # print(self.parent.reproduction_method) #To test if the reproduction_method updates correctly

class DisplayParameters():
    def __init__(self, widgetsParent):
        self.parent=widgetsParent
        self.createWidgets()

    def createWidgets(self):
        self.labelGraphic=QLabel("Graphic display :", self.parent)
        self.checkBoxGraphic=QCheckBox(self.parent)
        if self.parent.graphic:
            self.checkBoxGraphic.setCheckState(Qt.Checked)
        else:
            self.checkBoxGraphic.setCheckState(Qt.Unchecked)
        self.checkBoxGraphic.stateChanged.connect(self.graphicState)
        self.parent.layoutLabel.append(self.labelGraphic)

        self.labelDisplayType = QLabel("Display type :", self.parent)
        self.parent.layoutLabel.append(self.labelDisplayType)
        self.comboBoxDisplayType = QComboBox(self.parent)
        self.comboBoxDisplayType.addItem("Isometric : 2.5D")
        self.comboBoxDisplayType.addItem("Top View : 2D")
        self.comboBoxDisplayType.setCurrentText(self.parent.display_type)
        self.comboBoxDisplayType.currentTextChanged.connect(self.displayTypeSelection)
        self.parent.comboBoxList.append(self.comboBoxDisplayType)


        self.labelFullscreen=QLabel("Display mode :",self.parent)
        self.parent.layoutLabel.append(self.labelFullscreen)

        self.comboBoxFullscreen=QComboBox(self.parent)
        self.comboBoxFullscreen.addItem("Fullscreen")
        self.comboBoxFullscreen.addItem("Windowed")
        if self.parent.fullscreen:
            self.comboBoxFullscreen.setCurrentText("Fullscreen")
        else:
            self.comboBoxFullscreen.setCurrentText("Windowed")
        self.comboBoxFullscreen.currentTextChanged.connect(self.fullscreenSelection)
        self.parent.comboBoxList.append(self.comboBoxFullscreen)

        self.labelResolution = QLabel("Resolution :",self.parent)
        self.parent.layoutLabel.append(self.labelResolution)
        self.comboBoxResolution = QComboBox(self.parent)
        self.comboBoxResolution.addItem("Auto")
        self.comboBoxResolution.addItem("1080p")
        self.comboBoxResolution.addItem("720p")
        self.comboBoxResolution.addItem("480p")
        self.comboBoxResolution.addItem("240p")
        self.comboBoxResolution.setCurrentText(self.parent.resolution)
        self.comboBoxResolution.currentTextChanged.connect(self.resolutionChange)

    def graphicState(self):
        self.parent.graphic=(self.checkBoxGraphic.checkState()!=0)
        if self.parent.graphic:
            if self.parent.display_type=="Isometric : 2.5D":
                self.comboBoxFullscreen.show()
                self.labelFullscreen.show()
                self.labelResolution.show()
                self.comboBoxResolution.show()
            self.comboBoxDisplayType.show()
            self.labelDisplayType.show()
        else:
            self.comboBoxFullscreen.hide()
            self.labelFullscreen.hide()
            self.comboBoxDisplayType.hide()
            self.labelDisplayType.hide()
            self.labelResolution.hide()
            self.comboBoxResolution.hide()
        # print("Graphic Display = ",self.parent.graphic) #comment if not testing

    def fullscreenSelection(self):
        fullscreen=self.comboBoxFullscreen.currentIndex()
        self.parent.fullscreen = (fullscreen == 0)
        # print("Fullscreen :", self.parent.fullscreen) #Comment if not testing

    def displayTypeSelection(self):
        if (self.comboBoxDisplayType.currentText()=="Top View : 2D"):
            self.parent.display_type="Top View : 2D"
            self.comboBoxResolution.hide()
            self.labelResolution.hide()
            self.comboBoxFullscreen.hide()
            self.labelFullscreen.hide()
        else:
            self.parent.display_type="Isometric : 2.5D"
            self.comboBoxResolution.show()
            self.labelResolution.show()
            self.comboBoxFullscreen.show()
            self.labelFullscreen.show()
        # print("Display Type =", self.parent.display_type) #Comment if not testing

    def resolutionChange(self):
        self.parent.resolution = self.comboBoxResolution.currentText()

class FoodParameters():
    def __init__(self, parentwidget):
        self.parent=parentwidget
        self.createWidgets()

    def createWidgets(self):
        self.labelNbFood=QLabel("Number of food per day :", self.parent)
        self.lineEditNbFood = QLineEdit(str(self.parent.food_per_day), self.parent)
        self.lineEditNbFood.textChanged.connect(self.getLineEditNbFoodValue)
        self.parent.layoutLabel.append(self.labelNbFood)

    def getLineEditNbFoodValue(self):
        self.parent.food_per_day=self.lineEditNbFood.text()
        # print("Number of food per day =", self.parent.food_per_day) #Comment if not testing

class TicksParameters():
    def __init__(self, widgetsParent):
        self.parent=widgetsParent
        self.createWidgets()

    def createWidgets(self):
        self.labelNbTicks = QLabel("Number of ticks per day :", self.parent)
        self.parent.layoutLabel.append(self.labelNbTicks)

        self.lineEditNbTicks = QLineEdit(str(self.parent.nbTicks),self.parent)
        self.lineEditNbTicks.textChanged.connect(self.getLineEditNbTicksValue)

        self.labelTickDuration = QLabel("Tick duration :", self.parent)
        self.parent.layoutLabel.append(self.labelTickDuration)

        self.lineEditTickDuration = QLineEdit(str(self.parent.tick_duration), self.parent)
        self.lineEditTickDuration.textChanged.connect(self.getLineEditTickDurationValue)

        self.labelTickDurationUnit = QLabel("ms", self.parent)


    def getLineEditNbTicksValue(self):
        self.parent.nbTicks = self.lineEditNbTicks.text()
        # print("Number of ticks per day = ", self.parent.nbTicks) #comment if not testing

    def getLineEditTickDurationValue(self):
        self.parent.tick_duration = self.lineEditTickDuration.text()
        # print("Duration of a single tick = ", self.parent.tick_duration) #Comment if not testion

class MemoryParameters():
    def __init__(self, parent):
        self.parent=parent
        self.createWidgets()

    def createWidgets(self):
        self.labelMemoryMutation = QLabel("Memory mutation : ", self.parent)
        self.parent.layoutLabel.append(self.labelMemoryMutation)
        self.checkBoxMemory = QCheckBox(self.parent)
        if self.parent.memory_mutation:
            self.checkBoxMemory.setCheckState(Qt.Checked)
        else:
            self.checkBoxMemory.setCheckState(Qt.Unchecked)
        self.checkBoxMemory.stateChanged.connect(self.memoryState)

        self.labelMemory = QLabel("Memory Capacity : ", self.parent)
        self.parent.layoutLabel.append(self.labelMemory)
        self.lineEditMemory = QLineEdit(str(self.parent.memory),self.parent)
        self.lineEditMemory.textChanged.connect(self.getMemoryValue)

    def getMemoryValue(self):
        self.parent.memory = self.lineEditMemory.text()

    def memoryState(self):
        self.parent.memory_mutation = (self.checkBoxMemory.checkState() != 0)
        # print(self.parent.memory_mutation) #TEST

class KeyBinding():
    def __init__(self, widgetsParent):
        self.parent=widgetsParent
        self.createWidgets()

    def createWidgets(self):
        self.labelCurrentKey = QLabel("Current Key",self.parent)
        self.labelCurrentKey.setAlignment(Qt.AlignCenter)
        self.labelDefaultKey = QLabel("Reset to default", self.parent)
        self.labelDefaultKey.setAlignment(Qt.AlignCenter)
        labelVoid = QLabel("", self.parent)
        self.layoutKeybind = QGridLayout()
        self.layoutKeybind.addWidget(labelVoid,0,0)
        self.layoutKeybind.addWidget(self.labelCurrentKey,0,1)
        self.layoutKeybind.addWidget(self.labelDefaultKey,0,2)

        self.parent.layoutLabel.append(self.labelCurrentKey)
        self.parent.layoutLabel.append(self.labelDefaultKey)

        self.zoomIn = KeyToBind(self.parent, "Zoom +",self.parent.keyDictionnary["zoom_in"])
        self.zoomOut = KeyToBind(self.parent, "Zoom -", self.parent.keyDictionnary["zoom_out"])
        self.slowTime = KeyToBind(self.parent, "Slow Time", self.parent.keyDictionnary["slow_time"])
        self.speedUpTime = KeyToBind(self.parent, "Speed Up Time", self.parent.keyDictionnary["speed_up_time"])
        self.pauseGame = KeyToBind(self.parent, "Pause Game", self.parent.keyDictionnary["pause_game"])
        self.moveLeft = KeyToBind(self.parent, "Move Left", self.parent.keyDictionnary["move_left"])
        self.moveRight = KeyToBind(self.parent, "Move Right", self.parent.keyDictionnary["move_right"])
        self.moveUp = KeyToBind(self.parent, "Move Up", self.parent.keyDictionnary["move_up"])
        self.moveDown = KeyToBind(self.parent, "Move Down", self.parent.keyDictionnary["move_down"])

class KeyToBind():
    def __init__(self, widgetsParent, keytitle, key_to_change):
        super().__init__()
        self.parent = widgetsParent
        self.key = keytitle
        self.key_to_change = key_to_change
        if self.parent.keyList[self.key_to_change] not in weirdkeys:
            self.currentkey = chr(self.parent.keyList[self.key_to_change])
        else:
            self.currentkey = qtKeyToHuman(self.parent.keyList[self.key_to_change])
        self.new_key=0

        self.createWidgets()

    def createWidgets(self):
        self.labelKey = QLabel(self.key, self.parent)
        self.buttonKey = QPushButton(self.currentkey, self.parent)
        self.buttonKey.clicked.connect(self.onButtonClick)
        self.parent.buttonKeyBindList.append(self.buttonKey)
        self.parent.layoutLabel.append(self.labelKey)

        resetPixmap = QtGui.QPixmap("Resources/GUI/RandomAssets/reset.png")
        resetIcon = QtGui.QIcon(resetPixmap)
        self.buttonDefaultKey = QPushButton(resetIcon,"",self.parent)
        self.buttonDefaultKey.clicked.connect(self.onResetClick)

        self.keyLayout = QHBoxLayout()
        self.keyLayout.addWidget(self.labelKey)
        self.keyLayout.addWidget(self.buttonKey)
        self.keyLayout.addWidget(self.buttonDefaultKey)

    def onButtonClick(self):
        self.messageBoxKey = MessageBoxKeyBind(self.parent,self)

    def onResetClick(self):
        self.buttonKey.setText(self.parent.defaultKeysLabel[self.key_to_change])
        self.parent.keyList[self.key_to_change] = self.parent.defaultKeys[self.key_to_change]

        k = 0                   # We check if 2 or more options are bound to the same key, if so, we turn both push buttons to red
        while k < len(self.parent.keyList):
            j=0
            sameKeys = []
            if self.parent.buttonKeyBindList[k].styleSheet()== "background-color: red":
                while j < len(self.parent.keyList):
                    if j != k:
                        if self.parent.keyList[j] == self.parent.keyList[k]:
                            sameKeys.append(j)
                    j+=1
                if len(sameKeys)!=0:
                    for i in sameKeys:
                        self.parent.buttonKeyBindList[i].setStyleSheet("background-color: red")
                        self.parent.buttonKeyBindList[k].setStyleSheet("background-color: red")
                else:
                    self.parent.buttonKeyBindList[k].setStyleSheet("")
            elif k == self.key_to_change:
                while j < len(self.parent.keyList):
                    if j != k:
                        if self.parent.keyList[j] == self.parent.keyList[k]:
                            sameKeys.append(j)
                    j+=1
                if len(sameKeys)!=0:
                    for i in sameKeys:
                        self.parent.buttonKeyBindList[i].setStyleSheet("background-color: red")
                        self.parent.buttonKeyBindList[k].setStyleSheet("background-color: red")
                else:
                    self.parent.buttonKeyBindList[k].setStyleSheet("")
            k+=1

class MessageBoxKeyBind(QMessageBox):
    def __init__(self,parent,info):
        super().__init__()
        self.parent=parent
        self.info=info
        self.createWidgets()
        self.show()

    def createWidgets(self):
        self.setWindowTitle(self.info.labelKey.text())
        self.setText("Press any key . . .")
        self.setStandardButtons(QMessageBox.Cancel)

    def keyPressEvent(self,event):
        # print(f"The {self.info.key} key has been changed to {event.key()}")
        if event.key() not in weirdkeys:
            self.parent.keyList[self.info.key_to_change]=event.key()
            self.info.buttonKey.setText(chr(self.parent.keyList[self.info.key_to_change]))
        else:
            self.parent.keyList[self.info.key_to_change]=event.key()
            self.info.buttonKey.setText(qtKeyToHuman(event.key()))

        k = 0                   # We check if 2 or more options are bound to the same key, if so, we turn both push buttons to red
        while k < len(self.parent.keyList):
            j=0
            sameKeys = []
            if self.parent.buttonKeyBindList[k].styleSheet()== "background-color: red":
                while j < len(self.parent.keyList):
                    if j != k:
                        if self.parent.keyList[j] == self.parent.keyList[k]:
                            sameKeys.append(j)
                    j+=1
                if len(sameKeys)!=0:
                    for i in sameKeys:
                        self.parent.buttonKeyBindList[i].setStyleSheet("background-color: red")
                        self.parent.buttonKeyBindList[k].setStyleSheet("background-color: red")
                else:
                    self.parent.buttonKeyBindList[k].setStyleSheet("")
            elif k == self.info.key_to_change:
                while j < len(self.parent.keyList):
                    if j != k:
                        if self.parent.keyList[j] == self.parent.keyList[k]:
                            sameKeys.append(j)
                    j+=1
                if len(sameKeys)!=0:
                    for i in sameKeys:
                        self.parent.buttonKeyBindList[i].setStyleSheet("background-color: red")
                        self.parent.buttonKeyBindList[k].setStyleSheet("background-color: red")
                else:
                    self.parent.buttonKeyBindList[k].setStyleSheet("")
            k+=1

        self.close()

class WidgetforTab(QWidget):
    def __init__(self, parent, layout, *widgets):
        super().__init__()
        self.setParent(parent)
        grid=QGridLayout()
        widgetList=[]
        while widgets:
            widget, *widgets=widgets
            widgetList.append(widget)
        for i in widgetList:
            grid.addWidget(i[0], i[1], i[2])
        try :
            grid.addLayout(layout[0],layout[1],layout[2],layout[3],layout[4])
        except:
            pass
        self.setLayout(grid)

class TabBar(QTabBar):
    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt);
            painter.restore()

class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QTabWidget.West)

class ProxyStyle(QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QStyle.PM_TabBarIconSize)
            r = QRect(opt.rect)
            w =  0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QProxyStyle.drawControl(self, element, opt, painter, widget)
