import matplotlib.pyplot as plt

# Communication costs for different operations (in bits)
communication_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|GT|'  : 160,        # The size of an element in GT
    '|Zp|'  : 160,        # The size of an element in Zp
    '|id|'  : 40,         # The size of the user id 
}

def calc_revocation_costs(u):
    # Pre-calculate common terms
    G = communication_costs['|G|']
    Gt = communication_costs['|GT|']
    Zp = communication_costs['|Zp|']
    id_size = communication_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (u * id_size) + (2 * u * G) + (2 * u * Gt) + (u * Zp) 

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = (((2 * u) + 4) * G) + Gt + (u * Zp) 

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = (u * G) + (u * Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = 0

    # Our scheme
    our_scheme_cost = id_size + (u * G) + Gt + (u * Zp)

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

# Parameters for revocation
u_values = list(range(0, 100, 10)) # From 0 to 100 with step 10

# Compute the costs for revocation phase
mw2023_costs_revocation = []
mw2019_costs_revocation = []
mc2023_costs_revocation = []
mc2022_costs_revocation = []
our_scheme_costs_revocation =[]

for u in u_values:
    mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_revocation_costs(u)
    mw2023_costs_revocation.append(mw2023_cost/1000)           # Convert bits to kilobits
    mw2019_costs_revocation.append(mw2019_cost/1000)           # Convert bits to kilobits
    mc2023_costs_revocation.append(mc2023_cost/1000)           # Convert bits to kilobits
    mc2022_costs_revocation.append(mc2022_cost/1000)           # Convert bits to kilobits
    our_scheme_costs_revocation.append(our_scheme_cost/1000)   # Convert bits to kilobits

# Plotting the first revocation results (varying u)
plt.figure(figsize=(7, 5))

plt.plot(u_values, mw2023_costs_revocation, marker='D', label='[19]'
         , markersize=9, color='#1f77b4', linestyle=':')           #color: blue (#1f77b4)
plt.plot(u_values, mw2019_costs_revocation, marker='o', label='[16]'
         ,markersize=9, color='#ff8923', linestyle=':')            #color: orange (#ff8923)
plt.plot(u_values, mc2023_costs_revocation, marker='s', label='[15]'
         ,markersize=9, color='black', linestyle=':')             
plt.plot(u_values, mc2022_costs_revocation, marker='^', label='[20]'
         ,markersize=8, color='#d62728', linestyle=':')            #color: red (#d62728)
plt.plot(u_values, our_scheme_costs_revocation, marker='*', label='Our scheme'
         ,markersize=8, color='#2ca02c', linestyle=':')            #color: green (#2ca02c)

plt.xlabel('The number of unrevoked users ($u$)')
plt.ylabel('Communication cost (kbit)')
plt.title('Communication cost for revocation phase (Varying $u$)')
plt.legend()
plt.grid(True)
plt.show()
