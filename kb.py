import time, random, threading
from pynput.keyboard import Key, Controller

# control the script
PAUSED = False
RUNNING = True

# necessary constants
KEY = Key.f20 # the key to press
TIMEOUT = 300 # seconds bewteen inputs

# the keyboard simulator
KB = Controller()

# simulate a keystroke of a key in a direction and wait for some amount of time
def key_sim_and_pause(fn, duration):
    fn(KEY) # call a passed function
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

            # format output nicely
            if RUNNING:
                print("\n>", end=' ', flush=True)
                current = time.mktime(time.localtime()) # update the time

def main():
    global PAUSED
    global RUNNING

    sim_process = threading.Thread(target=sim_input, args=())
    sim_process.start()

    while True:
        user_input = input("> ").lower()

        if user_input == "pause":
            print("pausing...\n")
            PAUSED = True

        if user_input == "resume":
            print("resuming...\n")
            PAUSED = False

        if user_input == "stop":
            print("stopping...\n")
            RUNNING = False
            break

    # kill the sim process
    sim_process.join()

    # make sure that the key is released
    KB.release(KEY)

if __name__ == "__main__":
    main()
