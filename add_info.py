#Accept a list of csvs path from "add new exam". These csvs all belong to the same patient - this is important
#we copy the original spreadsheet (it's name is "spreadsheet"). The copy "spreadsheet_with_info has all the info about the patient, the series and the TE
#this script adds info for each CSV - for each CSV it adds the same patient info - name, ID, age, weight.
# for each CSV it adds is uniq values - series num, TE value.
#patien info read from one of the dicoms
#series number and TE values are taken from the PS.PS file that is placed in the same folder as the csv

import os
import shutil
from pydicom.filereader import dcmread
import mrs_strings as Strings
from dateutil.relativedelta import relativedelta
from datetime import date
import matplotlib.pyplot as plt
import easygui as gui


import gui_patient_info_req as patient_gui_req
import gui_patient_info_opt as patient_gui_opt
import gui_series_info as Series_gui
from Tkinter import SINGLE, MULTIPLE
import csv_functions as Csv_func



# getting the info that is not specific to a series, but general to this exam and patient.
# the exam info - exam date, is taken from the info
# for child - the basic patient info is taken from the dicom info
# for fetus - the mother's basic info is taken from the dicom info. Fetus info is entered manually
# INPUT - *PATH* to patient folder.
# RETURNS - patient info values - a *LIST* of all the values
    # only returns values. order of the list is important, because we don't have keys
    # in future version, this should be a dictionary with keys.
def get_patient_info_values(exam_folder, exam_dict):

    dcm_path = _find_dcm_path(exam_folder)  # we need to find any dicom, doesn't matter which one.
    # dcm_path = path. STRING

    dcm_info = dcmread(dcm_path)

    if 'fetus' in dcm_info.StudyDescription.lower() or 'fetal' in dcm_info.StudyDescription.lower():
        is_fetal = True
    else:
        is_fetal = False

    # the original date format is yearMonthDay - I want to make it day/month/year - so i need to break it
    study_date_year = dcm_info.StudyDate[0:4]
    study_date_month = dcm_info.StudyDate[4:6]
    study_date_day = dcm_info.StudyDate[6:8]

    # the age we get from dicoms is not accurate enough, so we find the age according to birth date and scan date
    patient_birth_year = dcm_info.PatientBirthDate[0:4]
    patient_birth_month = dcm_info.PatientBirthDate[4:6]
    patient_birth_day = dcm_info.PatientBirthDate[6:8]
    age = relativedelta( date(int(study_date_year),int(study_date_month),int(study_date_day)), date(int(patient_birth_year),int(patient_birth_month),int(patient_birth_day)) )
    age_in_months = round(age.years*12 + age.months + age.days/30.0, 3)
    age = round(age_in_months, 2)
    birth_date = patient_birth_day + '\\' + patient_birth_month + '\\' + patient_birth_year

    # now we need to add data that we can only get manually
    patient_title = dcm_info.PatientName.family_name + ' ' + dcm_info.PatientName.given_name + ', ID: ' + dcm_info.PatientID

    # first getting the required manual info
    # using script "patient_gui_req" - see more description in script
    fetus_age, main_diagnosis, is_normal = patient_gui_req.main(patient_title, Strings.DIAGNOSES, is_fetal)
    # fetus_age=STRING, main_diagnosis=STRING, is_normal=BOOLEAN
    if fetus_age != None:
        fetus_age = int(fetus_age)

    # getting optional data using script "patient_gui_opt" - see more description in script
    additional_diagnoses, fetus_due_date, fetus_gender, notes = patient_gui_opt.main (patient_title, Strings.DIAGNOSES, is_fetal)
    # additional_diagnoses=LIST of strings, fetus_due_date=STRING, fetus_gender=STRING, notes=STRING

    # combine all the data we have to a LIST
    # this is organized in the long way so it will be easier to understand what are we adding and in which order
        # only values. ORDER OF THE LIST IS IMPORTANT, because we don't have keys until end of function
    if not is_fetal:
        patient_info_values = []
        patient_info_values.append(study_date_day + '\\' + study_date_month + '\\' + study_date_year)
        patient_info_values.append (dcm_info.PatientName.family_name + '.' + dcm_info.PatientName.given_name) # this is the name format I started with, so this will be the name format
        patient_info_values.append (dcm_info.PatientID)
        patient_info_values.append (age)
        patient_info_values.append (birth_date)
        patient_info_values.append (dcm_info.PatientSex)
        patient_info_values.append (dcm_info.PatientWeight.real)
        patient_info_values.append (main_diagnosis)
        patient_info_values.append (is_normal)
        patient_info_values.append (additional_diagnoses)
        patient_info_values.append (str(notes)[0:len(notes)-1])
        patient_info_values.append (is_fetal)
    else:
        patient_info_values = []
        patient_info_values.append(study_date_day + '\\' + study_date_month + '\\' + study_date_year)
        patient_info_values.append(dcm_info.PatientName.family_name + '.' + dcm_info.PatientName.given_name)  # this is the name format I started with, so this will be the name format
        patient_info_values.append(dcm_info.PatientID)
        patient_info_values.append(age)
        patient_info_values.append(fetus_age)
        patient_info_values.append(birth_date)
        patient_info_values.append(fetus_due_date)
        patient_info_values.append(fetus_gender)
        patient_info_values.append(dcm_info.PatientWeight.real)
        patient_info_values.append(main_diagnosis)
        patient_info_values.append(is_normal)
        patient_info_values.append(additional_diagnoses)
        patient_info_values.append(str(notes)[0:len(notes) - 1])
        patient_info_values.append(is_fetal)

    is_fetal = patient_info_values[-1]  # we need to mind this. if changing the order this will be wrong
    patient_info_keys = Strings.INFO_KEYS[is_fetal]
    # pediatric and fetal exams have different patient info values and keys.

    patient_info_dict = dict(zip(patient_info_keys, patient_info_values))

    exam_dict[Strings.PATIENT_INFO].update(patient_info_dict)

    return exam_dict, patient_info_values



