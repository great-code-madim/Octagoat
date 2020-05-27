# Octagoat. 13 December 2019. Author: Mohammed Madi.
# Coursework 2 project for COMP16321.

# The goat background picture was taken on the
# 23rd of November 2019 at Snowdon, Wales by the author.

# The goat pixel drawings and the cage were produced
# using PixilArt online tool and modified using GIMP.


from tkinter import Tk, PhotoImage, Button
from tkinter import Menu, messagebox, Canvas, Label
from PIL import Image, ImageTk
import time


# Window dimensions.
def setWindowDimensions(w, h):
    window.title("Octagoat")
    # title of window
    ws = window.winfo_screenwidth()
    # computers screen width used for window dimensions
    hs = window.winfo_screenheight()
    # computers screen height used for window dimensions
    window.geometry(f"{ws}x{hs}")
    # window size
    return window


# Main menu with buttons and background picture.
def main_menu():
    global window, start, start2, start3, over
    global start4, start5, bg1, canvas, boss, start6
    if(over==True):
        Restart.destroy()
        exitb.destroy()
        menub.destroy()
    if(over==False):
        canvas = Canvas(window, bg="black", width=width, height=height)
    over = False
    background = canvas.create_image(0, 0, anchor='nw', image=bg1)

    start = Button(window, text="Play Normal mode", background="black",
                   foreground="white", activebackground="green", width="17", height="3",
                   font=('terminal', 20), command=lambda: normal())
    start.place(x=400, y=50)

    start2 = Button(window, text="Play Hard mode", background="black",
                    foreground="white", activebackground="green", width="17", height="3",
                    font=('terminal', 20), command=lambda: hard())
    start2.place(x=750, y=50)

    start3 = Button(window, text="Play Mating\nseason mode", background="black",
                    foreground="white", activebackground="green", width="17", height="3",
                    font=('terminal', 20), command=lambda: mating())
    start3.place(x=1100, y=50)

    start4 = Button(window, text="Leaderboard", background="black",
                    foreground="white", activebackground="green", width="17", height="3",
                    font=('terminal', 20))
    start4.place(x=1450, y=50)

    start5 = Button(window, text="Exit", background="black",
                    foreground="white", activebackground="green", width="17", height="3",
                    font=('terminal', 20), command=lambda: window.destroy())
    start5.place(x=50, y=200)

    start6 = Button(window, text="Tutorial", background="black",
                    foreground="white", activebackground="green", width="17", height="3",
                    font=('terminal', 20), command=lambda: tutorial())
    start6.place(x=50, y=50)
    boss = canvas.create_image(0, -width, anchor='nw', image=bosspic)


# Tutorial explaining different game elements and how to play.
def tutorial():
    messagebox.showinfo("Welcome to Octagoat",
                        "The name comes from Mixed Martial arts (MMA) cages, which are octagons,\
                        put goats in an octagon and you have an octagoat.")
    messagebox.showinfo("Welcome to Octagoat",
                        "Your character is a goat fighting other goats,\
                        the goats are running from,\
                        one side of the cage to the other trying to ram your goat,\
                        and your goat is trying to stomp the other goats (in Super Mario fashion)")
    messagebox.showinfo("Welcome to Octagoat",
                        " Stomp another goat once, and it will count as a win.\
                        but get rammed from another goat twice and you lose.\
                        You can stay on the ramp if you are too scared")
    messagebox.showinfo("Welcome to Octagoat",
                        "You can use the arrow keys to move your goat from\
                         side to side or jump. To get on the ramp jump to the top\
                         from underneath it. To get off the ramp simply walk off the sides")
    messagebox.showinfo("Welcome to Octagoat",
                        "Press B if someone passes. C stands for cheat and \
                        D stands for Diaz.\nWHEN PLAYING MATING \
                        SEASON TRY TO GET ON THE RAMP AS SOON AS YOU SPAWN")


def rightKey(event):
    global direction
    direction = "right"
    move()


