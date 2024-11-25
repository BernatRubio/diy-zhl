from dive import Dive

dive_obj = Dive()

print(dive_obj.safety_stop())
dive_obj.segment(4.97, f"{2}:{30}")
dive_obj.segment(4.97, f"{21}:0")
print(f"Safety stop at {dive_obj.safety_stop()} atm")

dive_obj.segment(3.4, f"{24}:0")

dive_obj.segment(3.4, f"{25}:0")
print(f"Safety stop at {dive_obj.safety_stop()} atm")

dive_obj.segment(3.1, f"{25}:{23}")
print(f"Safety stop at {dive_obj.safety_stop()} atm")

dive_obj.segment(3.1, f"{31}:{23}")
print(f"Safety stop at {dive_obj.safety_stop()} atm")

dive_obj.segment(2.8, f"{31}:{46}")

dive_obj.segment(2.8, f"{32}:{46}")
print(f"Safety stop at {dive_obj.safety_stop()} atm")