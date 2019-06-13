
import mrs_strings as Strings
import csv
import os




# reades the original csv - reads the MRS keys and values
def read_series_MRS_keys_values(path):
    with open(path, 'rb') as csvinput:
        reader = csv.reader(csvinput)
        # read the headers row.First time we do reader.next we get the first row
        keys_line = reader.next()
        # read the values row. Second time reader.next gives us the second row
        values_line = reader.next()
    return keys_line, values_line





def write_series_to_database_csv(data_dict, path, headers):

    if not os.path.isfile(path):
        is_new_database = True
    else:
        is_new_database = False


    if is_new_database:
        database_file = open(path, 'wb')
        # opening the file with "WB" will format the file befor it opens it - which mean we will get an empty file
        database_file_writer = csv.DictWriter(database_file, headers)
        # creating a dictionary writer
        database_file_writer.writeheader()
    else:
        database_file = open(path, 'ab')
        # opening file with "ab" opens the file and start writing from the last written row.
        database_file_writer = csv.DictWriter(database_file, headers)
        # creating a dictionary writer

    database_file_writer.writerow(data_dict)
    database_file.close()



# writes a row with ALL the data - patient info, series general data, and MRS values to the specific series csv
def write_series_to_series_csv(path, keys, values):

    with open(path, 'wb') as csvoutput: #now we open the same file only for writing
        writer = csv.writer(csvoutput, lineterminator='\n')

        writer.writerow(keys)
        # first row is the originals headers and after them the new headers

        writer.writerow(values) #now we add the originals values with the new values after them




























##### THE FOLLOWING FUNCTIONS ARE NOT IN USE, BUT MY BE IN USE FOR FUTURE FEATURES #####


#in case we want to read the complete series data from CSV. We already have this data in pkl and and exam dic
def get_series_data_from_series_csv (series_csv_path):
    #each series has it's own csv file.
    csv_file = open(series_csv_path, 'rb')

    reader_dict = csv.DictReader (csv_file) #series csv file only hold header and 1 row of data
    series_dic = reader_dict.next() #we read the first row as dict and save it

    csv_file.close()

    return series_dic



def get_database_data(database_path):

    database_data = []

    database_file = open(database_path,'rb')
    reader_dict = csv.DictReader(database_file)

    for row in reader_dict:   #since we can't use the reader_dict after we close the file, I copy it to a new list.
        database_data.append(row)

    database_file.close()

    return database_data #returns a list of dictionaries - each row in the list is a series

def get_clean_database_data(database_path):

    database_data = []

    database_file = open(database_path,'rb')
    reader_dict = csv.DictReader(database_file)

    for row in reader_dict:
        database_data.append(row)

    database_file.close()

    return database_data


def find_series_csv(series_folder_path):
    series_csv_path = None
    files = os.listdir(series_folder_path)
    for file in files:
        if Strings.CSV_WITH_INFO in file:
            series_csv_path = os.path.join (series_folder_path, file)
            break
    if series_csv_path == None:
        easygui.msgbox("Data is missing for this series. Please add the exam using \"Add New Exam\" before comparing this series.", "OK")
        sys.exit()
    return series_csv_path