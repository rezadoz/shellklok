#----shellklok v0.8-2025-11-1-------#
#----written by bryan reza----------#
#----bug fixes and optimizations----#

import datetime os subprocess sys time
import argparser configparser curses

#--constants--#
REFRESH_INTERVAL = 0.1
CONFIG_SAVE_DELAY = 2.0

def get_available_fonts():
    try:
        font_dir = subprocess.check_output(["figlet", "-I", "2"], universal_newlines=True).strip()
    except subprocess.CalledProcessError:
        font_dir = "/usr/share/figlet/fonts"

    fonts = []
    try:
        for f in os.listdir(font_dir):
            if f.endswith((".flf", ".tlf")):
                fonts.append(os.path.splitext(f)[0])
        fonts.sort()
    except FileNotFoundError:
        fonts = ["slant", "block", "jazmine"]

    if not fonts:
        raise RuntimeError("No figlet fonts found. Please install figlet.")

    return fonts

def load_config():
    defaults = {
        "FONT": 0,
        "COLOR": 0,
        "SECONDS": 0,
        "MODE": 0
    }
    config_dir = os.path.expanduser("~/.config/shellklok")
    config_path = os.path.join(config_dir, "config.ini")
    if not os.path.exists(config_path):
        return defaults.copy()

    config = configparser.ConfigParser()
    try:
        config.read(config_path)
    except (configparser.Error, IOError):
        return defaults.copy()

    state = defaults.copy()
    if not config.has_section('settings'):
        return state

    try:
        state["FONT"] = config.getint('settings', 'font')
    except (configparser.NoOptionError, ValueError):
        pass
    try:
        state["COLOR"] = config.getint('settings', 'color')
    except (configparser.NoOptionError, ValueError):
        pass
    try:
        state["SECONDS"] = config.getint('settings', 'seconds')
    except (configparser.NoOptionError, ValueError):
        pass
    try:
        state["MODE"] = config.getint('settings', 'mode')
    except (configparser.NoOptionError, ValueError):
        pass

    return state

def save_config(state):
    config_dir = os.path.expanduser("~/.config/shellklok")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.ini")
    config = configparser.ConfigParser()
    config['settings'] = {
        'font': str(state["FONT"]),
        'color': str(state["COLOR"]),
        'seconds': str(state["SECONDS"]),
        'mode': str(state["MODE"])
    }
    with open(config_path, 'w') as configfile:
        config.write(configfile)

class ClockMenu:
    def __init__(self, fonts):
        self.selected = 0
        self.items = [
            ("FONT", fonts),
            ("COLOR", ["white", "red", "green", "yellow",
                      "blue", "magenta", "cyan", "black"]),
            ("SECONDS", ["ON", "OFF"]),
            ("MODE", ["24h", "12h"])
        ]

    def show(self, stdscr, current_state):
        self.values = current_state.copy()
        curses.curs_set(0)
        stdscr.nodelay(0)

        while True:
            height, width = stdscr.getmaxyx()
            menu_height = len(self.items) + 2  # +2 for borders
            menu_width = 35

            if menu_height > height or menu_width > width:
                break

            win_y = (height - menu_height) // 2
            win_x = (width - menu_width) // 2
            win = curses.newwin(menu_height, menu_width, win_y, win_x)
            win.border()

            for idx, (label, options) in enumerate(self.items):
                if idx == self.selected:
                    win.attron(curses.A_REVERSE)

                current_val = options[self.values[label]]
                win.addstr(idx+1, 2, f"{label:8}: <{current_val:15}>")

                if idx == self.selected:
                    win.attroff(curses.A_REVERSE)

            win.refresh()
            key = stdscr.getch()

            if key in [ord('m'), 10, 13]:
                break
            elif key in [curses.KEY_UP, ord('k')]:
                self.selected = max(0, self.selected - 1)
            elif key in [curses.KEY_DOWN, ord('j')]:
                self.selected = min(len(self.items)-1, self.selected + 1)
            elif key in [curses.KEY_LEFT, ord('h')]:
                key_name = self.items[self.selected][0]
                self.values[key_name] = max(0, self.values[key_name]-1)
            elif key in [curses.KEY_RIGHT, ord('l')]:
                key_name = self.items[self.selected][0]
                max_val = len(self.items[self.selected][1])-1
                self.values[key_name] = min(max_val, self.values[key_name]+1)

        stdscr.nodelay(1)
        return self.values

def print_help():
    """Print help message to stdout."""
    help_text = """shellklok - an ASCII digital tty clock using figlet

Usage: shellklok [OPTIONS]

Options:
  -h, --help    Show this help message and exit

Interactive Controls:
  [q/x] - quit
  [c]   - cycle colors
  [f]   - cycle fonts forward
  [F]   - cycle fonts backward
  [s]   - toggle seconds
  [a]   - 12/24h mode
  [m]   - settings menu
  [h]   - show help dialog
"""
    print(help_text)

