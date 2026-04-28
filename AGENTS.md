# AGENTS.md

## Project Overview

**shellklok** is a single-file Python terminal clock that renders the current time as ASCII art using `figlet`. It runs in a `curses` TUI, supports interactive font/color/mode configuration, and persists settings across sessions via an INI file in `~/.config/shellklok/`.

The entire application lives in one file: `shellklok.py` (~351 lines, Python 3.6+).

---

## Repository Structure

```
shellklok/
├── shellklok.py   # Entire application — TUI loop, config, menus, figlet integration
├── shell.nix      # Nix dev shell (provides python3 + figlet)
├── README.md
└── LICENSE        # GPL-3.0
```

---

## Architecture

### Entry Point
`shellklok.py` is run directly. It uses `argparse` to handle `--help`, then hands off to `curses.wrapper(main)`.

### Key Functions

| Function | Purpose |
|---|---|
| `get_available_fonts()` | Queries figlet for its font directory, returns sorted list of `.flf`/`.tlf` font names |
| `load_config()` | Reads `~/.config/shellklok/config.ini`; returns defaults if missing or corrupt |
| `save_config(state)` | Writes current state to config; called on exit or after a debounce delay (`CONFIG_SAVE_DELAY = 2.0s`) |
| `ClockMenu.show()` | Draws a bordered curses window for interactive settings (font, color, seconds, 12/24h mode) |
| `show_help()` / `print_help()` | In-TUI help overlay (curses) and stdout help text (CLI `--help`) |
| `main(stdscr)` | Core event loop: reads keys, calls figlet via subprocess, renders centered ASCII art with curses color pairs |

### State Object
A plain dict is passed around everywhere:
```python
state = {
    "FONT":    int,   # index into fonts list
    "COLOR":   int,   # index into color_info list
    "SECONDS": 0|1,   # show seconds toggle
    "MODE":    0|1,   # 0 = 24h, 1 = 12h
}
```

### Figlet Integration
The time string is passed to `figlet` via `subprocess.check_output`. Output is cached and only regenerated when the displayed time string changes, keeping CPU usage low.

### Config Persistence
Config writes are debounced: a `config_dirty` flag is set on any state change, and `save_config()` is only called once `CONFIG_SAVE_DELAY` (2 seconds) has elapsed since the last change. A final save is also triggered on clean exit (`q` or `x`).

---

## Dependencies

- **Python 3.6+** with `curses` (stdlib)
- **figlet** (system binary — must be on `$PATH`)
- Python stdlib only: `os`, `sys`, `curses`, `datetime`, `subprocess`, `time`, `configparser`, `argparse`
- No `pip` dependencies.

The Nix dev shell (`shell.nix`) provides both `python3` and `figlet` automatically.

---

## How to Run

```bash
# Install figlet (Debian/Ubuntu)
sudo apt install figlet

# Run the clock
python3 shellklok.py

# Show CLI help
python3 shellklok.py --help
```

---

## Interactive Keybindings

| Key | Action |
|---|---|
| `q` / `x` | Quit |
| `h` | Show help overlay |
| `m` | Open settings menu |
| `c` | Cycle color forward |
| `f` / `F` | Cycle font forward / backward |
| `s` | Toggle seconds display |
| `a` | Toggle 12h / 24h mode |

In the settings menu, use arrow keys or `hjkl` to navigate, `←`/`→` to change values, and `m` or Enter to close.

---

## Configuration File

Auto-created at `~/.config/shellklok/config.ini` on first state change:

```ini
[settings]
font = 0
color = 0
seconds = 0
mode = 0
```

Values are indices into the corresponding option lists. Corrupt or missing keys fall back to defaults silently.

---

## Agent Guidelines

### Making Changes

- **All logic is in `shellklok.py`**. There are no modules, packages, or imports beyond stdlib + the `figlet` binary.
- The main loop runs at `REFRESH_INTERVAL = 0.1s`. Avoid adding blocking calls inside it.
- Figlet is called via subprocess — do not replace this with a Python figlet library without confirming the font discovery logic (`figlet -I 2`) still works.
- `curses` is finicky about writing to the last cell of the screen (`width-1` guard is intentional — don't remove it).

### Testing

There is no test suite. To manually validate:
1. Run `python3 shellklok.py` and confirm the clock renders and updates.
2. Exercise all keybindings.
3. Quit and relaunch — confirm settings persisted in `~/.config/shellklok/config.ini`.
4. Test with `figlet` uninstalled to confirm the error path in `get_available_fonts()` and the `FIGLET ERROR` fallback render gracefully.

### Nix Users

```bash
nix-shell   # drops into a shell with python3 + figlet
python3 shellklok.py
```

### Platform Notes

- **Linux**: Primary target. Works with any terminal with curses support.
- **macOS**: Supported; iTerm2 recommended.
- **Windows**: Not officially supported. WSL2 may work.

### Style

- No external dependencies — keep it that way.
- Keep the single-file structure; do not split into modules unless the file grows substantially.
- Use `subprocess.check_output` with `stderr=subprocess.DEVNULL` for figlet calls.
- State is a plain dict — no dataclasses or namedtuples needed at this scale.
