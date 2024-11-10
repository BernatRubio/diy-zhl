from dive import Dive

# The diver descends from the surface (1 atm) to a depth of 30 meters (4 atm) over 5 minutes 
# at a rate of 0.6 atm per minute, then remains at 30 meters (4 atm) for a bottom time 
# of 20 minutes. The diver ascends to 5 meters (1.5 atm) over 8.3 minutes at a rate 
# of 0.3 atm per minute, pauses for a 3-minute safety stop at 5 meters, and finally ascends 
# to the surface over 1.7 minutes at a rate of 0.3 atm per minute.

dive_obj = Dive()

# The diver descends to 4 atm in 5 min
dive_obj.segment(4.0, f"{5}:0")
print(f"NDL when diver arrives to 4 atm: {dive_obj.ndl(0)} min")

# The diver stays at 4 atm for 20 min
dive_obj.segment(4.0, f"{25}:0")

# The diver ascends to 1.5 atm
pressure = 4.0
time = 25
for i in range(8):
    pressure -= 0.3
    time += 1
    dive_obj.segment(pressure, f"{time}:0")
    print(f"Ceiling ascending to {round(pressure,2)} atm: {max(dive_obj.ceilings)} atm")
dive_obj.segment(1.5, f"{33}:{18}")
print(f"Ceiling ascending to 1.5 atm: {max(dive_obj.ceilings)} atm")

# The diver stops at 1.5 atm for 3 min
dive_obj.segment(1.5, f"{36}:{18}")
print(f"Ceiling staying at 1.5 atm for 3 min: {max(dive_obj.ceilings)} atm")

# The diver ascends to 1.2 atm
dive_obj.segment(1.5, f"{37}:{18}")
print(f"Ceiling ascending to 1.2 atm: {max(dive_obj.ceilings)} atm")

# The diver ascends to 1 atm
dive_obj.segment(1.5, f"{38}:0")
print(f"Ceiling ascending to 1 atm: {max(dive_obj.ceilings)} atm")


