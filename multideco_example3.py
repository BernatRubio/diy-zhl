from dive import Dive

dive_obj = Dive()
dive_obj.segment(3.0, f"{1}:{30}")
dive_obj.segment(3.0, f"{15}:0")
print(dive_obj.safety_stop())
dive_obj.segment(1.2, f"{17}:{15}")
print(dive_obj.safety_stop())
dive_obj.segment(0.9, f"{17}:{45}")
print(dive_obj.safety_stop())
dive_obj.segment(0.9, f"{18}:{30}")
print(dive_obj.safety_stop())
dive_obj.segment(0.6, f"{19}:{0}")
print(dive_obj.safety_stop())
dive_obj.segment(0.6, f"{19}:{30}")
print(dive_obj.safety_stop())
dive_obj.segment(0.3, f"{22}:{0}")
print(dive_obj.safety_stop())
dive_obj.segment(0.3, f"{22}:{30}")
print(dive_obj.safety_stop())
dive_obj.segment(0.0, f"{23}:0")