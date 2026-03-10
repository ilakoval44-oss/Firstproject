import math
import random
import tkinter as tk
import winsound
import sys
import os

# RESOURCE PATH
def resource_path(filename):
    """Возвращает путь к файлу внутри exe или в обычной папке"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

# WINDOW
window = tk.Tk()
window.title("LuckySpin (modified)")
window.geometry("650x650")
window.configure(bg="#2b2b2b")

canvas = tk.Canvas(window, width=400, height=400, bg="#1e1e1e", highlightthickness=0)
canvas.place(x=20, y=50)

#COLORS & EASTER EGGS -----------------
available_colors = [
    "red", "blue", "green", "yellow", "orange",
    "purple", "pink", "cyan", "magenta", "lime",
    "teal", "gold", "violet", "turquoise", "silver"
]

easter_eggs = {
    "Краузе": "Старый король",
    "Илья": "Мастер кода",
    "Кирилл": "Славян 4-Muerta",
    "Веталь": "Самый сильный шаринган",
    "Димон": "Покемон-кун",
    "Даня": "Ишак5",
    "Ростик": "Дика свиня",
    "Артем": "Игрок-казуалич",
    "Серега": "Бандит с черными форсами",
    "Давид": "SC-репер"
}

random.shuffle(available_colors)

confetti = []
my_list = []
sector_colors = []

angle = 0
is_spinning = False

# INTERFACE
entry_name = tk.Entry(window, bg="gray", fg="white")
entry_name.place(x=460, y=50)

status_label = tk.Label(window, text="Enter a name", bg="#2b2b2b", fg="white")
status_label.place(x=475, y=80)

listbox = tk.Listbox(window, height=10, width=15)
listbox.place(x=475, y=140)
listbox.config(bg="#1e1e1e", fg="white", selectbackground="#444", selectforeground="cyan", font=("Arial", 10))

forced_sector = tk.StringVar()
forced_sector.set("None")

tk.Label(window, text="Force result:", bg="#2b2b2b", fg="white").place(x=500, y=420)

option_menu = tk.OptionMenu(window, forced_sector, "None")
option_menu.place(x=500, y=450)

# LOGIC
def generate_random_color():
    return f'#{random.randint(0, 0xFFFFFF):06x}'

def get_unique_color():
    if available_colors:
        return available_colors.pop()
    return generate_random_color()

def circum():
    canvas.delete("all")
    x, y, radius = 200, 200, 150
    if not my_list:
        return
    parts = len(my_list)
    step = 360 / parts
    for i in range(parts):
        start = i * step + angle
        canvas.create_arc(x - radius, y - radius, x + radius, y + radius,
                          start=start, extent=step, fill=sector_colors[i], outline="white")
        mid_angle = math.radians(start + step / 2)
        tx = x + (radius * 0.6) * math.cos(mid_angle)
        ty = y - (radius * 0.6) * math.sin(mid_angle)
        canvas.create_text(tx, ty, text=my_list[i], fill="white", font=("Arial", 10, "bold"))
    canvas.create_polygon(200, 30, 190, 10, 210, 10, fill="red")
def update_option_menu():
    menu = option_menu["menu"]
    menu.delete(0, "end")

    for name in my_list:
        menu.add_command(label=name, command=lambda value=name: forced_sector.set(value))
def on_name():
    name = entry_name.get().strip()
    if name and name not in my_list:
        my_list.append(name)
        sector_colors.append(get_unique_color())
        entry_name.delete(0, tk.END)
        status_label.config(text=f"Added {name}")
        listbox.insert(tk.END, name)
        update_option_menu()
        circum()
    elif name in my_list:
        status_label.config(text="Name already exists!")

def start_spin():
    global is_spinning
    if not is_spinning and my_list:
        is_spinning = True
        winsound.PlaySound(resource_path("spin_sound.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
        animate()

def animate():
    global angle
    if is_spinning:
        angle += 10
        circum()
        window.after(10, animate)

def stop_spin():
    global is_spinning, angle
    if not my_list: 
        return
    is_spinning = False
    angle = random.uniform(0, 360)
    winsound.PlaySound(None, winsound.SND_PURGE)
    winsound.PlaySound(resource_path("mellstroy-raduet.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
    circum()
    status_label.config(text="Wheel stopped!")
    determine_winner()

# WINNER
def show_winner(name):
    popup = tk.Toplevel(window)
    popup.title("WINNER!")
    popup.geometry("400x400")
    popup.configure(bg="black")
    win_canvas = tk.Canvas(popup, width=400, height=400, bg="black", highlightthickness=0)
    win_canvas.pack()
    win_canvas.create_text(200, 150, text=f"🎉 {name} 🎉", fill="gold", font=("Arial", 28, "bold"))
    create_confetti(win_canvas)
    animate_confetti(win_canvas)

def create_confetti(win_canvas):
    global confetti
    confetti.clear()
    for _ in range(30):
        x = random.randint(0, 400)
        y = random.randint(0, 400)
        color = random.choice(["red", "yellow", "green", "blue", "pink"])
        dot = win_canvas.create_oval(x, y, x + 5, y + 5, fill=color)
        confetti.append(dot)

def animate_confetti(win_canvas):
    for dot in confetti:
        win_canvas.move(dot, 0, 5)
    win_canvas.after(50, lambda: animate_confetti(win_canvas))

def determine_winner():
    global angle
    if not my_list:  # <- перевірка на порожній список
        status_label.config(text="Список порожній! Додайте імена.")
        return

    if forced_sector.get() in my_list:
        winner = forced_sector.get()
    else:
        normalized_angle = angle % 360
        pointer_angle = (90 - normalized_angle) % 360
        step = 360 / len(my_list)
        index = int(pointer_angle // step)
        winner = my_list[index]

    winner_display = easter_eggs.get(winner, winner)
    show_winner(winner_display)
# IMAGE
img = tk.PhotoImage(file=resource_path("image.png"))
small_img = img.subsample(10, 10)
img_label = tk.Label(window, image=small_img, bg="#2b2b2b")
img_label.place(x=560, y=560)
img_label.image = small_img

# BUTTONS
tk.Button(window, text="Add", command=on_name).place(x=450, y=110)
tk.Button(window, text="Spin!", command=start_spin, bg="green", fg="white").place(x=500, y=110)
tk.Button(window, text="Stop!", command=stop_spin, bg="red", fg="white").place(x=540, y=110)

#  DEBUG
#print(os.path.exists(resource_path("spin_sound.wav")))
#print("Current working directory:", os.getcwd())
#print(os.listdir("."))

window.mainloop()