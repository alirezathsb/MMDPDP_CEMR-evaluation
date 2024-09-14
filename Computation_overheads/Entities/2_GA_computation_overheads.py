import matplotlib.pyplot as plt
import numpy as np

# Time costs for different operations (in milliseconds)
time_costs = {
    'T_exp_G'  : 721.93,     # Exponentiation on G
    'T_pair'   : 314.70,     # Bilinear pairing
    'T_inv'    : 0.009,      # Inversion
    'T_mul_G'  : 4.29,       # Multiplication on G
    'T_mul_Zp' : 0.93,       # Multiplication on Zp
    'T_hash_G' : 461.41,     # Hash to G
    'T_hash_Zp': 0.57,       # Hash on Zp
}

def calc_GA_costs(r, u, ξ):
    # Pre-calculate common terms
    exp_G = time_costs['T_exp_G']
    pair = time_costs['T_pair']
    inv = time_costs['T_inv']
    mul_G = time_costs['T_mul_G']
    mul_Zp = time_costs['T_mul_Zp']
    hash_G = time_costs['T_hash_G']
    hash_Zp = time_costs['T_hash_Zp']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = 0

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = (((2 * r) + (2 * u) + 4) * exp_G) + ((r + u + 2) * pair) \
    + ((r + u + 1) * mul_G) + ((r + u + 1) * inv) + ((r + u) * hash_G)

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = (((2 * r) + u) * exp_G) + ((r + u) * mul_Zp) + ((r + u) * hash_Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = 0

    # Our scheme
    our_scheme_cost = ((ξ - 1) * mul_G) 
    
    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

def create_3d_plot(X, Y, Z_values, x_label, y_label, z_label, title, legends):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    for Z, label in zip(Z_values, legends):
        ax.plot_surface(X, Y, Z, label=label, alpha=0.7)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    plt.show()

def varying_parameters(x_values, y_values, x_label, y_label, title, varying_params):
    # Prepare 2D arrays to store costs
    mw2023_costs = np.zeros((len(x_values), len(y_values)))
    mw2019_costs = np.zeros((len(x_values), len(y_values)))
    mc2023_costs = np.zeros((len(x_values), len(y_values)))
    mc2022_costs = np.zeros((len(x_values), len(y_values)))
    our_scheme_costs = np.zeros((len(x_values), len(y_values)))

    for i, x in enumerate(x_values):
        for j, y in enumerate(y_values):
            params = varying_params.copy()
            params[x_label] = x
            params[y_label] = y
            
            mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_GA_costs(
                r=params.get('The number of registered users ($r$)', 3), 
                u=params.get('The number of unrevoked users ($u$)', 3),  
                ξ=params.get('The number of CSPs ($ξ$)', 3), 
            )
            
            # Compute the costs for GA
            mw2023_costs[i, j] = mw2023_cost / 1000             # Convert millisecond to second
            mw2019_costs[i, j] = mw2019_cost / 1000             # Convert millisecond to second
            mc2023_costs[i, j] = mc2023_cost / 1000             # Convert millisecond to second
            mc2022_costs[i, j] = mc2022_cost / 1000             # Convert millisecond to second
            our_scheme_costs[i, j] = our_scheme_cost / 1000     # Convert millisecond to second

    # Create meshgrid for x_values and y_values
    X, Y = np.meshgrid(x_values, y_values)
    
    # Plot the surfaces
    create_3d_plot(X, Y, [mw2023_costs.T, mw2019_costs.T, mc2023_costs.T, mc2022_costs.T, our_scheme_costs.T],
                   x_label, y_label, 'Time cost (second)', title,
                   ['[19]', '[16]', '[15]', '[20]', 'Our scheme'])

def varying_r_and_u():
    # Parameters for GA
    r_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    u_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(r_values, u_values, 'The number of registered users ($r$)'
                       , 'The number of unrevoked users ($u$)', 
                       'Computation cost for GA (Varying $r$ and $u$)', 
                       {'ξ': 3})
    
def varying_r_and_ξ():
    # Parameters for GA
    r_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(r_values, ξ_values, 'The number of registered users ($r$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Computation cost for GA (Varying $r$ and $ξ$)', 
                       {'u': 3})
    
def varying_u_and_ξ():
    # Parameters for GA
    u_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(u_values, ξ_values, 'The number of unrevoked users ($u$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Computation cost for GA (Varying $u$ and $ξ$)', 
                       {'r': 3})
        
varying_r_and_u()       # Generates a plot for varying r and u  
varying_r_and_ξ()       # Generates a plot for varying r and ξ  
varying_u_and_ξ()       # Generates a plot for varying u and ξ  