def leftKey(event):
    global direction
    direction = "left"
    move()


def upKey(event):
    global direction, sprite
    direction = "up"
    move()


# Movement function for player
def move():
    # This function includes movement, and collision with the ramp
    global direction, ramp, score, sprite, speed, paused
    if paused == 0:
        if direction == "left":
            canvas.move(sprite, -speed, 0)
        elif direction == "right":
            canvas.move(sprite, speed, 0)
        elif direction == "up":
            canvas.move(sprite, 0, -150)
            window.after(350, lambda: canvas.move(sprite, 0, 150))
        a = canvas.bbox(sprite)
        c = canvas.bbox(box)
        # Ramp collision
        if a[1] in range((c[3]-100), c[3]) and(a[0] in range
                                               (int(c[0]), int(c[2])) or a[2] in range(int(c[0]), int(c[2]))):
            canvas.move(sprite, 0, -420)
            ramp = True
        if a[0] not in range(int(c[0]), int(c[2]-50.0)) and(
                a[2] not in range(int(c[0]+50.0), int(c[2])) and ramp):
            window.after(10, lambda: canvas.move(sprite, 0, 120))
            window.after(250, lambda: canvas.move(sprite, 0, 150))
            window.after(450, lambda: canvas.move(sprite, 0, 150))
            ramp = False


def checkCollision(g, frame):
    global width, dir, hit, score, scoreText
    a = canvas.bbox(sprite)
    if a[3] in range((g[3]-150), (g[3])) and(a[0] in range
                                                ((g[0]), (g[2]-75)) or a[2] in range((g[0]+75), (g[2]))):
        if frame == enemy or frame == enemytr:
            canvas.move(frame, (width-g[0]), 0)
        else:
            canvas.move(frame, (-g[0]), 0)

        score += 10
        txt = "Goats knocked out:" + str(score)
        canvas.itemconfigure(scoreText, text=txt)
        canvas.move(sprite, 0, -25)
        window.after(250, lambda: canvas.move(sprite, 0, 25))
    # Enemy collision (Losing condition)
    if a[1] in range((g[1]), (g[3])) and(a[0] in range
                                            ((g[0]), (g[2]-75)) or a[2] in range((g[0]+75), (g[2]))):
        canvas.move(sprite, 0, -250)
        window.after(250, lambda: canvas.move(sprite, 0, 250))
        hit += 1
        canvas.delete(health1)
        # Enemy hit player twice (game over).
        if hit == 2:
            canvas.move(sprite, 0, -height)
            canvas.delete(health2)
            messagebox.showinfo("Game over",
                                "Natural selection got you.\nSurvival of the fittest.\n")
            gameover()
            return


# Enemy movement function (only for normal mode)
# Update: now also controls mating season second goat on right side
def moveenemy():
    global width, dir, hit, score, scoreText, paused, dir3
    mov1 = 12
    mov2 = 8
    if paused == 0:
        g = canvas.bbox(enemy)

        if(diff == "mating"):
            g3 = canvas.bbox(enemytr)
            if g3[0] < 100:
                dir3 = "right"
            if g3[2] > (width-100):
                dir3 = "left"
            if dir3 == "left":
                mov2 = -mov2
        if g[0] < 100:
            dir = "right"
        if g[2] > (width-100):
            dir = "left"
        if dir == "left":
            mov1 = -mov1

        canvas.move(enemy, mov1, 0)
        if(diff == "mating"):
            canvas.move(enemytr, mov2, 0)
        if(over == False):
            if(diff == "mating"):
                window.after(7, moveenemy)
            else:
                window.after(10, moveenemy)
        checkCollision(g, enemy)
        if(diff == "mating"):
            checkCollision(g3, enemytr)


