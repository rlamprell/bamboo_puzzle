# Solutions to the first programming assignment of COMP526
# Contains several algorithms, some with addtional adjustable parameters.
# Each one:
#   -- inherits on the parent class __MyAlgorithms 
#   -- uses the function run() to produce a specified queue length (iterations)
#
# The if __name__ == '__main__' can be used to test the plots against each of the 
# the algorithms quickly.  It will provide you with the best max-height attained 
# in the selected number of iterations alongside what the earliest queue length 
# this results was obtained. 
# 
# Additionally it will calculate as to whether or not the provided queue is 
# cycyled by the algorithm - This is not extensive and only checks for double
# the length of the queue.


#   Rob Lamprell 
#   username = sgrlampr
#   Last modified: 2021/04/22

import numpy as np



# This is the parent class for the assignment algorithms developed
# -- private to file so as it contains no algorithms
class __MyAlgorithms():
    def __init__(self, growthRates, iterations):

        # the growth rate of each tree
        self.growthRates = growthRates
        self.treeCount   = len(growthRates)

        self.sumGrowthRates = 0
        # all the growth rates added together
        for i in range(len(growthRates)):
            self.sumGrowthRates += self.growthRates[i]

        # record the heights of all the trees (h_0 = 0)
        self.heights     = np.zeros(self.treeCount)

        # order to output
        self.iterations  = iterations
        self.queue       = []


    # count the number of occurances of the max value in the list
    # -- return the indexes
    # -- (I think np.argmax actually does this)
    def count_max(self, thisList, max_):

        count   = 0
        indexes = []
        
        for item in range(len(thisList)-1):
            if (thisList[item] == thisList[item+1]) and (thisList[item] == self.heights[max_]):
                count+=1

                # if the last value of the list is == to the new LHS pair
                # -- don't add
                if len(indexes)>1: #or indexes[len(indexes)-1] != item:
                    if indexes[len(indexes)-1] != item:
                        indexes.append(item)
                        
                else:
                    indexes.append(item)

                # always add the second item as this is the first time checking it
                indexes.append(item+1)

        return indexes


    # return the queue -- list of indexes
    def getQueue(self):

        return self.queue




# cut the largest tree height at time (t)
class cutMaxHeight(__MyAlgorithms):
    def run(self):
        
        for i in range(self.iterations):

            # for every iteration add today's growth to the tree height
            for bamboos in range(self.treeCount):
                
                self.heights[bamboos] += self.growthRates[bamboos]

            # get the cut
            toCut = np.argmax(self.heights)

            self.queue.append(toCut)
            self.heights[toCut] = 0

        return self.queue




# cut the largest tree (but don't allow sequential cuts on the same tree)
# -- example: if you cut index 0 on turn 1, you cannot cut index 0 on turn 2
class cutMaxHeight_disallowSequential(__MyAlgorithms):
    def run(self):
        
        # record the previous cut
        previous_cut = -1

        for i in range(self.iterations):

            # for every iteration add today's growth to the tree height
            for bamboos in range(self.treeCount):

                self.heights[bamboos] += self.growthRates[bamboos]

            # if the tallest tree current has the same index as the previous tallest tree, then cut the next tallest
            if previous_cut == np.argmax(self.heights):
                
                height_copy = np.copy(self.heights)
                height_copy.sort()

                maxhigh = np.argmax(height_copy)

                value   = height_copy[maxhigh-1]

                toCut   = np.where(self.heights == value)     
                toCut   = toCut[0][0]

            # cut the tallest tree
            else:
                # get the cut and add to the queue
                toCut = np.argmax(self.heights)

            self.queue.append(toCut)

            # cut the tree in the heights container
            self.heights[toCut] = 0

            # record which index we've just cut
            previous_cut = toCut

        return self.queue




# cut largest tree with largest/smallest growth rate
# -- cutMinGrowthRate=False will take the max (default)
# -- cutMinGrowthRate=True  will take the min
class cutMaxHeight_minMaxGrowth(__MyAlgorithms):

    def __init__(self, growthRates, iterations, cutMinGrowthRate=False):
        super().__init__(growthRates, iterations)

        self.cutMinGrowthRate = cutMinGrowthRate


    def run(self):
        
        # for each iteration
        for i in range(self.iterations):

            # for every bamboo add today's growth to the tree height
            for bamboos in range(self.treeCount):

                self.heights[bamboos] += self.growthRates[bamboos]
            
            # get the indexes for each tree at the max height
            indexes = self.count_max(self.heights, np.argmax(self.heights))
            count = len(indexes)

            # if there is only one tree at the max height - cut it
            if count < 1:
                toCut = np.argmax(self.heights)

            # if there is more than one tree at the max height
            else:
                
                maxheight_growths = np.empty((0, 2), int)
                
                # for each index
                for index in indexes:    
                    # record indexes and growth rates for the trees with the max value
                    maxheight_growths = np.append(maxheight_growths, np.array([[self.growthRates[index], index]]), axis=0)
                
                # are we cutting based on the max or min growth rate?
                if self.cutMinGrowthRate:
                    # choose the lowerst growthrate
                    value_ = np.argmin(maxheight_growths[:, 0])
                else:
                    # choose the highest growthrate
                    value_ = np.argmax(maxheight_growths[:, 0])
                    
                toCut = maxheight_growths[value_, 1]

            # add the tree index to the queue
            self.queue.append(toCut)
            self.heights[toCut] = 0

        return self.queue




