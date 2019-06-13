

import os
import mrs_strings as Strings
#import pickle
#import csv

import pkl_functions as Pkl_func
import clean_series as Clean_series
import csv_functions as Csv_func







def add_series_to_csv_database(series_dic, database_path, headers):

    Csv_func.write_series_to_database_csv(series_dic, database_path, headers)



def add_series_to_pkl_database (temp_dict, pkl_path, database_type):

    if os.path.isfile(pkl_path):
        database_data = Pkl_func.read_pkl(pkl_path)

    else:
        database_data = {'full':[],'clean':[]}

    # pkl database starcture:
    # {'full': [series1, series2...],
    #  'clean' [series1, series2...]:
    # }
    # where series = {name:'NAME', ID:'23123', age:'5', 'TE':135, 'tissue':'WM','location':'Frontal',....}

    database_data[database_type].append(temp_dict)
    Pkl_func.save_pickle(pkl_path, database_data)




def main(exam_dict, is_fetal):

    print('add csv*s* to database')

    for series_num in exam_dict[Strings.ALL_SERIES].keys():

        seriesTE = exam_dict[Strings.ALL_SERIES][series_num][Strings.TE]
        if seriesTE == Strings.SHORT_TE or seriesTE == Strings.SHORT_TE_35:
            seriesTE = Strings.SHORT_TE
        else:
            seriesTE = Strings.LONG_TE

        series_dict = exam_dict[Strings.PATIENT_INFO].copy()
        series_values = exam_dict[Strings.ALL_SERIES][series_num].copy()
        series_dict.update(series_values)

        # add series to full database:
        headers = Strings.INFO_KEYS[is_fetal] + Strings.SERIES_KEYS + Strings.METABOLITS_ALL[seriesTE]
        csv_path = Strings.CSV_FULL_DATABASE_PATH[is_fetal][seriesTE]
        add_series_to_csv_database (series_dict ,csv_path, headers)

        pkl_path = Strings.PKL_FULL_DATABASE_PATH[is_fetal][seriesTE]
        add_series_to_pkl_database (series_dict, pkl_path, 'full')



        # add to clean database:
        clean_header = Strings.INFO_KEYS[is_fetal] + Strings.SERIES_KEYS + Strings.RELEVANT_METABOLITS_ALL[seriesTE]
        clean_csv_path = Strings.CSV_CLEAN_DATABASE_PATH[is_fetal][seriesTE]
        clean_series_dic = Clean_series.main(series_dict, clean_header)
        add_series_to_csv_database(clean_series_dic, clean_csv_path, clean_header)

        add_series_to_pkl_database (series_dict, pkl_path, 'clean')






if __name__ == '__main__':
    main()


