from dive import Dive

dive_obj = Dive()
dive_obj.segment(5.0, f"{2}:{30}")
dive_obj.segment(5.0, f"{25}:0")
dive_obj.segment(2.4, f"{28}:{15}")
print(dive_obj.safety_stop())
dive_obj.segment(2.4, f"{29}:0")
dive_obj.segment(2.1, f"{29}:{30}")
dive_obj.segment(2.1, f"{30}:0")
print(dive_obj.safety_stop())
dive_obj.segment(1.8, f"{30}:{30}")
print(dive_obj.safety_stop())
dive_obj.segment(1.8, f"{35}:0")
print(dive_obj.safety_stop())
dive_obj.segment(1.5, f"{35}:{30}")
print(dive_obj.safety_stop())
dive_obj.segment(1.5, f"{39}:0")
print(dive_obj.safety_stop())
dive_obj.segment(1.2, f"{39}:{30}")
print(dive_obj.safety_stop())
dive_obj.segment(1.2, f"{45}:{30}")
print(dive_obj.safety_stop())
dive_obj.segment(0.9, f"{46}:0")
print(dive_obj.safety_stop())
dive_obj.segment(0.9, f"{56}:0")
print(dive_obj.safety_stop())
dive_obj.segment(0.6, f"{56}:{30}")
print(dive_obj.safety_stop())
dive_obj.segment(0.6, f"{76}:0")
print(dive_obj.safety_stop())
dive_obj.segment(0.3, f"{76}:{30}")
print(dive_obj.safety_stop())
dive_obj.segment(0.3, f"{115}:{30}")
print(dive_obj.safety_stop())