# calculate a cut frequency for each tree
# -- cut the largest growth rate if no tree is ready to be cut
class cutFrequency(__MyAlgorithms):

    def run(self):
    
        # frequencies of cuts 
        # -- sum of all growth rates divided by this tree's growth rate
        #freqs = np.empty((0, 1), float)
        freqs = []
        for i in range(len(self.growthRates)):

            # record the frequency the tree should be cut at along with the count of turns since last cut
            freq = self.sumGrowthRates/self.growthRates[i]
            freqs.append(freq)

        # counters for each growth rate
        cutCounter = np.zeros(len(self.growthRates))


        # use the frequencies to establish the ordering
        for i in range(self.iterations):
            
            # add one to the counter for all trees
            cutCounter = cutCounter + 1

            # bool and container to establish cuts
            cut          = False
            cutCandidate = []

            # are any due to be cut?
            # -- if any of the counters are above or at the cut freq then 
            #    add to the cut candidate list
            for j in range(len(freqs)):

                if cutCounter[j] >= freqs[j]:
                    cut = True
                    cutCandidate.append(j)

            # if none are due to be cut, pick the highest tree
            if cut:
                # is there more than one tree above the threshold?
                if len(cutCandidate) > 1:

                    # get the actual growthrates
                    cutCandidateValues = []
                    for cutCand in cutCandidate:
                        cutCandidateValues.append(self.growthRates[cutCand]*(cutCounter[cutCand]+1))
                    
                    # cut the max growth rate of all of them
                    toCut = cutCandidate[np.argmax(cutCandidateValues)]     

                else:
                    # cut the only one in the list
                    toCut = cutCandidate[0]

            else:
                # cut highest growth rate
                toCut = np.argmax(self.growthRates)

            # reset the cut counter, for the tree we cut, to zero
            cutCounter[toCut] = 0
            
            # add the cut to the queue
            self.queue.append(toCut)

        return self.queue




# slack means that fequencies will always add up to 1
# -- it will adjust the final entry to 1-sum(all other fequencies)
class cutFrequency_power(__MyAlgorithms):

    def __init__(self, growthRates, iterations, p=2, removeSlack=True):
        super().__init__(growthRates, iterations)

        self.p              = p
        self.removeSlack    = removeSlack


    def run(self):

        # i need to order them first and save the index mapping
        treeMapping = np.copy(self.growthRates)

        # create a list of indexes and growth rates
        # -- this is used to lookup what the original bamboo positions were pre-sorting
        k = np.empty((0, 2), int)
        for i in range(len(self.growthRates)):
            
            item = np.array([i, self.growthRates[i]])
            k = np.vstack([k, item])

        # sort in descending order
        z = k[np.argsort(k[:, 1])]
        z = np.flip(z)

        # create containers to store the cut frequencies
        frequencies = []
        ps          = []

        # use the p^(n+1) formula and then divide 1/p to get the cut frequencies
        for i in range(len(self.growthRates)):
            
            # remove slack will ensure the frequencies add up to 1
            # -- in the case of p=2 it will make the last two plots have the same frequency
            if self.removeSlack:
                if i!=len(self.growthRates)-1:
                    pow_ = self.p**-(i+1)
        
                else:
                    pow_ = 1-sum(ps)
            else:
                pow_     = self.p**-(i+1)

            frequency = 1/pow_ 

            ps.append(pow_)
            frequencies.append(frequency)


        # containers for the cycle and counter (when it was last cut)
        cutCycle    = []
        cutCounter  = np.zeros(len(frequencies), int)

        # cut in order of highest frequency
        for i in range(self.iterations):
            
            # select a tree out of range
            toCut       = -1
            cutCounter  = cutCounter + 1

            # check, in-order, if a tree is due to be cut
            for tree in range(len(frequencies)):

                if cutCounter[tree] >= frequencies[tree]:
                    toCut = tree
                    break

            # if no tree is over due, cut the highest freq
            # that has not just been cut
            if toCut==-1:

                # traverse in-order and return first which 
                # has not entered the cycle
                notYetPicked = len(frequencies) - (len(frequencies)-len(cutCycle))

                # if this value is actually a tree (within the plot range)
                # then cut
                if (notYetPicked<len(frequencies)):
                    toCut = notYetPicked
                # else choose the largest
                else:
                    toCut = np.argmax(frequencies)
 

            # check if this tree has been cut already
            exists = False
            for cuts in range(len(cutCycle)):
                if cutCycle[cuts]==toCut:
                    exists = True
            
            # if not, add it to the list
            if exists==False:
                cutCycle.append(toCut)

            cutCycle                = list(set(cutCycle))
            cutCounter[int(toCut)]  = 0
            toCut                   = z[toCut][1]

            # append to the queue
            self.queue.append(toCut)

        return self.queue




