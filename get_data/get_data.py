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



def pivot_raw_table(cursor):
    cursor.execute(
        '''
    CREATE TABLE pivoted_table
    AS SELECT
        dict_id,
        t_step,
        MAX(CASE WHEN key = 'state_id' THEN value END) as state,
        MAX(CASE WHEN key = 'cause' THEN value END) as cause,
        MAX(CASE WHEN key = 'method' THEN value END) as method,
        MAX(CASE WHEN key = 'response' THEN value END) as response,
        MAX(CASE WHEN key = 'stance' THEN value END) as stance,
        MAX(CASE WHEN key = 'repost' THEN value END) as repost,
        CAST(MAX(CASE WHEN key = 'id_message' THEN value END) AS INT) as id_message,
        MAX(CASE WHEN key = 'parent_id' THEN value END) as parent_id
    FROM history
    WHERE t_step != 0
    AND dict_id != 'env'
    AND value != 'neutral'
    AND value != 'died'
    GROUP BY dict_id,t_step
    ORDER BY id_message;
    ''')


def select_pivoted_table(cursor):
    cursor.execute(
        "SELECT * FROM pivoted_table")
    data = cursor.fetchall()
    return data

def get_pivoted_data(analysis_path, sql_table_path):
    cur = get_cursor(analysis_path=analysis_path,
                     sql_table_path=sql_table_path)
    pivot_raw_table(cur)
    data = select_pivoted_table(cur)
    cur.execute('DROP TABLE pivoted_table')
    return data
