import matplotlib.pyplot as plt
import numpy as np

# Communication costs for different operations (in bits)
communication_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|GT|'  : 160,        # The size of an element in GT
    '|Zp|'  : 160,        # The size of an element in Zp
    '|id|'  : 40,         # The size of the user id 
}

def calc_PKG_costs(r, u):
    # Pre-calculate common terms
    G = communication_costs['|G|']
    Gt = communication_costs['|GT|']
    Zp = communication_costs['|Zp|']
    id_size = communication_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = ((r + u) * id_size) + (((4 * r) + (2 * u) + 5) * G) \
    + (((2 * r) + (2 * u) + 1) * Gt) + (((2 * r) + u) * Zp)

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = 0
    
    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = ((r + 3) * G) + ((r + 1) * Zp)

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = (4 * G)

    # Our scheme
    our_scheme_cost = (((4 * r) + u + 6) * G) + ((r + 1) * Gt) + (((3 * r) + u) * Zp)

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

def varying_r_and_u():
    # Parameters for PKG
    r_values = list(range(0, 100, 10))  # From 0 to 100 with step 10
    u_values = list(range(0, 100, 10))  # From 0 to 100 with step 10

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
            mw2023_costs_PKG[i, j] = mw2023_cost / 1000             # Convert bits to kilobits
            mw2019_costs_PKG[i, j] = mw2019_cost / 1000             # Convert bits to kilobits
            mc2023_costs_PKG[i, j] = mc2023_cost / 1000             # Convert bits to kilobits
            mc2022_costs_PKG[i, j] = mc2022_cost / 1000             # Convert bits to kilobits
            our_scheme_costs_PKG[i, j] = our_scheme_cost / 1000     # Convert bits to kilobits

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
    ax.set_zlabel('Communication cost (kbit)')
    ax.set_title('Communication cost for PKG (Varying $r$ and $u$)')
    ax.legend()
    ax.grid(True)
    plt.show()

varying_r_and_u()       # Generates a plot for varying r and u
