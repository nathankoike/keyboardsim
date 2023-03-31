import time, random, threading, sys
from pynput.keyboard import Key, Controller

# control the script
PAUSED = False
RUNNING = True
FULL_MANUAL = False

# desired automatic start time and pause duration
START_TIME = "08:00:00"
END_TIME = "16:30:00"

# necessary constants
KEY = Key.f20 # the key to press
TIMEOUT = 50 # seconds bewteen inputs
WEEKEND_START = 5 # on which day does the weekend start?

# the keyboard simulator
KB = Controller()

# return true if time1 >= time2
def check_time(time1, time2):
	[time1_h, time1_m, time1_s] = time1
	[time2_h, time2_m, time2_s] = time2

	# hours
	if time1_h > time2_h:
		return True
	if time1_h < time2_h:
		return False

	# minutes
	if time1_m > time2_m:
		return True
	if time1_m < time2_m:
		return False

	# seconds
	if time1_s < time2_s:
		return False

	return True

# simulate a keystroke of a key in a direction and wait for some amount of time
def key_sim_and_pause(fn, duration):
	fn(KEY)
	time.sleep(0.001 * duration) # sleep for some number of ms

# simulate some keypresses
def sim_input():
	# the current time
	current = time.mktime(time.localtime())

	while RUNNING:
		# don't simulate unnecessary keystrokes
		if time.mktime(time.localtime()) - current < TIMEOUT:
			continue

		if not PAUSED:
			# simulate some keystrokes
			for i in range(10):
				key_sim_and_pause(KB.press, random.randint(20, 31))
				key_sim_and_pause(KB.release, random.randint(100, 501))

			# update the time
			current = time.mktime(time.localtime())

# check the current time against the start and end times
def time_check():
	global PAUSED, RUNNING, FULL_MANUAL, START_TIME, END_TIME, WEEKEND_START

	start_time = [int(i) for i in START_TIME.split(':')[:]]
	end_time = [int(i) for i in END_TIME.split(':')[:]]

	while RUNNING:
		current = time.localtime()
		[current_day, current_hrs, current_min, current_sec] = [
			current.tm_wday,
			current.tm_hour,
			current.tm_min,
			current.tm_sec]

		# conditionally toggle the script on
		if current_day < WEEKEND_START and \
			check_time([current_hrs, current_min, current_sec], start_time) and \
			check_time(end_time, [current_hrs, current_min, current_sec]) and \
			not FULL_MANUAL and \
			PAUSED:
				print("\nresuming...\n\n> ", end="")
				PAUSED = False

		# conditionally toggle the script off
		elif check_time([current_hrs, current_min, current_sec], end_time) and \
			not FULL_MANUAL and not PAUSED:
			print("\npausing...\n\n> ", end="")
			PAUSED = True

def main():
	global PAUSED, RUNNING, FULL_MANUAL, START_TIME, END_TIME

	# set the start and end times based on the flags
	start_time_flag = sys.argv.index("-s") if "-s" in sys.argv else -1
	end_time_flag = sys.argv.index("-e") if "-e" in sys.argv else -1

	if start_time_flag >= 0:
		START_TIME = sys.argv[start_time_flag + 1]
	if end_time_flag >= 0:
		END_TIME = sys.argv[end_time_flag + 1]

	[start_hrs, start_min, start_sec] = [int(i) for i in START_TIME.split(':')[:]]
	[end_hrs, end_min, end_sec] = [int(i) for i in END_TIME.split(':')[:]]

	current_time = time.localtime()
	[current_day, current_hrs, current_min, current_sec] = [
		current_time.tm_wday,
		current_time.tm_hour,
		current_time.tm_min,
		current_time.tm_sec]

	# # current, start
	# # end, current
	# print(current_day < WEEKEND_START and \
	# 		check_time([current_hrs, current_min, current_sec], [start_hrs, start_min, start_sec]) and \
	# 		check_time([end_hrs, end_min, end_sec], [current_hrs, current_min, current_sec]))
	# return

	# start the multithreaded processes
	time_process = threading.Thread(target=time_check, args=())
	sim_process = threading.Thread(target=sim_input, args=())

	time_process.start()
	sim_process.start()

	# user input loop
	while True:
		user_input = input("> ").lower()

		if user_input == "pause":
			print("pausing...\n")
			PAUSED = True

		if user_input == "resume":
			print("resuming...\n")
			PAUSED = False

		# toggle automatatic controls
		if user_input == "full manual":
			print("toggling manual control...\n")
			FULL_MANUAL = not FULL_MANUAL

		# kill the program
		if user_input == "stop":
			print("stopping...\n")
			RUNNING = False
			break

	# kill the multithreaded processes
	sim_process.join()
	time_process.join()

	# make sure that the key is released
	KB.release(KEY)

if __name__ == "__main__":
	main()
