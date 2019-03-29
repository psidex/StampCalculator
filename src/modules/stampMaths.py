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


def calcStampAmount(aimPrice, listOfAvailableStamps):
    """
    Work out in multiple different ways and choose the one with the least stamps
    """
    # possibleStampLists is a master list of lists
    possibleStampLists = []

    # See if any stamps fit exactly into aimPrice
    for stamp in listOfAvailableStamps:
        if aimPrice % stamp == 0:
            possibleStampLists.append([stamp for x in range(int(aimPrice / stamp))])

    # Decreasing first-fit algorithm
    largestStamp = max(listOfAvailableStamps)
    firstFitUsed = []
    while aimPrice > 0:
        if aimPrice - largestStamp < 0:
            if abs(aimPrice - largestStamp) < min(listOfAvailableStamps):
                firstFitUsed.append(largestStamp)
                break
            listOfAvailableStamps.remove(largestStamp)
            try:
                largestStamp = max(listOfAvailableStamps)
            except ValueError:
                firstFitUsed.append(largestStamp)
                break
            continue
        firstFitUsed.append(largestStamp)
        aimPrice -= largestStamp

    possibleStampLists.append(firstFitUsed)

    # find list that contains lowest about of stamps
    shortest = possibleStampLists[0]
    for l in possibleStampLists:
        if len(shortest) > len(l):
            shortest = l

    return shortest


if __name__ == "__main__":
    """
    Run some tests
    """
    c = calcStampAmount
    assert c(380, [200, 190, 100, 50, 20, 10]) == [190, 190]
    assert c(40, [10, 20, 215]) == [20, 20]
    assert c(50, [50]) == [50]
    assert c(50, [100]) == [100]
    assert c(50, [13]) == [13, 13, 13, 13]
