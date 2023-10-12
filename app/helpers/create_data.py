import names
import pandas as pd
import random

def generate_dummy_students_data(rows):
    column_names = ['ID', 'Name', 'Score']

    dummy_data = [[f'{random.randint(222,999)}', names.get_full_name(), round(random.random() * 10, 2)] for i in range(rows)]

    dummy_df = pd.DataFrame(dummy_data, columns=column_names)
    dummy_df.to_csv('../data/students_dum_30.csv', index=False, sep=',', mode='w')

generate_dummy_students_data(30)