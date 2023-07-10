import matplotlib.pyplot as plt
plt.plot([1,2,3,4])
import numpy as np

my_list = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11 ,12], [13, 14, 15, 16]]
new_list = list()

for sub_list in my_list:
    for element in sub_list:
        new_list.append(element)
        
print(new_list)