# To get patient info we need to read the dicom header.
# We search the patient folder until we find A dicom.
# RETURNS the dicom *PATH* - string
def _find_dcm_path(exam_folder_path):
    for root, dirs, files in os.walk(exam_folder_path):
        for file in files:
            if file.endswith('.dcm'):
                dcm_path = os.path.join(root, file)
                return dcm_path


def add_data_to_each_series(all_csvs_path, all_RGBs_path, exam_dict, patient_info_values):

    #is_fetal = patient_info_values[-1]
    is_fetal = exam_dict[Strings.PATIENT_INFO][Strings.IS_FETAL]

    for single_csv_path in all_csvs_path:
    # go through all the CSVS (one csv for each series) and add the data for the series to the csv with info

        print('* Current csv  path is: ' + single_csv_path + ' *')

        series_values = get_series_data(single_csv_path, all_RGBs_path)
        # series_values = LIST. getting TE, location, and tissue for series. also getting csv path
        # we have the patient info, now for each series we need to find it's data
        # if future version series_values should be a dict

        temp_ID = exam_dict[Strings.PATIENT_INFO][Strings.PATIENT_ID]
        if '-' in temp_ID:
            temp_ID = temp_ID.replace('-','')
        temp_series_num = series_values[1]
        temp_TE = series_values[2]
        # when "series_values" will be a dict, series_num and TE would be found according to keys.
        new_csv_name = 'MRS_results_ID.' + temp_ID + '.SE' + temp_series_num + '.TE' + temp_TE + '.csv'

        # for the following lines:
        # In future version I should create a dict to write to the CSV file and not send it in lists. This is bad but I don't have time to change.
        # I have to use "patient_info_values" here and not "exam_dict[Strings.PATIENT_INFO]" since the order is important:
            # I collect a list of all the headers and a list of all the values and write the headers in order and after them the values in order.
            # should fix it ASAP, it can create big problems.
        patient_series_values = patient_info_values + series_values
        # LIST. this holds all the data (only values) except for the metabolites Keys and Results (the MRS keys and values).

        MRS_keys, MRS_values = Csv_func.read_series_MRS_keys_values(os.path.join(single_csv_path, Strings.CSV_ORIG))
        # LIST, LIST
        # We read the original MRS results from the original file

        exam_dict = update_exam_dict(exam_dict, temp_series_num, series_values, MRS_keys, MRS_values)

        keys = Strings.INFO_KEYS[is_fetal] + Strings.SERIES_KEYS + MRS_keys
        values = patient_series_values + MRS_values
        save_info_to_series_csv (single_csv_path, new_csv_name, keys, values)

    return exam_dict


def get_series_data(single_csv_path, all_RGBs_path):

    series_num, TE = read_TE_and_series_from_ps(single_csv_path)
    # series = STRING, TE = STRING
    # first get the TE ans series number corresponding to this csv
    # these values can be found in the ps file

    series_description = 'current series: TE =' + ' ' + TE + ' , series number =' + ' ' + series_num
    # getting the series description for the presentation of the RGB files
    show_series_RGB (series_num, all_RGBs_path)
    # after seeing thr RGB for the series, the user can code the location, tissue type.

    tissue = Series_gui.main(series_description, 'Select the tissue type', Strings.TISSUES, SINGLE)
    # using script "series_gui". Single selection.
    # tissue = STRING
    location = Series_gui.main(series_description, 'Select the location', Strings.LOCATIONS[tissue], SINGLE)
    # using script "series_gui". Single selection.
    # location = STRING

    series_values = [single_csv_path, series_num, TE, tissue, location]
    # make a list of this csv specific data - series num, TE and it's path and returning this list

    return series_values
    # series_values = LIST


