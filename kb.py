import time, multiprocessing
from pynput.keyboard import Key, Controller

# whether the script is running
PAUSED = False

# The keyboard simulator
KB = Controller()

# simulate some keypresses
def sim_input():
    while True:
        if not PAUSED:
            # press a key that does nothing
            for _ in range(5):
                KB.press(Key.f20)
                KB.release(Key.f20)
                time.sleep(1)

        # wait for 5 mins
        time.sleep(300)

def main():
    global PAUSED

    running = True

    # simulate the keyboard
    sim_process = multiprocessing.Process(target=sim_input, args=())
    sim_process.start()

    while running:
        user_input = input("> ")

        # pause the script
        if not PAUSED and user_input.lower() == "pause":
            print("pausing...")
            PAUSED = True

        # resume the script
        if PAUSED and user_input.lower() == "resume":
            print("resuming...")
            PAUSED = False

        # end the script
        if user_input == "STOP":
            running = False

    # kill the sim process
    sim_process.terminate()
    sim_process.join()

    # make sure that the key is released
    KB.release(Key.f20)

if __name__ == "__main__":
    main()
