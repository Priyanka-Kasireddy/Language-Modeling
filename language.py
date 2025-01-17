"""
Language Modeling Project
Name:
Roll No:
"""

from os import X_OK
import language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    f = open(filename)
    x = []
    y = f.read().splitlines()
    for i in y:
        if len(i)>0:
            x.append(i.split( ))
    return x


'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):
    count = 0
    for i in corpus:
        for j in i:
            count+= 1
    return count


'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):
    x= []
    for i in corpus:
        for j in i:
            if j not in x:
                x.append(j)
    return  x


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    x={ }
    for i in corpus:
        for j in i:
            if j not in x:
                x[j] = 1
            else:
                x[j]+= 1
    return  x


'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus):
    x=[]
    for i in corpus:
        if i[0] not in x:
            x.append(i[0])
    return  x


'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    x={}
    for i in corpus:
        if i[0] not in x:
            x[i[0]] =1
        else:
            x[i[0]]+=1
    return x


'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    x={}
    for s in corpus:
        for j in range(len(s)-1):
            if s[j] not in x:
                x[s[j]] = {}
            if s[j+1] in x[s[j]]:
                x[s[j]][s[j+1]] += 1
            else:
                x[s[j]][s[j+1]] = 1
    return x


### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    x=[]
    for i in unigrams:
        prob=1/len(unigrams)
        x.append(prob)
    return x


'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    x=[]
    for word in unigrams:
        count=unigramCounts[word]
        y=(count/totalCount)
        x.append(y)
    return x


'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):
    x={}
    for prevWord in bigramCounts:
        word=[]
        prob=[]
        for key,values in bigramCounts[prevWord].items():
            word.append(key)
            prob.append(values/unigramCounts[prevWord])
            y={}
            y["words"]=word
            y["probs"]=prob
        x[prevWord]=y
    return x


'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
def getTopWords(count, words, probs, ignoreList):
    wProb = {}
    Top = {}
    for i in range(len(words)):
        if words[i] not in ignoreList:
           wProb[words[i]] = probs[i]
    sorted_list = sorted(wProb, key=wProb.get, reverse=True)
    for sort_words in sorted_list:
        if len(Top)<count:
           Top[sort_words]= wProb[sort_words]
    return Top


'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
import random
def generateTextFromUnigrams(count, words, probs):
    s=""
    for i in range(0,count):
        randomList = random.choices(words,weights=probs)
        s= s + randomList[0]+" "
    return s


'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    sent=""
    z= random.choices(startWords,weights=startWordProbs)[0]
    sent +=z
    for i in range(count-1):
        if (z!="."):
                x=bigramProbs[z]['words']
                y=bigramProbs[z]['probs']
                z = random.choices(x,weights=y)[0]  
                sent+=" " +z
        else:
            z= random.choices(startWords,weights=startWordProbs)[0]
            sent += " " +z
    return sent


### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTop50Words(corpus):
    words = buildVocabulary(corpus)
    count = getCorpusLength(corpus)
    uni_count = countUnigrams(corpus)
    uni_probs = buildUnigramProbs(words, uni_count, totalCount=count)
    top_words = getTopWords(50,words,uni_probs,ignore)
    plot = barPlot(top_words, "Top 50 Words")
    return plot


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):
    startWords=getStartWords(corpus)
    startWordCounts=countStartWords(corpus)
    startWordProbs=buildUnigramProbs(startWords,startWordCounts,len(corpus))
    count=getTopWords(50,startWords,startWordProbs,ignore)
    plot=barPlot(count,"Top state words")
    return plot


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):
    unigCounts=countUnigrams(corpus)
    bigCounts=countBigrams(corpus)
    bigProbs=buildBigramProbs(unigCounts,bigCounts)
    count=getTopWords(10,bigProbs[word]["words"],bigProbs[word]["probs"],ignore)
    plot=barPlot(count,"Top NextWords")
    return plot


'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount):
    dic={}
    countp1=[]
    countp2=[]
    ugram1=buildVocabulary(corpus1)
    ucount1=countUnigrams(corpus1)
    len1=getCorpusLength(corpus1)
    prob1=buildUnigramProbs(ugram1,ucount1,len1)
    top1=getTopWords(topWordCount,ugram1,prob1,ignore)
    ugram2=buildVocabulary(corpus2)
    ucount2=countUnigrams(corpus2)
    len2=getCorpusLength(corpus2)
    prob2=buildUnigramProbs(ugram2,ucount2,len2)
    top2=getTopWords(topWordCount,ugram2,prob2,ignore)
    lst=list(top1.keys())+list(top2.keys())
    twords=list(dict.fromkeys(lst))
    for i in range(len(twords)):
        if twords[i] in ugram1:
            y=ugram1.index(twords[i])
            countp1.append(prob1[y])
        else:
            countp1.append(0)
        if twords[i] in ugram2:
            y=ugram2.index(twords[i])
            countp2.append(prob2[y])
    dic["topWords"]=twords
    dic["corpus1Probs"]=countp1
    dic["corpus2Probs"]=countp2
    return dic


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    dic=setupChartData(corpus1,corpus2,numWords)
    sideBySideBarPlots(dic["topWords"],dic["corpus1Probs"],dic["corpus2Probs"],name1,name2,title)
    return


'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    dic=setupChartData(corpus1,corpus2,numWords)
    scatterPlot(dic["corpus1Probs"],dic["corpus2Probs"],dic["topWords"],title)
    return


### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()
    # test.testLoadBook()
    # test.testGetCorpusLength()
    # test.testBuildVocabulary()
    # test.testCountUnigrams()
    # test.testGetStartWords()
    # test.testCountStartWords()
    # test.testCountBigrams()
    # test.testBuildUniformProbs()
    # test.testBuildUnigramProbs()
    # test.testBuildBigramProbs()
    # test.testGetTopWords()
    # test.testGenerateTextFromUnigrams()
    # test.testGenerateTextFromBigrams()   
    ## Uncomment these for Week 2 ##
# """
#     print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
#     test.week2Tests()
    # print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek2()
# """

    ## Uncomment these for Week 3 ##
# """
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
# """