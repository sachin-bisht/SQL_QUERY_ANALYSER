import os

def check_where_sql(query):
    search = 'where'
    q_len = len(query)
    s_len = len(search)

    if q_len < s_len:
        return -1
    else:
        for i in range(q_len):
            # search for r in s until not enough characters are left
            if query[i:i + s_len] == search:
                return 1
        return 0
def choosing_query(file_path):
    if os.path.exists(file_path) == True:
        file = open(file_path, 'r')
        queries = file.readlines()
        updated_queries = []
        for query in queries:
            value = check_where_sql(query)
            if value == 1:
                query = query.split()
                query.append(';\n')
                query = ' '.join(query)
                updated_queries.append(query)
            elif value == -1:
                print ('Error : Query not found.', query)

        file.close()
        return updated_queries

    else:
        return -1


def performance_query():
    queries = choosing_query('./output.txt')
    if queries == -1:
        print ('File not exists')
    else:
        file = open('updated_queries.txt', 'w')
        for query in queries:
            file.write(query)
        file.close()