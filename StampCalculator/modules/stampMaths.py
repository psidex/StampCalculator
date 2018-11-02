"""
Decreasing first-fit algorithm:
    1. Get the largest size stamp value
    2. Remove the stamp value from the aim price until the aim price is 0 or < 0
    3. If the modulus of the aim price minus the stamp value is less than the
       smallest value of stamp, remove the stamp value from the aim price and
       break
    4. Otherwise change the stamp being used to the next largest stamp value and
       continue
"""

def calcStampAmount(aim_price, list_of_available_stamps):
    """
    Work out in multiple different ways and choose the one with the least stamps
    """
    largest_stamp = max(list_of_available_stamps)
    mod_used = []
    first_fit_used = []

    """See if any stamps fit into aim_price"""
    for stamp in list_of_available_stamps:
        if aim_price % stamp == 0:
            mod_used.append([stamp for x in range(int(aim_price/stamp))])

    """Decreasing first-fit algorithm"""
    while aim_price > 0:
        if aim_price - largest_stamp < 0:
            if abs(aim_price - largest_stamp) < min(list_of_available_stamps):
                first_fit_used.append(largest_stamp)
                break
            list_of_available_stamps.remove(largest_stamp)
            try:
                largest_stamp = max(list_of_available_stamps)
            except ValueError:
                first_fit_used.append(largest_stamp)
                break
            continue
        first_fit_used.append(largest_stamp)
        aim_price -= largest_stamp

    # use mod_used as a master list of lists
    mod_used.append(first_fit_used)

    # find list that contains lowest about of stamps
    shortest = mod_used[0]
    for l in mod_used:
        if len(shortest) > len(l):
            shortest = l

    return shortest

if __name__ == "__main__":
    """ Tests """
    c = calcStampAmount
    assert(c(380, [200,190,100,50,20,10]) == [190, 190])
    assert(c(40, [10, 20, 215]) == [20, 20])
    assert(c(50, [50]) == [50])
    assert(c(50, [100]) == [100])
    assert(c(50, [13]) == [13, 13, 13, 13])
