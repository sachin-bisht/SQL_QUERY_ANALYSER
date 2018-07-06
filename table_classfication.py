import os
import re
import random
import csv
import check_table_and_column as ctac

def file_read(file_path):
    if os.path.exists(file_path) == True:
        file = open(file_path, 'r')
        file_content = file.readlines()
        file.close()
        return file_content
    else:
        print('Error : File not found. updated_queries,txt')
        return -1


def find_column_name(query):
    column_name = []

    patterns = [r'\w+\s*(?:=|>|<)',
                r'\w+\s+(?:[Nn][Oo][Tt]\s+|)[Ll][Ii][Kk][Ee]\s+',
                r'\w+\s+(?:[Nn][Oo][Tt]\s+|)[Ii][Nn]\s*[\(]',
                r'\w+\s+(?:[Nn][Oo][Tt]\s+|)[Bb][Ee][Tt][Ww][Ee][Ee][Nn]\s+',
                r'\w+\s+[Rr][Ee][Gg][Ee][Xx][Pp]\s+']

    col_left_to_right = {}

    for pattern in patterns:
        temp = query

        pos = 0

        while True:
            res = re.search(pattern, temp)
            if not res:
                break
            else:
                col = temp[res.span()[0]:res.span()[1]]
                exp = r'\w+'
                name = re.search(exp, col)
                name = col[name.span()[0]:name.span()[1]]
                pos += res.span()[1]
                if name not in column_name:
                    col_left_to_right[pos] = name
                    column_name.append(name)

                temp = temp[res.span()[1]:]

    exp = r'\s+[Ww][Hh][Ee][Rr][Ee]\s+'
    pat = re.search(exp, query)
    pos = 0
    if pat:
        pos = pat.span()[1]
    column_ordered = []
    for i in sorted(col_left_to_right):
        if i > pos:
            column_ordered.append(col_left_to_right[i])
    return column_ordered

