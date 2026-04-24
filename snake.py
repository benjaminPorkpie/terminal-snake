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
    try:
        return int(file_path.read_text())
    except:
        return 0

def save_high_score(score):
    if score > load_high_score():
        file_path.write_text(str(score))

# ---------------- MENU ----------------
def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(0)

    options = ["Original Snake", "Quit"]
    selected = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "SNAKE GAME"
        stdscr.addstr(5, (w - len(title)) // 2, title)

        hint = "SPACE = Jump (invincibility) | Walls are deadly"
        if w > len(hint):
            stdscr.addstr(7, (w - len(hint)) // 2, hint)

        for i, option in enumerate(options):
            x = (w - len(option)) // 2
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
            return None if selected == 1 else "play"

        stdscr.refresh()

# ---------------- GAME OVER ----------------
def game_over_menu(stdscr, score):
    curses.curs_set(0)
    stdscr.nodelay(0)

    options = ["Play Again", "Menu", "Quit"]
    selected = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "GAME OVER"
        stdscr.addstr(5, (w - len(title)) // 2, title)

        score_text = f"Score: {score}"
        high_text = f"High Score: {load_high_score()}"

        stdscr.addstr(7, (w - len(score_text)) // 2, score_text)
        stdscr.addstr(8, (w - len(high_text)) // 2, high_text)

        for i, option in enumerate(options):
            x = (w - len(option)) // 2
            y = 12 + i

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
            return options[selected]

        stdscr.refresh()

# ---------------- GAME ----------------
def run_game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)

    snake = [(HEIGHT // 2, WIDTH // 2)]
    direction = (0, 1)

    # Wall boundaries (deadly tiles)
    min_x, max_x = 1, WIDTH - 2
    min_y, max_y = 1, HEIGHT - 2

    # Full arena bounds (snake can roam outside walls, wrapping)
    arena_rows = HEIGHT + 2   # some buffer
    arena_cols = WIDTH + 2

    def spawn_food():
        while True:
            f = (
                random.randint(min_y + 1, max_y - 1),
                random.randint(min_x + 1, max_x - 1)
            )
            if f not in snake:
                return f

    food = spawn_food()
    score = 0

    move_delay = 0.1
    last_move = time.time()

    # --- Jumping state ---
    jumping_ticks = 0       # ticks of invincibility remaining
    jump_cooldown_end = 0.0  # timestamp when cooldown expires
    JUMP_COOLDOWN = 5.0      # seconds

    def is_wall(y, x):
        """Returns True if (y, x) is a wall tile."""
        on_top    = (y == min_y - 1)
        on_bottom = (y == max_y + 1)
        on_left   = (x == min_x - 1)
        on_right  = (x == max_x + 1)
        in_col_range = (min_x - 1 <= x <= max_x + 1)
        in_row_range = (min_y - 1 <= y <= max_y + 1)
        return (on_top or on_bottom) and in_col_range or \
               (on_left or on_right) and in_row_range

    while True:
        key = stdscr.getch()

        new_dir = direction
        if key == ord("q"):
            return "menu"
        elif key in [curses.KEY_UP, ord("w")]:
            new_dir = (-1, 0)
        elif key in [curses.KEY_DOWN, ord("s")]:
            new_dir = (1, 0)
        elif key in [curses.KEY_LEFT, ord("a")]:
            new_dir = (0, -1)
        elif key in [curses.KEY_RIGHT, ord("d")]:
            new_dir = (0, 1)
        elif key == ord(" "):
            now = time.time()
            if jumping_ticks == 0 and now >= jump_cooldown_end:
                jumping_ticks = score + 2
                jump_cooldown_end = now + JUMP_COOLDOWN

        if new_dir != opposites[direction]:
            direction = new_dir

        if time.time() - last_move < move_delay:
            continue
        last_move = time.time()

        hy, hx = snake[0]
        new_head = (hy + direction[0], hx + direction[1])

        # Determine if new head is on a wall
        head_on_wall = is_wall(new_head[0], new_head[1])

        if jumping_ticks > 0:
            # Invincible: walls don't kill, self-collision doesn't kill
            jumping_ticks -= 1
            if jumping_ticks == 0:
                # Cooldown starts now (already set when jump was activated)
                pass
        else:
            # Normal: wall or self = death
            if head_on_wall or new_head in snake:
                save_high_score(score)
                return score

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = spawn_food()
        else:
            snake.pop()

        stdscr.erase()

        # Draw walls (always visible)
        for x in range(min_x - 1, max_x + 2):
            try:
                stdscr.addch(min_y - 1, x, "#")
                stdscr.addch(max_y + 1, x, "#")
            except curses.error:
                pass

        for y in range(min_y - 1, max_y + 2):
            try:
                stdscr.addch(y, min_x - 1, "#")
                stdscr.addch(y, max_x + 1, "#")
            except curses.error:
                pass

        # Draw food
        try:
            stdscr.addch(food[0], food[1], "●", curses.color_pair(2))
        except curses.error:
            pass

        # Draw snake (cyan while jumping, red otherwise)
        snake_color = curses.color_pair(3) if jumping_ticks > 0 else curses.color_pair(1)
        for y, x in snake:
            try:
                stdscr.addch(y, x, "O", snake_color)
            except curses.error:
                pass

        # HUD
        now = time.time()
        cooldown_remaining = max(0.0, jump_cooldown_end - now)

        if jumping_ticks > 0:
            jump_status = f"[JUMPING: {jumping_ticks}]"
        elif cooldown_remaining > 0:
            jump_status = f"[COOLDOWN: {cooldown_remaining:.1f}s]"
        else:
            jump_status = "[JUMP READY - SPACE]"

        try:
            stdscr.addstr(HEIGHT, 0, f"Score: {score}   High Score: {load_high_score()}   {jump_status}")
        except curses.error:
            pass

        stdscr.refresh()

# ---------------- MAIN LOOP ---------------
def main(stdscr):
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)  # jumping color

    while True:
        menu_choice = main_menu(stdscr)

        if menu_choice is None:
            break

        while True:
            result = run_game(stdscr)

            if result == "menu":
                break

            choice = game_over_menu(stdscr, result)

            if choice == "Play Again":
                continue
            elif choice == "Menu":
                break
            elif choice == "Quit":
                return

if __name__ == "__main__":
    curses.wrapper(main)
