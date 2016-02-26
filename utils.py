# some auxiliary functions.
__author__ = 'nb254'
import csv

def save_to_csv(lines, header, filename):
   myfile = open(filename, 'wb')
   wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
   wr.writerow(header)
   for line in lines:
      try:
         wr.writerow(line)
      except UnicodeError:
         fixed_line = list(line)
         print 'Unicode exception for a line, converting to utf-8'
         for elem in fixed_line:
            if isinstance(elem, unicode):
               index = fixed_line.index(elem)
               fixed_line[index] = fixed_line[index].encode('utf-8')
         print fixed_line
         wr.writerow(fixed_line)

def saveStatToCSV(file_name, data, header, one_row):
    with open(file_name, 'wb') as myfile:
        wr = csv.writer(myfile)
        if header != '':
            wr.writerow(header)
        if one_row:
            wr.writerow(data)
        else:
            wr.writerows(data)
    return

def saveElemsToCSV(file_name, data, header):
    with open(file_name, 'wb') as myfile:
        wr = csv.writer(myfile)
        if header != '':
            wr.writerow(header)
        for elem in data:
            #print elem
            wr.writerow([elem])
    return

def openListFromCSV(filename):
   with open(filename, 'rb') as f:
       reader = csv.reader(f)
       listfromCSV = list(reader)
   flattened = [val for sublist in listfromCSV for val in sublist]
   return flattened

def openDictfromCSV(filename):
    reader = csv.reader(open(filename, 'rb'))
    dictfromCSV = dict(reader)
    return dictfromCSV

def writeDict(filename, mydict):
    writer = csv.writer(open(filename, 'wb'))
    for key, value in mydict.items():
        writer.writerow([key, value])

