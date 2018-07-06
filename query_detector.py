import os.path
import remove_comments as rc

#read the file, if not found return -1
def file_read(file_path):

	if os.path.exists(file_path) == True:
		file = open(file_path, 'r')
		file_content = file.read()
		file.close()
		return file_content

	else:
		return -1

#Search all the pattern 'r' in the string 's' and return all their end position
def pattern_pos(s, r):
	s_len = len(s)
	r_len = len(r)

	if s_len < r_len:
		return -1
	else:
		_complete = []
		for i in range(s_len):
			# search for r in s until not enough characters are left
			if s[i:i + r_len] == r:
				if len(_complete) == 0:
					_complete.append(i+r_len)
				elif _complete[len(_complete)-1]+r_len <= i:
					_complete.append(i+r_len)
			else:
				i = i + 1
		return (_complete)

#detects all the functions in the contents string using def and return them seperately
def get_func(contents):
	def_pos = pattern_pos(contents, 'def ')

	def_contents = []
	def_pos_len = len(def_pos)
	for i in range(def_pos_len):
		if i+1 < def_pos_len:
			def_contents.append(contents[def_pos[i]-4 : def_pos[i+1]-4])
		else:
			def_contents.append(contents[def_pos[i] : len(contents)])\

	return def_contents

#extract the variable name that stores the query
def extract_query(contents, pos):
	contents_len = len(contents)
	while pos < contents_len and contents[pos] != '(':
		pos += 1
	pos += 1
	if pos >= contents_len:
		return -1, pos
	while pos < contents_len and (contents[pos] == ' ' or contents[pos] == '\n' or contents[pos] == '\t'):
		pos += 1
	if pos >= contents_len:
		return -1, pos
	res = []

	if contents[pos:pos+3] == '"""':
		pos += 3
		res.append('"')
		while pos < contents_len and contents[pos] != '"':
			res.append(contents[pos])
			pos += 1
		pos += 2
		res.append('"')

	elif contents[pos] == '"':
		pos += 1
		res.append('"')
		while pos < contents_len and contents[pos] != '"':
			res.append(contents[pos])
			pos += 1
		res.append('"')
	elif contents[pos] == "'":
		pos += 1
		res.append('"')
		while pos < contents_len and contents[pos] != "'":
			res.append(contents[pos])
			pos += 1
		res.append('"')
	else:
		while pos < contents_len and contents[pos] != ' ' and contents[pos] != ',' and contents[pos] != ')':
			res.append(contents[pos])
			pos += 1
	if pos >= contents_len:
		return -1, pos
	else:
		res = ''.join(res)
		return res, pos

#return all the variables name that contains query
def get_query(contents, indexes):
	queries = []

	indlen = len(indexes)
	i, nxt = 0, 0
	while i <  indlen:
		if nxt > indexes[i]:
			i += 1
			continue
		query, nxt = extract_query(contents, indexes[i])
		
		if query == -1:
			return -1

		queries.append(query)
		i += 1
	return queries

def query_check(content, search, st):
	s_len = len(content)
	r_len = len(search)

	if s_len < r_len:
		return -1
	else:
		for i in range(st, s_len):
			# search for r in s until not enough characters are left
			if content[i:i + r_len] == search:
				result = []
				j = i + r_len
				return j
	return -1

# def pattern_once(content, search, st):
# 	s_len = len(content)
# 	r_len = len(search)
#
# 	if s_len < r_len:
# 		return -1, 0
# 	else:
# 		for i in range(st, s_len):
# 			if content[i:i + r_len] == search:
# 				result = []
# 				j = i + r_len
# 				while j < s_len and content[j] != '=':
# 					j += 1
# 				if j >= s_len:
# 					return -1, 0
# 				j += 1
# 				while j < s_len and (content[j] != '"' and content[j] != "'"):
# 					if content[j] != " ":
# 						j = query_check(content, search, j)
# 						if j == -1:
# 							return -1, 0
# 						while j < s_len and content[j] != '=':
# 							j += 1
# 						if j >= s_len:
# 							return -1, 0
# 						j += 1
# 					j += 1
# 				if j >= s_len:
# 					return -1, 0
# 				j += 1
# 				if content[j-1] == '"':
# 					while j < s_len and content[j] != '"':
# 						result.append(content[j])
# 						j += 1
# 					if j >= s_len:
# 						return -1, 0
# 				else:
# 					while j < s_len and content[j] != "'":
# 						result.append(content[j])
# 						j += 1
# 					if j >= s_len:
# 						return -1, 0
#
# 				result = ''.join(result)
#
# 				return result, j
# 		return -1, 0
#
#


