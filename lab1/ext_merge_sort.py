import time


def parseAndSortFile(inputFile, outputFile):
    intList = []
    with open(inputFile) as r:
        for line in r:
            intList.append(int(line.strip('\n')))
    intList.sort()
    tempString = ''
    for num in intList:
        tempString = tempString + str(num) + '\n'
    with open(outputFile, 'w+') as w:
        w.write(tempString[:len(tempString)])


def removeSingleNum(inputFile):
    # remove first line from file and write it back to the same file.
    intList = []
    with open(inputFile) as r:
        for line in r:
            if line.strip('\n') is None:
                return -1
            intList.append(int(line.strip('\n')))
    tempString = ''
    for num in range(1, len(intList)):
        tempString = tempString + str(intList[num]) + '\n'
    with open(inputFile, 'w+') as w:
        w.write(tempString[:len(tempString)])
    if len(intList) == 0:
        return 10000
    else:
        return intList[0]


def sort():
    # Load buffer
    buffer = []
    for i in range(1, 11):
        inFile = 'input\\unsorted_' + str(i) + '.txt'
        outFile = 'output\\sorted_' + str(i) + '.txt'
        parseAndSortFile(inFile, outFile)
        buffer.append(removeSingleNum(outFile))

    # find min and put in txt file
    mergedOutput = 'output\\sorted_merged.txt'
    emptyPage = 0
    outputBuffer = []
    while emptyPage != 10:
        i = buffer.index(min(buffer))
        # emptyPage = emptyPage+1
        # move the lowest into buffer
        outputBuffer.append(buffer[i])
        valueFromFile = removeSingleNum('output\\sorted_' + str(i + 1) + '.txt')
        if valueFromFile == 10000:
            emptyPage = emptyPage + 1
            buffer[i] = valueFromFile
            continue
        else:
            buffer[i] = valueFromFile
        if len(outputBuffer) == 100 or len(outputBuffer) > 0:
            tempString = ''
            for num in outputBuffer:
                tempString = tempString + str(num) + '\n'
            with open(mergedOutput, 'a') as a:
                a.write(tempString)
            outputBuffer = []
    if len(outputBuffer) > 0:
        tempString = ''
        for num in outputBuffer:
            tempString = tempString + str(num) + '\n'
        with open(mergedOutput, 'a') as a:
            a.write(tempString)
    return


start = time.time()
sort()
print('Execution Time: ', time.time() - start)
