#from sqlalchemy import create_engine # for online version
#import psycopg2 # for online version
import pandas as pd

def get_input_data(libpq_connection_str: str):
  conn = psycopg2.connect(libpq_connection_str)
  conn.autocommit = True

  in_fert_mm = pd.read_sql_query('select * from at_python.in_fertilizers_mm', conn)
  in_prod_fert = pd.read_sql_query('select * from at_python.in_product_fertilizers', conn)
  in_data_chain = pd.read_sql_query('select * from at_python.in_fields_data_chain_item', conn)

  conn.commit()
  conn.close()

  return in_data_chain, in_fert_mm, in_prod_fert

def upload_market(mart:pd.DataFrame, sql_alchemy_conn_str: str, schema_name: str, table_name: str):
  engine = create_engine(sql_alchemy_conn_str)
  conn = engine.connect()
  mart.to_sql(table_name, schema=schema_name, con=conn, if_exists='append', index=False)
  print(f'Data mart was successfully uploaded to {sql_alchemy_conn_str}')

def execute_sql_query(libpq_connection_str: str, sql_command: str):
  conn = psycopg2.connect(libpq_connection_str)
  conn.autocommit = True

  cursor = conn.cursor()
  cursor.execute(sql_command)

  conn.commit()
  conn.close()