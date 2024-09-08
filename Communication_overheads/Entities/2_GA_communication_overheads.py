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

def calc_GA_costs(r, u, n, c, m, s, ξ):
    # Pre-calculate common terms
    G = communication_costs['|G|']
    Gt = communication_costs['|GT|']
    Zp = communication_costs['|Zp|']
    sig = communication_costs['|sig|']
    id_size = communication_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = id_size

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = (((2 * r) + (2 * u) + 8) * G) + ((r + 2) * Gt) + ((r + u) * Zp)

    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = ((r + u) * G) + ((r + u) * Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = 0 

    # Our scheme
    our_scheme_cost = id_size + (((n * m) + (8 * ξ) + m + 7) * G) + (((2 * ξ) + 2) * Gt) \
    + (ξ * sig) + (((n * m) + (ξ * n) + (2 * ξ * c) + (14 * ξ) + (2 * m) + s + 14) * Zp)

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
                n=params.get('The block number ($n$)', 3), 
                c=params.get('The number of challenge blocks ($c$)', 3), 
                m=params.get('The copy number ($m$)', 3), 
                s=params.get('The number of sectors in each block ($s$)', 3), 
                ξ=params.get('The number of CSPs ($ξ$)', 3)
            )
            
            # Compute the costs for GA
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

def varying_r_and_u():
    # Parameters for GA
    r_values = list(range(0, 300, 30))  # From 0 to 300 with step 30
    u_values = list(range(0, 300, 30))  # From 0 to 300 with step 30

    varying_parameters(r_values, u_values, 'The number of registered users ($r$)'
                       , 'The number of unrevoked users ($u$)', 
                       'Communication cost for GA (Varying $r$ and $u$)', 
                       {'n': 3, 'c': 3, 'm': 3, 's': 3, 'ξ': 3})

def varying_r_and_n():
    # Parameters for GA
    r_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    n_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(r_values, n_values, 'The number of registered users ($r$)'
                       , 'The block number ($n$)', 
                       'Communication cost for GA (Varying $r$ and $n$)', 
                       {'u': 3, 'c': 3, 'm': 3, 's': 3, 'ξ': 3})
    
def varying_r_and_c():
    # Parameters for GA
    r_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    c_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(r_values, c_values, 'The number of registered users ($r$)'
                       , 'The number of challenge blocks ($c$)', 
                       'Communication cost for GA (Varying $r$ and $c$)', 
                       {'u': 3, 'n': 3, 'm': 3, 's': 3, 'ξ': 3})
    
def varying_r_and_m():
    # Parameters for GA
    r_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    m_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(r_values, m_values, 'The number of registered users ($r$)'
                       , 'The copy number ($m$)', 
                       'Communication cost for GA (Varying $r$ and $m$)', 
                       {'u': 3, 'n': 3, 'c': 3, 's': 3, 'ξ': 3})

def varying_r_and_s():
    # Parameters for GA
    r_values = list(range(0, 500, 50))  # From 0 to 500 with step 50
    s_values = list(range(0, 500, 50))  # From 0 to 500 with step 50

    varying_parameters(r_values, s_values, 'The number of registered users ($r$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Communication cost for GA (Varying $r$ and $s$)', 
                       {'u': 3, 'n': 3, 'c': 3, 'm': 3, 'ξ': 3})
    
def varying_r_and_ξ():
    # Parameters for GA
    r_values = list(range(0, 300, 30))  # From 0 to 300 with step 30
    ξ_values = list(range(0, 300, 30))  # From 0 to 300 with step 30

    varying_parameters(r_values, ξ_values, 'The number of registered users ($r$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for GA (Varying $r$ and $ξ$)', 
                       {'u': 3, 'n': 3, 'c': 3, 'm': 3, 's': 3})

def varying_u_and_n():
    # Parameters for GA
    u_values = list(range(0, 300, 30))  # From 0 to 300 with step 30
    n_values = list(range(0, 300, 30))  # From 0 to 300 with step 30

    varying_parameters(u_values, n_values, 'The number of unrevoked users ($u$)'
                       , 'The block number ($n$)', 
                       'Communication cost for GA (Varying $u$ and $n$)', 
                       {'r': 3, 'c': 3, 'm': 3, 's': 3, 'ξ': 3})
    
def varying_u_and_c():
    # Parameters for GA
    u_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    c_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(u_values, c_values, 'The number of unrevoked users ($u$)'
                       , 'The number of challenge blocks ($c$)', 
                       'Communication cost for GA (Varying $u$ and $c$)', 
                       {'r': 3, 'n': 3, 'm': 3, 's': 3, 'ξ': 3})
    
def varying_u_and_m():
    # Parameters for GA
    u_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    m_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    varying_parameters(u_values, m_values, 'The number of unrevoked users ($u$)'
                       , 'The copy number ($m$)', 
                       'Communication cost for GA (Varying $u$ and $m$)', 
                       {'r': 3, 'n': 3, 'c': 3, 's': 3, 'ξ': 3})
    
def varying_u_and_s():
    # Parameters for GA
    u_values = list(range(0, 500, 50))  # From 0 to 500 with step 50
    s_values = list(range(0, 500, 50))  # From 0 to 500 with step 50

    varying_parameters(u_values, s_values, 'The number of unrevoked users ($u$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Communication cost for GA (Varying $u$ and $s$)', 
                       {'r': 3, 'n': 3, 'c': 3, 'm': 3, 'ξ': 3})

