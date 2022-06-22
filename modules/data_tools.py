import pandas as pd

def get_fert_prod_params(in_fert_mm, in_prod_fert, option_data):
  avail_combos = in_prod_fert[(in_prod_fert['product_nm'] == option_data['product']) & (in_prod_fert['is_avail'] == 1)][['fert_nm','min_fert_rate', 'max_fert_rate']]
  combo_data = pd.merge(avail_combos, in_fert_mm[in_fert_mm['fert_nm'].isin(list(avail_combos['fert_nm']))], on="fert_nm")
  return {
    'fert_names': list(combo_data['fert_nm']),
    'p_contents': combo_data['p_content'].to_numpy(),
    'k_contents': combo_data['k_content'].to_numpy(),
    'fert_costs': combo_data['fert_cost'].to_numpy(),
    'min_fert_rates': combo_data['min_fert_rate'].to_numpy(),
    'max_fert_rates': combo_data['max_fert_rate'].to_numpy(),
    'k_norm': option_data['k_norm'],
    'p_norm': option_data['p_norm']
  }

def make_data_marts(optim_output: pd.DataFrame):
  optim_output['item_id'] = optim_output.index
  mart_1_cols = list(optim_output.columns)
  mart_1_cols.remove('cost_var')
  mart_1_cols.remove('fert')
  mart_1_cols.remove('fert_rate')
  mart_2_cols = ['item_id','holding','farm','field','year','square','product','plan_yield','fert','fert_rate']

  return optim_output[mart_1_cols].rename(columns={'square':'harvarea'}), optim_output[mart_2_cols].rename(columns={'square':'harvarea'})