def replace_placeholder(query, table_name, table_column_detail, columnlist):
    result = query

    spcase = r'\w+\s+(?:[Nn][Oo][Tt]\s+|)[Ii][Nn]\s*[\(]\s*(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\')'

    pattern1 = [r'\w+\s*(?:=|>|<)\s*(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))',
                r'\w+\s+(?:[Nn][Oo][Tt]\s+|)[Ll][Ii][Kk][Ee]\s*(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))',
                r'\w+\s+(?:[Nn][Oo][Tt]\s+|)[Bb][Ee][Tt][Ww][Ee][Ee][Nn]\s*(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))',
                r'\w+\s+(?:[Nn][Oo][Tt]\s+|)[Ii][Nn]\s*[\(]\s*(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\')',
                r'\w+\s+(?:[Nn][Oo][Tt]\s+|)[Bb][Ee][Tt][Ww][Ee][Ee][Nn]\s*[\(]?\s*(?:"|\')]?\s*[\w-]+\s*(?:"|\'[\)]?\s*)?\s+[Aa][Nn][Dd]\s+(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))',
                r'\w+\s+[Rr][Ee][Gg][Ee][Xx][Pp]\s*(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))'
                r'[Ll][Ii][Mm][Ii][Tt]\s+(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))']

    pattern2 = [r'[Ll][Ii][Mm][Ii][Tt]\s+(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))\s*,\s*(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))',
                r'\w+\s+(?:[Nn][Oo][Tt]\s+|)[Bb][Ee][Tt][Ww][Ee][Ee][Nn]\s*(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))\s+[Aa][Nn][Dd]\s+(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))']

    lower_limit = 10

    for pattern in pattern1:

        while True:
            res = re.search(pattern, result)
            if not res:
                break
            else:
                col = result[res.span()[0]:res.span()[1]]
                exp = r'\w+'
                name = re.search(exp, col)
                name = col[name.span()[0]:name.span()[1]]

                table = 'limit'
                for t in table_name:
                    if name in columnlist[t]:
                        table = t
                        break
                ipos = None
                if table != 'limit':
                    ipos = columnlist[t].index(name)

                pat = r'(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))'

                if pattern == spcase:
                    pat = r'(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\')'
                placeh = re.search(pat, result)
                if table == 'limit':
                    result = result.replace(result[placeh.span()[0]:placeh.span()[1]], str(lower_limit), 1)
                else:
                    value = []
                    for i in str(table_column_detail[table][random.randint(0,len(table_column_detail[table])-1)][ipos]):
                        if i == "'":
                            value.append('\\')
                        value.append(i)
                    value = ''.join(value)

                    result = result.replace(result[placeh.span()[0]:placeh.span()[1]], "'"+value+"'", 1)

    for pattern in pattern2:
        while True:
            res = re.search(pattern, result)
            if not res:
                break
            else:
                col = result[res.span()[0]:res.span()[1]]
                exp = r'\w+'
                name = re.search(exp, col)
                name = col[name.span()[0]:name.span()[1]]

                table = 'limit'
                for t in table_name:
                    if name in columnlist[t]:
                        table = t
                        break

                ipos = None
                if table != 'limit':
                    ipos = columnlist[t].index(name)

                pat = r'(?:%s|%d|"%s"|"%d"|\'%s\'|\'%d\'|\(%s\)|\(%d\))'
                placeh = re.search(pat, result)
                if table == 'limit':
                    result = result.replace(result[placeh.span()[0]:placeh.span()[1]], str(0), 1)
                else:
                    value = []
                    for i in str(table_column_detail[table][random.randint(0,len(table_column_detail[table])-1)][ipos]):
                        if i == "'":
                            value.append('\\')
                        value.append(i)
                    value = ''.join(value)

                    result = result.replace(result[placeh.span()[0]:placeh.span()[1]], "'"+value+"'", 1)

                placeh = re.search(pat, result)
                if table == 'limit':
                    result = result.replace(result[placeh.span()[0]:placeh.span()[1]], str(lower_limit), 1)
                else:
                    value = []
                    for i in str(table_column_detail[table][random.randint(0, len(table_column_detail[table])-1)][ipos]):
                        if i == "'":
                            value.append('\\')
                        value.append(i)
                    value = ''.join(value)

                    result = result.replace(result[placeh.span()[0]:placeh.span()[1]], "'"+value+"'", 1)

    return result


