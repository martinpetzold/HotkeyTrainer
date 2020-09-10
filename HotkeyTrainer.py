#Martin Petzold
#September 2020

from pynput import keyboard,mouse
import tkinter as tk 
import tkinter.font as tkFont
import datetime
import random
import csv
import time
import threading

class HotkeyTrainer():
    def __init__(self,hotkeyList):
        self.hotkeyList = hotkeyList
        self.window = tk.Tk()
        self.duration = 25
        self.comboCount = 1
        self.currQuest = ""
        self.oldQuest = ""
        self.window.title("Hotkey-Trainer")
        fontStyle = tkFont.Font(family="Lucida Grande", size=12)
        frame = tk.Frame(master=self.window, width=400, height=300)
        frame.pack()

        #Build1: Create ScoreText
        self.scoreVal = 0
        self.score = tk.StringVar()
        self.score.set(str(self.scoreVal))
        scoreLabel = tk.Label(master=frame,text="Score:",width=6,bg="white", font=fontStyle)
        scoreLabel.place(x=20,y=20)
        scoreLabel = tk.Label(master=frame,textvariable=self.score,width=14,bg="white", font=fontStyle)
        scoreLabel.place(x=160,y=20)
        
        #Build2: Create start button
        button = tk.Button(
            text="start",
            width=30,
            height=2,
            bg="white",
            fg="black",
            font=fontStyle,
            command=self.start)
        button.place(x=50,y=200)
        self.timerRunning = False
        
        #Build3: Create Timer
        self.timer = tk.StringVar()
        self.timer.set(str(self.duration))
        scoreLabel = tk.Label(master=frame,text="Time remaining:",width=12,bg="white", font=fontStyle)
        scoreLabel.place(x=20,y=60)
        scoreLabel = tk.Label(master=frame,textvariable=self.timer,width=14,bg="white", font=fontStyle)
        scoreLabel.place(x=160,y=60)

        #Build3: Create Question
        self.question = tk.StringVar()
        self.question.set(str("-"))
        self.questLabel = tk.Label(master=frame,text="Combo:",width=12,bg="white", font=fontStyle)
        self.questLabel.place(x=20,y=120)
        self.questLabel = tk.Label(master=frame,textvariable=self.question,width=22,bg="white", font=fontStyle)
        self.questLabel.place(x=160,y=120)

        #Config Keboard/Mouse Listener
        def on_press(key):
            try:
                key.char #enforce error if special key
                print("input: " +str(key))
                self.checkInput(key)
            except AttributeError:
                pass
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        def on_click(x, y, button, pressed):
            if pressed:
                print('{0} at {1}'.format(
                'Pressed' if pressed else 'Released',
                (x, y)))
                print("input: " + str(button))
                self.checkInput("'"+str(button)+"'")
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        
    def start(self):
        self.scoreVal = 0
        self.score.set(str(self.scoreVal))
        if self.timerRunning == False:
            self.timerRunning = True
            self.currTime = self.duration
            self.threadtimer = threading.Thread(target=timer, args=(self,))
            self.threadtimer.start()
            self.newQuest()
    
    def checkInput(self,inputVal):
        if self.timerRunning == True:
            if not str(inputVal) == "'" + self.currQuest[self.comboCount] + "'":
                self.questLabel.configure(bg = "#FF3030") # red
                time.sleep(0.1)
                self.questLabel.configure(bg = "white")
                print("Combo Incorrect")
                self.newQuest()
            else: 
                self.score.set(str(self.scoreVal))
                self.comboCount += 1
                if self.comboCount > len(self.currQuest)-1:
                    self.questLabel.configure(bg = "#00EE76") # green
                    time.sleep(0.1)
                    self.questLabel.configure(bg = "white")
                    self.scoreVal += 1
                    self.score.set(str(self.scoreVal))
                    print("Combo Correct")
                    self.newQuest()

    def gameOver(self):
        print("Game Over");

    def newQuest(self):
        self.oldQuest = self.currQuest
        while self.currQuest == self.oldQuest:
            self.currQuest = random.choice(self.hotkeyList)
            self.question.set(str(self.currQuest[0]))
            self.comboCount = 1
            print(self.currQuest)        
            
def timer(refObj):
    while refObj.currTime>=0:
        refObj.timer.set(str(refObj.currTime))
        time.sleep(1)
        refObj.currTime-=1
    refObj.timerRunning = False
    refObj.gameOver()
            
with open('Hotkeys.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',',)
    hotkeyList = list(reader)
    print("Hotkeylist:")
    print(hotkeyList)

hkt = HotkeyTrainer(hotkeyList)
hkt.window.mainloop()
input('Press ENTER to exit')
