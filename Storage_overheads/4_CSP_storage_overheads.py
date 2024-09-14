import matplotlib.pyplot as plt
import numpy as np

# Storage costs for different operations (in bits)
storage_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|GT|'  : 160,        # The size of an element in GT
    '|Zp|'  : 160,        # The size of an element in Zp
    '|sig|' : 160,        # The length of the digital signature
    '|id|'  : 40,         # The size of the user id 
}

def calc_CSP_costs(n, m, s, n_l):
    # Pre-calculate common terms
    G = storage_costs['|G|']
    Gt = storage_costs['|GT|']
    Zp = storage_costs['|Zp|']
    sig = storage_costs['|sig|']
    id_size = storage_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (((2 * n) + 3) * G) + Gt + (((2 * n) + 6) * Zp) 

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = ((n + s + 3) * G) + Gt + ((n + 7) * Zp) 

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = id_size + ((n + 3) * G) + sig + ((n * (1 + (m * s))) * Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = (((n * (n_l + 1)) + 2) * G) + (((n * n_l) + 1) * Zp)
    
    # Our scheme
    our_scheme_cost = (((n * n_l) + 5) * G) + Gt + sig + (((n * (n_l + 1)) + 7) * Zp)

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
            
            mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_CSP_costs(
                n=params.get('The block number ($n$)', 3), 
                m=params.get('The copy number ($m$)', 3), 
                s=params.get('The number of sectors in each block ($s$)', 3), 
                n_l=params.get('The copy number stored in every CSP ($n_l$)', 3)
            )
            
            # Compute the costs for CSP
            mw2023_costs[i, j] = mw2023_cost / 1000             # Convert bits to kilobits
            mw2019_costs[i, j] = mw2019_cost / 1000             # Convert bits to kilobits
            mc2023_costs[i, j] = mc2023_cost / 1000             # Convert bits to kilobits
            mc2022_costs[i, j] = mc2022_cost / 1000             # Convert bits to kilobits
            our_scheme_costs[i, j] = our_scheme_cost / 1000     # Convert bits to kilobits

    # Create meshgrid for x_values and y_values
    X, Y = np.meshgrid(x_values, y_values)
    
    # Plot the surfaces
    create_3d_plot(X, Y, [mw2023_costs.T, mw2019_costs.T, mc2023_costs.T, mc2022_costs.T, our_scheme_costs.T],
                   x_label, y_label, 'Storage cost (kbit)', title,
                   ['[19]', '[16]', '[15]', '[20]', 'Our scheme'])

def varying_n_and_m():
    # Parameters for CSP
    n_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    m_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(n_values, m_values, 'The block number ($n$)'
                       , 'The copy number ($m$)', 
                       'Storage cost for CSP (Varying $n$ and $m$)', 
                       {'s': 3, 'n_l': 3})    
    
def varying_n_and_s():
    # Parameters for CSP
    n_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    s_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(n_values, s_values, 'The block number ($n$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Storage cost for CSP (Varying $n$ and $s$)', 
                       {'m': 3, 'n_l': 3})  
    
def varying_n_and_n_l():
    # Parameters for CSP
    n_values = list(range(0, 50, 5))    # From 0 to 50 with step 5
    n_l_values = list(range(0, 50, 5))  # From 0 to 50 with step 5

    varying_parameters(n_values, n_l_values, 'The block number ($n$)'
                       , 'The copy number stored in every CSP ($n_l$)', 
                       'Storage cost for CSP (Varying $n$ and $n_l$)', 
                       {'m': 3, 's': 3})
    
def varying_m_and_s():
    # Parameters for CSP
    m_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    s_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(m_values, s_values, 'The copy number ($m$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Storage cost for CSP (Varying $m$ and $s$)', 
                       {'n': 3, 'n_l': 3}) 
    
def varying_m_and_n_l():
    # Parameters for CSP
    m_values = list(range(0, 30, 3))    # From 0 to 30 with step 3
    n_l_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(m_values, n_l_values, 'The copy number ($m$)'
                       , 'The copy number stored in every CSP ($n_l$)', 
                       'Storage cost for CSP (Varying $m$ and $n_l$)', 
                       {'n': 3, 's': 3}) 
    
def varying_s_and_n_l():
    # Parameters for CSP
    s_values = list(range(0, 50, 5))    # From 0 to 50 with step 5
    n_l_values = list(range(0, 50, 5))  # From 0 to 50 with step 5

    varying_parameters(s_values, n_l_values, 'The number of sectors in each block ($s$)'
                       , 'The copy number stored in every CSP ($n_l$)', 
                       'Storage cost for CSP (Varying $s$ and $n_l$)', 
                       {'n': 3, 'm': 3}) 
    
varying_n_and_m()       # Generates a plot for varying n and m
varying_n_and_s()       # Generates a plot for varying n and s
varying_n_and_n_l()     # Generates a plot for varying n and n_l
varying_m_and_s()       # Generates a plot for varying m and s
varying_m_and_n_l()     # Generates a plot for varying m and n_l
varying_s_and_n_l()     # Generates a plot for varying s and n_l
