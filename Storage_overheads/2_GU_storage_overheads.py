import matplotlib.pyplot as plt
import numpy as np

# Storage costs for different operations (in bits)
storage_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|GT|'  : 160,        # The size of an element in GT
    '|Zp|'  : 160,        # The size of an element in Zp
    '|id|'  : 40,         # The size of the user id 
}

def calc_GU_costs(r, s):
    # Pre-calculate common terms
    G = storage_costs['|G|']
    Gt = storage_costs['|GT|']
    Zp = storage_costs['|Zp|']
    id_size = storage_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = id_size + (3 * G) + Gt + (2 * Zp) 

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = (r * id_size) + (2 * G) + (r * Gt) + Zp
    
    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = id_size + (3 * G) + (3 * Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = G + ((s + 1) * Zp)

    # Our scheme
    our_scheme_cost = id_size + (4 * G) + Gt + ((s + 4) * Zp)

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

def varying_r_and_s():
    # Parameters for GU
    r_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    s_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

    # Prepare 2D arrays to store costs
    mw2023_costs_GU = np.zeros((len(r_values), len(s_values)))
    mw2019_costs_GU = np.zeros((len(r_values), len(s_values)))
    mc2023_costs_GU = np.zeros((len(r_values), len(s_values)))
    mc2022_costs_GU = np.zeros((len(r_values), len(s_values)))
    our_scheme_costs_GU = np.zeros((len(r_values), len(s_values)))

    # Compute the costs for GU 
    for i, r in enumerate(r_values):
        for j, s in enumerate(s_values):
            mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_GU_costs(r, s)
            mw2023_costs_GU[i, j] = mw2023_cost / 1000             # Convert bits to kilobits
            mw2019_costs_GU[i, j] = mw2019_cost / 1000             # Convert bits to kilobits
            mc2023_costs_GU[i, j] = mc2023_cost / 1000             # Convert bits to kilobits
            mc2022_costs_GU[i, j] = mc2022_cost / 1000             # Convert bits to kilobits
            our_scheme_costs_GU[i, j] = our_scheme_cost / 1000     # Convert bits to kilobits

    # Create the 3D plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Create meshgrid for r_values and s_values
    R, S = np.meshgrid(r_values, s_values)

    # Plot the surfaces
    ax.plot_surface(R, S, mw2023_costs_GU.T, label='[19]', color='#1f77b4', alpha=0.7)
    ax.plot_surface(R, S, mw2019_costs_GU.T, label='[16]', color='#ff8923', alpha=0.7)
    ax.plot_surface(R, S, mc2023_costs_GU.T, label='[15]', color='#2ca02c', alpha=0.7)
    ax.plot_surface(R, S, mc2022_costs_GU.T, label='[20]', color='#d62728', alpha=0.7)
    ax.plot_surface(R, S, our_scheme_costs_GU.T, label='Our scheme', color='#9467bd', alpha=0.7)

    ax.set_xlabel('The number of registered users ($r$)')
    ax.set_ylabel('The number of sectors in each block ($s$)')
    ax.set_zlabel('Storage cost (kbit)')
    ax.set_title('Storage cost for GU (Varying $r$ and $s$)')
    ax.legend()
    ax.grid(True)
    plt.show()

varying_r_and_s()       # Generates a plot for varying r and s
