from re import search


def national_id_validator(input):
    if not search(r'^\d{10}$', input):
        return False

    check = int(input[9])
    s = sum([int(input[x]) * (10 - x) for x in range(9)]) % 11
    return (2 > s == check) or (s >= 2 and check + s == 11)