def different_table(content):

    final_details = {}

    table_index_count = {}
    table_column_index = {}

    table_column_detail = {}
    table_index_detail = {}
    table_index_col_detail = {}

    table_found_switch = [r'\s+[Ff][Rr][Oo][Mm]\s+\w+',
                            r'[Uu][Pp][Dd][Aa][Tt][Ee]\s+\w+',
                            r'\s+[Jj][Oo][Ii][Nn]\s+\w+']

    exp = r'[a-zA-Z][a-zA-Z0-9_]*,?'

    queries_status = []
    k = 1

    show_table = ctac.get_tablename()

    for query in content:
        query = query[:-2]
        details = {'Query':'', 'Table':[], 'Table Found':True, 'Column Found':True, 'Index Used':[]}
        details['Query'] = query
        table_name = []

        for exp in table_found_switch:
            temp_query = query
            while True:
                res = re.search(exp, temp_query)
                if not res:
                    break

                temp = temp_query[res.span()[0]:res.span()[1]]
                temp = temp[::-1]

                name = re.search(r'\w+', temp)
                name = temp[name.span()[0]:name.span()[1]]
                name = name[::-1]
                if name not in table_name:
                    table_name.append(name)
                temp_query = temp_query[res.span()[1]:]

                while True:
                    pattern = r'\s*(?:\w+|),\s*\w+'
                    res = re.search(pattern, temp_query)
                    if not res:
                        break
                    if res.span()[0] != 0:
                        break
                    temp = temp_query[res.span()[0]:res.span()[1]]
                    temp = temp[::-1]

                    name = re.search(r'\w+', temp)
                    name = temp[name.span()[0]:name.span()[1]]
                    name = name[::-1]
                    if name not in table_name:
                        table_name.append(name)
                    temp_query = temp_query[res.span()[1]:]

        details['Table'] = table_name

        for table in table_name:
            if table not in show_table:
                details['Table Found'] = False
                if table not in final_details.keys():
                    final_details[table] = {'Table Found' : None, 'Queries' : [], 'Column Not Found': [], 'New Index Suggest' : None, 'Index Not Helpful': None}
                final_details[table]['Table Found'] = False
                final_details[table]['Column Not Found'] = None
                final_details[table]['Queries'].append(query)
                break

            if table not in final_details.keys():
                final_details[table] = {'Table Found': None, 'Queries': [], 'Column Not Found' : [], 'New Index Suggest' : None, 'Index Not Helpful': None}
            final_details[table]['Table Found'] = True

            if table not in table_column_detail.keys():
                table_column_detail[table] = ctac.get_columns(table)

        if not details['Table Found']:
            details['Column Found'] = False
        else:
            columnlist = {}
            for table in table_name:
                clist = ctac.get_columnlist(table)
                columnlist[table] = clist

            query_column = {}

            column_names_ordered = find_column_name(query)
            for name in column_names_ordered:
                f = 0
                for table in table_name:
                    if table not in query_column:
                        query_column[table] = []
                for table in table_name:
                    if name in columnlist[table]:
                        f = 1
                        query_column[table].append(name)
                        break

                if f == 0:
                    for table in table_name:
                        final_details[table]['Column Not Found'].append(name)
                        if query not in final_details[table]['Queries']:
                            final_details[table]['Queries'].append(query)
                    details['Column Found'] = False

            if details['Column Found']:
                indexlist = []
                new_query = replace_placeholder(query, table_name, table_column_detail, columnlist)
                details['Query'] = new_query
                for table in table_name:
                    if table not in table_column_index.keys():
                        table_column_index[table] = []
                    # ALL INDEX LIST, need only used
                    if table not in table_index_detail.keys():
                        table_index_detail[table], table_index_col_detail[table] = ctac.get_index(table)

                        temp = {}
                        for index in table_index_col_detail[table].values():
                            temp[index] = 0
                        table_index_count[table] = temp

                    one_index = ctac.explain_query(new_query, table_index_detail[table])

                    indexlist.append(one_index)
                    for index in one_index:
                        ind_to_col = table_index_col_detail[table][index]
                        table_index_count[table][ind_to_col] += 1

                    if len(one_index) == 0:
                        table_column_index[table].append(query_column[table])

                details['Index Used'] = indexlist
        queries_status.append(details)



    # with open('step1.csv', 'w') as csvfile:
    #     fieldnames = ['Query','Table', 'Table Found', 'Column Found', 'Index Used']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for status in queries_status:
    #         writer.writerow(status)
    # csvfile.close()

    for table in table_column_index:
        table_column_index[table].sort(reverse=True)

        flag = [False for i in table_column_index[table]]
        k = 0
        for pot in table_column_index[table]:
            if flag[k] or len(pot) == 0:
                k += 1
                continue
            potlist = pot
            pot = ','.join(pot)

            co = 1

            temp = k+1
            while temp < len(table_column_index[table]):
                if len(table_column_index[table][temp]) == 0:
                    temp += 1
                    continue
                if table_column_index[table][temp][0] != potlist[0]:
                    break
                posbindex = ','.join(table_column_index[table][temp])
                pos = pot.find(posbindex)
                if pos == 0:
                    if pot == posbindex:
                        co += 1
                        flag[temp] = True
                    elif pot[len(posbindex)] == ',':
                        co += 1
                        flag[temp] = True
                temp += 1

            if pot not in table_index_count[table].keys():
                table_index_count[table].update({pot:co})
            else:
                table_index_count[table][pot] += co
            k += 1


    new_index_suggest = {}
    index_not_helpful = {}

    for table in table_index_count:
        sort_table_index = [(k, table_index_count[table][k]) for k in sorted(table_index_count[table], reverse=True)]
        flag = [False for i in sort_table_index]
        index_not_helpful[table] = []

        kj = 0
        for index_column in sort_table_index:
            if flag[kj]:
                kj += 1
                continue
            if index_column[0] not in table_index_col_detail[table].values():
                temp = kj+1
                while temp < len(sort_table_index):
                    if flag[temp]:
                        temp += 1
                        continue
                    pos = index_column[0].find(sort_table_index[temp][0])
                    pot = index_column[0]
                    posbindex = sort_table_index[temp][0]

                    if pos == 0:
                        if len(pot) > len(posbindex) and pot[len(posbindex)] == ',':
                            index_for_column = ''
                            for i in table_index_col_detail[table]:
                                if table_index_col_detail[table][i] == posbindex and index_for_column.upper() != 'PRIMARY':
                                    index_for_column = i
                                if index_for_column == 'PRIMARY':
                                    break
                            if index_for_column != 'PRIMARY' and index_for_column not in index_not_helpful[table]:
                                index_not_helpful[table].append(index_for_column)
                            flag[temp] = True
                    temp += 1
            kj += 1


    for table in table_index_count:
        sort_table_index = [(k, table_index_count[table][k]) for k in sorted(table_index_count[table], key=table_index_count[table].get, reverse=True)]

        k = 0

        tot_index = 0
        index_suggest = []
        for index_column in sort_table_index:
            if index_column[0] not in table_index_col_detail[table].values():
                if index_column[1] > 0 :
                    index_suggest.append(index_column[0])
                    tot_index += 1
            else:
                if index_column[1] > 0:
                    tot_index += 1
                else:
                    if index_column[0] not in index_not_helpful[table]:
                        posbbindex = index_column[0]
                        index_for_column = ''
                        for i in table_index_col_detail[table]:
                            if table_index_col_detail[table][i] == posbbindex and index_for_column.upper() != 'PRIMARY':
                                index_for_column = i
                            if index_for_column == 'PRIMARY':
                                break
                        if index_for_column != 'PRIMARY' and index_for_column not in index_not_helpful[table]:
                            index_not_helpful[table].append(index_for_column)
            if tot_index >= 5:
                break
        new_index_suggest[table] = index_suggest


    # with open('step2.csv', 'w') as csvfile:
    #     fieldnames = ['Table Name', 'New Index Suggest', 'Index Not Helpful']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for table in new_index_suggest:
    #         # row = [table, new_index_suggest[table], index_not_helpful[table]]
    #         writer.writerow({'Table Name':table, 'New Index Suggest':new_index_suggest[table], 'Index Not Helpful': index_not_helpful[table]})
    # csvfile.close()

    for table in final_details:
        if table in new_index_suggest:
            final_details[table]['New Index Suggest'] = new_index_suggest[table]
            final_details[table]['Index Not Helpful'] = index_not_helpful[table]


    with open('analyser.csv', 'w') as csvfile:
        fieldnames = ['Table Name', 'Table Found', 'Column Not Found', 'Queries', 'New Index Suggest', 'Index Not Helpful']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for table in final_details:
            writer.writerow({'Table Name': table, 'Table Found': final_details[table]['Table Found'],
                             'Column Not Found': final_details[table]['Column Not Found'],
                             'Queries': final_details[table]['Queries'],
                             'New Index Suggest': final_details[table]['New Index Suggest'],
                             'Index Not Helpful': final_details[table]['Index Not Helpful']})

def generate_result():
    filepath = './updated_queries.txt'
    content = file_read(filepath)
    if content != -1:
        tables = different_table(content)
        return True
    return False

