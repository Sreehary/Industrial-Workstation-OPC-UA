import random
from datetime import datetime

bool_val = ["True", "False"]
turn_table_pos = [1, 2, 3, 4, 5, 6]
data_list = []
hb = 0


async def get_sim_values():
    global hb
    hb += 1
    hb = 0 if hb > 10 else hb
    # drill
    drill_home_pos = random.choice(bool_val)
    if drill_home_pos == "False":
        drilling = "True"
    else:
        drilling = "False"
    data_list.append(("W1:D1:M1", drill_home_pos))
    data_list.append(("W1:D1:M2", drilling))
    data_list.append(("W1:D1:M3", drilling))
    data_list.append(("W1:D1:M4", hb))

    # turn table
    if drill_home_pos and not drilling:
        checker_pos = "True"
    else:
        checker_pos = "False"

    data_list.append(("W1:D2:M5", drill_home_pos))
    data_list.append(("W1:D2:M6", drilling))
    data_list.append(("W1:D2:M7", checker_pos))
    data_list.append(("W1:D2:M8", random.choice(turn_table_pos)))
    data_list.append(("W1:D2:M9", hb))

    # checker
    if checker_pos:
        checker_home_pos = "True"
    else:
        checker_home_pos = "False"
    data_list.append(("W1:D3:M10", checker_home_pos))
    data_list.append(("W1:D3:M11", str(datetime.now())))
    data_list.append(("W1:D3:M12", random.choice(bool_val)))
    data_list.append(("W1:D3:M13", hb))

    # ejector A
    data_list.append(("W1:D4:M14", random.choice(bool_val)))
    data_list.append(("W1:D4:M15", hb))

    # ejector B
    data_list.append(("W1:D5:M16", random.choice(bool_val)))
    data_list.append(("W1:D5:M17", hb))

    return data_list
