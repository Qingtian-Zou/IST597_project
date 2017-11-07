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
        entry=str.split(str='\t',line)
        if not i%5: #a new file comes every 5 lines
            files.append(entry[0])
            results.append([])
            scores.append([])
        results[i/5].append(entry[1])
        scores[i/5].append(entry[2])
        i+=1
    fi.close()

def showStatistic():
    # TODO: statistic results