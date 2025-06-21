#!/usr/bin/env python3
import sys
import subprocess
import os

def check_python_libs():
    try:
        import cv2
        import numpy as np
        return True
    except ImportError:
        return False

def install_deps():
    print("Installing dependencies: opencv-python, numpy ...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "opencv-python", "numpy"])
        print("Dependencies installed successfully! Please rerun the eggspionage command.")
    except subprocess.CalledProcessError:
        print("Failed to install dependencies automatically. Please install manually:")
        print("  pip install --user opencv-python numpy")

def main():
    if "--setup" in sys.argv:
        install_deps()
        sys.exit(0)

    if not check_python_libs():
        print("Error: Required Python packages are missing.\n")
        print("Run this command to install them:")
        print("  eggspionage --setup")
        sys.exit(1)

    import cv2
    import numpy as np

    try:
        from colorama import init, Fore, Style
        init()
        COLORAMA = True
    except ImportError:
        COLORAMA = False

    ASCII_CHARS = " .:-=+*#%@"
    WIDTH = 120
    HEIGHT = int(WIDTH * 0.55)
    RESET_COLOR = '\033[0m'

    MULTICOLOR_RGB = [
        (255, 0, 0), (255, 255, 0), (0, 255, 0),
        (0, 255, 255), (0, 0, 255), (255, 0, 255),
    ]

    MULTICOLOR_SEQ = [
        '\033[31m', '\033[33m', '\033[32m',
        '\033[36m', '\033[34m', '\033[35m',
    ]

    def supports_color():
        return sys.stdout.isatty()

    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m" if supports_color() else ''

    COLOR_CODES = {
        'r': rgb_to_ansi(255, 0, 0),
        'g': rgb_to_ansi(0, 255, 0),
        'b': rgb_to_ansi(0, 150, 255),
    }

    def clear_terminal():
        os.system("cls" if os.name == "nt" else "clear")

    def lerp_color(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    def frame_to_ascii(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (WIDTH, HEIGHT))
        normalized = resized / 255.0
        ascii_frame = [
            "".join(ASCII_CHARS[int(val * (len(ASCII_CHARS) - 1))] for val in row)
            for row in normalized
        ]
        return ascii_frame

    def colorize_ascii(ascii_lines, color_mode, frame_count, smooth_step=20):
        if color_mode == 'm':
            total_colors = len(MULTICOLOR_RGB)
            phase = (frame_count // smooth_step) % total_colors
            next_phase = (phase + 1) % total_colors
            t = (frame_count % smooth_step) / smooth_step
            r, g, b = lerp_color(MULTICOLOR_RGB[phase], MULTICOLOR_RGB[next_phase], t)
            color = rgb_to_ansi(r, g, b)
            colored_lines = [color + line + RESET_COLOR for line in ascii_lines]

        elif color_mode == 'd':
            color = MULTICOLOR_SEQ[frame_count % len(MULTICOLOR_SEQ)]
            colored_lines = [color + line + RESET_COLOR for line in ascii_lines]

        elif color_mode in COLOR_CODES:
            color = COLOR_CODES[color_mode]
            colored_lines = [color + line + RESET_COLOR for line in ascii_lines]

        else:
            colored_lines = ascii_lines

        return colored_lines

    def run_ascii_cam(color_mode=None):
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("fragile: Couldn't access camera.")
            sys.exit(1)

        frame_count = 0
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                ascii_lines = frame_to_ascii(frame)
                colored_ascii = colorize_ascii(ascii_lines, color_mode, frame_count)
                clear_terminal()
                print("\n".join(colored_ascii))
                frame_count += 1

                if cv2.waitKey(1) == 27:
                    break
        except KeyboardInterrupt:
            print("\nEggspionage ended 🐣🕵️‍♂️")
        finally:
            cap.release()

    color_arg = None
    if len(sys.argv) > 2 and sys.argv[1] == '-c':
        color_arg = sys.argv[2].lower()
        if color_arg not in ['r', 'g', 'b', 'm', 'd']:
            print("fragile: Invalid color mode. Use one of r, g, b, m, d")
            sys.exit(1)

    run_ascii_cam(color_mode=color_arg)

if __name__ == "__main__":
    main()
