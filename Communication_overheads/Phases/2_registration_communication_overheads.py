import matplotlib.pyplot as plt

# Communication costs for different operations (in bits)
communication_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|GT|'  : 160,        # The size of an element in GT
    '|Zp|'  : 160,        # The size of an element in Zp
    '|id|'  : 40,         # The size of the user id 
}

def calc_registration_costs(r):
    # Pre-calculate common terms
    G = communication_costs['|G|']
    Gt = communication_costs['|GT|']
    Zp = communication_costs['|Zp|']
    id_size = communication_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = ((r + 1) * id_size) + (4 * r * G) + (2 * r * Gt) + (2 * r * Zp) 

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = id_size + (2 * r * G) + (r * Gt) + (r * Zp) 

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = (2 * id_size) + (((2 * r) + 2) * G) + (2 * r * Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = 0

    # Our scheme
    our_scheme_cost = id_size + (4 * r * G) + (r * Gt) + (3 * r * Zp)

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

# Parameters for registration
r_values = list(range(0, 100, 10)) # From 0 to 100 with step 10

# Compute the costs for registration phase
mw2023_costs_registration = []
mw2019_costs_registration = []
mc2023_costs_registration = []
mc2022_costs_registration = []
our_scheme_costs_registration =[]

for r in r_values:
    mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_registration_costs(r)
    mw2023_costs_registration.append(mw2023_cost/1000)           # Convert bits to kilobits
    mw2019_costs_registration.append(mw2019_cost/1000)           # Convert bits to kilobits
    mc2023_costs_registration.append(mc2023_cost/1000)           # Convert bits to kilobits
    mc2022_costs_registration.append(mc2022_cost/1000)           # Convert bits to kilobits
    our_scheme_costs_registration.append(our_scheme_cost/1000)   # Convert bits to kilobits

# Plotting the first registration results (varying r)
plt.figure(figsize=(7, 5))

plt.plot(r_values, mw2023_costs_registration, marker='o', label='[19]'
         , markersize=9, color='#1f77b4', linestyle='-')           #color: blue (#1f77b4)
plt.plot(r_values, mw2019_costs_registration, marker='^', label='[16]'
         ,markersize=9, color='#ff8923', linestyle='-')            #color: orange (#ff8923)
plt.plot(r_values, mc2023_costs_registration, marker='D', label='[15]'
         ,markersize=8, color='#2ca02c', linestyle='-')            #color: green (#2ca02c)
plt.plot(r_values, mc2022_costs_registration, marker='v', label='[20]'
         ,markersize=9, color='#d62728', linestyle='-')            #color: red (#d62728)
plt.plot(r_values, our_scheme_costs_registration, marker='s', label='Our scheme'
         ,markersize=8, color='#9467bd', linestyle='-')            #color: purple (#9467bd)

plt.xlabel('The number of registered users ($r$)')
plt.ylabel('Communication cost (kbit)')
plt.title('Communication cost for registration phase (Varying $r$)')
plt.legend()
plt.grid(True)
plt.show()
