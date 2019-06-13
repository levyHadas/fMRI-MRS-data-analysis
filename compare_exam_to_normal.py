# we need to see each exam in comparison to other exam with the same parameters. Since each exam has a few serieses which differ in the location and tissue type,
# we need to plot each series
# the prarmaters are: age_group, tissue_type, location and lateralization. These might change in the futur and are all saved in the MRS-strings script.
# each parameter has a few optional values and each series matches one of the values.
# the user can chose weather to plot all the metabolites, or only part of them
# the user can chose to force the parameters, so he will see not only the data that is corsponsive to the series params, but also to other params


import easygui as gui
import os
import sys
import mrs_strings as Strings
import filters as Filters
import plot_and_save as Plot
import collections
import pkl_functions as Pkl_func




def find_exam_pkl (exam_path):
    exam_pkl_path = None
    files = os.listdir(exam_path)
    for file in files:
        if 'pkl' in file:
            exam_pkl_path = os.path.join (exam_path, file)
            break
    if exam_pkl_path == None:
        gui.msgbox("Data is missing for this series. Please add the exam using \"Add New Exam\" before comparing this series.", "OK")
        sys.exit()
    return exam_pkl_path
    # exam_pkl_path = STRING. path



def compare_series_to_normal(series_dict, is_fetal, exam_folder_path):

    print('compare_series_to_normal')

    if series_dict[Strings.TE] == Strings.SHORT_TE or series_dict[Strings.TE] == Strings.SHORT_TE_35:
        seriesTE = Strings.SHORT_TE
    else:
        seriesTE = Strings.LONG_TE

    series_data_set = get_series_data_set(series_dict, seriesTE)
    # series_data_set = DICT
    # first we found the data that we want to compare for this series: series_data_set

    series_filters = Filters.create_filters_from_series(series_dict, seriesTE, is_fetal)
    # series_filters = DICT
    # we find the filters that match - meaning - what is the age group, the TE and and the locations
    # see more info in "Filters" script

    modify_filter = False # CURRENTLY, THIS WILL BE SET TO False ALWAYS, so we won't get this question all the time.
    # after getting the series default filter, we allow the user to modify them
    # modify_filter = gui.ynbox(msg='Do you wish to modify the filter? if not, the filter will be according to the series params:', title='',choices=('Yes', 'No'), default_choice='No', cancel_choice='No') #the first in choices return True, the second returns False
        # need to add text - for which series am I asking this?
    if modify_filter:
        series_filters = Filters.modify_series_filters(series_filters, is_fetal)

    database_pk_path = Strings.PKL_FULL_DATABASE_PATH[is_fetal][seriesTE]
    database_data = Pkl_func.read_pkl(database_pk_path)['clean']
    # we only want to plot the clean data

    database_data_set = find_database_data_set(database_data, series_filters, seriesTE)
    # database_data_set = DICT
    # getting all the series in the database that are corresponding to the series filters: database_data_set


    while len(database_data_set) == 0 and gui.ynbox(msg= "There is no data in the database that co-respond with series              * * " + series_dict[Strings.SERIES_NUM] +
            " * *   filters (TE, age_group, tissue, location). \nwould you like to modify the series filters and try again?",
                                  title='',choices=['Yes', 'No'], default_choice='No', cancel_choice='No'):
            # if we didn't find dataset that fits: we ask the user to change filters and try again
            series_filters = Filters.modify_series_filters(series_filters, is_fetal)
            database_data_set = find_database_data_set(database_data, series_filters, seriesTE)
    if len(database_data_set) != 0:
        # check if no we found data after modifying filters. if there is data - plot it
        Plot.main(series_data_set, database_data_set, series_dict, exam_folder_path)
        # Plot.main OUTPUT = .png files saved in main exam folder, under folder "plots"


def get_series_data_set(series_dict, seriesTE):
    metabolits_values_data_set = collections.OrderedDict()
    for metabolite in Strings.METABOLITS_TO_COMPARE[seriesTE]:
        metabolits_values_data_set[metabolite] = [round(float(series_dict[metabolite]), 3)]
    return metabolits_values_data_set
    # metabolits_values_data_set = DICT of each metabolite and it's value


