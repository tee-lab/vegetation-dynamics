from numpy import delete, loadtxt, transpose, zeros
from matplotlib import pyplot as plt
from tqdm import tqdm
from os import path


def get_tricritical_phase_diagram(phase_diagram_path, q_value):
    file_path = path.join(phase_diagram_path, "phase_diagram.txt")
    phase_diagram_data = transpose(loadtxt(open(file_path, 'r')))

    p, q, value = phase_diagram_data[0], phase_diagram_data[1], phase_diagram_data[2]
    p_values = []
    densities = []

    for i in range(len(p)):
        if q[i] == q_value:
            p_values.append(p[i])
            densities.append(value[i])

    return p_values, densities


def get_cluster_distribution(folder, file_name):
    file_path = path.join(data_path, folder, file_name)
    cluster_distribution_data = transpose(loadtxt(open(file_path, 'r')))
    cluster_sizes, num = cluster_distribution_data[0][1:], cluster_distribution_data[1][1:]

    inverse_cdf = zeros(len(num))
    for i in range(len(num)):
        inverse_cdf[i] = sum(num[i:])
    inverse_cdf = inverse_cdf / sum(num)

    remove_indices = []
    for i in range(len(cluster_sizes) - 1):
        if inverse_cdf[i] == inverse_cdf[i + 1]:
            remove_indices.append(i)

    cluster_sizes = delete(cluster_sizes, remove_indices)
    inverse_cdf = delete(inverse_cdf, remove_indices)

    return cluster_sizes, inverse_cdf


if __name__ == '__main__':
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    dataset = "100x100"

    # q = 0
    # p_values = [0.72, 0.69, 0.66, 0.63]
    # critical_threshold = 0.62
    # percolation_threshold = 0.72
    # percolation_density = 0.54

    # q = 0.25
    # p_values = [0.65, 0.62, 0.6, 0.58]
    # critical_threshold = 0.57
    # percolation_threshold = 0.65
    # percolation_density = 0.535

    q = 0.5
    p_values = [0.55, 0.53, 0.52, 0.51]
    critical_threshold = 0.5
    percolation_threshold = 0.55
    percolation_density = 0.53

    subfolder = "q" + str(q).replace('.', 'p')
    phase_diagram_path = path.join(results_path, model)
    data_path = path.join(phase_diagram_path, subfolder, dataset)

    num_cols = len(p_values)
    plt.subplots(2, num_cols, figsize=(20, 11))

    for i in tqdm(range(len(p_values))):
        col = i + 1
        p = p_values[i]
        folder_name= str(p).replace('.', 'p')

        row = 0
        birth_prob, densities = get_tricritical_phase_diagram(phase_diagram_path, q)
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title(f"Phase diagram, p = {p}", fontsize=14)
        plt.xlabel("p", fontsize=12)

        if col == 1:
            plt.ylabel("density", fontsize=12)
        else:
            plt.yticks([])
        plt.plot(birth_prob, densities, label="steady state density")
        plt.plot(percolation_threshold, percolation_density, 'x', label="percolation threshold")
        plt.plot(critical_threshold, 0, 'x', label="critical threshold")
        plt.legend()

        plt.plot(p, densities[birth_prob.index(p)], 'o', label="current point")
        plt.legend()

        row = 1
        file_name = f"{folder_name}_cluster_distribution.txt"
        cluster_sizes, inverse_cdf = get_cluster_distribution(folder_name, file_name)
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title("Cluster size distribution (log-log)", fontsize=14)
        plt.xlabel("s", fontsize=12)

        if col == 1:
            plt.ylabel("P(S > s)", fontsize=12)
        plt.loglog(cluster_sizes, inverse_cdf, 'o')

    plt.savefig(f'q{str(q).replace(".", "p")}_ews1.png', bbox_inches='tight')
    plt.show()