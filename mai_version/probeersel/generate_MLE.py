itemnbs = "13  1  9  1  1  8 12 11 15 12 15  5  4  7  9  5  2  9  2  9 10 15  9 13 12 16 12 11 15 16  7  1  3  8  7  5 12 14 16  3  2  6 14 13  2  7 15  4 12  5"
itemnbs = itemnbs.rsplit()
prologstr = ""

print(itemnbs)


#####################
def rainy_weather(count):
    return "weather(" + str(count) + ", rainy).\n"


def sunny_weather(count):
    return "weather(" + str(count) + ", sunny).\n"


def do_walk(count):
    return "walk(" + str(count) + ", no).\n"


def do_not_walk(count):
    return "walk(" + str(count) + ", yes).\n"


def hot_temperature(count):
    return "temperature(" + str(count) + ", hot).\n"


def cold_temperature(count):
    return "temperature(" + str(count) + ", cold).\n"


def mild_windy(count):
    return "windy(" + str(count) + ", mild).\n"


def storm_windy(count):
    return "windy(" + str(count) + ", storm).\n"


###############################
def walking(count, item, offset, divisor):
    if float(item) <= offset + divisor:
        return do_walk(count)
    else:
        return do_not_walk(count)


def windy(count, item, offset, divisor):
    if float(item) <= offset + divisor:
        return mild_windy(count) + walking(count, item, offset, divisor / 2)
    else:
        return storm_windy(count) + walking(count, item, offset + divisor, divisor / 2)


# -----------------
def weather(count, item, offset, divisor):
    if float(item) <= offset + divisor:
        return rainy_weather(count) + windy(count, item, offset, divisor / 2)
    else:
        return sunny_weather(count) + windy(count, item, offset + divisor, divisor / 2)


# -----------------------------
def temperature(count, item, offset, divisor):
    if float(item) <= offset + divisor:
        return hot_temperature(count) + weather(count, item, offset, divisor / 2)
    else:
        return cold_temperature(count) + weather(count, item, offset + divisor, divisor / 2)


###########################
for index, item in enumerate(itemnbs):
    # temperature
    id = index + 1
    prologstr = prologstr + temperature(id, item, 0, 16 / 2) + "\n"

    # if item == "1":
    #     prologstr = prologstr + rainy_weather(count) + do_walk(count) + "\n"
    # elif item == "2":
    #     prologstr = prologstr + rainy_weather(count) + do_not_walk(count) + "\n"
    # elif item == "3":
    #     prologstr = prologstr + sunny_weather(count) + do_walk(count) + "\n"
    # elif item ==  "4":
    #     prologstr = prologstr + sunny_weather(count) + do_not_walk(count) + "\n"
    # else :
    #     raise Exception("something went wrong")

print(prologstr)
