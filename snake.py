import curses
import random
import sys
import subprocess
from pathlib import Path

data_folder = Path("data")
file_path = data_folder / "high-score.txt"
data_folder.mkdir(exist_ok=True)

if not file_path.exists():
    with open("data/high-score.txt", "w", encoding="utf-8") as f:
        f.write("0")

# Game Configuration
WIDTH = 80
HEIGHT = 40

opposites = {
    (-1, 0): (1, 0),
    (1, 0): (-1, 0),
    (0, -1): (0, 1),
    (0, 1): (0, -1)
}

def main(stdscr):
    def save_high_score(score):
        with open("data/high-score.txt", "r", encoding="utf-8") as f:
            data = f.read()

        if int(data) < score:
            with open("data/high-score.txt", "w", encoding="utf-8") as f:
                f.write(str(score))
    def is_valid_direction_change(current, new):
        return new != opposites(current)

    def pause_game(stdscr):
        stdscr.nodelay(0)

        stdscr.clear()
        stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 5, "PAUSED")
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('p'):
                break

        stdscr.nodelay(1)

    with open("data/high-score.txt", "r", encoding="utf-8") as f:
            high_score_data = f.read()

    curses.start_color()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    paused = False

    # Colors
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    # Initial snake setup
    snake = [(HEIGHT // 2, WIDTH // 2)]
    direction = (0, 1)  # moving right

    food = (random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2))
    score = 0

    while True:
        stdscr.clear()

        # Draw borders
        for x in range(WIDTH):
            stdscr.addch(0, x, "#")
            stdscr.addch(HEIGHT - 1, x, "#")
        for y in range(HEIGHT):
            stdscr.addch(y, 0, "#")
            stdscr.addch(y, WIDTH - 1, "#")

        # Draw food
        stdscr.addch(food[0], food[1], "¤", curses.color_pair(2))

        # Draw snake
        for y, x in snake:
            stdscr.addch(y, x, "O", curses.color_pair(1))

        stdscr.addstr(HEIGHT, 0, f"Score: {score}")
        stdscr.addstr(HEIGHT+2, 0, f"High Score: {high_score_data}")

        key = stdscr.getch()

        new_direction = direction
        if key == ord('q'):
            return
        elif key == ord('p'):
            pause_game(stdscr)
        elif key == curses.KEY_UP or key == ord("w"):
            new_direction = (-1, 0)
        elif key == curses.KEY_DOWN or key == ord("s"):
            new_direction = (1, 0)
        elif key == curses.KEY_LEFT or key == ord("a"):
            new_direction = (0, -1)
        elif key == curses.KEY_RIGHT or key == ord("d"):
            new_direction = (0, 1)

        if new_direction != opposites[direction]:
            direction = new_direction

        # Move snake
        head_y, head_x = snake[0]
        new_head = (head_y + direction[0], head_x + direction[1])

        # Collision with wall or self
        if (
            new_head[0] in [0, HEIGHT - 1] or
            new_head[1] in [0, WIDTH - 1] or
            new_head in snake
        ):
            stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 5, "GAME OVER")
            stdscr.refresh()
            curses.napms(1500)

            save_high_score(score=score)

            subprocess.run(["python3", "snake.py"])
            sys.exit()

        snake.insert(0, new_head)

        # Eat food
        if new_head == food:
            score += 1
            while True:
                food = (random.randint(1, HEIGHT - 2),
                        random.randint(1, WIDTH - 2))
                if food not in snake:
                    break
        else:
            snake.pop()

        stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
