import matplotlib.pyplot as plt
import numpy as np

# Communication costs for different operations (in bits)
communication_costs = {
    '|G|'   : 160,        # The size of an element in G 
    '|GT|'  : 160,        # The size of an element in GT
    '|Zp|'  : 160,        # The size of an element in Zp
    '|id|'  : 40,         # The size of the user id 
}

def calc_setup_costs(s, ξ):
    # Pre-calculate common terms
    G = communication_costs['|G|']
    Gt = communication_costs['|GT|']
    Zp = communication_costs['|Zp|']
    id_size = communication_costs['|id|']

    # MW2023: Multi-writer 2023 [19]
    mw2023_cost = (5 * G) + Gt

    # MW2019: Multi-writer 2019 [16]
    mw2019_cost = (4 * G) + Gt
    
    # MC2023: Multi-copy 2023 [15]
    mc2023_cost = (3 * G) + Zp

    # MC2022: Multi-copy 2022 [20]
    mc2022_cost = id_size + ((s + ξ + 9) * G)

    # Our scheme
    our_scheme_cost = (6 * G) + Gt

    return mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost

def varying_s_and_ξ():
    # Parameters for setup
    s_values = list(range(0, 10, 1))  # From 0 to 10 with step 1
    ξ_values = list(range(0, 10, 1))  # From 0 to 10 with step 1

    # Prepare 2D arrays to store costs
    mw2023_costs_setup = np.zeros((len(s_values), len(ξ_values)))
    mw2019_costs_setup = np.zeros((len(s_values), len(ξ_values)))
    mc2023_costs_setup = np.zeros((len(s_values), len(ξ_values)))
    mc2022_costs_setup = np.zeros((len(s_values), len(ξ_values)))
    our_scheme_costs_setup = np.zeros((len(s_values), len(ξ_values)))

    # Compute the costs for setup phase
    for i, s in enumerate(s_values):
        for j, ξ in enumerate(ξ_values):
            mw2023_cost, mw2019_cost, mc2023_cost, mc2022_cost, our_scheme_cost = calc_setup_costs(s, ξ)
            mw2023_costs_setup[i, j] = mw2023_cost / 1000             # Convert bits to kilobits
            mw2019_costs_setup[i, j] = mw2019_cost / 1000             # Convert bits to kilobits
            mc2023_costs_setup[i, j] = mc2023_cost / 1000             # Convert bits to kilobits
            mc2022_costs_setup[i, j] = mc2022_cost / 1000             # Convert bits to kilobits
            our_scheme_costs_setup[i, j] = our_scheme_cost / 1000     # Convert bits to kilobits

    # Create the 3D plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Create meshgrid for s_values and ξ_values
    S, ζ = np.meshgrid(s_values, ξ_values)

    # Plot the surfaces
    ax.plot_surface(S, ζ, mw2023_costs_setup.T, label='[19]', color='#1f77b4', alpha=0.7)               #color: blue (#1f77b4)
    ax.plot_surface(S, ζ, mw2019_costs_setup.T, label='[16]', color='#ff8923', alpha=0.7)               #color: orange (#ff8923)
    ax.plot_surface(S, ζ, mc2023_costs_setup.T, label='[15]', color='#2ca02c', alpha=0.7)               #color: green (#2ca02c)
    ax.plot_surface(S, ζ, mc2022_costs_setup.T, label='[20]', color='#d62728', alpha=0.7)               #color: red (#d62728)
    ax.plot_surface(S, ζ, our_scheme_costs_setup.T, label='Our scheme', color='#9467bd', alpha=0.7)     #color: purple (#9467bd)

    ax.set_xlabel('The number of sectors in each block ($s$)')
    ax.set_ylabel('The number of CSPs ($ξ$)')
    ax.set_zlabel('Communication cost (kbit)')
    ax.set_title('Communication cost for setup phase (Varying $s$ and $ξ$)')
    ax.legend()
    ax.grid(True)
    plt.show()

varying_s_and_ξ()
