# monkeys numpy

import numpy as np
import multiprocessing as mp
from os import cpu_count


# constants that will not change in the middle of the script
TARGET_WORD = "i chimp, therefore i am"
TARGET_WORD = TARGET_WORD.upper()
TARGET_CHARS = np.array(list(TARGET_WORD), dtype=str)
WINDOW_SIZE = len(TARGET_WORD)
CHARACTERS_PER_CYCLE = 10000000
LIST_OF_CHARS = np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ ,.'"), dtype=str)


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
            if chars_genned % 1000000000 == 0:
                print(f"reached {chars_genned // 1000000000}b chars genned without a match")
        #print(identical_check)
        
        
# order is:
# - create shared flag
# - generate workers

collected_data = []
trackers = []

if __name__ == "__main__":
    print(f"Estimated probability is 1/{len(LIST_OF_CHARS) ** len(TARGET_CHARS):,} or 1/{len(LIST_OF_CHARS ** len(TARGET_CHARS)):.2e}")
    mp_manager = mp.Manager()
    shared_flag = mp_manager.Event()
    worker_count = cpu_count()
    worker_pool = mp.Pool(worker_count)
    for i in range(worker_count):
        print(f"Creating worker {i + 1}")
        process = worker_pool.apply_async(gen_and_test, (LIST_OF_CHARS, TARGET_CHARS, WINDOW_SIZE, CHARACTERS_PER_CYCLE, shared_flag))
        trackers.append(process)

    for tracker in trackers:
        collected_data.append(tracker.get())

    for item in collected_data:
        if item[0] == True:
            print(f"!! found true in {item} !!")
            break

# check which ones tuple starts with True as that one found the target