def show_help(stdscr):
    help_text = [
        "shellklok",
        "an ASCII digital tty clock using figlet",
        "[q/x] - quit",
        "[c]   - cycle colors",
        "[f]   - cycle fonts forward",
        "[F]   - cycle fonts backward",
        "[s]   - toggle seconds",
        "[a]   - 12/24h mode",
        "[m]   - settings menu",
        "[h]   - this help"
    ]
    height, width = stdscr.getmaxyx()
    window_height = len(help_text) + 2  # +2 for borders
    window_width = max(len(line) for line in help_text) + 4

    if window_height > height or window_width > width:
        return

    win = curses.newwin(window_height, window_width,
                       (height - window_height) // 2,
                       (width - window_width) // 2)
    win.border()
    for i, line in enumerate(help_text):
        win.addstr(i+1, 2, line)
    win.refresh()

    stdscr.nodelay(0)
    stdscr.getch()
    stdscr.nodelay(1)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    curses.start_color()

    # color configuration
    color_info = [
        ("white", curses.COLOR_WHITE),
        ("red", curses.COLOR_RED),
        ("green", curses.COLOR_GREEN),
        ("yellow", curses.COLOR_YELLOW),
        ("blue", curses.COLOR_BLUE),
        ("magenta", curses.COLOR_MAGENTA),
        ("cyan", curses.COLOR_CYAN),
        ("black", curses.COLOR_BLACK)
    ]

    # initialize color pairs once
    for pair_num, (name, color) in enumerate(color_info, start=1):
        curses.init_pair(pair_num, color, curses.COLOR_BLACK)

    # create color mapping dictionary once
    color_map = {name: pair_num for pair_num, (name, color) in enumerate(color_info, start=1)}

    try:
        fonts = get_available_fonts()
    except RuntimeError as e:
        stdscr.addstr(0, 0, str(e))
        stdscr.refresh()
        time.sleep(3)
        return

    menu = ClockMenu(fonts)
    state = load_config()

    # clamp loaded state to valid ranges
    state["FONT"] = max(0, min(state["FONT"], len(fonts)-1))
    state["COLOR"] = max(0, min(state["COLOR"], len(color_info)-1))
    state["SECONDS"] = 1 if state["SECONDS"] else 0
    state["MODE"] = 1 if state["MODE"] else 0

    # cache for figlet output
    last_time_str = ""
    cached_art = ""

    # debounced config saving
    config_dirty = False
    last_change_time = 0

    while True:
        current_time = time.time()

        # save config if dirty and enough time has passed
        if config_dirty and (current_time - last_change_time) >= CONFIG_SAVE_DELAY:
            save_config(state)
            config_dirty = False

        key = stdscr.getch()
        if key in [ord('q'), ord('x')]:
            if config_dirty:
                save_config(state)
            break
        elif key == ord('h'):
            show_help(stdscr)
        elif key == ord('m'):
            new_state = menu.show(stdscr, state)
            state = new_state
            config_dirty = True
            last_change_time = current_time
        elif key == ord('c'):
            state["COLOR"] = (state["COLOR"] + 1) % len(color_info)
            config_dirty = True
            last_change_time = current_time
        elif key == ord('f'):
            if fonts:
                state["FONT"] = (state["FONT"] + 1) % len(fonts)
                config_dirty = True
                last_change_time = current_time
        elif key == ord('F'):
            if fonts:
                state["FONT"] = (state["FONT"] - 1) % len(fonts)
                config_dirty = True
                last_change_time = current_time
        elif key == ord('s'):
            state["SECONDS"] = 1 - state["SECONDS"]
            config_dirty = True
            last_change_time = current_time
        elif key == ord('a'):
            state["MODE"] = 1 - state["MODE"]
            config_dirty = True
            last_change_time = current_time

        # time formatting
        if state["MODE"] == 1:
            time_format = "%I:%M:%S %p" if state["SECONDS"] == 1 else "%I:%M %p"
        else:
            time_format = "%H:%M:%S" if state["SECONDS"] == 1 else "%H:%M"

        time_str = datetime.datetime.now().strftime(time_format)

        # update figlet output only if time has changed
        if time_str != last_time_str:
            try:
                cached_art = subprocess.check_output(
                    ["figlet", "-t", "-f", fonts[state["FONT"]], time_str],
                    universal_newlines=True,
                    stderr=subprocess.DEVNULL
                )
                last_time_str = time_str
            except (subprocess.CalledProcessError, FileNotFoundError):
                cached_art = "FIGLET ERROR\nPlease install figlet"
                last_time_str = time_str

        stdscr.erase()
        height, width = stdscr.getmaxyx()
        lines = cached_art.split('\n')
        start_y = max(0, (height - len(lines)) // 2)

        # get current color
        color_name = menu.items[1][1][state["COLOR"]]
        color_pair = color_map[color_name]

        for i, line in enumerate(lines):
            if i >= height:
                break
            x = max(0, (width - len(line)) // 2)
            if x < width:
                stdscr.addstr(start_y + i, x, line[:width-1], curses.color_pair(color_pair))

        stdscr.refresh()
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="shellklok - an ASCII digital tty clock using figlet",
        add_help=False
    )
    parser.add_argument('-h', '--help', action='store_true',
                       help='Show this help message and exit')

    args = parser.parse_args()

    if args.help:
        print_help()
        sys.exit(0)

    curses.wrapper(main)
