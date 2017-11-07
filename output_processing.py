files=[]
results=[]
scores=[]

def loadFile(file):
    global files
    global results
    global scores

    fi=open(file,'r')
    i=0 # for counting number of lines
    for line in fi:
        entry=line.split('\t')
        if not i%5: #a new file comes every 5 lines
            files.append(entry[0])
            results.append([])
            scores.append([])
        results[int(i/5)].append(entry[1])
        scores[int(i/5)].append(entry[2])
        i+=1
    fi.close()

def confidenceProcessing():
    global files
    global results
    global scores
    # TODO: processing rules:
    #       1. If none of the scores of results for a file is greater than 0.6, then all results should present.
    #       2. If there is only one score of a result is greater than 0.6, and all other scores are significantly low (no greater than 0.2), then delete all other results.
    #       3. If there is only one score of a result is greater than 0.6, and not all other scores are significantly low (no greater than 0.2), then save all results whose scores are greater than 0.1.
    #       4. If multiple results are greater than 0.6, then save all results whose scores are greater than 0.4.

def showStatistic():
    global files
    global results
    global scores
    # TODO: statistic results
