from matplotlib import pyplot as plt
from numpy import delete, transpose, loadtxt, zeros
from os import path
from tqdm import tqdm


def get_sde(folder_path, file_name):
    cluster_ds_data = transpose(loadtxt(open(path.join(folder_path, file_name), 'r')))
    mean_ds_data, mean_ds_sq_data, number_samples = cluster_ds_data[1], cluster_ds_data[2], cluster_ds_data[3]

    limit = 0
    for i in range(1, len(mean_ds_data)):
        if number_samples[i] < samples_threshold:
            limit = i
            break

    return range(1, limit), mean_ds_data[1:limit], mean_ds_sq_data[1:limit]


if __name__ == '__main__':
    results_path = path.join(path.dirname(__file__), "..", "results")
    control_model = "null_stochastic"
    samples_threshold = 10000

    models = []
    model_names = []
    model_params = []
    model_densities = []
    model_datasets = []
    model_variables = []

    # models.append(path.join("tricritical", "q0"))
    # model_names.append("Contact Process")
    # model_datasets.append("paper")
    # model_params.append([0.65, 0.7, 0.72])
    # model_densities.append([0.27, 0.48, 0.54])
    # model_variables.append("p")
    
    # models.append(path.join("tricritical", "q0p5"))
    # model_names.append("TDP (q = 0.5)")
    # model_datasets.append("paper")
    # model_params.append([0.51, 0.535, 0.55])
    # model_densities.append([0.25, 0.45, 0.53])
    # model_variables.append("p")

    # models.append(path.join("scanlon_kalahari"))
    # model_names.append("Scanlon (R = 2)")
    # model_datasets.append("r2")
    # model_params.append([500, 770, 850])
    # model_densities.append([0.26, 0.49, 0.56])
    # model_variables.append("rainfall")

    # models.append(path.join("scanlon_kalahari"))
    # model_names.append("Scanlon (R = 4)")
    # model_datasets.append("r4")
    # model_params.append([500, 770, 850])
    # model_densities.append([0.26, 0.49, 0.56])
    # model_variables.append("rainfall")

    models.append(path.join("scanlon_kalahari"))
    model_names.append("Scanlon (R = 8)")
    model_datasets.append("paper")
    model_params.append([500, 770, 850])
    model_densities.append([0.26, 0.49, 0.56])
    model_variables.append("rainfall")

    # models.append(path.join("tricritical", "q0p25"))
    # model_names.append("TDP (q = 0.25)")
    # model_datasets.append("paper")
    # model_params.append([0.585, 0.62, 0.64])
    # model_densities.append([0.27, 0.45, 0.52])
    # model_variables.append("p")

    # models.append(path.join("tricritical", "q0p75"))
    # model_names.append("TDP (q = 0.75)")
    # model_datasets.append("paper")
    # model_params.append([0.405, 0.41, 0.42])
    # model_densities.append([0.24, 0.38, 0.52])
    # model_variables.append("p")

    title_size = 14
    label_size = 12
    tick_size = 10
    legend_size = 10

    num_rows = len(models)
    num_cols = len(model_params[0])
    plt.subplots(num_rows, num_cols, figsize=(8.27, 8.27 * num_rows / num_cols))
    plt.suptitle("Growth Rate of Clusters", fontsize=title_size)

    for i in tqdm(range(len(models))):
        row = i
        model = models[i]
        model_name = model_names[i]
        model_dataset = model_datasets[i]
        model_param = model_params[i]
        model_density = model_densities[i]
        model_variable = model_variables[i]

        dataset_path = path.join(results_path, model, model_dataset)

        # dynamics plots
        for j in range(len(model_param)):
            file_prefix = str(model_param[j]).replace(".", "p")
            file_name = file_prefix + "_cluster_ds.txt"
            folder_path = path.join(dataset_path, file_prefix)
            cluster_sizes, mean_ds, mean_ds_sq = get_sde(folder_path, file_name)

            null_prefix = str(model_density[j]).replace(".", "p")
            null_file_name = null_prefix + "_cluster_ds.txt"
            null_folder_path = path.join(results_path, control_model, null_prefix)
            null_cluster_sizes, null_mean_ds, null_mean_ds_sq = get_sde(null_folder_path, null_file_name)

            plt.subplot(num_rows, num_cols, row * num_cols + j + 1)

            if row == num_rows - 1:
                plt.xlabel("cluster size (s)", fontsize=label_size)
            if j == 0:
                plt.ylabel("Mean Growth Rate", fontsize=label_size)

            if row == 0 and j == 0:
                plt.plot(cluster_sizes, mean_ds, 'b-', label=f"model")
                plt.plot(null_cluster_sizes, null_mean_ds, '0.8', label=f"null")
            else:
                plt.plot(cluster_sizes, mean_ds, 'b-')
                plt.plot(null_cluster_sizes, null_mean_ds, '0.8')
            plt.axhline(y=0, linestyle="--")

            if j == 0:
                plt.xlim([0, 100])
            elif j == 1:
                plt.xlim([0, 1500])
            elif j == 2:
                plt.xlim([0, 5000])

            # if j == num_cols - 1:
            #     plt.ylabel(model_name, fontsize=label_size, rotation=270, labelpad=15)
            #     ax = plt.gca()
            #     ax.yaxis.set_label_position("right")

            if row != num_rows - 1:
                plt.xticks([])

            if row == 2 and j == 1:
                ax = plt.gca()
                lim = 200
                axins = ax.inset_axes([0.3, 0.2, 0.6, 0.5])
                axins.plot(cluster_sizes[:lim], mean_ds[:lim], 'b-')
                axins.plot(null_cluster_sizes[:lim], null_mean_ds[:lim], '0.8')
                axins.axhline(y=0, linestyle="--")

            plt.title(chr(65 + row) + str(j + 1), loc="left", fontsize=title_size)

            # plt.legend(fontsize=legend_size)
            plt.tight_layout()

    plt.figlegend(loc="upper right", fontsize=legend_size, bbox_to_anchor=(0.99, 0.99))
    plt.savefig("fig3.png", dpi=300)
    plt.show()