def find_database_data_set(database_data, filters, seriesTE):
    # database_data = LIST of DICTS where every dict is a series from the dataBase
    metabolits_values_data_set = collections.OrderedDict()
    # ordered dict. Using ordered so ploting will always be the same order

    for series in database_data:
        if series[Strings.NORMAL] == True and check_series_match_to_filters(series, filters):
        # for each line in the database, if the line is a match to current series filters, do:
            for metabolite in Strings.METABOLITS_TO_COMPARE[seriesTE]:
                # for each metabolite that we wish to plot:
                if metabolite in series.keys() and series[metabolite] != '*':
                    # if this metabolite is in this line (suppose to be. this check is only to be safe), and this metabolite has value:
                    # add this value to the dict:
                    if metabolits_values_data_set.has_key(metabolite):
                        metabolits_values_data_set[metabolite].append( round(float(series[metabolite]),3) )
                    else:
                        metabolits_values_data_set[metabolite] = [ round(float(series[metabolite]),3) ]

    if len(metabolits_values_data_set) == 0:
        print("There is no data in the Database that co-respond with the current series filters (TE, age_group, tissue, location")
    return metabolits_values_data_set
    # metabolits_values_data_set =  DICT of each metabolite and it's valueS
    # for each metabolite we have a LIST all the values of all the series that matches the filters
    # dict structure: {metabolite_name1:[value1, value2, value3], metabolite_name2:[value1, value2...],...}


def check_series_match_to_filters(series, filters):

    for single_filter_name in filters.keys():
    # single_filter_name would be onE of: location, tissue, age_group etc.)
        single_filter_match = _check_sub_match(series, single_filter_name, filters[single_filter_name])
        # filter[single_filter_name] will give a list of possible values for the sub_filter_name
        if not single_filter_match:

            return False #if one of the filters does not match - the series does not match the filters and should not be included

    return True #if we got here, it means all sub_filters were a match and the series should be included



def _check_sub_match(series, filter_name, filter): #type(filter) = list of values
    # filter_name = STRING. the filter we are currently checking( TE, age group, tissue, location...)
    # filter = LIST of possible values for the filter in "filter_name"
    for option in filter:
    # if one of the options matches, then the single filter matches
        if filter_name == Strings.AGE_GROUP_NAME:
            if Filters.get_age_group_for_age( series[Strings.PATIENT_AGE] ) == option:
                return True
        else:
            if series[filter_name].lower() == option.lower() :
                return True
    return False
    # if non of the option of the sub_filter matches the series - then the series does not match





# INPUT = exam_dict = DICT, is_fetal = BOOLEAN
# OUTPUT = shows plots of each series in comparision to database
# OUTPUT = saves .png images of the plots in the main exam folder inside folder calles "plots".
def main(exam_folder_path = None, exam_dict = None, is_fetal = None):
    if exam_dict == None:
        # if csv_path = None it means the the user chose "plot series" and he will need to chose the series that he wishes to plot
        exam_folder_path = gui.diropenbox('select the series you wish to see', '', '//fmri-df1/users/MRS_Pediatric/Siemense')
        exam_pkl_path = find_exam_pkl(exam_folder_path)
        # exam_pkl_path = STRING. path
        exam_dict = Pkl_func.read_pkl(exam_pkl_path)
        is_fetal = exam_dict[Strings.PATIENT_INFO][Strings.IS_FETAL]
        # exam_dict = DICT

    # if series_dict is received, it means that we need to plot the series as part of the "adding new exam" process,

    for series_num in exam_dict[Strings.ALL_SERIES].keys():
        series_dict = exam_dict[Strings.PATIENT_INFO].copy()
        series_values = exam_dict[Strings.ALL_SERIES][series_num].copy()
        series_dict.update(series_values)
        # we need to use the series dict, so we locate it in the exam dict and copy it
        # we copy it to avoid problems with pointers
        compare_series_to_normal(series_dict, is_fetal, exam_folder_path)




if __name__ == '__main__':
    main()

