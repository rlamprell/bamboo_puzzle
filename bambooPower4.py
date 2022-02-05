subtaskId = 2
growthRate = [3, 12, 48, 192, 768, 3072]

# Dont change anything above this line
# ===================================

# enter your username for EVERY file you submit
username = "sgrlampr"

# generate your solution as a list
from bambooSolutions import cutFrequency_power

queue = cutFrequency_power(growthRates=growthRate, iterations=32, p=2, removeSlack=True).run()

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
