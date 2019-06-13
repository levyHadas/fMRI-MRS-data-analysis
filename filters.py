#when ploting we need to filter the data that is ploted.
#the critiria for filtering is as follwing:
    #filter from series: same TE, same age group, same tissue type, same location
    #filter according to series, but with manual changes: force series filters means that the user can change the filters - we will get a plot of the database according to the manual
        #given parameters and than plot the series. User can only manualy change: age group, tissue type and location. can not change the TE filter
    #filter only according to manualy given params - create filter from user input - this is used when we want to see behaviour in the database and not to compare it
        #to a specific series. Here you can chose: metabolite, TE, age group, Tissue Type and Loacation.
#after the filter is ready, we use "find data set for filters: getting all the serieses in the database the match the filters.



import easygui as gui
import mrs_strings as Strings
import collections
import gui_series_info as Series_gui
from Tkinter import SINGLE, MULTIPLE



# create filters with the same TE, age_group, tissue_type and location as the series we are dealing with
def create_filters_from_series(series_dict, seriesTE, is_fetal): # type(series) = dict

    if not is_fetal:
        age_group = get_age_group_for_age ( series_dict[Strings.PATIENT_AGE] )
        filters = {Strings.AGE_GROUP_NAME:[age_group], Strings.TISSUE_TYPE: [series_dict[Strings.TISSUE_TYPE]],
                   Strings.LOCATION: [series_dict[Strings.LOCATION]]}
    else:
        #need to define age_group for fetus and add this age group to the filter
        filters = {Strings.TISSUE_TYPE: [series_dict[Strings.TISSUE_TYPE]],
                   Strings.LOCATION: [series_dict[Strings.LOCATION]]}

    return filters  # type(filter) = {age_group:[],location:[],tissue:[]} each len(list) = 1
    #the values in the dict are a list in order to be able to add more values when modifying the filters

def get_age_group_for_age (age):

    for group in Strings.AGE_GROUPS.keys():
        if int(float(age)) in range( Strings.AGE_GROUPS[group]['min'], Strings.AGE_GROUPS[group]['max'] ):
            return group


#when plotting a series, sometimes the filters according to the series will be to strict and we would like to change them
#you can force the age_group, the tissue type and the location.
def modify_series_filters(filters, is_fetal):
    if not is_fetal:
        age_group_extra = gui.multchoicebox('which age group would you like to add? (all, one, or more)', '',
                                            Strings.AGE_GROUPS.keys(), preselect=False)
        filters[Strings.AGE_GROUP_NAME].extend(age_group_extra)

    else:
        pass
        #need to define extra age filters for fetus
    #for both:
    current_tissue = filters[Strings.TISSUE_TYPE][0]
    location_extra = gui.multchoicebox('which tissue would you like to add? (all, one, or more)', '',
                                       Strings.LOCATIONS[current_tissue])
    filters[Strings.LOCATION].extend(location_extra)


    #we need to make an option to see all exams and not only the normal ones


    return filters
    #return filters  # type(filter) = {age_group:[],location:[],tissue:[]} each len(list) >= 1
    #get user input for force different params then series








#***********************this function needs work********************************
#for free plotting, we want to chose all the parameters:
def create_filter_from_user_input():
    #return filters # type(filter) = {age_group:[],location:[],tissue:[]} .  each len(list) >= 1
    TE_filter = gui.choicebox(msg='which location would you like to see? (one)', title='',
                              choices=[Strings.SHORT_TE, Strings.LONG_TE])
    age_group_filter = gui.multchoicebox('which age group would you like to see? (all, one, or more)', '', Strings.AGE_GROUPS.keys())
    tissue_type_filter = gui.choicebox('which tissue would you like to see? (only one)', '', Strings.TISSUES)
    location_filter = gui.multchoicebox('which location would you like to see? (all, one, or more)', '', Strings.LOCATIONS[tissue_type_filter])

    filters = {Strings.AGE_GROUP_NAME: age_group_filter, Strings.TISSUE_TYPE: [tissue_type_filter], Strings.LOCATION: location_filter}
    return filters, TE_filter
#***********************this function needed work********************************









