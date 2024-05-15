from aiy.board import Board, Led
from aiy.voice.audio import play_wav

import threading
import subprocess

def button_listener():
	VOLUME_LEVELS = [0, 100, 75, 50]
	volume_index = 0
	with Board() as board:
		while True:
			board.button.wait_for_press()
			board.led.state = Led.ON
			
			board.button.wait_for_release()
			board.led.state = Led.OFF
			
			volume_index += 1
			volume_index = volume_index % len(VOLUME_LEVELS)
			set_volume(VOLUME_LEVELS[volume_index])

def main():
	set_volume(0)
	thread = threading.Thread(target=button_listener, args=())
	thread.start()
	while True:
		play_wav('./brown_noise.wav')

def set_volume(percent):
    cmd = ['amixer', 'set', 'Master', '--', '%d%%' %(percent)]
    print("Changing volume")
    print(" ".join(cmd))
    subprocess.Popen(cmd).wait()

if __name__ == '__main__':
	main()

