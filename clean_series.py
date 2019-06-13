#EACH MATABOLITE HAS 3 VALUES:
#1. raw value
#2. normalized value: metabolit/Cr+PCr
#3. SD value : metabolit %SD
#The raw value is not interesting - we will only work with the normalized value, so we want to remove the raw values
#The metabolit is relevant only if it's SD is smaller then 20 - otherwise - we don't want to use the value.
#For LACTAT and only LACTAT - the SD value is not interesting - if metabolit value is >0.99 - it pathological and we want to keep it.


import csv
import os
import mrs_strings as Strings











def remove_raw_data(series_dict, wanted_headers):
    # all the data is normalized to the same scala: /Cr+PCr. We have no use for the unnormalized values, so we want to remove them
    my_keys = series_dict.keys()
    for key in my_keys:
        if (Strings.SD_STRING not in key) and (Strings.NORMALIZATION_STRING not in key) and (key not in wanted_headers):
            series_dict.pop(key)
    return series_dict


def remove_irrelevant_metabolits(series_dict, wanted_headers):
    my_keys = series_dict.keys()
    for key in my_keys:
        if key not in wanted_headers:
            series_dict.pop(key)
    return series_dict



def remove_metabolits_with_high_SD(series_dict):

    my_keys = series_dict.keys()

    for key in my_keys:

        if (key!='') and ('%SD' in key) and (key != Strings.LACTAT_METABOLIT) and (key != Strings.LACTAT_SD):
            if int( series_dict[key]) >= 20:
                metabolite_SD = key
                metabolite = metabolite_SD.split(' ')[1] #zero place is always ' ', first will be the name of the matbolit and second will be the %SD string
                metabolite = ' ' + metabolite + '/Cr+PCr'
                series_dict[metabolite] = '*'
                series_dict[metabolite_SD] = '*'

        if key == Strings.LACTAT_METABOLIT: #LACTAT is special - regardless of the SD value- any value that is smaller than one is not interesting, any value bigger than 0.99 is pathological.
            metabolite = Strings.LACTAT_METABOLIT
            metabolite_SD = Strings.LACTAT_SD
            if float(series_dict[metabolite]) < 1:
                series_dict[metabolite] = '*'
                series_dict[metabolite_SD] = '*'

    return series_dict
    #now we need to write this series to the cleaned database







def main(series, wanted_headers):


    clean_series = remove_raw_data(series, wanted_headers)
    clean_series = remove_irrelevant_metabolits(clean_series, wanted_headers)
    # remove_raw_data and remove_irrelevant_metabolits can be in the same function for a better time complexity, but sometimes we would want to do one but not the other
    clean_series = remove_metabolits_with_high_SD(clean_series)
    try:
        clean_series[Strings.PATIENT_AGE] = round( float(clean_series[Strings.PATIENT_AGE]),3 )
    except:
        clean_series[Strings.MOTHER_AGE] = round( float(clean_series[Strings.MOTHER_AGE]),3 )


    return clean_series












if __name__ == '__main__':
    main()








#add_multiple_serieses_to_database ()

#def create_clean_database_from_existing_database():

#def add_exam_to_clean_data_base (csv_writer_dic_shortTE)




#series_csv_file = open(single_series_path)
#series_csv_reader_dic = csv.DictReader(series_csv_file)

# for row in csv_reader_dict_shortTE:
#   series_dict = row
#  clean_series_dict = remove_raw_data (series_dict)
# clean_series_dict = find_high_SD_and_remove_the_matabolit_value(clean_series_dict)
# add_series_to_clean_database (clean_series_dict, csv_writer_dic_shortTE)

#for row in reader_dict_longTE:
 #   series_dict = row
  #  clean_series_dict = remove_raw_data(series_dict)
   # clean_series_dict = find_high_SD_and_remove_the_matabolit_value(clean_series_dict)
    #add_multi_series_to_clean_database(clean_series_dict, writer_dict_longTE)



