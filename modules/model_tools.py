# My modules
from modules.data_tools import *
# External modules
from ortools.linear_solver import pywraplp
import numpy as np
import time

def create_solver(ferts_params):
  solver = pywraplp.Solver.CreateSolver('CBC')
  infinity = solver.infinity()
  fert_num = len(ferts_params['fert_costs'])
  fert_rates, fert_bools = np.empty(fert_num, dtype=pywraplp.Variable), np.empty(fert_num, dtype=pywraplp.Variable)

  # Vars
  for j in range(fert_num):
    fert_rates[j] = solver.IntVar(0, infinity, f'fert_rate_{j}')
    fert_bools[j] = solver.IntVar(0, 1, f'fert_bool_{j}')

  # Constraints
  for j in range(fert_num):
    solver.Add(fert_rates[j] <= fert_bools[j] * ferts_params['max_fert_rates'][j])
    solver.Add(fert_rates[j] >= fert_bools[j] * ferts_params['min_fert_rates'][j])

  if ferts_params['p_norm'] > 0:
    constraint_expr = [fert_rates[j] * ferts_params['p_contents'][j] for j in range(fert_num)]
    solver.Add(sum(constraint_expr) >= ferts_params['p_norm'])

  if ferts_params['k_norm'] > 0:
    constraint_expr = [fert_rates[j] * ferts_params['k_contents'][j] for j in range(fert_num)]
    solver.Add(sum(constraint_expr) >= ferts_params['k_norm'])

  solver.Add(solver.Sum(fert_bools) <= 1)

  # Objective
  obj_expr = [fert_rates[j] * ferts_params['fert_costs'][j] for j in range(fert_num)]
  solver.Minimize(solver.Sum(obj_expr))

  return solver

def find_optimal_variants(in_data_chain, in_fert_mm, in_prod_fert):
  output = in_data_chain.copy().set_index('item_id')
  output['revenue_crop'] = output['plan_yield'] * output['crop_price'] * output['square']
  output['cost_var_total'] = output['cost_var'] * output['square']
  output['fert_rate'],output['cost_fertilizer_total'],output['p_deposit'],output['k_deposit'],output['fert']=0,0,0,0,''

  #Iterating over all the options
  start_time = time.time()
  options_IDs = list(output.index)
  for id in options_IDs:
    option_data = output.loc[id,['product','square','k_norm','p_norm']].squeeze().to_dict()
    ferts_params = get_fert_prod_params(in_fert_mm, in_prod_fert, option_data)

    solver = create_solver(ferts_params)
    status = solver.Solve()

    if solver.Objective().Value() == -0 or status != pywraplp.Solver.OPTIMAL:
      continue

    var_num = len(solver.variables())
    for j in range(1,var_num,2):
      if solver.variable(j).solution_value() == 1:
        opt_fert_id, opt_fert_rate = int(solver.variable(j).name().split('_')[2]), solver.variable(j - 1).solution_value()
        break

    output.loc[id, 'fert_rate'] = opt_fert_rate
    output.loc[id, 'fert'] = ferts_params['fert_names'][opt_fert_id]
    output.loc[id, 'cost_fertilizer_total'] = ferts_params['fert_costs'][opt_fert_id] * opt_fert_rate * option_data['square']
    output.loc[id, 'p_deposit'] = ferts_params['p_contents'][opt_fert_id] * opt_fert_rate
    output.loc[id, 'k_deposit'] = ferts_params['k_contents'][opt_fert_id] * opt_fert_rate
  print("Mixed integer programming solution time for all options: %s seconds" % (time.time() - start_time))

  output['variable_costs'] = output['cost_var_total'] + output['cost_fertilizer_total']
  output['gross_margin'] = output['revenue_crop'] - output['variable_costs']

  return make_data_marts(output)