import sqlite3
import os

def get_cursor(analysis_path, sql_table_path):
    complete_path = os.path.join(analysis_path, sql_table_path)
    conn = sqlite3.connect(complete_path)
    cur = conn.cursor()
    return cur


def get_raw_info(cursor):
    cursor.execute(
        "SELECT dict_id, t_step, key, value FROM history WHERE t_step != 0 ORDER BY t_step, dict_id, key DESC")
    data = cursor.fetchall()
    return data



def pivot_raw_table(cursor, attributes):
    initial_str = '''
    CREATE TABLE pivoted_table
    AS SELECT
        dict_id,
        t_step,
        CAST(MAX(CASE WHEN key = 'id_message' THEN value END) AS INT) as id_message,
        MAX(CASE WHEN key = 'parent_id' THEN value END) as parent_id,
        MAX(CASE WHEN key = 'state_id' THEN value END) as state,'''
    final_str = '''
    FROM history
    WHERE t_step != 0
    AND dict_id != 'env'
    AND value != 'neutral'
    AND value != 'died'
    GROUP BY dict_id,t_step
    ORDER BY id_message;
    '''
    attr_str = ""
    for attribute in attributes:
        attr_str += "\n" + " "*8 + f"MAX(CASE WHEN key = '{attribute}' THEN value END) as {attribute},"
    select_str = initial_str + attr_str
    select_str = select_str.strip(",")
    cursor.execute(select_str+final_str)


def select_pivoted_table(cursor):
    cursor.execute(
        "SELECT * FROM pivoted_table")
    data = cursor.fetchall()
    return data

def get_pivoted_data(analysis_path, sql_table_path, attributes):
    cur = get_cursor(analysis_path=analysis_path,
                     sql_table_path=sql_table_path)
    pivot_raw_table(cur, attributes)
    data = select_pivoted_table(cur)
    cur.execute('DROP TABLE pivoted_table')
    return data

def _get_types_agents(cursor):
    cursor.execute(
        "SELECT dict_id, value FROM history WHERE key='type'")
    data = cursor.fetchall()
    return data

def get_type_agents(analysis_path, sql_table_path):
    cur = get_cursor(analysis_path, sql_table_path)
    data = _get_types_agents(cur)
    data = list(map(lambda x: (int(x[0]), x[1]), data))
    dict_i = dict(data)
    return dict_i