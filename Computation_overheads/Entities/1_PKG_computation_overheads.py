import matplotlib.pyplot as plt
import numpy as np

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

def calc_PKG_costs(r, u):
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
    mw2023_cost =  (((3 * r) + u + 5) * exp_G) + ((r + u) * exp_Gt) + pair + (((2 * r) + u) * mul_G) \
    + ((r + u) * mul_Zp) + (((2 * r) + 4) * inv) + (r * hash_G) + ((r + 2) * hash_Zp) 

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = 0 

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = ((r + 2) * exp_G) + (r * mul_Zp) + (r * hash_Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = (3 * exp_G) + (3 * pair) + mul_Gt + (4 * hash_G)

    # Our scheme
    our_scheme_cost = (((2 * r) + 7) * exp_G) + ((r + 1) * pair) + (r * mul_G) \
    + (3 * mul_Zp) + (r * inv) + (r * hash_G) + (3 * hash_Zp)

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

def varying_r_and_u():
    # Parameters for PKG
    r_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    u_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    # Prepare 2D arrays to store costs
    mw2023_costs_PKG = np.zeros((len(r_values), len(u_values)))
    mw2019_costs_PKG = np.zeros((len(r_values), len(u_values)))
    mc2023_costs_PKG = np.zeros((len(r_values), len(u_values)))
    mc2022_costs_PKG = np.zeros((len(r_values), len(u_values)))
    our_scheme_costs_PKG = np.zeros((len(r_values), len(u_values)))

    # Compute the costs for PKG 
    for i, r in enumerate(r_values):
        for j, u in enumerate(u_values):
            mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_PKG_costs(r, u)
            mw2023_costs_PKG[i, j] = mw2023_cost / 1000           # Convert millisecond to second
            mw2019_costs_PKG[i, j] = mw2019_cost / 1000           # Convert millisecond to second
            mc2023_costs_PKG[i, j] = mc2023_cost / 1000           # Convert millisecond to second
            mc2022_costs_PKG[i, j] = mc2022_cost / 1000           # Convert millisecond to second
            our_scheme_costs_PKG[i, j] = our_scheme_cost / 1000   # Convert millisecond to second

    # Create the 3D plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Create meshgrid for r_values and u_values
    R, U = np.meshgrid(r_values, u_values)

    # Plot the surfaces
    ax.plot_surface(R, U, mw2023_costs_PKG.T, label='[19]', color='#1f77b4', alpha=0.7)
    ax.plot_surface(R, U, mw2019_costs_PKG.T, label='[16]', color='#ff8923', alpha=0.7)
    ax.plot_surface(R, U, mc2023_costs_PKG.T, label='[15]', color='#2ca02c', alpha=0.7)
    ax.plot_surface(R, U, mc2022_costs_PKG.T, label='[20]', color='#d62728', alpha=0.7)
    ax.plot_surface(R, U, our_scheme_costs_PKG.T, label='Our scheme', color='#9467bd', alpha=0.7)

    ax.set_xlabel('The number of registered users ($r$)')
    ax.set_ylabel('The number of unrevoked users ($u$)')
    ax.set_zlabel('Time cost (second)')
    ax.set_title('Computation cost for PKG (Varying $r$ and $u$)')
    ax.legend()
    ax.grid(True)
    plt.show()
    
varying_r_and_u()       # Generates a plot for varying r and u 
