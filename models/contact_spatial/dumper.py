from concurrent.futures import ThreadPoolExecutor
from numba import njit
from numpy import array, copy, sum
from numpy.random import randint
from pickle import dump
from random import random

import os


@njit(nogil=True, fastmath=True)
def update(lattice, birth_probability):
    for _ in range(0.1 * length * length):
        i, j = get_random_site(lattice)

        if i == -1 and j == -1:
            # no active sites
            return
        else:
            if random() < birth_probability:
                # birth
                new_i, new_j = get_random_neighbour(i, j)
                lattice[new_i, new_j] = 1
            else:
                # death
                lattice[i, j] = 0


@njit(nogil=True, fastmath=True)
def get_random_site(lattice):
    num_active = sum(lattice)

    if num_active == 0:
        return -1, -1
    elif num_active == 1:
        for i in range(length):
            for j in range(length):
                if lattice[i, j] == 1:
                    return i, j
    else:
        while True:
            i = randint(0, length)
            j = randint(0, length)
            if lattice[i, j] == 1:
                return i, j


@njit(nogil=True, fastmath=True)
def get_random_neighbour(i, j):
    neighbour = randint(0, 4)
    # periodic boundary conditon
    if neighbour == 0:
        return (i + 1) % length, j
    elif neighbour == 1:
        return (i - 1 + length) % length, j
    elif neighbour == 2:
        return i, (j + 1) % length
    elif neighbour == 3:
        return i, (j - 1 + length) % length


def simulate(simulation_index):
    lattice = randint(0, 2, (length, length))
    time_series = [copy(lattice)]

    if simulation_index == 0:
        print("Compiling functions...")

    for i in range(time):
        update(lattice, birth_probability)
        time_series.append(copy(lattice))

        if simulation_index == 0:
            print(f"{i * 100 / time} %", end="\r")

    return time_series


def save_automaton_data(time_series):
    """ Saves the entire simulation data in a pickle file, in the same folder """
    current_path = os.path.dirname(__file__)
    files_list = os.listdir(current_path)

    num_automaton_simulations = 0
    for file_name in files_list:
        if file_name.startswith("simulation_") and file_name.endswith(".pkl"):
            num_automaton_simulations += 1

    file_name = 'simulation_{}.pkl'.format(num_automaton_simulations)
    save_path = os.path.join(current_path, file_name)
    info_string = f"Contact Process with birth probability = {birth_probability}\n"

    automaton_data = {}
    automaton_data["time_series"] = array(time_series, dtype=bool)
    automaton_data["info"] = info_string
    dump(automaton_data, open(save_path, 'wb'))

    info_path = os.path.join(current_path, "info.txt")
    with open(info_path, 'a') as info_file:
        info_file.write(info_string)


def contact_spatial(p = 0.5, num_parallel = 10, save = False):
    # model parameters
    global length, time, birth_probability
    
    length = 100
    time = 100
    birth_probability = p

    print(f"Simulating {num_parallel} automata in parallel ...")
    with ThreadPoolExecutor(num_parallel) as pool:
        time_series_records = list(pool.map(simulate, range(num_parallel)))

    if save:
        print("Saving data...")
        for time_series in time_series_records:
            save_automaton_data(time_series)

    avg_final_density = 0
    for time_series in time_series_records:
        avg_final_density += (sum(time_series[-1]) / (length * length))
    avg_final_density /= num_parallel

    return avg_final_density


if __name__ == '__main__':
    print(contact_spatial(0.75, 1, True))