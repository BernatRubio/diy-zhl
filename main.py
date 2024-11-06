from dive import Dive
import copy

dive_obj = Dive()
tmp_obj = Dive()

bar = 5.0

dive_obj.segment(bar, f"{5}:0")
i = 0
k = False
tmp_obj = copy.deepcopy(dive_obj)
while True:
    i+=1
    tmp_obj.segment(bar, f"{5+i}:0")
    for ceiling in tmp_obj.ceilings:
        if ceiling > 1:
            break
    else:
        continue
    break
print(i)
print(dive_obj.ndl(0)) # Aquest calcula el ndl en intervals de 15 segons.

# dive_obj.segment(5.0, f"{15}:0")
# dive_obj.segment(2.0, f"{20}:0")
#print(dive_obj.ceilings)