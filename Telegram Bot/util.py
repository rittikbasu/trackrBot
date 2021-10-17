def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        return False

    return True