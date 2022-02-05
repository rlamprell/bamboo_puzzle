subtaskId = 4
growthRate = [1, 1, 2, 3, 5, 8, 13, 21]

# Dont change anything above this line
# ===================================

# enter your username for EVERY file you submit
username = "sgrlampr"

# generate your solution as a list
from bambooSolutions import cutMaxHeight_minMaxGrowth   

queue = cutMaxHeight_minMaxGrowth(growthRates=growthRate, iterations=105).run()

print("queue:", queue)

# ====================================
# Dont change anything below this line

from collections import deque

solution = deque()
# add each element to the solution
for i in queue:
    solution.append(i)

import bamboo

# records your solution
bamboo.calculateRatio(growthRate, solution, username, subtaskId)
