from python_mysql_dbconfig import read_db_config
import pymysql
def get_columnlist(table):
    query = 'desc {}'.format(table)
    dbconfig = read_db_config()
    res = []
    try:
        conn = pymysql.connect(dbconfig['host'], dbconfig['user'], dbconfig['password'], dbconfig['database'])

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        res = [row[0] for row in rows]
    except Exception as e:
        print (query)
        print(e)

    finally:
        cursor.close()
        conn.close()
        return res

def get_index(table):
    query = 'show index from {}'.format(table)
    dbconfig = read_db_config()
    result = []
    col_result = {}

    try:
        conn = pymysql.connect(dbconfig['host'], dbconfig['user'], dbconfig['password'], dbconfig['database'])

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            if len(result) == 0:
                result.append(row[2])
                col_result[row[2]] = row[4]
            elif result[len(result)-1] != row[2]:
                result.append(row[2])
                col_result[row[2]] = row[4]
            else:
                temp = col_result[row[2]]
                temp = ''.join(temp)
                temp = temp + ',' + row[4]
                col_result[row[2]] = temp

    except Exception as e:
        print (e)

    finally:
        cursor.close()
        conn.close()
        return result, col_result

def explain_query(query, table_index):
    q = 'explain ' + query[:-1]
    dbconfig = read_db_config()
    indexlist = []

    explain_q = ['id', 'select_type', 'table', 'type', 'possible_keys', 'key', 'key_len','ref', 'rows', 'extra']

    try:
        conn = pymysql.connect(dbconfig['host'], dbconfig['user'], dbconfig['password'], dbconfig['database'])

        cursor = conn.cursor()
        cursor.execute(q)
        rows = cursor.fetchall()

        for row in rows:
            if str(row[2])[0] == '<':
                continue
            if str(row[5]) != 'None':
                if row[5] in table_index and row[5] not in indexlist:
                    indexlist.append(row[5])

    except Exception as e:
        print(q)
        print (e)

    finally:
        cursor.close()
        conn.close()
        return indexlist

def get_columns(table):
    query = 'SELECT * from {} order by rand() limit 2;'.format(table)

    rows = []
    dbconfig = read_db_config()
    try:
        conn = pymysql.connect(dbconfig['host'], dbconfig['user'], dbconfig['password'], dbconfig['database'])

        cursor = conn.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()

    except Exception as e:
        print (e)

    finally:
        cursor.close()
        conn.close()
        return rows


def get_tablename():
    query = 'SHOW TABLES'
    found = 0
    dbconfig = read_db_config()
    try:

        conn = pymysql.connect(dbconfig['host'], dbconfig['user'], dbconfig['password'], dbconfig['database'])

        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()
        names = [row[0] for row in rows]

        return names

    except Exception as e:
        print(query)
        print ('Error:' , e)

    finally:
        cursor.close()
        conn.close()
    if found == 1:
        return True
    return False

