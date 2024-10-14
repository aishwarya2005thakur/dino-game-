import curses
import time

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Don't block on getch()
    stdscr.timeout(100) # Set a timeout for getch()

    height, width = stdscr.getmaxyx()
    score = 0
    speed = 40
    jump_height = 0

    def display_instructions():
        stdscr.clear()
        stdscr.addstr(1, 10, "Press X to Exit, Press Space to Jump")
        stdscr.addstr(1, 62, "SCORE: ")
        stdscr.addstr(1, 70, str(score))
        stdscr.addstr(height - 1, 0, '�' * (width - 1))

    def draw_character(jump_state):
        nonlocal jump_height
        if jump_state == 0:
            jump_height = 0
        elif jump_state == 1:
            jump_height += 1
        elif jump_state == 2:
            jump_height -= 1

        for i in range(6):
            stdscr.addstr(15 - jump_height + i, 2, " " * 20)  # Clear previous character
        stdscr.addstr(15 - jump_height, 2, "         #####")
        stdscr.addstr(16 - jump_height, 2, "         #####")
        stdscr.addstr(17 - jump_height, 2, "         #####")
        stdscr.addstr(18 - jump_height, 2, "    #    #####")
        stdscr.addstr(19 - jump_height, 2, "   ###   ######")
        stdscr.addstr(20 - jump_height, 2, "  ###########  ")
        stdscr.addstr(21 - jump_height, 2, "    ########    ")
        stdscr.addstr(22 - jump_height, 2, "     ####      ")
        stdscr.refresh()

    def draw_obstacle(x):
        stdscr.addstr(20, width - x, "  O   O ")
        stdscr.addstr(21, width - x, "  O   O ")
        stdscr.addstr(22, width - x, " OOOOOO ")
        stdscr.addstr(23, width - x, "   O    ")
        stdscr.addstr(24, width - x, "   O    ")
        stdscr.refresh()

    x = 0
    while True:
        display_instructions()
        jump_state = 0

        # Move the character and check for input
        while True:
            draw_character(jump_state)
            draw_obstacle(x)
            x += 1

            if x == width - 10:  # Reset obstacle position
                x = 0
                score += 1
                if speed > 20:
                    speed -= 1
            
            time.sleep(0.1)  # Adjust speed

            # Handle user input
            key = stdscr.getch()
            if key == curses.KEY_SPACE:
                jump_state = 1
                for _ in range(10):  # Jump up
                    draw_character(jump_state)
                    time.sleep(0.05)
                jump_state = 2
                for _ in range(10):  # Fall down
                    draw_character(jump_state)
                    time.sleep(0.05)
                jump_state = 0
            elif key == ord('x'):
                return

            # Check for collision
            if x >= width - 10 and jump_height < 4:
                stdscr.addstr(height // 2, width // 2 - 5, "Game Over!")
                stdscr.refresh()
                stdscr.getch()
                return

curses.wrapper(main)