# Second enemy movement function in Hard mode.
# Update: now also controls mating season second goat on left side
def moveenemy2():
    global width, dir2, hit, score, scoreText, paused, dir4
    mov1 = 12
    mov2 = 8
    if paused == 0:
        g2 = canvas.bbox(enemy2)

        if(diff == "mating"):
            g4 = canvas.bbox(enemytl)
            if g4[0] < 100:
                dir4 = "left"
            if g4[2] > (width-100):
                dir4 = "right"
            if dir4 == "right":
                mov2 = -mov2
        if g2[0] < 100:
            dir2 = "left"
        if g2[2] > (width-100):
            dir2 = "right"
        if dir2 == "right":
            mov1 = -mov1

        canvas.move(enemy2, mov1, 0)
        if(diff == "mating"):
            canvas.move(enemytl, mov2, 0)
        if (over == False):
            if(diff == "mating"):
                window.after(7, moveenemy2)
            else:
                window.after(10, moveenemy2)
        checkCollision(g2, enemy2)
        if(diff == "mating"):
            checkCollision(g4, enemytl)


# Normal mode function which is called for hard and Mating season modes.
def normal():
    global score, sprite, enemy, health2, health1, box, scoreText
    global start, start2, start3, diff, boss, start4, start5, start6
    start.destroy()
    start2.destroy()
    start3.destroy()
    start4.destroy()
    start5.destroy()
    start6.destroy()
    diff = "normal"
    bg = canvas.create_image(0, 0, anchor='nw', image=mint)
    sprite = canvas.create_image((width/2), (height-350),
                                 anchor='nw', image=img)

    enemy = canvas.create_image((width-250), (height-350),
                                anchor='nw', image=img2)

    health1 = canvas.create_image(220, 0, anchor='ne', image=snoop)
    health2 = canvas.create_image(100, 0, anchor='ne', image=snoop)
    box = canvas.create_rectangle((width/2-190), (height-610),
                                  (width/2+120), (height-560), fill="brown")

    scoreText = canvas.create_text(width/2, 10, fill="black",
                                   font="terminal 28", text=txt)

    if diff == "normal":
        boss = canvas.create_image(0, -width, anchor='nw', image=bosspic)
    over = False

    moveenemy()
    return


# Hard Mode adds an extra goat.
def hard():
    global enemy2, diff, boss
    normal()
    diff = "hard"
    enemy2 = canvas.create_image(0, (height-350), anchor='nw', image=img)
    if diff == "hard":
        boss = canvas.create_image(0, -width, anchor='nw', image=bosspic)
    over = False
    moveenemy2()
    return


# Mating season adds 2 extra fast goats.
def mating():
    global enemytr, enemytl, diff, boss
    normal()
    hard()
    diff = "mating"

    enemytr = canvas.create_image((width-250), (height-350), # tr=top right    
                                  anchor='nw', image=img2)
    
    enemytl = canvas.create_image(0, (height-350), anchor='nw', image=img) # tl=top left
    boss = canvas.create_image(0, -width, anchor='nw', image=bosspic)
    over = False

    return


# Pause function
def pause(event):
    global paused
    if paused == 0:
        pausetxt = Label(canvas, text="Game paused\
            \nReturn?\nThe game will pause for 3 seconds when\
            you press p again", font="terminal 15", bg="green")
        pausetxt.place(x=width/3, y=100)
        paused += 1
        window.after(10000, lambda: pausetxt.destroy())
    elif paused == 1:
        time.sleep(3)
        paused = 0
    moveenemy()
    move()
    moveenemy2()


# Bosskey
def bosskey(event):
    global boss, width
    canvas.move(boss, 0, width)


# Bosskey reversal button
def bossisgone(event):
    global boss, width
    canvas.move(boss, 0, -width)