# a completely Naive solution - just cut each tree once in the cycle
class cutEachTreeOnce(__MyAlgorithms):

    def run(self):
        
        # ordering doesn't matter as the largest value will always be sizeOfThePlot*max(growthRate)
        for i in range(len(self.growthRates)):

            self.queue.append(i)

        return self.queue




# This is a copy of calculateRatio from bamboo.py
# -- it was used to test the effectiveness of the algorithms
# -- it needed to be a copy as i wanted to return the maxheight rather than print it
from collections import deque
def __calculateRatio(growthRate, solution: deque, username: str, position: int, NUMBER_OF_ITERATIONS=10000):
    n                   = len(growthRate)
    maxHeight           = 0
    count               = n * [1]
    sumOfGrowthRates    = sum(growthRate)

    for i in range(0, NUMBER_OF_ITERATIONS):
        toCut = solution.popleft()
        for j in range(0, n):
            maxHeight = max(maxHeight, count[j] * growthRate[j])
        for j in range(0, n):
            if j == toCut:
                count[j] = 1
            else:
                count[j] += 1
        solution.append(toCut)

    return maxHeight




# used to evalute if there is a cycle (of a certain length) within the code
def checkIsCycle(queue, cycleLen):

    # create a container
    cycle = []
    
    # create the queue we think may be a cycle
    for i in range(cycleLen):
        cycle.append(queue[i])

    # loop through each value, offset by the cycle value
    # -- if any do not match, return False
    isCycle = True
    for i in range(len(queue)):

        if queue[i]!=cycle[i%len(cycle)]:
            isCycle = False
            break

    return isCycle




# testing method to help find cycles which can solve
def __minHeight_queueFinder(growthRate, algorithm, maxHeight_lowerBound=10, test_iterations=10000):

    results = []
    for j in range(1, 2000):

        queue = algorithm(growthRate, j).run()

        solution = deque()
        # add each element to the solution
        for i in queue:
            solution.append(i)

        # record the solution
        maxheight = __calculateRatio(growthRate, solution, username, subtaskId, test_iterations)
        results.append(maxheight)

        # inform user that the process has started
        if j==1:
            print("Calculating...")

        # update the user as to how many iterations have been performed
        if j%100 == 0:
            print()
            print("up to iteration:", j)
        
        # if searching for a specific low value the algorithm will stop early if a solution is found
        if maxheight <= maxHeight_lowerBound:
            print()
            print("=======================================")
            print("Results for input -",  growthRate)
            print("---------------------------------------")
            print("jth term:", j)
            print("Acheived a maxheight of:", maxheight)
            print("---------------------------------------")
            break
    
    # print results of search 
    # -- +1 to account for the out by one by not checking 0 range
    queue_length = np.argmin(results)+1
    print("=======================================")
    print("Max-height obtained:", results[np.argmin(results)])
    print("Acheived at queue length:", queue_length)
    print("---------------------------------------")

    # does the alogorithm cycle this queue?
    # -- queue2 runs the algorithm and produces a queue twice the size of the original
    # -- it then compares that to the original queue
    # -- if they match it returns True
    # -- else it returns False
    queue2 = algorithm(growthRate, queue_length*2).run()
    print("The algorithm cycles this queue: ", checkIsCycle(queue2, queue_length))
    print("=======================================")
    



# container for the bamboo plots
# -- makes it easier to test each plot in the __main__
class __BambooPlots:
    def inequality(self):
        return [2000, 1, 1]

    def powers4(self):
        return [3, 12, 48, 192, 768, 3072]

    def factors(self):
        return [1, 2, 3, 4, 12]

    def fibonacci(self):
        return [1, 1, 2, 3, 5, 8, 13, 21]

    def precision(self):
        return [1000, 1999, 2001]


        

# below is an example of what was used in order to obtain the results in table-1 of the submitted report
# -- individual files contain 
if __name__ == '__main__':
    
    username    = 'sgrlampr'
    subtaskId   = -1

    # change this to switch plots
    growthRate  = __BambooPlots().factors()

    # change this to alter the algorithm
    __minHeight_queueFinder(growthRate, cutMaxHeight_disallowSequential)