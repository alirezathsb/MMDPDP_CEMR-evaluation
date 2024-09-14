import matplotlib.pyplot as plt

# Storage costs for different operations (in bits)
storage_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|GT|'  : 160,        # The size of an element in GT
    '|Zp|'  : 160,        # The size of an element in Zp
    '|id|'  : 40,         # The size of the user id 
}

def calc_GA_costs(r):
    # Pre-calculate common terms
    G = storage_costs['|G|']
    Gt = storage_costs['|GT|']
    Zp = storage_costs['|Zp|']
    id_size = storage_costs['|id|']
    
    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (r * id_size) + (r * Gt) 

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = (2 * r * id_size) + (((2 * r) + 1) * G) + (r * Gt) \
    + ((r + 2) * Zp)

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = (2 * r * id_size) + (r * G) + Zp

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = 0

    # Our scheme
    our_scheme_cost = (r * id_size) + (r * Gt) 

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

# Parameters for GA
r_values = list(range(0, 100, 10)) # From 0 to 100 with step 10

# Compute the costs for GA 
mw2023_costs_GA = []
mw2019_costs_GA = []
mc2023_costs_GA = []
mc2022_costs_GA = []
our_scheme_costs_GA =[]

for r in r_values:
    mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_GA_costs(r)
    mw2023_costs_GA.append(mw2023_cost/1000)           # Convert bits to kilobits
    mw2019_costs_GA.append(mw2019_cost/1000)           # Convert bits to kilobits
    mc2023_costs_GA.append(mc2023_cost/1000)           # Convert bits to kilobits
    mc2022_costs_GA.append(mc2022_cost/1000)           # Convert bits to kilobits
    our_scheme_costs_GA.append(our_scheme_cost/1000)   # Convert bits to kilobits

# Plotting the first GA results (varying r)
plt.figure(figsize=(7, 5))

plt.plot(r_values, mw2023_costs_GA, marker='o', label='[19]'
         , markersize=9, color='black', linestyle=':')           
plt.plot(r_values, mw2019_costs_GA, marker='s', label='[16]'
         ,markersize=8, color='#ff8923', linestyle=':')            #color: orange (#ff8923)
plt.plot(r_values, mc2023_costs_GA, marker='^', label='[15]'
         ,markersize=8, color='#1f77b4', linestyle=':')            #color: blue (#1f77b4)
plt.plot(r_values, mc2022_costs_GA, marker='v', label='[20]'
         ,markersize=8, color='#d62728', linestyle=':')            #color: red (#d62728)
plt.plot(r_values, our_scheme_costs_GA, marker='*', label='Our scheme'
         ,markersize=8, color='#2ca02c', linestyle=':')            #color: green (#2ca02c)

plt.xlabel('The number of registered users ($r$)')
plt.ylabel('Storage cost (kbit)')
plt.title('Storage cost for GA (Varying $r$)')
plt.legend()
plt.grid(True)
plt.show()