def gameover():
    global window, Restart, exitb, menub, hit, over, score
    Restart = Button(window, text="Restart", background="black",
                     foreground="white", activebackground="green", width="17", height="3",
                     font=('terminal', 20), command=lambda: restart())
    Restart.place(x=50, y=50)

    exitb = Button(window, text="Exit", background="black",
                   foreground="white", activebackground="green", width="17", height="3",
                   font=('terminal', 20), command=lambda: window.destroy())
    exitb.place(x=1450, y=50)

    menub = Button(window, text="Return to\nmain menu", background="black",
                   foreground="white", activebackground="green", width="17", height="3",
                   font=('terminal', 20), command=lambda: main_menu())

    menub.place(x=1100, y=50)
    hit = 0
    score = 0
    over = True
    return


# Restart option after losing
def restart():
    global Restart, exitb, menub, diff, speeden, speeden2, hit, over
    Restart.destroy()
    exitb.destroy()
    menub.destroy()
    over = False
    if diff == "normal":
        normal()
    if diff == "hard":
        hard()
    if diff == "mating":
        mating()
    return


# Cheat code 1
def invincibility(event):
    global hit
    if hit == 3:
        hit = 0
        diaz2 = Label(canvas, text="Nick Diaz has retired.\n\
                      You are no longer invincible", font="terminal 15", bg="green")
        diaz2.place(x=width/2, y=100)
        window.after(3000, lambda: diaz2.destroy())
    else:
        hit = 3
        diaz = Label(canvas, text="You have been blessed with the powers of Nick Diaz.\
                     \nYou are now invincible due to high amounts  of THC\
                     (cannabis psychoactive component) in your system.",
                     font="terminal 15", bg="green")
        diaz.place(x=250, y=100)
        window.after(3000, lambda: diaz.destroy())
    return


# Cheat code 2
def speedcheat(event):
    global speed
    if speed == 75:
        speed = 125
        fast = Label(canvas, text="You've been training with Usain Bolt\
                     \nYou are now faster than even the people on steroids. ",
                     font="terminal 15", bg="green")
        fast.place(x=250, y=100)
        window.after(3000, lambda: fast.destroy())
    else:
        speed = 75
        diaz = Label(canvas, text="Your speed is back to normal.\
                     \nStill pretty fast for a goat.", font="terminal 15", bg="green")
        diaz.place(x=250, y=100)
        window.after(3000, lambda: diaz.destroy())

# TKinter window commands.
window = Tk()
width = window.winfo_screenwidth()
# width of screen resolution used for program.
height = window.winfo_screenheight()
# height of screen resolution used for program.
window = setWindowDimensions(width, height)

# Resizing background images to fit different resolutions
image = Image.open("goat.png")
image = image.resize((width, height), Image.ANTIALIAS)
image.save("goatnewres.png")

image2 = Image.open("cage.png")
image2 = image2.resize((width, height), Image.ANTIALIAS)
image2.save("cagenewres.png")

# Images loaded for the program.
img = ImageTk.PhotoImage(file="greg.png")
img2 = ImageTk.PhotoImage(file="gregleft.png")
mint = ImageTk.PhotoImage(file="goatnewres.png")
snoop = ImageTk.PhotoImage(file="420.png")
bosspic = ImageTk.PhotoImage(file="bosspic.png")
bg1 = ImageTk.PhotoImage(file="cagenewres.png")

# Variables used for collision functionality.
ramp = False
hit = 0

# Pause.
over = False
paused = 0

# Directions for enemies.
dir = "left"
dir2 = "right"
dir3 = "left"
dir4 = "right"
speed = 75

# Score text and score variable.
score = 0
txt = "Goats knocked out:" + str(score)

main_menu()

# Key bindings
canvas.bind("<Left>", leftKey)
canvas.bind("<Right>", rightKey)
canvas.bind("<Up>", upKey)
canvas.bind("<p>", pause)
canvas.bind("<b>", bosskey)
canvas.bind("<u>", bossisgone)
canvas.bind("<d>", invincibility)
canvas.bind("<c>", speedcheat)
canvas.focus_set()

# Player direction
direction = ""

# TKinter commands foro opening the window and packing the canvas
canvas.pack()
window.mainloop()
