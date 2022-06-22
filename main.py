# My modules
from modules.db_connector import *
from modules.model_tools import *
# External modules
import time
from os import listdir

if __name__ == '__main__':

    # DB connection strings
    #libpq_conn = "dbname=secret user=secret password=secret host=00.00.0.000 port=0000"
    #sql_alchemy_conn = 'postgresql+psycopg2://secret:secret@00.00.0.000/secret'

    # Clear the db tables for testing
    '''execute_sql_query(libpq_conn, "DELETE FROM at_python.out_field_matrix")
    execute_sql_query(libpq_conn, "DELETE FROM at_python.out_mu_fert")'''

    ################################################# Testing ##########################################################
    start_time = time.time()
    #in_data_chain, in_fert_mm, in_prod_fert = get_input_data(libpq_conn) # Get data for online version
    in_prod_fert, in_data_chain, in_fert_mm = [pd.read_csv('test_data' + '/' + file_name) for file_name in listdir('test_data')]
    mart_1, mart_2 = find_optimal_variants(in_data_chain, in_fert_mm, in_prod_fert)
    #upload_market(mart_1, sql_alchemy_conn, 'at_python', 'out_field_matrix') # Upload data for online version
    #upload_market(mart_2, sql_alchemy_conn, 'at_python', 'out_mu_fert') # Upload data for online version

    print("Whole program execution time: %s seconds" % (time.time() - start_time))
    print('\nMart 1:')
    print(mart_1.head(5).drop(['item_id', 'holding', 'farm'], axis=1)[['field','year','harvarea','product','plan_yield',
                                                                       'p_norm','k_norm', 'p_deposit','k_deposit',
                                                                       'cost_fertilizer_total','cost_var_total',
                                                                       'variable_costs','gross_margin', 'crop_price',
                                                                       'revenue_crop']].to_string(index=False))
    print('\nMart 2:')
    print(mart_2.head(5).drop(['item_id','holding','farm'],axis=1).to_string(index=False))


    '''print(mart_1.head(10).drop(['item_id', 'holding', 'farm'], axis=1).columns)
    print(mart_1[['field', 'year', 'harvarea', 'product', 'plan_yield', 'p_norm',
       'k_norm',  'p_deposit', 'k_deposit', 'cost_var_total',
       'cost_fertilizer_total', 'variable_costs','gross_margin', 'crop_price', 'revenue_crop']])'''
