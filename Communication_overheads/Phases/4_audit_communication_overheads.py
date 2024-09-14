import matplotlib.pyplot as plt
import numpy as np

# Communication costs for different operations (in bits)
communication_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|Zp|'  : 160,        # The size of an element in Zp
    '|sig|' : 160,        # The length of the digital signature
    '|id|'  : 40,         # The size of the user id 
}

def calc_audit_costs(c, m, s, ξ):
    # Pre-calculate common terms
    G = communication_costs['|G|']
    Zp = communication_costs['|Zp|']
    sig = communication_costs['|sig|']
    id_size = communication_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (c * G) + (((2 * c) + s) * Zp)

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = (c * G) + ((c + s) * Zp)

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = id_size + (4 * G) + sig + (((m * s) + c + (2 * ξ)) * Zp) 

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = (((c * ξ) + ξ + c + 3) * G) + (((3 * ξ) + (2 * s) + 3) * Zp) 

    # Our scheme
    our_scheme_cost = (2 * G) + (((2 * ξ * c) + (2 * c) + (2 * s) + (2 * m)) * Zp)

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
            
            mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_audit_costs(
                c=params.get('The number of challenge blocks ($c$)', 3), 
                m=params.get('The copy number ($m$)', 3), 
                s=params.get('The number of sectors in each block ($s$)', 3), 
                ξ=params.get('The number of CSPs ($ξ$)', 3)
            )
            
            # Compute the costs for audit phase
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

def varying_c_and_m():
    # Parameters for audit
    c_values = list(range(0, 50, 5))  # From 0 to 50 with step 5
    m_values = list(range(0, 50, 5))  # From 0 to 50 with step 5

    varying_parameters(c_values, m_values, 'The number of challenge blocks ($c$)'
                       , 'The copy number ($m$)', 
                       'Communication cost for audit phase (Varying $c$ and $m$)', 
                       {'s': 3, 'ξ': 3})

def varying_c_and_s():
    # Parameters for audit
    c_values = list(range(0, 50, 5))  # From 0 to 50 with step 5
    s_values = list(range(0, 50, 5))  # From 0 to 50 with step 5

    varying_parameters(c_values, s_values, 'The number of challenge blocks ($c$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Communication cost for audit phase (Varying $c$ and $s$)', 
                       {'m': 3, 'ξ': 3})

def varying_c_and_ξ():
    # Parameters for audit
    c_values = list(range(0, 10, 1))   # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))   # From 0 to 10 with step 1

    varying_parameters(c_values, ξ_values, 'The number of challenge blocks ($c$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for audit phase (Varying $c$ and $ξ$)', 
                       {'m': 3, 's': 3})

def varying_m_and_s():
    # Parameters for audit
    m_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    s_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(m_values, s_values, 'The copy number ($m$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Communication cost for audit phase (Varying $m$ and $s$)', 
                       {'c': 3, 'ξ': 3})

def varying_m_and_ξ():
    # Parameters for audit
    m_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(m_values, ξ_values, 'The copy number ($m$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for audit phase (Varying $m$ and $ξ$)', 
                       {'c': 3, 's': 3})

def varying_s_and_ξ():
    # Parameters for audit
    s_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    ξ_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    
    varying_parameters(s_values, ξ_values, 'The number of sectors in each block ($s$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for audit phase (Varying $s$ and $ξ$)', 
                       {'c': 3, 'm': 3})

varying_c_and_m()   # Generates a plot for varying c and m
varying_c_and_s()   # Generates a plot for varying c and s
varying_c_and_ξ()   # Generates a plot for varying c and ξ
varying_m_and_s()   # Generates a plot for varying m and s
varying_m_and_ξ()   # Generates a plot for varying m and ξ
varying_s_and_ξ()   # Generates a plot for varying s and ξ
