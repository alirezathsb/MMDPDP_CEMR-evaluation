import matplotlib.pyplot as plt
import numpy as np

# Time costs for different operations (in milliseconds)
time_costs = {
    'T_exp_G'  : 721.93,     # Exponentiation on G
    'T_exp_GT' : 18.01,      # Exponentiation on GT
    'T_pair'   : 314.70,     # Bilinear pairing
    'T_mul_G'  : 4.29,       # Multiplication on G
    'T_mul_GT' : 1.06,       # Multiplication on GT
    'T_mul_Zp' : 0.93,       # Multiplication on Zp
    'T_hash_G' : 461.41,     # Hash to G
    'T_hash_Zp': 0.57,       # Hash on Zp
}

def calc_TPA_costs(c, m, s, ξ):
    # Pre-calculate common terms
    exp_G = time_costs['T_exp_G']
    exp_Gt = time_costs['T_exp_GT']
    pair = time_costs['T_pair']
    mul_G = time_costs['T_mul_G']
    mul_Gt = time_costs['T_mul_GT']
    mul_Zp = time_costs['T_mul_Zp']
    hash_G = time_costs['T_hash_G']
    hash_Zp = time_costs['T_hash_Zp']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = ((c + 1) * exp_G) + ((c - 1) * mul_G) + (s * mul_Zp) 

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = ((s + c + 28) * exp_G) + (10 * exp_Gt) + (8 * pair) \
    + ((s + c + 12) * mul_G) + (8 * mul_Gt) + (2 * hash_Zp)

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = (((ξ * c) + (m * s) + 2) * exp_G) + (2 * pair) \
    + (((ξ - 1) + ((ξ - 1) * (c - 1)) + ((m - 1) * (s - 1)) + 4) * mul_G) \
    + (((ξ * c) + (m * s)) * hash_G) + (2 * hash_Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = (((m * c) + s + 1) * exp_G) + (((2 * ξ) + 3) * pair) \
    + ((((m - 1) * (c - 1)) + s) * mul_G) + mul_Gt + mul_Zp + (((m * c) + ξ + 1) * hash_G)

    # Our scheme
    our_scheme_cost = (((m * c) + s + 2) * exp_G) + (2 * pair) \
    + ((((m - 1) * (c - 1)) + s + 3) * mul_G) + (m * c * hash_G) + (2 * hash_Zp)

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
            
            mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_TPA_costs(
                c=params.get('The number of challenge blocks ($c$)', 3),  
                m=params.get('The copy number ($m$)', 3), 
                s=params.get('The number of sectors in each block ($s$)', 3),
                ξ=params.get('The number of CSPs ($ξ$)', 3)
            )
            
            # Compute the costs for TPA
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

def varying_c_and_m():
    # Parameters for TPA
    c_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    m_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(c_values, m_values, 'The number of challenge blocks ($c$)'
                       , 'The copy number ($m$)', 
                       'Computation cost for TPA (Varying $c$ and $m$)', 
                       {'s': 3, 'ξ': 3})
    
def varying_c_and_s():
    # Parameters for TPA
    c_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    s_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(c_values, s_values, 'The number of challenge blocks ($c$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Computation cost for TPA (Varying $c$ and $s$)', 
                       {'m': 3, 'ξ': 3})

def varying_c_and_ξ():
    # Parameters for TPA
    c_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(c_values, ξ_values, 'The number of challenge blocks ($c$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Computation cost for TPA (Varying $c$ and $ξ$)', 
                       {'m': 3, 's': 3})
 
def varying_m_and_s():
    # Parameters for TPA
    m_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    s_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(m_values, s_values, 'The copy number ($m$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Computation cost for TPA (Varying $m$ and $s$)', 
                       {'c': 3, 'ξ': 3})

def varying_m_and_ξ():
    # Parameters for TPA
    m_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    ξ_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(m_values, ξ_values, 'The copy number ($m$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Computation cost for TPA (Varying $m$ and $ξ$)', 
                       {'c': 3, 's': 3})

def varying_s_and_ξ():
    # Parameters for TPA
    s_values = list(range(0, 22))  # From 0 to 22
    ξ_values = list(range(0, 22))  # From 0 to 22

    varying_parameters(s_values, ξ_values, 'The number of sectors in each block ($s$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Computation cost for TPA (Varying $s$ and $ξ$)', 
                       {'c': 3, 'm': 3})
 
varying_c_and_m()       # Generates a plot for varying c and m 
varying_c_and_s()       # Generates a plot for varying c and s 
varying_c_and_ξ()       # Generates a plot for varying c and ξ 
varying_m_and_s()       # Generates a plot for varying m and s 
varying_m_and_ξ()       # Generates a plot for varying m and ξ 
varying_s_and_ξ()       # Generates a plot for varying s and ξ 
