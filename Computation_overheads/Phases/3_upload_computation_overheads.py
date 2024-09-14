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

def calc_upload_costs(n, m, s, ξ , n_l):
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
    mw2023_cost =  (((3 * n) + 7) * exp_G) + (15 *  + exp_Gt) \
    + (((2 * n) + 10) * pair) + ((n + 2) * mul_G) + (13 * mul_Gt) \
    + (((n * s) + 7) * mul_Zp) + (((3 * n) + 2) * hash_Zp)

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = (((n * s) + 43) * exp_G) + (16 * exp_Gt) + (12 * pair) \
    + (((n * s) - n + 19) * mul_G) + (13 * mul_Gt) + (9 * mul_Zp) + (3 * hash_Zp)
    
    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = (((ξ * n * m * s) + (n * m * s) + (ξ * n) + (2 * n)) * exp_G) + (2 * n * pair) \
    + (((ξ * n * m * s) - (ξ * n * m) - (ξ * n * s) + (n * m * s) - (n * m) - (n * s) + (2 * ξ * n) + (5 * n)) * mul_G) \
    + (((ξ * n * m * s) + (n * m * s) + (ξ * n) + n) * hash_G) + (((ξ * n) + (2 * n)) * hash_Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = (((s * n_l * n) + (2 * n * m) + ξ + 2) * exp_G) + (((2 * ξ) + 5) * pair) \
    + (((2 * (n_l - 1) * (n-1)) + (2 * n * m) + s) * mul_G) + mul_Gt + (n * m * s * mul_Zp) \
    + (((n * m) + (ξ * n) + (n_l * n) + (2 * ξ) + 3) * hash_G) + (n * m * hash_Zp)

    # Our scheme
    our_scheme_cost = (((2 * n * m) + (2 * s) + 31) * exp_G) + (6 * exp_Gt) + (10 * pair) \
    + (((2 * (n_l - 1) * (n - 1)) + (n * m) + s + 15) * mul_G) + (9 * mul_Gt) \
    + (((n * m * s) + 9) * mul_Zp) + (((n * m) + (n_l * n)) * hash_G) + (((ξ * n) + 4) * hash_Zp)

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
            
            mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_upload_costs(
                n=params.get('The block number ($n$)', 3), 
                m=params.get('The copy number ($m$)', 3), 
                s=params.get('The number of sectors in each block ($s$)', 3),
                ξ=params.get('The number of CSPs ($ξ$)', 3),  
                n_l=params.get('The copy number stored in every CSP ($n_l$)', 3)
            )
            
            # Compute the costs for upload
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

def varying_n_and_m():
    # Parameters for Upload
    n_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    m_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(n_values, m_values, 'The block number ($n$)'
                       , 'The copy number ($m$)', 
                       'Computation cost for upload phase (Varying $n$ and $m$)', 
                       {'s': 3, 'ξ': 3, 'n_l': 3})
    
def varying_n_and_s():
    # Parameters for Upload
    n_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    s_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(n_values, s_values, 'The block number ($n$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Computation cost for upload phase (Varying $n$ and $s$)', 
                       {'m': 3, 'ξ': 3, 'n_l': 3})
    
def varying_n_and_ξ():
    # Parameters for Upload
    n_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(n_values, ξ_values, 'The block number ($n$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Computation cost for upload phase (Varying $n$ and $ξ$)', 
                       {'m': 3, 's': 3, 'n_l': 3})
    
def varying_n_and_n_l():
    # Parameters for Upload
    n_values = list(range(0, 30, 3))    # From 0 to 30 with step 3
    n_l_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(n_values, n_l_values, 'The block number ($n$)'
                       , 'The copy number stored in every CSP ($n_l$)', 
                       'Computation cost for upload phase (Varying $n$ and $n_l$)', 
                       {'m': 3, 's': 3, 'ξ': 3})
    
def varying_m_and_s():
    # Parameters for Upload
    m_values = list(range(0, 10, 1))    # From 0 to 10 with step 1
    s_values = list(range(0, 10, 1))    # From 0 to 10 with step 1

    varying_parameters(m_values, s_values, 'The copy number ($m$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Computation cost for upload phase (Varying $m$ and $s$)', 
                       {'n': 3, 'ξ': 3, 'n_l': 3})
    
def varying_m_and_ξ():
    # Parameters for Upload
    m_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(m_values, ξ_values, 'The copy number ($m$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Computation cost for upload phase (Varying $m$ and $ξ$)', 
                       {'n': 3, 's': 3, 'n_l': 3})
    
def varying_m_and_n_l():
    # Parameters for Upload
    m_values = list(range(0, 30, 3))    # From 0 to 30 with step 3
    n_l_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(m_values, n_l_values, 'The copy number ($m$)'
                       , 'The copy number stored in every CSP ($n_l$)', 
                       'Computation cost for upload phase (Varying $m$ and $n_l$)', 
                       {'n': 3, 's': 3, 'ξ': 3})

def varying_s_and_ξ():
    # Parameters for Upload
    s_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(s_values, ξ_values, 'The number of sectors in each block ($s$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Computation cost for upload phase (Varying $s$ and $ξ$)', 
                       {'n': 3, 'm': 3, 'n_l': 3})
       
def varying_s_and_n_l():
    # Parameters for Upload
    s_values = list(range(0, 30, 3))    # From 0 to 30 with step 3
    n_l_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(s_values, n_l_values, 'The number of sectors in each block ($s$)'
                       , 'The copy number stored in every CSP ($n_l$)', 
                       'Computation cost for upload phase (Varying $s$ and $n_l$)', 
                       {'n': 3, 'm': 3, 'ξ': 3})
    
def varying_ξ_and_n_l():
    # Parameters for Upload
    ξ_values = list(range(0, 30, 3))    # From 0 to 30 with step 3
    n_l_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(ξ_values, n_l_values, 'The number of CSPs ($ξ$)'
                       , 'The copy number stored in every CSP ($n_l$)', 
                       'Computation cost for upload phase (Varying $ξ$ and $n_l$)', 
                       {'n': 3, 'm': 3, 's': 3})
    
varying_n_and_m()       # Generates a plot for varying n and m
varying_n_and_s()       # Generates a plot for varying n and s
varying_n_and_ξ()       # Generates a plot for varying n and ξ
varying_n_and_n_l()     # Generates a plot for varying n and n_l
varying_m_and_s()       # Generates a plot for varying m and s
varying_m_and_ξ()       # Generates a plot for varying m and ξ
varying_m_and_n_l()     # Generates a plot for varying m and n_l
varying_s_and_ξ()       # Generates a plot for varying s and ξ
varying_s_and_n_l()     # Generates a plot for varying s and n_l
varying_ξ_and_n_l()     # Generates a plot for varying ξ and n_l