# in this function we need to find the PS.PS file that is in closest folder to our csv path.
# We go to the CSV path and dig in until we find the PS.PS file. usually it will be in the same folder, but we can't be sure.
def read_TE_and_series_from_ps (csv_path):
    for root, dirs, files in os.walk(csv_path):
        for file in files:
            if file.endswith('.ps') or file.endswith('.PS'):
                ps_file = open ( os.path.join(csv_path,file) )
                line = None
                while line != '':
                    # read the file until we find the line that holds the 'TR/TE/NS' and the 'Series/Acq'
                    line = ps_file.readline()
                    if 'TR/TE/NS' in line and 'Series/Acq' in line:
                        series_TE_line = line # once we found this line we save it
                        series, TE = _get_series_and_TE_values_from_string(series_TE_line)
                        # series = STRING, TE = STRING. break the string in order to get the series and TE values
                        # once we found the series and TE values we can stop looking and return the values
                        return series, TE
                        # series = STRING, TE= STRING



def _get_series_and_TE_values_from_string(TE_SE_string):
    # the string looks like this: '25/1 \\(2018.04.30 17:39\\) svs_se_30  TR/TE/NS=2000/30/80,  3.375E+00mL \\(M)s}lst\n'

    se_temp = TE_SE_string.split('Series/Acq=')[1]
    # zero part of the line is beginning until 'Series/Acq=', first part of line is after 'Series/Acq=' and until end of line - we want the first part of the line, because it holds the series value
    series = se_temp.split('/')[0]

    te_temp = TE_SE_string.split('TR/TE/NS=')[1]
    TE = te_temp.split('/')[1]
    # TR is in zero place, TE in first, NS and the rest of the line is in second place

    return series, TE
    # series = STRING, TE= STRING




def show_series_RGB (series_num, all_RGBs):
    # all_RGBs is a list of all the RGBS path for the patient (for all series)

    for RGB in all_RGBs: # RGB is a RGB path

        RGB_dcm_info = dcmread(RGB)
        RGB_series_num = RGB_dcm_info.ImageComments.split(' ')[1]

        if RGB_series_num == series_num:
            # if the RGB series num matches ths series num for current series:
            display_dcm_img(RGB, series_num)
            # open the file with title of the series name
            # opening the file with os.system ('\"' + RGB + '\"') doesn't work for DF1 server, so this is a work around.


def display_dcm_img (RGB_path, series_num):

    # get the image ready:
    dicom_file = dcmread(RGB_path)
    dicom_img = dicom_file.pixel_array
    # this is writen the long way for more to understand what I'm doing here

    # get the figure ready:
    figure_axes = plt.axes()
    # get axes object
    plt.Axes.set_axis_off(figure_axes)
    # we don't want to see axes, only image
    plt.suptitle('* RGB for series: ' + series_num + ' * ', fontsize=14)
    plt.title('(in path: ' + RGB_path + ')', fontsize=8)
    plt.imshow(dicom_img)

    plt.show()



def update_exam_dict(exam_dict, series_num, series_values, MRS_keys, MRS_values):
    series_dict = dict(zip(Strings.SERIES_KEYS, series_values))
    series_dict.update(dict(zip(MRS_keys, MRS_values)))
    # add to all series to a dict of this series
    # the dict is already updated with the patient info (we did this in "get_patient_info_values"+main)
    exam_dict[Strings.ALL_SERIES].update({series_num: series_dict})
    return exam_dict




