import curses
import random
import time
from pathlib import Path

# ---------------- FILE SETUP ----------------
data_folder = Path("data")
file_path = data_folder / "high-score.txt"
data_folder.mkdir(exist_ok=True)

if not file_path.exists():
    file_path.write_text("0", encoding="utf-8")

# ---------------- CONFIG ----------------
WIDTH = 80
HEIGHT = 40

opposites = {
    (-1, 0): (1, 0),
    (1, 0): (-1, 0),
    (0, -1): (0, 1),
    (0, 1): (0, -1)
}

# ---------------- UTIL ----------------
def load_high_score():
    return int(file_path.read_text())

def save_high_score(score):
    current = load_high_score()
    if score > current:
        file_path.write_text(str(score))

# ---------------- MENU ----------------
def main_menu(stdscr):
    options = [
        "1. Original Snake",
        "2. Expanding Map",
        "3. Shrinking Map",
        "Quit"
    ]

    selected = 0

    while True:
        stdscr.clear()

        h, w = stdscr.getmaxyx()

        stdscr.addstr(5, w//2 - 6, "SNAKE GAME")

        for i, option in enumerate(options):
            x = w//2 - len(option)//2
            y = 10 + i

            if i == selected:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, option)

        key = stdscr.getch()

        if key in [curses.KEY_UP, ord("w")]:
            selected = (selected - 1) % len(options)
        elif key in [curses.KEY_DOWN, ord("s")]:
            selected = (selected + 1) % len(options)
        elif key in [10, 13]:
            if selected == 3:
                return None
            return selected

        stdscr.refresh()

# ---------------- GAME ----------------
def run_game(stdscr, mode):
    curses.curs_set(0)
    stdscr.nodelay(1)

    snake = [(HEIGHT // 2, WIDTH // 2)]
    direction = (0, 1)

    min_x, max_x = 1, WIDTH - 2
    min_y, max_y = 1, HEIGHT - 2

    def spawn_food():
        while True:
            f = (random.randint(min_y, max_y),
                 random.randint(min_x, max_x))
            if f not in snake:
                return f

    food = spawn_food()
    score = 0

    move_delay = 0.1
    last_move = time.time()

    while True:
        key = stdscr.getch()

        new_dir = direction
        if key == ord("q"):
            return
        elif key in [curses.KEY_UP, ord("w")]:
            new_dir = (-1, 0)
        elif key in [curses.KEY_DOWN, ord("s")]:
            new_dir = (1, 0)
        elif key in [curses.KEY_LEFT, ord("a")]:
            new_dir = (0, -1)
        elif key in [curses.KEY_RIGHT, ord("d")]:
            new_dir = (0, 1)

        if new_dir != opposites[direction]:
            direction = new_dir

        now = time.time()
        if now - last_move < move_delay:
            continue
        last_move = now

        head_y, head_x = snake[0]
        new_head = (head_y + direction[0], head_x + direction[1])

        # COLLISION
        if (
            new_head[0] < min_y or new_head[0] > max_y or
            new_head[1] < min_x or new_head[1] > max_x or
            new_head in snake
        ):
            save_high_score(score)
            return

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = spawn_food()

            # GAME MODES
            if mode == 1:  # expanding
                min_x = max(1, min_x - 1)
                min_y = max(1, min_y - 1)
                max_x = min(WIDTH - 2, max_x + 1)
                max_y = min(HEIGHT - 2, max_y + 1)

            elif mode == 2:  # shrinking
                min_x += 1
                min_y += 1
                max_x -= 1
                max_y -= 1

        else:
            snake.pop()

        # DRAW
        stdscr.erase()

        # Borders
        for x in range(min_x - 1, max_x + 2):
            stdscr.addch(min_y - 1, x, "#")
            stdscr.addch(max_y + 1, x, "#")

        for y in range(min_y - 1, max_y + 2):
            stdscr.addch(y, min_x - 1, "#")
            stdscr.addch(y, max_x + 1, "#")

        # Food
        stdscr.addch(food[0], food[1], "¤")

        # Snake
        for y, x in snake:
            stdscr.addch(y, x, "O")

        stdscr.addstr(HEIGHT, 0, f"Score: {score}")
        stdscr.addstr(HEIGHT + 1, 0, f"High Score: {load_high_score()}")

        stdscr.refresh()

# ---------------- MAIN LOOP ----------------
def main(stdscr):
    curses.start_color()
    curses.use_default_colors()

    while True:
        mode = main_menu(stdscr)

        if mode is None:
            break

        run_game(stdscr, mode)

        # GAME OVER SCREEN
        stdscr.clear()
        stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 5, "GAME OVER")
        stdscr.addstr(HEIGHT // 2 + 1, WIDTH // 2 - 10, "Press any key...")
        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
