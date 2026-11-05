import tkinter as tk
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        



#game window

window = tk.Tk()
window.title("Snake")
window.resizable(False, False)


canvas = tk.Canvas(window, bg="green" , width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()


#center the wondow

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initilize game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #single tile snake. Snake head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE) #food tile
snake_body = [] # snake tiles body parts
velocity_x = 0
velocity_y = 0
game_over = False
score = 0


def change_direction(e):
    #print(e.keysym)
    global velocity_x, velocity_y, game_over

    if(game_over):
        return

    if(e.keysym == "Up" and velocity_y != 1):  # Prevent the snake from reversing
        velocity_x = 0
        velocity_y = -1
    elif(e.keysym == "Down" and velocity_y != -1):  # Prevent the snake from reversing
        velocity_x = 0
        velocity_y = 1
    elif(e.keysym == "Left" and velocity_x != 1):  # Prevent the snake from reversing
        velocity_x = -1
        velocity_y = 0
    elif(e.keysym == "Right" and velocity_x != -1):  # Prevent the snake from reversing
        velocity_x = 1
        velocity_y = 0



def move_snake():
    global snake, food, snake_body, game_over, score

    if(game_over):
        return

    if(snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return

    for tile in snake_body:
        if(snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    #check for colition with food
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))  # Add a new tile to the snake's body
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if(i == 0):
            tile.x = snake.x                
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y 

    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE



def draw():
    global snake, food, snake_body, game_over, score  # get the variables from the global scope
    move_snake()

    canvas.delete("all")  # clear the canvas before drawing the new frame

    canvas.create_rectangle(food.x, food.y, food.x+TILE_SIZE, food.y+TILE_SIZE, fill= "Red") # create food og color;

    canvas.create_rectangle(snake.x, snake.y, snake.x+TILE_SIZE, snake.y+TILE_SIZE, fill= "Blue") # create snaken og colour;

    for til in snake_body:
        canvas.create_rectangle(til.x, til.y, til.x+TILE_SIZE, til.y+TILE_SIZE, fill= "Blue") # create snaken og colour;

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, text=f"GAME OVER You got: {score} Apples", font=("Arial", 20), fill="white")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score:{score}", fill = "white") #display score


    window.after(90, draw) #draw per 100 ms 

   

draw() #call draw function to start the game loop


window.bind("<KeyRelease>", change_direction) #bind key release event to the windo

window.mainloop()