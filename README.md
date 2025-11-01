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

<img width="855" height="565" alt="image" src="https://github.com/user-attachments/assets/d62b7a10-949c-483f-be69-4da267c95994" />
<img width="855" height="565" alt="image" src="https://github.com/user-attachments/assets/9dc7fc4f-7416-4527-81a1-46ac1fac9502" />
<img width="855" height="565" alt="image" src="https://github.com/user-attachments/assets/23933f6b-e26a-4ef6-9059-d0ee8649cbad" />

