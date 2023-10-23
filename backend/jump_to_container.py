#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import docker
import subprocess

client = docker.from_env()

screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
screen.keypad(1)
selection = -1
option = 0

containers = sorted(
    list(filter(
        lambda cnt: cnt.status == u'running',
        client.containers.list()
    )),
    key=lambda cnt: cnt.name
)
list_len = len(containers) + 1

while selection < 0:
    screen.clear()
    h = [0] * list_len
    h[option] = curses.color_pair(1)

    current_idx = 0
    current_line = 2

    for container in containers:
        screen.addstr(current_line, 4, container.name, h[current_idx])
        current_line += 1
        current_idx += 1
    screen.addstr(current_line, 4, "Exit ('q')", h[current_idx])
    screen.refresh()

    q = screen.getch()
    if q == curses.KEY_UP or q == ord('k'):      # KEY_UP or 'k' on vim mode
        option = (option - 1) % list_len
    elif q == curses.KEY_DOWN or q == ord('j'):  # KEY_DOWN or 'j' on vim mode
        option = (option + 1) % list_len
    elif q == ord('\n'):
        selection = option
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        subprocess.call(["docker", "exec", "-ti", containers[selection].name, "bash"])
    if q == ord('q') or selection == list_len:  # If 'q' or select 'Exit', then quit
        break


curses.nocbreak()
curses.echo()
curses.endwin()
