# Snake

A terminal Snake game written in Python using `curses`. Classic gameplay with a few twists built on top — nothing too fancy, just a solid snake game you can actually sit down and play.

## Requirements

- Python 3.7+
- A terminal with at least 80x42 characters
- `curses` (standard library on Linux/macOS; on Windows, use WSL or install `windows-curses`)

## Running the game

```bash
python snake.py
```

That's it. High scores are saved automatically to `data/high-score.txt`.

## Controls

| Key | Action |
|-----|--------|
| `W` / `↑` | Move up |
| `S` / `↓` | Move down |
| `A` / `←` | Move left |
| `D` / `→` | Move right |
| `Q` | Quit to menu |

## Gameplay

Eat the red food (`●`) to grow and earn points. Avoid the walls and your own tail — hit either and it's game over. The snake speeds up as you play.

There's a special food item that shows up occasionally as a yellow `*`. It works a bit differently from normal food, so does eating it.

There's a useful action that can be done to save yourself, or to just have fun, though it costs you a point!

## Scoring

- +1 point per normal food eaten
- High score is saved between sessions

## Files

```
snake.py          # main game file
data/
  high-score.txt  # auto-created on first run
```

## Notes

The game was designed for an 80x40 play area. If your terminal is smaller, things might render oddly — resize it before launching. The menu navigates with the same WASD/arrow keys as the game.
