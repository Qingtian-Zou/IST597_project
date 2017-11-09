import sys
import os
import argparse
import collections
import itertools
from shutil import copyfile

FLAGS=None

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
        scores[int(i/5)].append(float(entry[2]))
        i+=1
    fi.close()
    confidenceProcessing()

def confidenceProcessing():
    global files
    global results
    global scores
    # processing rules:
    #   1. If none of the scores of results for a file is greater than 0.6, then all results should present.
    #   2. If there is only one score of a result is greater than 0.6, and all other scores are significantly low (no greater than 0.2), then delete all other results.
    #   3. If there is only one score of a result is greater than 0.6, and not all other scores are significantly low (no greater than 0.2), then save all results whose scores are greater than 0.1.
    #   4. If multiple results are greater than 0.6, then save all results whose scores are greater than 0.4.
    # Just a reminder: the scores are already sorted from high to low when written into file.
    for i in range(len(files)):
        #  case 1
        if scores[i][0]<0.6:
            continue
        # case 2
        elif scores[i][1]<0.2:
            del results[i][1]
            del results[i][1] # Attention: index change on del!
            del results[i][1]
            del results[i][1]
            del scores[i][1]
            del scores[i][1]
            del scores[i][1]
            del scores[i][1]
            continue
        # case 3
        elif scores[i][1]<=0.6:
            for j in range(2,5):
                if scores[i][j]<0.1:
                    for _ in range(5-j):
                        del results[i][j]
                        del scores[i][j]
            continue
        # case 4
        else:
            for j in range(1,5):
                if scores[i][j]<=0.4:
                    for _ in range(5-j):
                        del results[i][j]
                        del scores[i][j]
            continue
    showStatistic()

def showStatistic():
    global files
    global results
    global scores
    counter = collections.Counter(itertools.chain.from_iterable(results))
    print(counter.most_common())

def copy2labels(source_folder, dest_folder):
    global files
    global results
    global scores
    if not os.path.exists(source_folder)&os.path.isdir(source_folder):
        print("Image folder does not exist!")
        sys.exit(1)
    try:
        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)
        counter = collections.Counter(itertools.chain.from_iterable(results))
        for folder in counter.keys():
            os.mkdir(os.path.join(dest_folder,folder))
        for i in range(len(files)):
            for re in results[i]:
                copyfile(os.path.join(source_folder,files[i]),os.path.join(dest_folder,re,files[i]))
    except IOError as identifier:
        print('Failed!')
        print(identifier)
    else:
        print('Processing succeeded!')

def main():
    loadFile(FLAGS.output_file)
    copy2labels(FLAGS.source_folder,FLAGS.dest_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output_file',
        type=str,
        default=os.path.join(os.getcwd(),'output.txt'),
        help='Absolute path to the output file.'
    )
    parser.add_argument(
        '--image_folder',
        type=str,
        default='',
        help='Absolute path to the image file folder.'
    )
    parser.add_argument(
        '--dest_folder',
        type=str,
        default=os.path.join(os.getcwd(),'Categorized pictures'),
        help='Absolute path to the destination folder'
    )
    FLAGS, unparsed = parser.parse_known_args()
    main()