# shellklok

An interactive configurable ASCII clock for terminals using figlet fonts

## Usage
Press `h` to display a help menu that lists keyboard shortcuts.

Press `m` to display a menu of various settings.

## Requirements

### Core Dependencies
1. **Python 3.6+** (with `curses` support)
2. **figlet** - ASCII art generator

### Python Modules
- `configparser` (included in Python Standard Library since 3.2)

---

## Installation

### 1. Install figlet
#### Linux:
```bash
# Debian/Ubuntu/Baby's First Linux Distro
sudo apt install figlet

# Fedora/RHEL
sudo dnf install figlet

# Arch
sudo pacman -S figlet
```

#### macOS (Homebrew):
```bash
brew install figlet
```

### 2. Optional: Install Additional Fonts
```bash
# Debian/Ubuntu/Baby's First Linux Distro
sudo apt install figlet-fonts

# Fedora/RHEL
sudo dnf install figlet-fonts

# Arch User Repository (AUR)
yay figlet-fonts

# Or download fonts manually from:
# http://www.figlet.org/fontdb.cgi
```

### 3. Verify Installation
Test figlet works in your terminal:
```bash
figlet "Test"
```

---

## Platform Notes
- **Linux**: Works best with full-featured terminals (kitty, gnome-terminal, etc)
- **macOS**: Requires terminal with curses support (iTerm2 recommended)
- **Windows**: Not officially supported (curses compatibility issues), but might work in WSL2. You're a windows user, I'm sure you can figure it out /s.

---

## Configuration
The program automatically creates:
```bash
~/.config/shellklok/config.ini
```
on first run to store your preferences.

![a screencap](https://i.imgur.com/TCN5nba.png)
![a second screencap](https://i.imgur.com/wKxglrk.png)
![a third screencap](https://i.imgur.com/lU52MVW.png)
