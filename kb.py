import time, multiprocessing, random, threading
from pynput.keyboard import Key, Controller

PAUSED = False
RUNNING = True

# The keyboard simulator
KB = Controller()

# simulate some keypresses
def sim_input():
    while RUNNING:
        if not PAUSED:
            print("\nsending inputs...")

            # simulate a keyboard
            for i in range(10):
                KB.press(Key.f20)

                # pause for a short amount of time (at least 20 ms)
                time.sleep(0.001 * random.randint(20, 31))

                KB.release(Key.f20)

                # pause for a random amount of time (at least 100 ms)
                time.sleep(0.001 * random.randint(100, 501))

            # format output nicely
            if RUNNING:
                print("\n>", end=' ', flush=True)

        # wait for 5 mins
        time.sleep(3)

def main():
    global PAUSED
    global RUNNING

    # simulate the keyboard
    sim_process = threading.Thread(target=sim_input, args=())
    sim_process.start()

    while True:
        user_input = input("> ")

        if user_input.lower() == "pause":
            print("pausing...\n")
            PAUSED = True

        if user_input.lower() == "resume":
            print("resuming...\n")
            PAUSED = False

        if user_input == "STOP":
            print("stopping...\n")
            RUNNING = False
            break

    # kill the sim process
    sim_process.join()

    # make sure that the key is released
    KB.release(Key.f20)

if __name__ == "__main__":
    main()
