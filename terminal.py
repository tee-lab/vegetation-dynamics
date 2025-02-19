"""
This script imports all models and analysis scripts
We used this to run jobs on the computing cluster
Code snippets for carrying out analysis of all models are included in the code_snippets folder

IMPORTANT: set_spawn_method("spawn") is required for multiprocessing to work on Linux
"""


# libraries
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from math import floor
from multiprocessing import cpu_count, Pool, set_start_method
from numpy import abs, arange, array, concatenate, zeros
from os import makedirs, path
from skimage.measure import label
from tqdm import tqdm
# models
from models.contact_spatial.in_place_processing import contact_spatial
from models.null_static.spanning_cluster import null_static as null_static_spanning
from models.null_stochastic.in_place_processing import null_stochastic
from models.null_stochastic.spanning_cluster import null_stochastic as null_stochastic_spanning
from models.scanlon_kalahari.in_place_processing import scanlon_kalahari
from models.scanlon_kalahari.spanning_cluster import scanlon_kalahari as scanlon_kalahari_spanning
from models.tricritical.coarse_dynamics import tricritical as tricritical_coarse
from models.tricritical.dumper import tricritical as tricritical_fast
from models.tricritical.final_lattice import tricritical as tricritical_final
from models.tricritical.in_place_processing import tricritical
from models.tricritical.spanning_cluster import tricritical as tricritical_spanning
# analysis
from compile_changes import compile_changes
from plot_changes import plot_changes
from purge_data import purge_data
from utils import load_automaton_data


if __name__ == '__main__':
    set_start_method("spawn")
    num_simulations = 50
    p_values = [0.55]
    q = 0.5

    for p in p_values:
        purge_data()
        print(f"\n---> Simulating p = {p} <---")
        file_string = str(p).replace('.', 'p')
        tricritical(p, q, num_simulations, save_series=False, save_cluster=True)
        compile_changes("tricritical", range(num_simulations), plot_name=file_string)
        plot_changes(file_string)


    rainfall_values = [500, 770, 850]

    for rainfall in rainfall_values:
        purge_data()
        print(f"\n---> Simulating rainfall = {rainfall} <---")
        file_string = str(rainfall).replace('.', 'p')
        scanlon_kalahari(rainfall, num_simulations, save_series=False, save_cluster=True)
        compile_changes("scanlon_kalahari", range(num_simulations), plot_name=file_string)
        plot_changes(file_string)