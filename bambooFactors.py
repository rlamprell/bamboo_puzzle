subtaskId = 3
growthRate = [1, 2, 3, 4, 12]

# Dont change anything above this line
# ===================================

# enter your username for EVERY file you submit
username = "sgrlampr"

# generate your solution as a list
from bambooSolutions import cutMaxHeight_disallowSequential

queue = cutMaxHeight_disallowSequential(growthRates=growthRate, iterations=20).run()

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
