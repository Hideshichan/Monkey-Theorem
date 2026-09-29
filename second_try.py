# monkeys numpy

import numpy as np

rng = np.random.default_rng()

TARGET_WORD = "banana"
TARGET_WORD = TARGET_WORD.upper()
TARGET_CHARS = np.array(list(TARGET_WORD), dtype=str)
WINDOW_SIZE = len(TARGET_WORD)
CHARACTERS_PER_CYCLE = 10000000
LIST_OF_CHARS = np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ ,.'"), dtype=str)

chars_genned = 0
end_of_last_rng = []


def gen_and_test(pCHARS, pTARGET, pWINSIZE, pCPC):
    while True:
        random_chars = rng.choice(pCHARS, pCPC)
        new_rng_arr = np.concatenate((end_of_last_rng, random_chars))
        window = np.lib.stride_tricks.sliding_window_view(random_chars, window_shape=pWINSIZE)

        # for the dice rolling i broke into 2 lists of first and seconds rolls and then compared as 1 value vs 1 value
        # so either compare each item in list of target vs each item in list of window or concatenate and compare 2 strings

        # need a way to check if an array inside the comparison is all true using np
        ufahgbagab = np.all((window == pTARGET), 1) # surely this is how to do it
        if np.any(ufahgbagab):
            print(f"yeah, found match at index {np.where(ufahgbagab)[0][0]:,} after {chars_genned + np.where(ufahgbagab)[0][0]:,} characters")
            print(f"{window[np.where(ufahgbagab)[0]]}")
            break
        else:
            #print("no match")
            end_of_last_rng = random_chars[-pWINSIZE + 1:]
            chars_genned += pCPC
            if chars_genned % 1000000000 == 0:
                print(f"reached {chars_genned // 1000000000}b chars genned")
        #print(ufahgbagab)