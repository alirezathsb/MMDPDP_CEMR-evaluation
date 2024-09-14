import matplotlib.pyplot as plt

# Storage costs for different operations (in bits)
storage_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|Zp|'  : 160,        # The size of an element in Zp
}

def calc_PKG_costs():
    # Pre-calculate common terms
    G = storage_costs['|G|']
    Zp = storage_costs['|Zp|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (2 * G) + (5 * Zp) 

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = 0
    
    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = Zp

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = Zp

    # Our scheme
    our_scheme_cost = G + (4 * Zp)

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

# Compute the costs for PKG
mw2023_costs_PKG = []
mw2019_costs_PKG = []
mc2023_costs_PKG = []
mc2022_costs_PKG = []
our_scheme_costs_PKG =[]

mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_PKG_costs()
mw2023_costs_PKG.append(mw2023_cost/1000)           # Convert bits to kilobits
mw2019_costs_PKG.append(mw2019_cost/1000)           # Convert bits to kilobits
mc2023_costs_PKG.append(mc2023_cost/1000)           # Convert bits to kilobits
mc2022_costs_PKG.append(mc2022_cost/1000)           # Convert bits to kilobits
our_scheme_costs_PKG.append(our_scheme_cost/1000)   # Convert bits to kilobits

# Plotting the first PKG results
plt.figure(figsize=(7, 5))

plt.plot(mw2023_costs_PKG, marker='s', label='[19]'
         , markersize=9, color='black', linestyle='-')             
plt.plot(mw2019_costs_PKG, marker='^', label='[16]'
         ,markersize=9, color='#ff8923', linestyle='-')            #color: orange (#ff8923)
plt.plot(mc2023_costs_PKG, marker='D', label='[15]'
         ,markersize=8, color='#1f77b4', linestyle='-')            #color: blue (#1f77b4)
plt.plot(mc2022_costs_PKG, marker='v', label='[20]'
         ,markersize=9, color='#d62728', linestyle='-')            #color: red (#d62728)
plt.plot(our_scheme_costs_PKG, marker='*', label='Our scheme'
         ,markersize=8, color='#2ca02c', linestyle='-')            #color: green (#2ca02c)

plt.ylabel('Storage cost (kbit)')
plt.title('Storage cost for PKG')
plt.legend()
plt.grid(True)
plt.show()
