"""
1. Get the largest size stamp value
2. Remove the stamp value from the aim price until the aim price is 0 or < 0
3. If the modulus of the aim price minus the stamp value is less than the smallest value of stamp, remove the stamp value from the aim price and break
4. Otherwise change the stamp being used to the next largest stamp value and continue j8h
"""

def stamps(aim_price, list_of_available_stamps):
    largest_stamp = max(list_of_available_stamps)
    used = []

    while aim_price > 0:
        if aim_price - largest_stamp < 0:
            if abs(aim_price - largest_stamp) < min(list_of_available_stamps):
                used.append(largest_stamp)
                break
            list_of_available_stamps.remove(largest_stamp)
            try:
                largest_stamp = max(list_of_available_stamps)
            except ValueError:
                used.append(largest_stamp)
                break
            continue
        used.append(largest_stamp)
        aim_price -= largest_stamp

    return used

if __name__ == "__main__":
    """ Tests """
    # print(stamps(895, [10, 20, 215]))
    # print(stamps(50, [50]))
    # print(stamps(50, [100]))
    # print(stamps(50, [13]))

    print(stamps(380, [200,190,100,50,20,10]))
