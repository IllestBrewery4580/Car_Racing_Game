import tkinter as tk
import random

# ---- CONFIG ----
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
MISSILE_SPEED = 5
INTERCEPTOR_SPEED = 10

drivers = ["Gummy Gabe", "Lolli Luna", "Fizz Finn", "Lemon Daphne", "Moon Maisy", "Trolli Turbo", "Mushroom Turtle"]
cars = ["Candy Cruiser", "Fudge Rocket", "Marshmellow Drifter"]

# ---- GLOBALS ----
selected_driver = None
selected_car = None
missile = []
interceptors = []

# ---- SELECTION SCREEN ----
def show_selection_screen():
    selection_win = tk.Tk()
    selection_win.title("Choose Your Candy Champion")
    selection_win.geometry("400x300")

    def select_driver(d):
        global selective_driver
        selected_driver = d
        driver_label.config(text=f"Driver: {d}")

    def select_car(c):
        global selected_car
        selected_car = c
        car_label.config(text=f"Car: {c}")

    def start_game():
        if selected_driver and selected_car:
            selection_win.destroy()
            start_race_window()
        else:
            warning_label.config(text="Please choose both a driver and a car!")

    tk.Label(selection_win, text="Pick Your Driver", font=("Helvetica", 14)).pack()
    for d in drivers:
        tk.Button(selection_win, text=d, command=lambda d=d: select_driver(d)).pack()

    driver_label = tk.Label(selection_win, text="Driver: None", fg="blue")
    driver_label.pack(pady=5)

    tk.Label(selection_win, text="Pick Your Car", font=("Helvetica", 14)).pack()
    for c in cars:
        tk.Button(selection_win, text=c, command=lambda c=c: select_car(c)).pack()

    car_label = tk.Label(selection_win, text="Car: None", fg="green")
    car_label.pack(pady=5)

    warning_label = tk.Label(selection_win, text="", fg="red")
    warning_label.pack()

    tk.Button(selection_win, text="Start Race!", font=("Helvetica", 12, "bold"), command=start_game).pack(pady=10)

    selection_win.mainloop()

#---- SETUP ----
root = tk.Tk()
root.title("Sugar Rush Showdown")
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="pink")
canvas.pack()

# ---- SPRITES ----
car = canvas.create_rectangle(270, 350, 330, 380, fill="violet", outline="white")
missile = []
interceptors = []

# ---- CHECK COLLISIONS ----
def check_collisions():
    score += 10
    update_score()
    for m in missile[:]:
        mx1, my1, mx2, my2 = canvas.coords(m)
        for i in interceptors[:]:
            ix1, iy1, ix2, iy2 = canvas.coords(i)
            # Simple AABB collision
            if mx1 < ix2 and mx2 > ix1 and my1 < iy2 and my2 > iy1:
                canvas.delete(m)
                canvas.delete(i)
                missile.remove(m)
                interceptors.remove(i)
                break

# ---- MOVE CAR ----
CAR_SPEED = 5
car_speed = 0

def move_car(event):
    global car_speed
    if event.keysym == "LEFT":
        canvas.move(car, -CAR_SPEED, 0)
    elif event.keysym == "Right":
        canvas.move(car, CAR_SPEED, 0)
    elif event.keysym == "Up":
        car_speed += 1  # simulate acceleration
    elif event.keysym == "Down":
        car_speed = max(0, car_speed - 1)

canvas.bind_all("<KeyPress>", move_car)

# ---- MOVE MISSILES ----
def move_missile():
    for m in missile:
        canvas.move(m, 0, MISSILE_SPEED)
        if canvas.coords(m)[1] > WINDOW_HEIGHT:
            canvas.delete(m)
            missile.remove(m)
    root.after(50, move_missile)

# ---- SCORE WHEN DESTROYING MISSILE ----
score = 0
score_text = canvas.create_text(500, 20, text=f"Score: {score}", font=("Helvetica", 14, "bold"), fill="white")

def update_score():
    canvas.itemconfig(score_text, text=f"Score: {score}")

# ---- RANKS ----
round_num = 1
round_text = canvas.create_text(500, 50, text=f"Wave: {round_num}", font=("Helvetica", 14), fill="white")

def update_round():
    global round_numround_num += 1
    canvas.itemconfig(round_text, text=f"Wave: {round_num}")

# ---- FIRE INTERCEPTOR ----
def fire_interceptor(event):
    interceptor = canvas.create_oval(290, 340, 310, 360, fill="cyan", outline="white")
    interceptors.append(interceptor)

def move_interceptors():
    for i in interceptors:
        canvas.move(i, 0, -INTERCEPTOR_SPEED)
        if canvas.coords(i)[3] < 0:
            canvas.delete(i)
            interceptors. remove(i)
    root.after(50, move_interceptors)

# ---- SPAWN MISSILE ----
def spawn_missile():
    x = random.randint(50, WINDOW_WIDTH - 50)
    m = canvas.create_oval(x, 0, x + 20, 20, fill="red", outline="white")
    missile.append(m)
    root.after(1500, spawn_missile)

def game_loop():
    move_missile()
    move_interceptors()
    check_collisions()
    root.after(16, game_loop) # ~60 FPS

# ---- START GAME ----
canvas.bind_all("<space>", fire_interceptor)
spawn_missile()
move_missile()
move_interceptors()

game_loop()
root.mainloop()

# ---- LAUNCH ----
show_selection_screen()
