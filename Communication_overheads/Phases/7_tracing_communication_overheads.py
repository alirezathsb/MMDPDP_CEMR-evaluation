import matplotlib.pyplot as plt

# Communication costs for different operations (in bits)
communication_costs = {
    '|GT|'  : 160,        # The size of an element in GT
    '|id|'  : 40,         # The size of the user id 
}

def calc_trace_costs():
    # Pre-calculate common terms
    Gt = communication_costs['|GT|']
    id_size = communication_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (2 * id_size) + (2 * Gt) 

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = 0

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = 0

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = 0

    # Our scheme
    our_scheme_cost = (2 * id_size) + (2 * Gt) 

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

# Compute the costs for trace phase
mw2023_costs_trace = []
mw2019_costs_trace = []
mc2023_costs_trace = []
mc2022_costs_trace = []
our_scheme_costs_trace =[]

mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_trace_costs()
mw2023_costs_trace.append(mw2023_cost/1000)           # Convert bits to kilobits
mw2019_costs_trace.append(mw2019_cost/1000)           # Convert bits to kilobits
mc2023_costs_trace.append(mc2023_cost/1000)           # Convert bits to kilobits
mc2022_costs_trace.append(mc2022_cost/1000)           # Convert bits to kilobits
our_scheme_costs_trace.append(our_scheme_cost/1000)   # Convert bits to kilobits

# Plotting the first trace results
plt.figure(figsize=(7, 5))

plt.plot(mw2023_costs_trace, marker='s', label='[19]'
         , markersize=9, color='black', linestyle='-')             
plt.plot(mw2019_costs_trace, marker='^', label='[16]'
         ,markersize=9, color='#ff8923', linestyle='-')            #color: orange (#ff8923)
plt.plot(mc2023_costs_trace, marker='D', label='[15]'
         ,markersize=8, color='#1f77b4', linestyle='-')            #color: blue (#1f77b4)
plt.plot(mc2022_costs_trace, marker='v', label='[20]'
         ,markersize=9, color='#d62728', linestyle='-')            #color: red (#d62728)
plt.plot(our_scheme_costs_trace, marker='*', label='Our scheme'
         ,markersize=8, color='#2ca02c', linestyle='-')            #color: green (#2ca02c)

plt.ylabel('Communication cost (kbit)')
plt.title('Communication cost for trace phase')
plt.legend()
plt.grid(True)
plt.show()
