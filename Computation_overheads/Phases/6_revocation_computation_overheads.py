import matplotlib.pyplot as plt

# Time costs for different operations (in milliseconds)
time_costs = {
    'T_exp_G'  : 721.93,     # Exponentiation on G
    'T_exp_GT' : 18.01,      # Exponentiation on GT
    'T_pair'   : 314.70,     # Bilinear pairing
    'T_inv'    : 0.009,      # Inversion
    'T_mul_G'  : 4.29,       # Multiplication on G
    'T_mul_Zp' : 0.93,       # Multiplication on Zp
    'T_hash_G' : 461.41,     # Hash to G
    'T_hash_Zp': 0.57,       # Hash on Zp
}

def calc_revocation_costs(u):
    # Pre-calculate common terms
    exp_G = time_costs['T_exp_G']
    exp_Gt = time_costs['T_exp_GT']
    pair = time_costs['T_pair']
    inv = time_costs['T_inv']
    mul_G = time_costs['T_mul_G']
    mul_Zp = time_costs['T_mul_Zp']
    hash_G = time_costs['T_hash_G']
    hash_Zp = time_costs['T_hash_Zp']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = ((u + 3) * exp_G) + ((u + 1) * exp_Gt) + ((u + 1) * mul_G) \
    + (u * mul_Zp) + (2 * inv) + (3 * hash_Zp)

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost =  (((2 * u) + 3) * exp_G) + ((u + 2) * pair) \
    + ((u + 2) * mul_G) + ((u + 2) * inv) + (u * hash_G)

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = ((u + 2) * exp_G) + mul_G + (u * mul_Zp) + ((u + 1) * hash_Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = 0

    # Our scheme 
    our_scheme_cost = (3 * exp_G) + exp_Gt + mul_G + mul_Zp + (2 * hash_Zp)
    
    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

# Parameters for revocation
u_values = list(range(0, 8))  # From 0 to 8

# Compute the costs for revocation phase
mw2023_costs_revocation = []
mw2019_costs_revocation = []
mc2023_costs_revocation = []
mc2022_costs_revocation = []
our_scheme_costs_revocation =[]

for u in u_values:
    mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_revocation_costs(u)
    mw2023_costs_revocation.append(mw2023_cost/1000)           # Convert millisecond to second
    mw2019_costs_revocation.append(mw2019_cost/1000)           # Convert millisecond to second
    mc2023_costs_revocation.append(mc2023_cost/1000)           # Convert millisecond to second
    mc2022_costs_revocation.append(mc2022_cost/1000)           # Convert millisecond to second
    our_scheme_costs_revocation.append(our_scheme_cost/1000)   # Convert millisecond to second

# Plotting the first revocation results (varying s)
plt.figure(figsize=(7, 5))

plt.plot(u_values, mw2023_costs_revocation, marker='o', label='[19]'
         , markersize=9, color='#1f77b4', linestyle='-')           #color: blue (#1f77b4)
plt.plot(u_values, mw2019_costs_revocation, marker='^', label='[16]'
         ,markersize=9, color='#ff8923', linestyle='-')            #color: orange (#ff8923)
plt.plot(u_values, mc2023_costs_revocation, marker='D', label='[15]'
         ,markersize=8, color='#2ca02c', linestyle='-')            #color: green (#2ca02c)
plt.plot(u_values, mc2022_costs_revocation, marker='v', label='[20]'
         ,markersize=9, color='#d62728', linestyle='-')            #color: red (#d62728)
plt.plot(u_values, our_scheme_costs_revocation, marker='s', label='Our scheme'
         ,markersize=8, color='#9467bd', linestyle='-')            #color: purple (#9467bd)

plt.xlabel('The number of unrevoked users ($u$)')
plt.ylabel('Time cost (second)')
plt.title('Computation cost for revocation phase (Varying $u$)')
plt.legend()
plt.grid(True)
plt.show()
