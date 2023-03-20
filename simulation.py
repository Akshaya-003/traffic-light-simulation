{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "09bbbf72",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "pygame 2.3.0 (SDL 2.24.2, Python 3.10.4)\n",
      "Hello from the pygame community. https://www.pygame.org/contribute.html\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Dell\\anaconda3\\envs\\new_environment\\lib\\site-packages\\IPython\\core\\interactiveshell.py:3406: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "import random\n",
    "import time\n",
    "import threading\n",
    "import pygame\n",
    "import sys\n",
    "\n",
    "# Default values of signal timers\n",
    "defaultGreen = {0:10, 1:10, 2:10, 3:10}\n",
    "defaultRed = 150\n",
    "defaultYellow = 5\n",
    "\n",
    "signals = []\n",
    "noOfSignals = 4\n",
    "currentGreen = 0   # Indicates which signal is green currently\n",
    "nextGreen = (currentGreen+1)%noOfSignals    # Indicates which signal will turn green next\n",
    "currentYellow = 0   # Indicates whether yellow signal is on or off \n",
    "\n",
    "speeds = {'car':2.25, 'bus':1.8, 'truck':1.8, 'bike':2.5}  # average speeds of vehicles\n",
    "\n",
    "# Coordinates of vehicles' start\n",
    "x = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[602,627,657]}    \n",
    "y = {'right':[348,370,398], 'down':[0,0,0], 'left':[498,466,436], 'up':[800,800,800]}\n",
    "\n",
    "vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}\n",
    "vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike'}\n",
    "directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}\n",
    "\n",
    "# Coordinates of signal image, timer, and vehicle count\n",
    "signalCoods = [(530,230),(810,230),(810,570),(530,570)]\n",
    "signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]\n",
    "\n",
    "# Coordinates of stop lines\n",
    "stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}\n",
    "defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}\n",
    "# stops = {'right': [580,580,580], 'down': [320,320,320], 'left': [810,810,810], 'up': [545,545,545]}\n",
    "\n",
    "# Gap between vehicles\n",
    "stoppingGap = 15    # stopping gap\n",
    "movingGap = 15   # moving gap\n",
    "\n",
    "pygame.init()\n",
    "simulation = pygame.sprite.Group()\n",
    "\n",
    "class TrafficSignal:\n",
    "    def __init__(self, red, yellow, green):\n",
    "        self.red = red\n",
    "        self.yellow = yellow\n",
    "        self.green = green\n",
    "        self.signalText = \"\"\n",
    "        \n",
    "class Vehicle(pygame.sprite.Sprite):\n",
    "    def __init__(self, lane, vehicleClass, direction_number, direction):\n",
    "        pygame.sprite.Sprite.__init__(self)\n",
    "        self.lane = lane\n",
    "        self.vehicleClass = vehicleClass\n",
    "        self.speed = speeds[vehicleClass]\n",
    "        self.direction_number = direction_number\n",
    "        self.direction = direction\n",
    "        self.x = x[direction][lane]\n",
    "        self.y = y[direction][lane]\n",
    "        self.crossed = 0\n",
    "        vehicles[direction][lane].append(self)\n",
    "        self.index = len(vehicles[direction][lane]) - 1\n",
    "        path = \"images/\" + direction + \"/\" + vehicleClass + \".png\"\n",
    "        self.image = pygame.image.load(path)\n",
    "\n",
    "        if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):    # if more than 1 vehicle in the lane of vehicle before it has crossed stop line\n",
    "            if(direction=='right'):\n",
    "                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].image.get_rect().width - stoppingGap         # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap\n",
    "            elif(direction=='left'):\n",
    "                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].image.get_rect().width + stoppingGap\n",
    "            elif(direction=='down'):\n",
    "                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].image.get_rect().height - stoppingGap\n",
    "            elif(direction=='up'):\n",
    "                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].image.get_rect().height + stoppingGap\n",
    "        else:\n",
    "            self.stop = defaultStop[direction]\n",
    "            \n",
    "        # Set new starting and stopping coordinate\n",
    "        if(direction=='right'):\n",
    "            temp = self.image.get_rect().width + stoppingGap    \n",
    "            x[direction][lane] -= temp\n",
    "        elif(direction=='left'):\n",
    "            temp = self.image.get_rect().width + stoppingGap\n",
    "            x[direction][lane] += temp\n",
    "        elif(direction=='down'):\n",
    "            temp = self.image.get_rect().height + stoppingGap\n",
    "            y[direction][lane] -= temp\n",
    "        elif(direction=='up'):\n",
    "            temp = self.image.get_rect().height + stoppingGap\n",
    "            y[direction][lane] += temp\n",
    "        simulation.add(self)\n",
    "\n",
    "    def render(self, screen):\n",
    "        screen.blit(self.image, (self.x, self.y))\n",
    "\n",
    "    def move(self):\n",
    "        if(self.direction=='right'):\n",
    "            if(self.crossed==0 and self.x+self.image.get_rect().width>stopLines[self.direction]):   # if the image has crossed stop line now\n",
    "                self.crossed = 1\n",
    "            if((self.x+self.image.get_rect().width<=self.stop or self.crossed == 1 or (currentGreen==0 and currentYellow==0)) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap))):                \n",
    "            # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)\n",
    "                self.x += self.speed  # move the vehicle\n",
    "        elif(self.direction=='down'):\n",
    "            if(self.crossed==0 and self.y+self.image.get_rect().height>stopLines[self.direction]):\n",
    "                self.crossed = 1\n",
    "            if((self.y+self.image.get_rect().height<=self.stop or self.crossed == 1 or (currentGreen==1 and currentYellow==0)) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap))):                \n",
    "                self.y += self.speed\n",
    "        elif(self.direction=='left'):\n",
    "            if(self.crossed==0 and self.x<stopLines[self.direction]):\n",
    "                self.crossed = 1\n",
    "            if((self.x>=self.stop or self.crossed == 1 or (currentGreen==2 and currentYellow==0)) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap))):                \n",
    "                self.x -= self.speed   \n",
    "        elif(self.direction=='up'):\n",
    "            if(self.crossed==0 and self.y<stopLines[self.direction]):\n",
    "                self.crossed = 1\n",
    "            if((self.y>=self.stop or self.crossed == 1 or (currentGreen==3 and currentYellow==0)) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):                \n",
    "                self.y -= self.speed\n",
    "\n",
    "# Initialization of signals with default values\n",
    "def initialize():\n",
    "    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])\n",
    "    signals.append(ts1)\n",
    "    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, defaultYellow, defaultGreen[1])\n",
    "    signals.append(ts2)\n",
    "    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])\n",
    "    signals.append(ts3)\n",
    "    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])\n",
    "    signals.append(ts4)\n",
    "    repeat()\n",
    "\n",
    "def repeat():\n",
    "    global currentGreen, currentYellow, nextGreen\n",
    "    while(signals[currentGreen].green>0):   # while the timer of current green signal is not zero\n",
    "        updateValues()\n",
    "        time.sleep(1)\n",
    "    currentYellow = 1   # set yellow signal on\n",
    "    # reset stop coordinates of lanes and vehicles \n",
    "    for i in range(0,3):\n",
    "        for vehicle in vehicles[directionNumbers[currentGreen]][i]:\n",
    "            vehicle.stop = defaultStop[directionNumbers[currentGreen]]\n",
    "    while(signals[currentGreen].yellow>0):  # while the timer of current yellow signal is not zero\n",
    "        updateValues()\n",
    "        time.sleep(1)\n",
    "    currentYellow = 0   # set yellow signal off\n",
    "    \n",
    "     # reset all signal times of current signal to default times\n",
    "    signals[currentGreen].green = defaultGreen[currentGreen]\n",
    "    signals[currentGreen].yellow = defaultYellow\n",
    "    signals[currentGreen].red = defaultRed\n",
    "       \n",
    "    currentGreen = nextGreen # set next signal as green signal\n",
    "    nextGreen = (currentGreen+1)%noOfSignals    # set next green signal\n",
    "    signals[nextGreen].red = signals[currentGreen].yellow+signals[currentGreen].green    # set the red time of next to next signal as (yellow time + green time) of next signal\n",
    "    repeat()  \n",
    "\n",
    "# Update values of the signal timers after every second\n",
    "def updateValues():\n",
    "    for i in range(0, noOfSignals):\n",
    "        if(i==currentGreen):\n",
    "            if(currentYellow==0):\n",
    "                signals[i].green-=1\n",
    "            else:\n",
    "                signals[i].yellow-=1\n",
    "        else:\n",
    "            signals[i].red-=1\n",
    "\n",
    "# Generating vehicles in the simulation\n",
    "def generateVehicles():\n",
    "    while(True):\n",
    "        vehicle_type = random.randint(0,3)\n",
    "        lane_number = random.randint(1,2)\n",
    "        temp = random.randint(0,99)\n",
    "        direction_number = 0\n",
    "        dist = [25,50,75,100]\n",
    "        if(temp<dist[0]):\n",
    "            direction_number = 0\n",
    "        elif(temp<dist[1]):\n",
    "            direction_number = 1\n",
    "        elif(temp<dist[2]):\n",
    "            direction_number = 2\n",
    "        elif(temp<dist[3]):\n",
    "            direction_number = 3\n",
    "        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])\n",
    "        time.sleep(1)\n",
    "\n",
    "class Main:\n",
    "    thread1 = threading.Thread(name=\"initialization\",target=initialize, args=())    # initialization\n",
    "    thread1.daemon = True\n",
    "    thread1.start()\n",
    "\n",
    "    # Colours \n",
    "    black = (0, 0, 0)\n",
    "    white = (255, 255, 255)\n",
    "\n",
    "    # Screensize \n",
    "    screenWidth = 1400\n",
    "    screenHeight = 800\n",
    "    screenSize = (screenWidth, screenHeight)\n",
    "\n",
    "    # Setting background image i.e. image of intersection\n",
    "    background = pygame.image.load('images/intersection.png')\n",
    "\n",
    "    screen = pygame.display.set_mode(screenSize)\n",
    "    pygame.display.set_caption(\"SIMULATION\")\n",
    "\n",
    "    # Loading signal images and font\n",
    "    redSignal = pygame.image.load('images/signals/red.png')\n",
    "    yellowSignal = pygame.image.load('images/signals/yellow.png')\n",
    "    greenSignal = pygame.image.load('images/signals/green.png')\n",
    "    font = pygame.font.Font(None, 30)\n",
    "\n",
    "    thread2 = threading.Thread(name=\"generateVehicles\",target=generateVehicles, args=())    # Generating vehicles\n",
    "    thread2.daemon = True\n",
    "    thread2.start()\n",
    "\n",
    "    while True:\n",
    "        for event in pygame.event.get():\n",
    "            if event.type == pygame.QUIT:\n",
    "                sys.exit()\n",
    "\n",
    "        screen.blit(background,(0,0))   # display background in simulation\n",
    "        for i in range(0,noOfSignals):  # display signal and set timer according to current status: green, yello, or red\n",
    "            if(i==currentGreen):\n",
    "                if(currentYellow==1):\n",
    "                    signals[i].signalText = signals[i].yellow\n",
    "                    screen.blit(yellowSignal, signalCoods[i])\n",
    "                else:\n",
    "                    signals[i].signalText = signals[i].green\n",
    "                    screen.blit(greenSignal, signalCoods[i])\n",
    "            else:\n",
    "                if(signals[i].red<=10):\n",
    "                    signals[i].signalText = signals[i].red\n",
    "                else:\n",
    "                    signals[i].signalText = \"---\"\n",
    "                screen.blit(redSignal, signalCoods[i])\n",
    "        signalTexts = [\"\",\"\",\"\",\"\"]\n",
    "\n",
    "        # display signal timer\n",
    "        for i in range(0,noOfSignals):  \n",
    "            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)\n",
    "            screen.blit(signalTexts[i],signalTimerCoods[i])\n",
    "\n",
    "        # display the vehicles\n",
    "        for vehicle in simulation:  \n",
    "            screen.blit(vehicle.image, [vehicle.x, vehicle.y])\n",
    "            vehicle.move()\n",
    "        pygame.display.update()\n",
    "\n",
    "\n",
    "Main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "3f881cc1",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting pygame\n",
      "  Downloading pygame-2.3.0-cp310-cp310-win_amd64.whl (10.5 MB)\n",
      "     ---------------------------------------- 10.5/10.5 MB 2.2 MB/s eta 0:00:00\n",
      "Installing collected packages: pygame\n",
      "Successfully installed pygame-2.3.0\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install pygame\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "60e92900",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