#appends all the queries in the new file
def explain_query(contents, queries):
	file = open('output.txt', 'w')

	for i in queries:
		file.write(i)
		file.write('\n')
	file.close()


def move_forward(contents, pos):
	c_len = len(contents)

	while pos < c_len and (contents[pos] == ' ' or contents[pos] == '\n' or contents[pos] == '\t'):
		pos += 1
	if pos >= c_len:
		return -1
	return pos


def query_statement(contents, query, pos):
	flag, f = 0, 0

	c_len = len(contents)
	q_len = len(query)
	if q_len > c_len:
		return -2, 0

	while flag == 0:
		#search query name
		for i in range(pos, c_len):
			if contents[i:i + q_len] == query:
				pos = i+q_len
				break

		if pos >= c_len:
			return -1, 0

		# search '='
		repflag = 0
		while pos < c_len and contents[pos] != '=':
			if contents[pos] != ' ':
				pos = move_forward(contents, pos)
				repflag = 1
				pos += 1
				break
			pos += 1
		if pos >= c_len:
			return -1, 0

		if repflag == 1:
			continue
		pos += 1
		#search ' or "
		while pos < c_len and contents[pos] != '"' and contents[pos] != "'":
			if contents[pos] != ' ':
				pos = move_forward(contents, pos)
				repflag = 1
				break
			pos += 1

		if pos >= c_len:
			return -1, 0
		if repflag == 1:
			continue
		break


	pos += 1
	result = []

	if contents[pos-1:pos+2] == '"""':
		pos += 2
		while pos < c_len and contents[pos] != '"':
			result.append(contents[pos])
			pos += 1
		pos += 2
	elif contents[pos-1] == '"':
		while pos < c_len and contents[pos] != '"':
			result.append(contents[pos])
			pos += 1
	else:
		while pos < c_len and contents[pos] != "'":
			result.append(contents[pos])
			pos += 1

	if pos >= c_len:
		return -1, 0
	return ''.join(result), pos


def detector(filename):
	#'./search_file/sop_module.py' './search_file/paylater.py' './search_file/partner_module.py'
	# filename = './search_file/sop_module.py'#input("Enter filepath: ")
	filename = os.path.join('./search_file', filename)
	value = rc.clean_python_file(filename)

	if value == -1:
		print('File not exists')
		return -1

	contents = file_read(filename)
	if contents == -1:
		print ('File not exists')
	else:

		many_functions = get_func(contents)
		if not many_functions:
			print ('No functions found')
			return

		search = ".executesql"
		values = []

		for content in many_functions:
			patterns = pattern_pos(content, search)
			queries = get_query(content, patterns)
			if queries == -1:
				print ('Error in file')
			else:
				st = 0
				for qq in queries:
					if qq[0] == '"':
						result = qq[1:len(qq)-1]
						values.append(qq[1:len(qq)-1])
						continue

					value, st = query_statement(content, qq, st)
					if value == -1:
						st = 0
						value, st = query_statement(content, qq, st)
						if value == -1:
							print ("Error :", qq, "variable not found")
							st = 0
							continue
					result = value
					values.append(result)

		results = []
		for i in values:
			if '\\' in i or '\n' in i:
				result = []
				for j in i:
					if j != '\\' and j != '\n':
						result.append(j)
				result = ''.join(result)
				results.append(result)
			else:
				results.append(i)
		explain_query(contents, results)