#filters = {'tissue': ['MISSING'], 'age_group': ['age_group1'], 'location': ['MISSING']}
#series = {' Asp': ' 1.06E+03', 'laterality': 'MISSING', ' MM20 %SD': '    8', ' NAA+NAAG': ' 2.08E+03', ' MM20+Lip20': ' 3.81E+03', ' -CrCH2/Cr+PCr': '  2.0E-02', ' GPC': '  606.516', ' NAAG/Cr+PCr': '  8.0E-02', ' PCr %SD': '    8', ' Lip20': '    0.000', 'location': 'MISSING', ' Glu+Gln %SD': '    3', ' Ala': '   46.535', ' NAA+NAAG/Cr+PCr': '    1.033', ' Asp %SD': '   11', ' NAAG %SD': '   28', ' MM14+Lip13a+L': ' 3.64E+03', ' Cr+PCr/Cr+PCr': '    1.000', 'name': 'ASRAF.ROMI', ' -CrCH2': '   40.069', 'weight': '9.0', ' GABA/Cr+PCr': '    0.136', ' Lac': '   82.229', ' Lip13a': '  524.351', 'gender': 'F', ' MM20+Lip20 %SD': '    8', ' Lip13a+Lip13b/Cr+PCr': '    0.261', ' GPC+PCh': '  606.516', ' Lip13a+Lip13b %SD': '   71', ' Lip13a+Lip13b': '  524.351', ' Scyllo': '   11.072', ' Glu/Cr+PCr': '    1.344', ' MM14+Lip13a+L/Cr+PCr': '    1.811', ' MM20': ' 3.81E+03', ' Cr+PCr %SD': '    2', ' Ins %SD': '    4', ' Glu+Gln': ' 4.31E+03', ' Glu %SD': '    4', ' MM12 %SD': '   17', ' Scyllo %SD': '  104', ' MM20+Lip20/Cr+PCr': '    1.895', ' Cr %SD': '    8', 'path': '\\\\fmri-df1\\users\\MRS_Pediatric\\Siemense\\ASRAF_ROMI\\MRS\\27_TE30', ' Cr+PCr': ' 2.01E+03', ' Lip20 %SD': '  999', ' MM14 %SD': '   17', ' MM09+Lip09/Cr+PCr': '    0.990', ' PCr/Cr+PCr': '    0.505', ' GPC+PCh/Cr+PCr': '    0.301', ' NAA+NAAG %SD': '    2', 'series/acq': '27', ' -CrCH2 %SD': '  128', ' GSH': ' 1.29E+03', 'Row': '  1', ' Tau/Cr+PCr': '    0.110', ' Lip20/Cr+PCr': '    0.000', ' GPC %SD': '    2', ' MM17/Cr+PCr': '    0.912', ' GABA %SD': '   33', ' Gln': ' 1.60E+03', 'date of birth': '08\\09\\2014', ' Glu+Gln/Cr+PCr': '    2.142', ' Glc': '  817.987', ' Gln %SD': '    7', ' GPC+PCh %SD': '    2', ' MM14+Lip13a+L %SD': '    8', ' Ala %SD': '  113', ' GSH %SD': '    5', ' NAA %SD': '    3', ' Col': '   1', ' Lip09': '    0.000', ' Cr/Cr+PCr': '    0.495', ' MM09': ' 1.99E+03', ' Tau': '  221.778', ' Glc/Cr+PCr': '    0.407', ' Ala/Cr+PCr': '  2.3E-02', ' Tau %SD': '   28', ' PCr': ' 1.02E+03', ' MM20/Cr+PCr': '    1.895', ' PCh': '    0.000', ' Cr': '  995.864', ' PCh %SD': '  999', ' MM09+Lip09 %SD': '    7', ' Glu': ' 2.70E+03', ' MM14/Cr+PCr': '    1.067', ' Lac %SD': '   70', ' Lip13a %SD': '   71', ' MM12': '  971.657', ' MM14': ' 2.15E+03', ' MM17': ' 1.84E+03', ' MM12/Cr+PCr': '    0.483', 'date of scan': '07\\04\\2015', ' Asp/Cr+PCr': '    0.527', ' Lip13a/Cr+PCr': '    0.261', ' Lac/Cr+PCr': '  4.1E-02', ' Lip09 %SD': '  999', ' Lip13b/Cr+PCr': '    0.000', 'tissue': 'MISSING', ' GSH/Cr+PCr': '    0.641', ' GABA': '  274.593', ' MM09/Cr+PCr': '    0.990', ' Lip13b %SD': '  999', ' Lip09/Cr+PCr': '    0.000', ' MM17 %SD': '   16', 'TE': '30', ' PCh/Cr+PCr': '    0.000', ' Ins': ' 1.17E+03', ' Ins/Cr+PCr': '    0.584', ' Scyllo/Cr+PCr': '  5.5E-03', ' MM09+Lip09': ' 1.99E+03', 'ID': '34031310-5', ' NAA/Cr+PCr': '    0.953', ' NAAG': '  161.943', ' NAA': ' 1.92E+03', ' MM09 %SD': '    7', 'age': '7.0', ' GPC/Cr+PCr': '    0.301', ' Glc %SD': '    9', ' Gln/Cr+PCr': '    0.797', ' Lip13b': '    0.000'}
#_check_series_match_to_filters(series, filters)



















