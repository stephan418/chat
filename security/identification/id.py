import time
import random
from security.encode.number_encode import b64encode

# Initialize some counter and variables
msg_number = 0
msg_time = time.time() * 1000


# This function creates a (unless used too frequently) unique timestamp
def create_unique_ts_number():
    """
    Creates a uniq    :return: timestamp
ue timestamp
    """
    global msg_number
    global msg_time
    t = time.time() * 1000

    if t - msg_time > 10:
        msg_time = t
        msg_number = 0

    msg_number += 1
    return msg_number


# Create a unique id consisting of a timestamp, a number timestamp revision number and a random number
def create_unique_id() -> int:
    """
    Creates a unique ID to be used in databases
    :return: Integer ID
    """
    return int(str(int(time.time() * 1000)) + str(create_unique_ts_number()) +
               str(random.randint(1111111111111, 9999999999999)))
