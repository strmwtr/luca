'''
Python 3.6 script to compare Census Address List with Charlottesville's 
Master Address Table
'''
import unicodecsv

fldr = r'C:\Users\brownr\Desktop\db\LUCA\csv'
mat_src = r'{0}\src\master_address_tbl.csv'.format(fldr)
luca_src = r'{0}\src\luca20_PL5114968_censusaddr.csv'.format(fldr)

def csv_to_list(csv_name):
  with open(csv_name, 'rb') as f:
    reader = unicodecsv.DictReader(f)
    return list(reader)

def add_MA_field_mat(mat_as_list):
  for x in mat_as_list:
    MA = '{0} {1} {2} {3} {4} {5} {6}'.format(x['ST_NUMBER'],
    x['PREDIR'], x['ST_NAME'], x['SUFFIX'], x['POSTDIR'],
    x['UNIT_TYPE'], x['ST_UNIT'])
    while '  ' in MA: MA = MA.replace('  ', ' ')
    MA = MA.strip()
    x['MA'] = MA
    x['match'] = ''
    x['MAFID'] = ''
    x['test_num'] = ''
  return mat_as_list

def add_MA_field_luca(luca_as_list):
  for x in luca_as_list:
    MA = '{0} {1} {2}'.format(x['HOUSENUM'],x['STREETNAME'], x['UNIT'])
    while '  ' in MA: MA = MA.replace('  ', ' ')
    MA = MA.strip()
    MA = MA.upper()
    x['MA'] = MA
    x['MasterAddr'] = ''
    x['test_num'] = ''
  return luca_as_list

def remove_NKATB():
  luca_rm =[x for x in luca if x['MA'] != 'NO KNOWN ADDRESSES IN THIS BLOCK']
  return luca_rm

def t1():
  t1_list = []
  for row in mat:
    for x in luca:
      if x['MA'] == row['MA']:
        t1_list.append(row)
        row['MAFID'] = x['MAFID']
        row['test_num'] = 1
        x['MasterAddr'] = row['MasterAddr']
        x['test_num'] = 1
  return t1_list

def t2():
  t2_list = []
  for r in mat:
    if r['test_num'] != '':
      temp1 = '{0} {1} {2} {3} {4}'.format(r['ST_NUMBER'],
      r['PREDIR'], r['ST_NAME'], r['SUFFIX'], r['POSTDIR'])
      while '  ' in temp1: temp1 = temp1.replace('  ', ' ')
      temp1 = temp1.strip().upper()
      for x in luca:
        if x['test_num'] != '':
          temp2 = '{0} {1}'.format(x['HOUSENUM'],x['STREETNAME'])
          while '  ' in temp2: temp2 = temp2.replace('  ', ' ')
          temp2 = temp2.strip()
          temp2 = temp2.upper()
          if temp1 == temp2:
            t2_list.append(r)
            r['MAFID'] = x['MAFID']
            r['test_num'] = 2
            x['MasterAddr'] = r['MasterAddr']
            x['test_num'] = 2
  return t2_list

mat_as_list = csv_to_list(mat_src)
luca_as_list = csv_to_list(luca_src)
mat = add_MA_field_mat(mat_as_list)
luca = add_MA_field_luca(luca_as_list)
print('-'*10,'Initial','-'*10)
print('MAT Starting: ', len(mat))
print('LUCA Starting: ', len(luca))
print('\n')

print('-'*10,'Clean NO KNOWN ADDRESSES IN THIS BLOCK','-'*10)
luca = remove_NKATB()
print('LUCA after removing NO KNOWN ADDRESSES IN THIS BLOCK: ', 
len(luca))
print('\n')

print('-'*10,'Test if LUCA[MA] == MAT[MA]','-'*10)
print(len(t1()))
print('MAT post t1: ',len([x for x in mat if x['MAFID'] != '']))
print('LUCA post t2: ',len([x for x in luca if x['MasterAddr'] != '']))
u_MA = set([x['MasterAddr'] for x in luca if x != ''])
for x in u_MA:
  z = [[y['MAFID'],y['MA']] for y in luca if y['MasterAddr'] == x and x != '']
  if len(z) > 1:
    print(z)
print (len((set([str(x) for x in t2()]))))
#print(len(set(t2())))