'''
class Strings:

    dataBase_shortTE_path = 'M:\\clinica\Hadas\MRS\\MRS_dataBase_shortTE.csv'
    dataBase_longTE_path = 'M:\\clinica\\Hadas\\MRS\\MRS_dataBase_longTE.csv'
    clean_dataBase_shortTE_path = 'M:\\clinica\\Hadas\\MRS\\MRS_dataBase_shortTE_CLEANED.csv'
    clean_dataBase_longTE_path = 'M:\\clinica\\Hadas\\MRS\\MRS_dataBase_longTE_CLEANED.csv'

    #headers_shortTE = ['Row', ' Col', ' Ala', ' Ala %SD', ' Ala/Cr+PCr', ' Asp', ' Asp %SD', ' Asp/Cr+PCr', ' Cr', ' Cr %SD', ' Cr/Cr+PCr', ' PCr', ' PCr %SD', ' PCr/Cr+PCr', ' GABA', ' GABA %SD', ' GABA/Cr+PCr', ' Glc', ' Glc %SD', ' Glc/Cr+PCr', ' Gln', ' Gln %SD', ' Gln/Cr+PCr', ' Glu', ' Glu %SD', ' Glu/Cr+PCr', ' GPC', ' GPC %SD', ' GPC/Cr+PCr', ' PCh', ' PCh %SD', ' PCh/Cr+PCr', ' GSH', ' GSH %SD', ' GSH/Cr+PCr', ' Ins', ' Ins %SD', ' Ins/Cr+PCr', ' Lac', ' Lac %SD', ' Lac/Cr+PCr', ' NAA', ' NAA %SD', ' NAA/Cr+PCr', ' NAAG', ' NAAG %SD', ' NAAG/Cr+PCr', ' Scyllo', ' Scyllo %SD', ' Scyllo/Cr+PCr', ' Tau', ' Tau %SD', ' Tau/Cr+PCr', ' -CrCH2', ' -CrCH2 %SD', ' -CrCH2/Cr+PCr', ' GPC+PCh', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG', ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr', ' Cr+PCr', ' Cr+PCr %SD', ' Cr+PCr/Cr+PCr', ' Glu+Gln', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' Lip13a', ' Lip13a %SD', ' Lip13a/Cr+PCr', ' Lip13b', ' Lip13b %SD', ' Lip13b/Cr+PCr', ' Lip09', ' Lip09 %SD', ' Lip09/Cr+PCr', ' MM09', ' MM09 %SD', ' MM09/Cr+PCr', ' Lip20', ' Lip20 %SD', ' Lip20/Cr+PCr', ' MM20', ' MM20 %SD', ' MM20/Cr+PCr', ' MM12', ' MM12 %SD', ' MM12/Cr+PCr', ' MM14', ' MM14 %SD', ' MM14/Cr+PCr', ' MM17', ' MM17 %SD', ' MM17/Cr+PCr', ' Lip13a+Lip13b', ' Lip13a+Lip13b %SD', ' Lip13a+Lip13b/Cr+PCr', ' MM14+Lip13a+L', ' MM14+Lip13a+L %SD', ' MM14+Lip13a+L/Cr+PCr', ' MM09+Lip09', ' MM09+Lip09 %SD', ' MM09+Lip09/Cr+PCr', ' MM20+Lip20', ' MM20+Lip20 %SD', ' MM20+Lip20/Cr+PCr', 'path', 'series/acq', 'TE', 'name', 'ID', 'age', 'sex', 'weight', 'date of scan']
    #headers_longTE = ['Row', ' Col', ' Ala', ' Ala %SD', ' Ala/Cr+PCr', ' Cr', ' Cr %SD', ' Cr/Cr+PCr', ' PCr', ' PCr %SD', ' PCr/Cr+PCr', ' Gln', ' Gln %SD', ' Gln/Cr+PCr', ' Glu', ' Glu %SD', ' Glu/Cr+PCr', ' GPC', ' GPC %SD', ' GPC/Cr+PCr', ' PCh', ' PCh %SD', ' PCh/Cr+PCr', ' GSH', ' GSH %SD', ' GSH/Cr+PCr', ' Ins', ' Ins %SD', ' Ins/Cr+PCr', ' Lac', ' Lac %SD', ' Lac/Cr+PCr', ' NAA', ' NAA %SD', ' NAA/Cr+PCr', ' NAAG', ' NAAG %SD', ' NAAG/Cr+PCr', ' Scyllo', ' Scyllo %SD', ' Scyllo/Cr+PCr', ' -CrCH2', ' -CrCH2 %SD', ' -CrCH2/Cr+PCr', ' GPC+PCh', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG', ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr', ' Cr+PCr', ' Cr+PCr %SD', ' Cr+PCr/Cr+PCr', ' Glu+Gln', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' Lip13a', ' Lip13a %SD', ' Lip13a/Cr+PCr', ' Lip13b', ' Lip13b %SD', ' Lip13b/Cr+PCr', ' Lip20', ' Lip20 %SD', ' Lip20/Cr+PCr', ' Lip13a+Lip13b', ' Lip13a+Lip13b %SD', ' Lip13a+Lip13b/Cr+PCr', 'path', 'series/acq', 'TE', 'name', 'ID', 'age', 'sex', 'weight', 'date of scan']

    header_without_raw_shortTE = ['Row', ' Col', ' Ala %SD', ' Ala/Cr+PCr', ' Asp %SD', ' Asp/Cr+PCr', ' Cr %SD', ' Cr/Cr+PCr', ' PCr %SD', ' PCr/Cr+PCr', ' GABA %SD', ' GABA/Cr+PCr', ' Glc %SD', ' Glc/Cr+PCr', ' Gln %SD', ' Gln/Cr+PCr', ' Glu %SD', ' Glu/Cr+PCr', ' GPC %SD', ' GPC/Cr+PCr', ' PCh %SD', ' PCh/Cr+PCr', ' GSH %SD', ' GSH/Cr+PCr', ' Ins %SD', ' Ins/Cr+PCr', ' Lac %SD', ' Lac/Cr+PCr', ' NAA %SD', ' NAA/Cr+PCr', ' NAAG %SD', ' NAAG/Cr+PCr', ' Scyllo %SD', ' Scyllo/Cr+PCr', ' Tau %SD', ' Tau/Cr+PCr', ' -CrCH2 %SD', ' -CrCH2/Cr+PCr', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr', ' Cr+PCr %SD', ' Cr+PCr/Cr+PCr', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' Lip13a %SD', ' Lip13a/Cr+PCr', ' Lip13b %SD', ' Lip13b/Cr+PCr', ' Lip09 %SD', ' Lip09/Cr+PCr', ' MM09 %SD', ' MM09/Cr+PCr', ' Lip20 %SD', ' Lip20/Cr+PCr', ' MM20 %SD', ' MM20/Cr+PCr', ' MM12 %SD', ' MM12/Cr+PCr', ' MM14 %SD', ' MM14/Cr+PCr', ' MM17 %SD', ' MM17/Cr+PCr', ' Lip13a+Lip13b %SD', ' Lip13a+Lip13b/Cr+PCr', ' MM14+Lip13a+L %SD', ' MM14+Lip13a+L/Cr+PCr', ' MM09+Lip09 %SD', ' MM09+Lip09/Cr+PCr', ' MM20+Lip20 %SD', ' MM20+Lip20/Cr+PCr', 'path', 'series/acq', 'TE', 'name', 'ID', 'age', 'sex', 'weight', 'date of scan']
    header_without_raw_longTE = ['Row', ' Col', ' Ala %SD', ' Ala/Cr+PCr', ' Cr %SD', ' Cr/Cr+PCr', ' PCr %SD', ' PCr/Cr+PCr', ' Gln %SD', ' Gln/Cr+PCr', ' Glu %SD', ' Glu/Cr+PCr', ' GPC %SD', ' GPC/Cr+PCr', ' PCh %SD', ' PCh/Cr+PCr', ' GSH %SD', ' GSH/Cr+PCr', ' Ins %SD', ' Ins/Cr+PCr', ' Lac %SD', ' Lac/Cr+PCr', ' NAA %SD', ' NAA/Cr+PCr', ' NAAG %SD', ' NAAG/Cr+PCr', ' Scyllo %SD', ' Scyllo/Cr+PCr', ' -CrCH2 %SD', ' -CrCH2/Cr+PCr', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr', ' Cr+PCr %SD', ' Cr+PCr/Cr+PCr', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' Lip13a %SD', ' Lip13a/Cr+PCr', ' Lip13b %SD', ' Lip13b/Cr+PCr', ' Lip20 %SD', ' Lip20/Cr+PCr', ' Lip13a+Lip13b %SD', ' Lip13a+Lip13b/Cr+PCr', 'path', 'series/acq', 'TE', 'name', 'ID', 'age', 'sex', 'weight', 'date of scan']

    ONLY_RELEVANT_HEADERS = [' Glu %SD', ' Glu/Cr+PCr', ' GPC %SD', ' GPC/Cr+PCr', ' Ins %SD', ' Ins/Cr+PCr', ' Lac %SD', ' Lac/Cr+PCr', ' NAA %SD', ' NAA/Cr+PCr', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' MM09+Lip09 %SD', ' MM09+Lip09/Cr+PCr', ' MM20+Lip20 %SD', ' MM20+Lip20/Cr+PCr', 'path', 'series/acq', 'TE', 'name', 'ID', 'age', 'sex', 'weight', 'date of scan']
    #RIGHT NOW WE WANT DATABASE WITHOUT RAW VALUES, ONLY WITH THE CHOSEN MATABOLITS AND WITH INFO KEYS. THIS IS WHAT 'ONLY RELEVENT HEADERS' CONTAINS.


    INFO_KEYS = ['path', 'series/acq', 'TE', 'name', 'ID', 'age', 'sex','weight', 'date of scan']

    LACTAT_MATABOLIT = ' Lac/Cr+PCr'
    LACTAT_SD = ' Lac %SD'

    NORMALIZATION_STRING = '/Cr+PCr'
    SD_STRING = '%SD'

    RELEVANT_MATABOLITS =[' Glu %SD', ' Glu/Cr+PCr', ' GPC %SD', ' GPC/Cr+PCr', ' Ins %SD', ' Ins/Cr+PCr', ' Lac %SD', ' Lac/Cr+PCr', ' NAA %SD', ' NAA/Cr+PCr', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' MM09+Lip09 %SD', ' MM09+Lip09/Cr+PCr', ' MM20+Lip20 %SD', ' MM20+Lip20/Cr+PCr']

    AGE_KEY = 'age'
'''



'''
def write_age_in_months(series):

    age = series[Strings.AGE_KEY][:-1]
    age_type = series[Strings.AGE_KEY][-1]

    if age_type.lower() == 'y':
        age = float(age)*12

    if age_type.lower() == 'm':
        age = float(age)

    if age_type.lower() == 'w':
        age = float(age)/4.2

    if age_type.lower() == 'd':
        age = float(age) / 4.2 / 7

    series[Strings.AGE_KEY] = age
'''
