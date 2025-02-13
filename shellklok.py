import os
import curses
import datetime
import subprocess
import time

def get_available_fonts():
    font_dir = "/usr/share/figlet/fonts"
    fonts = []
    try:
        for f in os.listdir(font_dir):
            if f.endswith((".flf", ".tlf")):
                fonts.append(os.path.splitext(f)[0])
        fonts.sort()
    except FileNotFoundError:
        fonts = ["slant", "block", "jazmine"]
    return fonts

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
            h, w = stdscr.getmaxyx()
            menu_h = len(self.items) + 2
            menu_w = 35

            if menu_h > h or menu_w > w:
                break

            win_y = (h - menu_h) // 2
            win_x = (w - menu_w) // 2
            win = curses.newwin(menu_h, menu_w, win_y, win_x)
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

def show_help(stdscr):
    help_text = [
        "shellklok",
        "an ASCII digital tty clock using figlet",
        "[q/x] - quit",
        "[c]   - cycle colors",
        "[f]   - cycle fonts",
        "[s]   - toggle seconds",
        "[a]   - 12/24h mode",
        "[m]   - settings menu",
        "[h]   - this help"
    ]
    h, w = stdscr.getmaxyx()
    win_h = len(help_text) + 2
    win_w = max(len(line) for line in help_text) + 4

    if win_h > h or win_w > w:
        return

    win = curses.newwin(win_h, win_w, (h-win_h)//2, (w-win_w)//2)
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

    # Updated color order with white first
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

    # Initialize color pairs (1-8)
    for pair_num, (name, color) in enumerate(color_info, start=1):
        curses.init_pair(pair_num, color, curses.COLOR_BLACK)

    # Create color mapping dictionary
    color_map = {name: pair_num for pair_num, (name, color) in enumerate(color_info, start=1)}

    fonts = get_available_fonts()
    menu = ClockMenu(fonts)

    state = {
        "FONT": 0,
        "COLOR": 0,  # Starts at 0 (white)
        "SECONDS": 0,
        "MODE": 0
    }

    while True:
        key = stdscr.getch()
        if key in [ord('q'), ord('x')]:
            break
        elif key == ord('h'):
            show_help(stdscr)
        elif key == ord('m'):
            new_state = menu.show(stdscr, state)
            if new_state is not None:
                state = new_state
        elif key == ord('c'):
            state["COLOR"] = (state["COLOR"] + 1) % len(color_info)
        elif key == ord('f'):
            state["FONT"] = (state["FONT"] + 1) % len(fonts)
        elif key == ord('s'):
            state["SECONDS"] = 1 - state["SECONDS"]
        elif key == ord('a'):
            state["MODE"] = 1 - state["MODE"]

        # Time formatting
        if state["MODE"] == 1:
            time_format = "%I:%M:%S %p" if state["SECONDS"] == 0 else "%I:%M %p"
        else:
            time_format = "%H:%M:%S" if state["SECONDS"] == 0 else "%H:%M"

        time_str = datetime.datetime.now().strftime(time_format)

        try:
            art = subprocess.check_output(
                ["figlet", "-t", "-f", fonts[state["FONT"]], time_str],
                universal_newlines=True
            )
        except:
            art = "FONT ERROR"

        stdscr.erase()
        h, w = stdscr.getmaxyx()
        lines = art.split('\n')
        start_y = max(0, (h - len(lines)) // 2)

        # Get current color (now white is index 0)
        color_name = menu.items[1][1][state["COLOR"]]
        color_pair = color_map[color_name]

        for i, line in enumerate(lines):
            if i >= h:
                break
            x = max(0, (w - len(line)) // 2)
            stdscr.addstr(start_y + i, x, line[:w-1], curses.color_pair(color_pair))

        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)
