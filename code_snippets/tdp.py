

if __name__ == '__main__':
    pass

    # p_values = [0.616, 0.618, 0.62, 0.625, 0.63, 0.64, 0.65, 0.7, 0.72]
    # p_values = [0.566, 0.569, 0.57, 0.575, 0.58, 0.59, 0.62, 0.64]
    # p_values = [0.498, 0.5, 0.502, 0.504, 0.506, 0.508, 0.51, 0.52, 0.53, 0.55]
    # p_values = [0.399, 0.4, 0.401, 0.403, 0.405, 0.41, 0.42]

    # CLUSTER SIZE DISTRIBUTION
    # set_start_method("spawn")
    # num_simulations = cpu_count() - 1
    # p_values = [0.65, 0.7, 0.72, 0.74]
    # q = 0

    # for p in p_values:
    #     print(f"\n---> Simulating p = {p} <---")
    #     tricritical_final(p, q, num_simulations)
    
    # CLUSTER DYNAMICS
    # set_start_method("spawn")
    # num_simulations = cpu_count() - 1
    # p_values = [0.70, 0.71]
    # q = 0.25

    # for p in p_values:
    #     purge_data()
    #     print(f"\n---> Simulating p = {p} <---")
    #     file_string = str(p).replace('.', 'p')
    #     tricritical(p, q, num_simulations, save_series=False, save_cluster=True)
    #     compile_changes("tricritical", range(num_simulations), plot_name=file_string)
    #     plot_changes(file_string)

    # COARSE DYNAMICS
    # set_start_method("spawn")
    # num_simulations = int(cpu_count() / 2)
    # p_values = [0.62, 0.65, 0.7, 0.72, 0.74]
    # q = 0
    # diff_values = [1, 5, 10, 50, 100]

    # for p in p_values:
    #     for diff in diff_values:
    #         tricritical_coarse(p, q, diff, num_simulations)

    # PHASE DIAGRAM
    # set_start_method("spawn")
    # num_simulations = 16
    # h = 0.005
    # p_range = arange(0, 1, h)
    # q_range = arange(0, 1, h)
    # densities = zeros((len(q_range), len(p_range)), dtype=float)
    # output_string = ""

    # for i, q in enumerate(q_range):
    #     print(f"---> Started q = {q:.4f} <---")
    #     for j, p in enumerate(p_range):
    #         print(f"Simulating p = {p:.3f}")
    #         densities[i, j] = tricritical_fast(p, q, num_parallel=num_simulations, save=False)
    #         output_string += f"{p:.4f} {q:.4f} {densities[i, j]:.6f}\n"

    # with open("phase_diagram.txt", "w") as f:
    #     f.write(output_string)

    # plt.title(f"Phase diagram of TDP model")
    # plt.xlabel("p")
    # plt.ylabel("q")
    # plt.imshow(densities, extent=[0, 1, 0, 1], origin="lower")
    # plt.colorbar()
    # plt.savefig("phase_diagram.png")
    # plt.show()


    # PERCOLATION
    # set_start_method("spawn")
    # num_simulations = cpu_count() - 1
    # p_values = arange(0, 1, 0.01)
    # q = 0.8
    # percolation_probablities = zeros(len(p_values), dtype=float)

    # for i, p in enumerate(p_values):
    #     print(f"\n---> Simulating p = {p} <---")
    #     _, percolation_probablities[i] = tricritical_spanning(p, q, num_simulations)

    # plt.title(f"Percolation probability vs birth probability for q = {q:.2f}")
    # plt.xlabel("Birth probability")
    # plt.ylabel("Percolation probability")
    # plt.plot(p_values, percolation_probablities)
    # plt.savefig("percolation_probability.png")
    # plt.show()


    # PERCOLATION DETAILED
    # set_start_method("spawn")
    # num_simulations = 2 * cpu_count() - 1

    # q_values = [0.92]

    # for q in q_values:
    #     if q == 0.0:
    #         p_values = concatenate([arange(0, 0.71, 0.01), arange(0.71, 0.74, 0.0001), arange(0.74, 1, 0.01)])
    #     elif q == 0.25:
    #         p_values = concatenate([arange(0, 0.64, 0.01), arange(0.64, 0.67, 0.0001), arange(0.67, 1, 0.01)])
    #     elif q == 0.5:
    #         p_values = concatenate([arange(0, 0.54, 0.01), arange(0.54, 0.57, 0.0001), arange(0.57, 1, 0.01)])
    #     elif q == 0.75:
    #         p_values = concatenate([arange(0, 0.41, 0.01), arange(0.41, 0.43, 0.0001), arange(0.43, 1, 0.01)])
    #     elif q == 0.92:
    #         p_values = concatenate([arange(0, 0.28, 0.01), arange(0.28, 0.29, 0.00001), arange(0.29, 1, 0.01)])

    #     percolation_probablities = zeros(len(p_values), dtype=float)
    #     avg_densities = zeros(len(p_values), dtype=float)

    #     for i in range(len(p_values)):
    #         avg_densities[i], percolation_probablities[i] = tricritical_spanning(p_values[i], q, num_simulations)

    #     output_string = ""
    #     for i in range(len(p_values)):
    #         output_string += f"{p_values[i]:.6f} {avg_densities[i]:.6f} {percolation_probablities[i]:.6f}\n"

    #     with open(f"{q:.2f}.txt", "w") as f:
    #         f.write(output_string)


    # COMPARE DIFFS
    # purge_data()
    # set_start_method("spawn")
    # num_simulations = int(cpu_count() / 2)

    # p = 0.65
    # q = 0
    # diffs = [1, 5, 10, 50]

    # plt.figure()
    # plt.title("Superimposed difference plots for various delta t")
    # for diff in diffs:
    #     changes = tricritical_coarse(p, q, diff, num_simulations)
    #     plt.semilogy(changes, label=f"diff = {diff} N^2")
    # plt.xlabel("Patch sizes in difference maps")
    # plt.ylabel("Number of patches")
    # plt.legend()
    # plt.savefig("combined_diff_plots.png")
    # plt.show()