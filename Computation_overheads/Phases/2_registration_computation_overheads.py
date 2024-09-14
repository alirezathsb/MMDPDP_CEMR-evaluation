import matplotlib.pyplot as plt

# Time costs for different operations (in milliseconds)
time_costs = {
    'T_exp_G'  : 721.93,     # Exponentiation on G
    'T_exp_GT' : 18.01,      # Exponentiation on GT
    'T_pair'   : 314.70,     # Bilinear pairing
    'T_inv'    : 0.009,      # Inversion
    'T_mul_G'  : 4.29,       # Multiplication on G
    'T_mul_GT' : 1.06,       # Multiplication on GT
    'T_mul_Zp' : 0.93,       # Multiplication on Zp
    'T_hash_G' : 461.41,     # Hash to G
    'T_hash_Zp': 0.57,       # Hash on Zp
}

def calc_registration_costs(r):
    # Pre-calculate common terms
    exp_G = time_costs['T_exp_G']
    exp_Gt = time_costs['T_exp_GT']
    pair = time_costs['T_pair']
    inv = time_costs['T_inv']
    mul_G = time_costs['T_mul_G']
    mul_Gt = time_costs['T_mul_GT']
    mul_Zp = time_costs['T_mul_Zp']
    hash_G = time_costs['T_hash_G']
    hash_Zp = time_costs['T_hash_Zp']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (((3 * r) + 4) * exp_G) + ((r + 1) * exp_Gt) + (4 * pair) \
    + (((2 * r) + 2) * mul_G) + mul_Gt + (r * mul_Zp) + (((2 * r) + 2) * inv) \
    + ((r + 1) * hash_G) + ((r + 3) * hash_Zp)

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost =  (((2 * r) + 1) * exp_G) + ((r + 5) * pair) + ((r + 1) * mul_G) \
    + mul_Gt + (r * inv) + ((r + 1) * hash_G)

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = (((3 * r) + 6) * exp_G) + (2 * mul_G) + (2 * r * mul_Zp) \
    + (((2 * r) + 2) * hash_Zp)
 
    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = 0 

    # Our scheme 
    our_scheme_cost = (((2 * r) + 7) * exp_G) + ((r + 5) * pair) + ((r + 3) * mul_G) \
    + mul_Gt + (2 * mul_Zp) + (r * inv) + ((r + 1) * hash_G) + (4 * hash_Zp)
    
    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

# Parameters for registration
r_values = list(range(0, 200, 20)) # From 0 to 200 with step 20

# Compute the costs for registration phase
mw2023_costs_registration = []
mw2019_costs_registration = []
mc2023_costs_registration = []
mc2022_costs_registration = []
our_scheme_costs_registration =[]

for r in r_values:
    mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_registration_costs(r)
    mw2023_costs_registration.append(mw2023_cost/1000)           # Convert millisecond to second
    mw2019_costs_registration.append(mw2019_cost/1000)           # Convert millisecond to second
    mc2023_costs_registration.append(mc2023_cost/1000)           # Convert millisecond to second
    mc2022_costs_registration.append(mc2022_cost/1000)           # Convert millisecond to second
    our_scheme_costs_registration.append(our_scheme_cost/1000)   # Convert millisecond to second

# Plotting the first registration results (varying r)
plt.figure(figsize=(7, 5))

plt.plot(r_values, mw2023_costs_registration, marker='D', label='[19]' 
         , markersize=9, color='black', linestyle=':')          
plt.plot(r_values, mw2019_costs_registration, marker='o', label='[16]'
         ,markersize=8, color='#ff8923', linestyle=':')                     #color: orange (#ff8923) 
plt.plot(r_values, mc2023_costs_registration, marker='^', label='[15]' 
         ,markersize=8, color='#2ca02c', linestyle=':')                     #color: green (#2ca02c)
plt.plot(r_values, mc2022_costs_registration, marker='*', label='[20]'     
         ,markersize=8, color='#d62728', linestyle=':')                     #color: red (#d62728)
plt.plot(r_values, our_scheme_costs_registration, marker='v', label='Our scheme'
         ,markersize=8, color='#1f77b4', linestyle=':')                     #color: blue (#1f77b4)

plt.xlabel('The number of registered users ($r$)')
plt.ylabel('Time cost (second)')
plt.title('Computation cost for registration phase (Varying $r$)')
plt.legend()
plt.grid(True)
plt.show()
