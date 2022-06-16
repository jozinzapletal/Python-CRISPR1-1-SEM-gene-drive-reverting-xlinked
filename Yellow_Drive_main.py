# This module will execute the model and generate the associated plots
# Developed by Josef Zapletal (jozinzapletal@gmail.com)

import os.path
import Yellow_Drive_Equation_Generation
from os import path

from Allele_Plots import generate_plots

file_name = 'Yellow_Drive_Equations.py'
if path.exists(file_name):
    pass
else:
    print('Yellow_Drive_Equations.py not found. Generating equations...')
    Yellow_Drive_Equation_Generation.eq_gen()
    print('Running model...')

from Yellow_Drive_model import Yellow_Drive_Progression

Yellow_Drive_Progression()
generate_plots()