# this function creates 2 csv files for current series.
# if CSV with file already exist, it creates a folder with today's date, save the old file there with the name "backup" and create 2 new files.
def save_info_to_series_csv(single_csv_path, new_csv_name, keys, values):

    csv_with_info_path_generic = os.path.join(single_csv_path, Strings.CSV_WITH_INFO)
    csv_with_info_path_details = os.path.join(single_csv_path, new_csv_name)

    csv_with_info_exist = os.path.isfile(csv_with_info_path_details)
    if csv_with_info_exist:
        # if there is already a csv with data, we need to make sure not to lose it, since some params are entered manually and will not be saved anywhere else
        override = gui.ynbox(msg='CSV with data already exist for this series, do you wish to override? DATA REGARDING TISSUE TYPE, LOCATION AND LATERALIZATION WILL HAVE TO BE RE-ENTERED MANUALLY', choices=('Yes', 'No'), default_choice='No', cancel_choice='No')
        if override:
        # title='WARNING!', choices=('Yes', 'No'), default_choice='No', cancel_choice='No')
            back_up_csv_with_data(single_csv_path)
            # if user want to override, we will save a backup up of the current file.
        else:
            print('* file already existed and was not override *')
            return
            # if user does not wish to override, we will continue with the current file and won't change it.

    shutil.copyfile(os.path.join(single_csv_path, Strings.CSV_ORIG),
                    csv_with_info_path_generic)
    # copy the original CSV - we don't want to touch it - save csv file with info with generic name
    shutil.copyfile(os.path.join(single_csv_path, Strings.CSV_ORIG),
                    csv_with_info_path_details)
    # copy the original CSV - we don't want to touch it - save csv file with info with informative name

    Csv_func.write_series_to_series_csv(csv_with_info_path_generic, keys, values)  # now write the data to the new file
    Csv_func.write_series_to_series_csv(csv_with_info_path_details, keys, values)  # now write the data to the new file


def back_up_csv_with_data(csv_path):
    today_dir = os.path.join(csv_path, str(date.today()))
    if not os.path.isdir(today_dir):
        os.mkdir(today_dir)  # make a new folder with today's date
    shutil.copyfile(os.path.join(csv_path, Strings.CSV_WITH_INFO),
                    os.path.join(today_dir,
                                 Strings.CSV_WITH_INFO_BACKUP))
    # make a copy of the csv_with_info in the today folder














def main(exam_folder,all_csvs_path, all_RGBs_path, exam_dict):

    print('Add Info to Exam and Series')

    exam_dict, patient_info_values = get_patient_info_values(exam_folder, exam_dict)
    # getting the info that is not specific to a series, but to all the series for this patient
    # exam_dict = DICT, patient_info_values = LIST

    exam_dict = add_data_to_each_series(all_csvs_path, all_RGBs_path, exam_dict, patient_info_values)

    return exam_dict




if __name__ == '__main__':
    main()

















'''

    #is_fetal = patient_info_values[-1] # we need to mind this. if changing the order this will be wrong
    #patient_info_keys = Strings.INFO_KEYS[is_fetal]
    # pediatric and fetal exams have different patient info values and keys.

    #exam_dict[Strings.PATIENT_INFO] = dict(zip(patient_info_keys,patient_info_values))


def find_rda_and_dcm_path(exam_folder_path):
    rda_path = None
    dcm_path = None
    for root, dirs, files in os.walk(exam_folder_path):
        for file in files:
            if file.endswith('.rda') and rda_path == None:
                rda_path = os.path.join(root, file)
            if file.endswith('.dcm') and dcm_path == None:
                dcm_path = os.path.join(root, file)
                break
        if rda_path != None and dcm_path != None:
            return rda_path, dcm_path



def get_all_csvs_path_for_patient(exam_folder_path):
    all_csvs_path=[]
    for root, dirs, files in os.walk(exam_folder_path):
        for file in files:
            if file.endswith('.dcm'):
                break
            if file.endswith('.csv') or file.endswith('.xslx') or file.endswith('.xsl'):
                all_csvs_path.append(root)
                #I need to duplicate that file and give it a name: spreadsheet_with_data.xsl
    return all_csvs_path

'''

'''
def find_patient_weight_from_rda(rda_file_path):
    with open(rda_file_path, 'rb') as rda_file:
        for line in rda_file:
            if Strings.WEIGHT in line:
                return line.split(':')[1].split(' ')[1].split('.')[0]
'''
#patient_info_dict={}  #currently not using this dictionary, but maybe in the futur i'll need it
# patient_info_dict[Strings.PATIENT_NAME] = last_name + '.' + first_name
# patient_info_dict[Strings.PATIENT_ID] = dcm_info.PatientID
# patient_info_dict[Strings.PATIENT_AGE] = dcm_info.PatientAge
# patient_info_dict[Strings.PATIENT_SEX] = dcm_info.PatientSex
# patient_info_dict[Strings.PATIENT_WEIGHT] = dcm_info.PatientWeight
# patient_info_dict[Strings.SCAN_DATE] = dcm_info.StudyDate



'''
class Strings:
    PATIENT_NAME = 'name'
    PATIENT_ID = 'ID'
    PATIENT_AGE = 'age'
    PATIENT_SEX = 'sex'
    PATIENT_WEIGHT = 'weight'
    SCAN_DATE = 'date of scan'
    SERIES_NUM = 'series/acq'
    CSV_PATH = 'path'
    TE = 'TE'
    PLACE = 'place'
'''
