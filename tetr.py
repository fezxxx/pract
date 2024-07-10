import tkinter as tk
from PIL import Image, ImageTk
import random
import tkinter.simpledialog
# Настройки игры
WIDTH = 800
HEIGHT = 600
EGG_WIDTH = 45
EGG_HEIGHT = 55
BOMB_WIDTH = 50
BOMB_HEIGHT = 50
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 100
SCORE_TO_WIN = 255
class CatcherGame:
    def __init__(self, root):
        self.root = root
        self.root.title('bloooooom')

        self.egg_image = ImageTk.PhotoImage(Image.open("C:/tt/egg.png"))
        self.bomb_image = ImageTk.PhotoImage(Image.open("C:/tt/bomb.png"))
        self.catcher_image = ImageTk.PhotoImage(Image.open("C:/tt/catcher.png"))

        self.canvas = tk.Canvas(root, bg='white', width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.catcher = self.canvas.create_image(WIDTH / 2, HEIGHT - CATCHER_HEIGHT / 2, image=self.catcher_image)
        self.canvas.bind_all('<Left>', self.move_left)
        self.canvas.bind_all('<Right>', self.move_right)

        self.eggs = []
        self.bombs = []
        self.score = 0
        self.egg_speed = 10
        self.bomb_speed = 10
        self.egg_interval = 4000
        self.bomb_interval = 5000

        self.set_difficulty()
        self.create_eggs()
        self.create_bombs()
        self.update_game()
        self.display_score()

    def set_difficulty(self):
        difficulty = tk.simpledialog.askstring("Сложность", "Выберите сложность: "
                                                            "легко, средне, тяжело")
        if difficulty == 'легко':
            self.egg_speed = 5
            self.bomb_speed = 5
            self.egg_interval = 5000
            self.bomb_interval = 6000
        elif difficulty == 'тяжело':
            self.egg_speed = 15
            self.bomb_speed = 15
            self.egg_interval = 3000
            self.bomb_interval = 4000

    def create_eggs(self):
        x = random.randint(0, WIDTH - EGG_WIDTH)
        y = 0
        new_egg = self.canvas.create_image(x + EGG_WIDTH / 2, y + EGG_HEIGHT / 2, image=self.egg_image)
        self.eggs.append(new_egg)
        self.root.after(self.egg_interval, self.create_eggs)

    def create_bombs(self):
        x = random.randint(0, WIDTH - BOMB_WIDTH)
        y = 0
        new_bomb = self.canvas.create_image(x + BOMB_WIDTH / 2, y + BOMB_HEIGHT / 2, image=self.bomb_image)
        self.bombs.append(new_bomb)
        self.root.after(self.bomb_interval, self.create_bombs)

    def move_left(self, event):
        x, y = self.canvas.coords(self.catcher)
        if x > CATCHER_WIDTH / 2:
            self.canvas.move(self.catcher, -20, 0)

    def move_right(self, event):
        x, y = self.canvas.coords(self.catcher)
        if x < WIDTH - CATCHER_WIDTH / 2:
            self.canvas.move(self.catcher, 20, 0)

    def check_catch(self):
        catcher_coords = self.canvas.coords(self.catcher)
        for egg in self.eggs:
            egg_coords = self.canvas.coords(egg)
            if self.check_overlap(catcher_coords, egg_coords):
                self.canvas.delete(egg)
                self.eggs.remove(egg)
                self.score += 5
                self.display_score()
                if self.score >= SCORE_TO_WIN:
                    self.end_game(win=True)
        for bomb in self.bombs:
            bomb_coords = self.canvas.coords(bomb)
            if self.check_overlap(catcher_coords, bomb_coords):
                self.canvas.delete(bomb)
                self.bombs.remove(bomb)
                self.end_game(win=False)

    def check_overlap(self, catcher_coords, obj_coords):
        x_catcher, y_catcher = catcher_coords
        x_obj, y_obj = obj_coords
        if (x_obj >= x_catcher - CATCHER_WIDTH / 2 and
                x_obj <= x_catcher + CATCHER_WIDTH / 2 and
                y_obj >= y_catcher - CATCHER_HEIGHT / 2 and
                y_obj <= y_catcher + CATCHER_HEIGHT / 2):
            return True
        return False

    def update_game(self):
        for egg in self.eggs:
            self.canvas.move(egg, 0, self.egg_speed)
            if self.canvas.coords(egg)[1] > HEIGHT:
                self.canvas.delete(egg)
                self.eggs.remove(egg)
        for bomb in self.bombs:
            self.canvas.move(bomb, 0, self.bomb_speed)
            if self.canvas.coords(bomb)[1] > HEIGHT:
                self.canvas.delete(bomb)
                self.bombs.remove(bomb)
        self.check_catch()
        self.canvas.after(100, self.update_game)

    def display_score(self):
        self.canvas.delete('score')
        score_text = f"Очки: {self.score}"
        self.canvas.create_text(70, 10, anchor='nw', text=score_text, fill='black', font=('Helvetica', 14),
                                tags='score')

    def end_game(self, win):
        end_text = "Игра окончена: Вы победили!" if win else "Игра окончена: Вы проиграли!"
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=end_text, fill="green", font=('Helvetica', 30))
        self.root.after(2000, self.root.destroy)
if __name__ == "__main__":
    root = tk.Tk()
    game = CatcherGame(root)
    root.mainloop()