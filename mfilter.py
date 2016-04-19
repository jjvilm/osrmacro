#takes out repeated coords to shorten the file
with open('mstats', 'r') as f:
    with open('filteredCoords', 'w') as filteredCoords:
        for line in f:
            for nextLine in f:
                if line != nextLine:
                    filteredCoords.write(nextLine)

