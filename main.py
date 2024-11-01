from dive import Dive

dive_obj = Dive()

newdepth = 1.0
# for i in range(5):
#     newdepth += 0.5
#     dive_obj.segment(newdepth, f"{i+1}:0")
dive_obj.segment(2.5, f"{5}:0")

print(dive_obj.ceilings)

#dive_obj.segment(dive_obj._P, f"{20}:0")

#dive_obj.segment(2.0, f"{50}:0")