def varying_u_and_ξ():
    # Parameters for GA
    u_values = list(range(0, 300, 30))  # From 0 to 300 with step 30
    ξ_values = list(range(0, 300, 30))  # From 0 to 300 with step 30

    varying_parameters(u_values, ξ_values, 'The number of unrevoked users ($u$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for GA (Varying $u$ and $ξ$)', 
                       {'r': 3, 'n': 3, 'c': 3, 'm': 3, 's': 3})
 
def varying_n_and_c():
    # Parameters for GA
    n_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    c_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(n_values, c_values, 'The block number ($n$)'
                       , 'The number of challenge blocks ($c$)', 
                       'Communication cost for GA (Varying $n$ and $c$)', 
                       {'r': 3, 'u': 3, 'm': 3, 's': 3, 'ξ': 3})

def varying_n_and_m():
    # Parameters for GA
    n_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    m_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(n_values, m_values, 'The block number ($n$)'
                       , 'The copy number ($m$)', 
                       'Communication cost for GA (Varying $n$ and $m$)', 
                       {'r': 3, 'u': 3, 'c': 3, 's': 3, 'ξ': 3})

def varying_n_and_s():
    # Parameters for GA
    n_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    s_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(n_values, s_values, 'The block number ($n$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Communication cost for GA (Varying $n$ and $s$)', 
                       {'r': 3, 'u': 3, 'c': 3, 'm': 3, 'ξ': 3})
        
def varying_n_and_ξ():
    # Parameters for GA
    n_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(n_values, ξ_values, 'The block number ($n$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for GA (Varying $n$ and $ξ$)', 
                       {'r': 3, 'u': 3, 'c': 3, 'm': 3, 's': 3})
    
def varying_c_and_m():
    # Parameters for GA
    c_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    m_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(c_values, m_values, 'The number of challenge blocks ($c$)'
                       , 'The copy number ($m$)', 
                       'Communication cost for GA (Varying $c$ and $m$)', 
                       {'r': 3, 'u': 3, 'n': 3, 's': 3, 'ξ': 3})
    
def varying_c_and_s():
    # Parameters for GA
    c_values = list(range(0, 50, 5))  # From 0 to 50 with step 5
    s_values = list(range(0, 50, 5))  # From 0 to 50 with step 5

    varying_parameters(c_values, s_values, 'The number of challenge blocks ($c$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Communication cost for GA (Varying $c$ and $s$)', 
                       {'r': 3, 'u': 3, 'n': 3, 'm': 3, 'ξ': 3})
    
def varying_c_and_ξ():
    # Parameters for GA
    c_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(c_values, ξ_values, 'The number of challenge blocks ($c$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for GA (Varying $c$ and $ξ$)', 
                       {'r': 3, 'u': 3, 'n': 3, 'm': 3, 's': 3})

def varying_m_and_s():
    # Parameters for GA
    m_values = list(range(0, 30, 3))  # From 0 to 30 with step 3
    s_values = list(range(0, 30, 3))  # From 0 to 30 with step 3

    varying_parameters(m_values, s_values, 'The copy number ($m$)'
                       , 'The number of sectors in each block ($s$)', 
                       'Communication cost for GA (Varying $m$ and $s$)', 
                       {'r': 3, 'u': 3, 'n': 3, 'c': 3, 'ξ': 3})
        
def varying_m_and_ξ():
    # Parameters for GA
    m_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(m_values, ξ_values, 'The copy number ($m$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for GA (Varying $m$ and $ξ$)', 
                       {'r': 3, 'u': 3, 'n': 3, 'c': 3, 's': 3})
    
def varying_s_and_ξ():
    # Parameters for GA
    s_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    varying_parameters(s_values, ξ_values, 'The number of sectors in each block ($s$)'
                       , 'The number of CSPs ($ξ$)', 
                       'Communication cost for GA (Varying $s$ and $ξ$)', 
                       {'r': 3, 'u': 3, 'n': 3, 'c': 3, 'm': 3})
    
varying_r_and_u()       # Generates a plot for varying r and u
varying_r_and_n()       # Generates a plot for varying r and n
varying_r_and_c()       # Generates a plot for varying r and c
varying_r_and_m()       # Generates a plot for varying r and m
varying_r_and_s()       # Generates a plot for varying r and s
varying_r_and_ξ()       # Generates a plot for varying r and ξ
varying_u_and_n()       # Generates a plot for varying u and n
varying_u_and_c()       # Generates a plot for varying u and c
varying_u_and_m()       # Generates a plot for varying u and m
varying_u_and_s()       # Generates a plot for varying u and s
varying_u_and_ξ()       # Generates a plot for varying u and ξ
varying_n_and_c()       # Generates a plot for varying n and c
varying_n_and_m()       # Generates a plot for varying n and m
varying_n_and_s()       # Generates a plot for varying n and s
varying_n_and_ξ()       # Generates a plot for varying n and ξ
varying_c_and_m()       # Generates a plot for varying c and m
varying_c_and_s()       # Generates a plot for varying c and s
varying_c_and_ξ()       # Generates a plot for varying c and ξ
varying_m_and_s()       # Generates a plot for varying m and s
varying_m_and_ξ()       # Generates a plot for varying m and ξ
varying_s_and_ξ()       # Generates a plot for varying s and ξ
