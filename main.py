from threading import Thread
from ahk import AHK
import time
import mido

mid = mido.MidiFile("Xi - Freedom Dive.mid")

# keycodes = list('1!2@34$5%6^78*9(0qQwWeErtTyYuiIoOpPasSdDfgGhHjJklLzZxcCvVbBnm') # starving pianists
middlec = keycodes.index('t') # t is middle c

notes = []

absolute_time = 0
for message in mid:
    absolute_time += message.time
    if message.type == 'note_on':
        note = message.note
        offset = note-60
        try:
                notes.append({
                'key': keycodes[middlec+offset],
                'time': absolute_time
            })
        except IndexError: pass

def play_key(note):
    while not all_threads_created:
        time.sleep(note['time'])
        if stop: return
        # print(note['key'])
        ahk.key_press(note['key'])
        '''ahk.key_down(note['key'])
        time.sleep(1)
        ahk.key_up(note['key'])'''

stop = False
ahk = AHK(executable_path=r'C:\Program Files\AutoHotkey\AutoHotkey.exe')

def stopprogram():
    global stop
    stop = not stop
    print('Stopping', stop)

ahk.add_hotkey('^x', callback=stopprogram) # stop
ahk.start_hotkeys()

win = ahk.win_get(title='Roblox')
win.activate()
        
all_threads_created = False
for note in notes:
    Thread(target=lambda: play_key(note)).start()
all_threads_created = True
