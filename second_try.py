# monkeys numpy

import numpy as np
import multiprocessing as mp
from os import cpu_count


# constants that will not change in the middle of the script
TARGET_WORD = "nate is a chud"
TARGET_WORD = TARGET_WORD.upper()
TARGET_CHARS = np.array(list(TARGET_WORD), dtype=str)
WINDOW_SIZE = len(TARGET_WORD)
CHARACTERS_PER_CYCLE = 10000000
LIST_OF_CHARS = np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ ,.'"), dtype=str)

# function to prettify
def convert_to_letter_suffix(pNUM):
    letters = ["", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "De"]
    # index goes 0 1 2 3 4 6 7 8 9 10 11
    # need exp go 0 3 6 9 12 15 18 21 24 27 30 33
    for index, suffix in enumerate(letters):
        if pNUM / (10 ** (index * 3)) < 1000:
            return str(round(pNUM / (10 ** (index * 3)))) + letters[index]

# main function
def gen_and_test(pCHARS, pTARGET, pWINSIZE, pCPC, pFLAG):
    # make a unique random rng, different for each worker
    rng = np.random.default_rng()
    chars_genned = 0
    end_of_last_rng = np.array([], dtype=str)
    while True:
        # check pFLAG to not waste resources on genning a new batch
        if pFLAG.is_set():
            return (False, pTARGET, None, None) # Didnt find it so cant return a index or characters genned, so they are None
            break
        
        random_chars = rng.choice(pCHARS, pCPC)
        new_rng_arr = np.concatenate((end_of_last_rng, random_chars))
        window = np.lib.stride_tricks.sliding_window_view(new_rng_arr, window_shape=pWINSIZE)

        # np.all checks if every value in an array is true, the "window == pTARGET" means that it compares the arrays for similarities at the same index
        identical_check = np.all((window == pTARGET), 1)
        if np.any(identical_check): # if this passes make the stop flag true to stop all other 
            pFLAG.set()
            found_index = np.where(identical_check)[0][0]
            fixed_chars_genned = chars_genned + found_index
            print(f"yeah, found match at index {found_index:,} after {fixed_chars_genned:,} characters")
            print(f"{window[np.where(identical_check)[0]]}") # gets starting index of match
            return (True, pTARGET, found_index, fixed_chars_genned)
            break
        else:
            #print("no match")
            # fetch end of last array to stick on start of new array
            end_of_last_rng = random_chars[-pWINSIZE + 1:]
            chars_genned += pCPC
        
        
# order is:
# - create shared flag
# - generate workers

collected_data = []
trackers = []

if __name__ == "__main__":
    try:
        print(f"Estimated probability is 1/{len(LIST_OF_CHARS) ** len(TARGET_CHARS):,} or 1/{convert_to_letter_suffix(len(LIST_OF_CHARS) ** len(TARGET_CHARS))}")
        mp_manager = mp.Manager()
        shared_flag = mp_manager.Event()
        worker_count = cpu_count()
        worker_pool = mp.Pool(worker_count)
        print(f"Creating workers...")
        for i in range(worker_count):
            process = worker_pool.apply_async(gen_and_test, (LIST_OF_CHARS, TARGET_CHARS, WINDOW_SIZE, CHARACTERS_PER_CYCLE, shared_flag))
            trackers.append(process)
            
        print("Workers created. Searching...")

        for tracker in trackers:
            collected_data.append(tracker.get())

        for item in collected_data:
            if item[0] == True:
                print(f"!! found true in {item} !!")
                break
    except KeyboardInterrupt as e:
        print("Ended by user manually")
