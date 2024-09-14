import matplotlib.pyplot as plt

# Time costs for different operations (in milliseconds)
time_costs = {
    'T_pair'   : 314.70,     # Bilinear pairing
    'T_mul_GT' : 1.06,       # Multiplication on GT
    'T_hash_G' : 461.41,     # Hash to G
}

def calc_trace_costs():
    # Pre-calculate common terms
    pair = time_costs['T_pair']
    mul_Gt = time_costs['T_mul_GT']
    hash_G = time_costs['T_hash_G']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (2 * pair) + mul_Gt + hash_G

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost =  (2 * pair) + mul_Gt + hash_G

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = 0

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = 0

    # Our scheme 
    our_scheme_cost = (2 * pair) + mul_Gt + hash_G

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost


# Compute the costs for trace phase
mw2023_costs_trace = []
mw2019_costs_trace = []
mc2023_costs_trace = []
mc2022_costs_trace = []
our_scheme_costs_trace =[]

mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_trace_costs()
mw2023_costs_trace.append(mw2023_cost/1000)           # Convert millisecond to second
mw2019_costs_trace.append(mw2019_cost/1000)           # Convert millisecond to second
mc2023_costs_trace.append(mc2023_cost/1000)           # Convert millisecond to second
mc2022_costs_trace.append(mc2022_cost/1000)           # Convert millisecond to second
our_scheme_costs_trace.append(our_scheme_cost/1000)   # Convert millisecond to second

# Plotting the first trace results
plt.figure(figsize=(7, 5))

plt.plot(mw2023_costs_trace, marker='o', label='[19]'
         , markersize=9, color='#1f77b4', linestyle='-')           #color: blue (#1f77b4)
plt.plot(mw2019_costs_trace, marker='^', label='[16]'
         ,markersize=9, color='#ff8923', linestyle='-')            #color: orange (#ff8923)
plt.plot(mc2023_costs_trace, marker='<', label='[15]'
         ,markersize=8, color='black', linestyle='-')            
plt.plot(mc2022_costs_trace, marker='>', label='[20]'
         ,markersize=9, color='#d62728', linestyle='-')            #color: red (#d62728)
plt.plot(our_scheme_costs_trace, marker='v', label='Our scheme'
         ,markersize=8, color='#2ca02c', linestyle='-')            #color: green (#2ca02c)

plt.ylabel('Time cost (second)')
plt.title('Computation cost for trace phase')
plt.legend()
plt.grid(True)
plt.show()
