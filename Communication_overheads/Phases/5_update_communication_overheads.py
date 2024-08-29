import matplotlib.pyplot as plt
import numpy as np

# Communication costs for different operations (in bits)
communication_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|GT|'  : 160,        # The size of an element in GT
    '|Zp|'  : 160,        # The size of an element in Zp
    '|sig|' : 160,        # The length of the digital signature
    '|id|'  : 40,         # The size of the user id  
}

def calc_update_costs(n, m, s, ξ):
    # Pre-calculate common terms
    G = communication_costs['|G|']
    Gt = communication_costs['|GT|']
    Zp = communication_costs['|Zp|']
    sig = communication_costs['|sig|']
    id_size = communication_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (((4 * n) + 6) * G) + (2 * Gt) + (((2 * n) + 12) * Zp)

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = (((2 * s) + 7) * G) + (2 * Gt) + (15 * Zp) 

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = (ξ * id_size) + (4 * ξ * G) + (ξ * sig) + (ξ * m * Zp) 

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = ((m + 1) * G) + (m * Zp) 

    # Our scheme
    our_scheme_cost = (((3 * ξ) + (2 * m) + 6) * G) + ((ξ + 2) * Gt) \
    + (((7 * ξ) + (2 * m) + 14) * Zp)

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
            
            mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_update_costs(
                n=params.get('The block number ($n$)', 3), 
                m=params.get('The copy number ($m$)', 3), 
                s=params.get('The number of sectors in each block ($s$)', 3), 
                ξ=params.get('The number of CSPs ($ξ$)', 3)
            )
            
            # Compute the costs for update phase
            mw2023_costs[i, j] = mw2023_cost / 1000             # Convert bits to kilobits
            mw2019_costs[i, j] = mw2019_cost / 1000             # Convert bits to kilobits
            mc2023_costs[i, j] = mc2023_cost / 1000             # Convert bits to kilobits
            mc2022_costs[i, j] = mc2022_cost / 1000             # Convert bits to kilobits
            our_scheme_costs[i, j] = our_scheme_cost / 1000     # Convert bits to kilobits

    # Create meshgrid for x_values and y_values
    X, Y = np.meshgrid(x_values, y_values)
    
    # Plot the surfaces
    create_3d_plot(X, Y, [mw2023_costs.T, mw2019_costs.T, mc2023_costs.T, mc2022_costs.T, our_scheme_costs.T],
                   x_label, y_label, 'Communication cost (kbit)', title,
                   ['[19]', '[16]', '[15]', '[20]', 'Our scheme'])

def varying_n_and_m():
    # Parameters for update
    n_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    m_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(n_values, m_values, 'The block number ($n$)'
                       , 'The copy number ($m$)', 
                       'Communication cost for update phase (Varying $n$ and $m$)', 
                       {'s': 3, 'ξ': 3})

def varying_n_and_s():
    # Parameters for update
    n_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    s_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(n_values, s_values, 'The block number ($n$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Communication cost for update phase (Varying $n$ and $s$)', 
                       {'m': 3, 'ξ': 3})

def varying_n_and_ξ():
    # Parameters for update
    n_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    ξ_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(n_values, ξ_values, 'The block number ($n$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for update phase (Varying $n$ and $ξ$)', 
                       {'m': 3, 's': 3})

def varying_m_and_s():
    # Parameters for update
    m_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    s_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(m_values, s_values, 'The copy number ($m$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Communication cost for update phase (Varying $m$ and $s$)', 
                       {'n': 3, 'ξ': 3})

def varying_m_and_ξ():
    # Parameters for update
    m_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    ξ_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(m_values, ξ_values, 'The copy number ($m$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for update phase (Varying $m$ and $ξ$)', 
                       {'n': 3, 's': 3})

def varying_s_and_ξ():
    # Parameters for update
    s_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    ξ_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    
    varying_parameters(s_values, ξ_values, 'The number of sectors in each block ($s$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for update phase (Varying $s$ and $ξ$)', 
                       {'n': 3, 'm': 3})

varying_n_and_m()   # Generates a plot for varying n and m
varying_n_and_s()   # Generates a plot for varying n and s
varying_n_and_ξ()   # Generates a plot for varying n and ξ
varying_m_and_s()   # Generates a plot for varying m and s
varying_m_and_ξ()   # Generates a plot for varying m and ξ
varying_s_and_ξ()   # Generates a plot for varying s and ξ
