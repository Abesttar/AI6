from tkinter import *
import random

# --- Global Variables ---
WIDTH = 900
HEIGHT = 300
PAD_W = 10
PAD_H = 100
BALL_RADIUS = 20
INITIAL_SPEED = 10
BALL_SPEED_UP = 1.05
BALL_MAX_SPEED = 40

PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# --- Score Update Function ---
def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)
    spawn_ball()

# --- Ball Spawn Function ---
def spawn_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    c.coords(BALL,
             WIDTH/2 - BALL_RADIUS,
             HEIGHT/2 - BALL_RADIUS,
             WIDTH/2 + BALL_RADIUS,
             HEIGHT/2 + BALL_RADIUS)
    direction = random.choice([-1, 1])
    BALL_X_SPEED = INITIAL_SPEED * direction
    BALL_Y_SPEED = random.randint(-INITIAL_SPEED, INITIAL_SPEED)

# --- Ball Bounce Function ---
def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_X_SPEED *= -BALL_SPEED_UP
        if abs(BALL_X_SPEED) > BALL_MAX_SPEED:
            BALL_X_SPEED = BALL_MAX_SPEED if BALL_X_SPEED > 0 else -BALL_MAX_SPEED
        BALL_Y_SPEED = random.randint(-10, 10)
    elif action == "ricochet":
        BALL_Y_SPEED *= -1

# --- Ball Movement Function ---
def move_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    ball_left, ball_top, ball_right, ball_bottom = c.coords(BALL)
    ball_center_y = (ball_top + ball_bottom) / 2

    c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)

    if ball_top + BALL_Y_SPEED < 0 or ball_bottom + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

    if ball_left + BALL_X_SPEED < PAD_W:
        if c.coords(LEFT_PAD)[1] < ball_center_y < c.coords(LEFT_PAD)[3]:
            bounce("strike")
        else:
            update_score("right")
    elif ball_right + BALL_X_SPEED > WIDTH - PAD_W:
        if c.coords(RIGHT_PAD)[1] < ball_center_y < c.coords(RIGHT_PAD)[3]:
            bounce("strike")
        else:
            update_score("left")

# --- Paddle Movement ---
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0
PAD_SPEED = 15

def move_pads():
    c.move(LEFT_PAD, 0, LEFT_PAD_SPEED)
    if c.coords(LEFT_PAD)[1] < 0:
        c.coords(LEFT_PAD, PAD_W/2, 0, PAD_W/2, PAD_H)
    elif c.coords(LEFT_PAD)[3] > HEIGHT:
        c.coords(LEFT_PAD, PAD_W/2, HEIGHT - PAD_H, PAD_W/2, HEIGHT)

    c.move(RIGHT_PAD, 0, RIGHT_PAD_SPEED)
    if c.coords(RIGHT_PAD)[1] < 0:
        c.coords(RIGHT_PAD, WIDTH - PAD_W/2, 0, WIDTH - PAD_W/2, PAD_H)
    elif c.coords(RIGHT_PAD)[3] > HEIGHT:
        c.coords(RIGHT_PAD, WIDTH - PAD_W/2, HEIGHT - PAD_H, WIDTH - PAD_W/2, HEIGHT)

# --- Keyboard Handlers ---
def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED

def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ("w", "s"):
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0

# --- Game Loop ---
def main_loop():
    move_ball()
    move_pads()
    root.after(10, main_loop)

# --- Setup Window ---
root = Tk()
root.title("Pong")
root.resizable(False, False)

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")
c.pack()

# --- Drawing Elements ---
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white", dash=(5, 5))

BALL = c.create_oval(0, 0, 0, 0, fill="white")
LEFT_PAD = c.create_line(PAD_W/2, HEIGHT/2 - PAD_H/2,
                         PAD_W/2, HEIGHT/2 + PAD_H/2,
                         width=PAD_W, fill="yellow")
RIGHT_PAD = c.create_line(WIDTH - PAD_W/2, HEIGHT/2 - PAD_H/2,
                          WIDTH - PAD_W/2, HEIGHT/2 + PAD_H/2,
                          width=PAD_W, fill="yellow")

p_1_text = c.create_text(WIDTH/4, PAD_H/4,
                         text=PLAYER_1_SCORE,
                         font="Arial 20", fill="white")
p_2_text = c.create_text(WIDTH * 3/4, PAD_H/4,
                         text=PLAYER_2_SCORE,
                         font="Arial 20", fill="white")

# --- Keyboard Bindings ---
root.bind("<KeyPress>", movement_handler)
root.bind("<KeyRelease>", stop_pad)

# --- Start Game ---
spawn_ball()
main_loop()
root.mainloop()
