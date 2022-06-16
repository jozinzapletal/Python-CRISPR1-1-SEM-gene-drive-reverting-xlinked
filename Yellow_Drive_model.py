# This module runs the CRISPR one-target location to one-target location using the equations generated and parameters
# set in the input file
#
# Model developed by Josef Zapletal (jozinzapletal@gmail.com)

import pandas as pd
import numpy as np
import math
import time
import Yellow_Drive_Equations


def Yellow_Drive_Progression():

    cols = ['w', 'v', 'u', 'r', 'g', 's', 'ww', 'wv', 'wu', 'wr', 'wg', 'ws', 'vv', 'vu', 'vr', 'vg', 'vs', 'uu', 'ur', 'ug', 'us', 'rr', 'rg', 'rs', 'gg', 'gs', 'ss']
    results_temp = []

    # Reading and assigning values from Excel document
    M = pd.read_excel('Yellow Drive Input Parameters.xlsx')

    sigma = M.iloc[5, 3]
    lamda = M.iloc[6, 3]

    q2 = M.iloc[8, 3]
    q1 = M.iloc[9, 3]
    P2 = M.iloc[10, 3]
    P1 = M.iloc[11, 3]
    delta2 = M.iloc[12, 3]
    delta1 = M.iloc[13, 3]
    epsilon1 = M.iloc[15, 3]
    epsilon2 = M.iloc[14, 3]
    gens = M.iloc[19, 3]
    span = gens


    male_alphas_init = M.iloc[0, 3:-1].values
    male_alphas = [i for i in male_alphas_init if not math.isnan(i)]  # refers to the male alpha values entered
    male_gammas_init = M.iloc[1, 3:-1].values
    male_gammas = [i for i in male_gammas_init if not math.isnan(i)]  # refers to the male gamma values entered

    female_alphas_init = M.iloc[2, 3:-1].values
    female_alphas = [i for i in female_alphas_init if not math.isnan(i)]  # refers to the male alpha values entered
    female_gammas_init = M.iloc[3, 3:-1].values
    female_gammas = [i for i in female_gammas_init if not math.isnan(i)]  # refers to the male gamma values entered

    # Assignment of initial conditions
    g0 = np.array(M.iloc[22:49, 3].values)

    # Assignment of initial fitness costs
    fitCost = np.array(M.iloc[22:49, 9].values)

    # Assignment of initial fitness costs
    mateCost = np.array(M.iloc[22:49, 14].values)

    # RUN THE MODEL

    # indexes are day
    next_Generation = [[0 for x in range(len(cols))] for y in range(span)]
    total_population_by_genotype = [[0 for x in range(len(cols))] for y in range(span)]

    for alpha1 in male_alphas:
        for alpha2 in female_alphas:
            for gamma1 in male_gammas:
                for gamma2 in female_gammas:

                    beta1 = 1 - (alpha1 + gamma1)
                    beta2 = 1 - (alpha2 + gamma2)

                    # loop through each time step
                    start_time = time.time()
                    for T in range(span):
                        if T == 0:
                            proportionPop = convert_to_proportion(g0)
                            next_Generation[0]
                            next_Generation[0] = Yellow_Drive_Equations.Yellow_Drive_Rates(proportionPop, sigma, lamda, delta1, delta2, fitCost, mateCost,
                                                 q1, q2, P1, P2, alpha1, alpha2, beta1, beta2, gamma1, gamma2, epsilon1, epsilon2)
                        elif 0 < T:
                            proportionPop = convert_to_proportion(next_Generation[T-1])
                            next_Generation[T] = Yellow_Drive_Equations.Yellow_Drive_Rates(proportionPop, sigma, lamda, delta1, delta2, fitCost, mateCost,
                                                 q1, q2, P1, P2, alpha1, alpha2, beta1, beta2, gamma1, gamma2, epsilon1, epsilon2)

                        # Store the values of the model into a list
                        total_population_by_genotype[T] = next_Generation[T]
                        total_population = sum(total_population_by_genotype[T])

                        male_w_count = total_population_by_genotype[T][0]
                        male_v_count = total_population_by_genotype[T][1]
                        male_u_count = total_population_by_genotype[T][2]
                        male_r_count = total_population_by_genotype[T][3]
                        male_g_count = total_population_by_genotype[T][4]
                        male_s_count = total_population_by_genotype[T][5]

                        female_w_count = 2*total_population_by_genotype[T][6] + sum(total_population_by_genotype[T][7:12])
                        female_v_count = total_population_by_genotype[T][7] + 2*total_population_by_genotype[T][12] + sum(total_population_by_genotype[T][13:17])
                        female_u_count = total_population_by_genotype[T][8] + total_population_by_genotype[T][13] + 2*total_population_by_genotype[T][17] + sum(total_population_by_genotype[T][18:21])
                        female_r_count = total_population_by_genotype[T][9] + total_population_by_genotype[T][14] + total_population_by_genotype[T][18] + 2*total_population_by_genotype[T][21] + sum(total_population_by_genotype[T][22:24])
                        female_g_count = total_population_by_genotype[T][10] + total_population_by_genotype[T][15] + total_population_by_genotype[T][19] + total_population_by_genotype[T][22] + 2*total_population_by_genotype[T][24] + total_population_by_genotype[T][25]
                        female_s_count = total_population_by_genotype[T][11] + total_population_by_genotype[T][16] + total_population_by_genotype[T][20] + total_population_by_genotype[T][23] + total_population_by_genotype[T][25] + 2*total_population_by_genotype[T][26]

                        w_count = (male_w_count + female_w_count) / (1.5*total_population)
                        v_count = (male_v_count + female_v_count) / (1.5*total_population)
                        u_count = (male_u_count + female_u_count) / (1.5*total_population)
                        r_count = (male_r_count + female_r_count) / (1.5*total_population)
                        g_count = (male_g_count + female_g_count) / (1.5*total_population)
                        s_count = (male_s_count + female_s_count) / (1.5*total_population)

                        output_line = [alpha1, gamma1, alpha2, gamma2, T, w_count, v_count, u_count, r_count, g_count, s_count, total_population]
                        results_temp.append(output_line)

                    print('Run complete in', time.time() - start_time, 'seconds.')

    # START HERE TO OUTPUT THE DATA
    cols = ['male_alpha', 'male_gamma', 'female_alpha', 'female_gamma', 'time', 'w', 'v', 'u', 'r', 'g', 's', 'total_population']
    results_df = pd.DataFrame(results_temp, columns=cols)

    results_df.to_excel('Yellow_Drive Results.xlsx', index=False)


# converts the list of genotype counts to a proportion by
def convert_to_proportion(K):

    K = [float(i) for i in K]

    males = K[:6]
    females = K[6:]

    male_total = sum(males)

    if male_total != 0:
        males = [m / male_total for m in males]

    output_list = []
    output_list.extend(males)
    output_list.extend(females)

    return output_list


# generates a list of genotypes based on a list of alleles
def generate_allele_combinations(allele_list):

    # create all the combinations of alleles possible
    allele_1_sequence = []
    allele_2_sequence = []

    allele_dels = allele_list.copy()
    for allele in allele_list:
        for remaining_allele in allele_dels:
            allele_1_sequence.append(allele)
        allele_dels.remove(allele)

    allele_dels = allele_list.copy()
    for allele in allele_list:
        for remaining_allele in allele_dels:
            allele_2_sequence.append(remaining_allele)
        allele_dels.remove(allele)

    # combine the two alleles together into a single genotype
    two_allele_combinations = [i + j for i, j in zip(allele_1_sequence, allele_2_sequence)]

    return two_allele_combinations