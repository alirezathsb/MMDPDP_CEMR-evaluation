 import matplotlib.pyplot as plt

# Time costs for different operations (in milliseconds)
time_costs = {
    'T_exp_G'  : 721.93,     # Exponentiation on G
    'T_pair'   : 314.70,     # Bilinear pairing
    'T_mul_G'  : 4.29,       # Multiplication on G
    'T_mul_GT' : 1.06,       # Multiplication on GT
    'T_hash_G' : 461.41,     # Hash to G
    'T_hash_Zp': 0.57,       # Hash on Zp
}

def calc_setup_costs(s):
    # Pre-calculate common terms
    exp_G = time_costs['T_exp_G']
    pair = time_costs['T_pair']
    mul_G = time_costs['T_mul_G']
    mul_Gt = time_costs['T_mul_GT']
    hash_G = time_costs['T_hash_G']
    hash_Zp = time_costs['T_hash_Zp']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (3 * exp_G) + pair
    
    # MW2019: Multi-writer 2019 [16]
    mw2019_cost =  (2 * exp_G) + pair

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = 2 * exp_G 

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = ((s + 6) * exp_G) + (7 * pair) + mul_G + mul_Gt + (7 * hash_G) + (4 * hash_Zp) 

    # Our scheme 
    our_scheme_cost = (4 * exp_G) + pair
    
    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

# Parameters for Setup
s_values = list(range(0, 8))  # From 0 to 8

# Compute the costs for Setup phase
mw2023_costs_setup = []
mw2019_costs_setup = []
mc2023_costs_setup = []
mc2022_costs_setup = []
our_scheme_costs_setup =[]

for s in s_values:
    mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_setup_costs(s)
    mw2023_costs_setup.append(mw2023_cost/1000)           # Convert millisecond to second
    mw2019_costs_setup.append(mw2019_cost/1000)           # Convert millisecond to second
    mc2023_costs_setup.append(mc2023_cost/1000)           # Convert millisecond to second
    mc2022_costs_setup.append(mc2022_cost/1000)           # Convert millisecond to second
    our_scheme_costs_setup.append(our_scheme_cost/1000)   # Convert millisecond to second

# Plotting the first Setup results (varying s)
plt.figure(figsize=(7, 5))

plt.plot(s_values, mw2023_costs_setup, marker='o', label='[19]'
         , markersize=9, color='#1f77b4', linestyle='-')           #color: blue (#1f77b4)
plt.plot(s_values, mw2019_costs_setup, marker='^', label='[16]'
         ,markersize=9, color='#ff8923', linestyle='-')            #color: orange (#ff8923)
plt.plot(s_values, mc2023_costs_setup, marker='v', label='[15]'
         ,markersize=8, color='#2ca02c', linestyle='-')            #color: green (#2ca02c)
plt.plot(s_values, mc2022_costs_setup, marker='D', label='[20]'
         ,markersize=9, color='#d62728', linestyle='-')            #color: red (#d62728)
plt.plot(s_values, our_scheme_costs_setup, marker='s', label='Our scheme'
         ,markersize=8, color='#9467bd', linestyle='-')            #color: purple (#9467bd)

plt.xlabel('The number of sectors in each block ($s$)')
plt.ylabel('Time cost (second)')
plt.title('Computation cost for setup phase (Varying $s$)')
plt.legend()
plt.grid(True)
plt.show()
