# Snake

A terminal Snake game made with Python's `curses` module.

## Requirements

- Python 3.7+
- A terminal with at least 80x42 characters
- `curses` (if on Windows, download `windows-curses` with `pip`.

## Running the game

```bash
python snake.py
```

High scores are saved in `data/high-score.txt`. If running from another directory, it will create a data folder and the file in that, so it's recommended to run the game in the directory with the game file in.

## Controls

| Key | Action |
|-----|--------|
| `W` or `↑` | Move up |
| `S` or `↓` | Move down |
| `A` or `←` | Move left |
| `D` or `→` | Move right |
| `Q` | Quit to menu |

## Gameplay

Eat the red food (`●`) to grow and get points. Avoid walls and your tail. There's an occasional yellow `*` food. 

## Scoring

- +1 point per normal food eaten
- High score is saved between sessions

## Files

```
snake.py          # main game file
data/
  high-score.txt  # auto-created
```

## Notes

The game was designed for an 80x42 play area. If your terminal is smaller, things might render weird, or the game might crash. You can play it on a bigger terminal, lower terminal font size, or tweak the game file to make the area smaller.
