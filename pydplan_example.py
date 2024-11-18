from dive import Dive

dive_obj = Dive()

dive_obj.segment(4.97, f"{2}:{30}")
dive_obj.segment(4.97, f"{22}:{30}")
print(dive_obj.safety_stop())