from dive import Dive

dive_obj = Dive()

gf_low = 30
gf_high = 80
final_stop_depth = 1.3
first_stop_depth = dive_obj._FSD
current_stop_depth = None
gf_slope = (gf_high - gf_low) / (final_stop_depth - first_stop_depth)

gf = gf_slope * current_stop_depth + gf_high # If we still don't know first stop depth we should make the gradient factor
# equal to 1 in some way, so when applied to buhlmann it doesn't affect the formula.

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