# adding a new MRS exam

# INPUT: exam path - the patient main folder

# OUTPUT:
    # 2 new csv files for EACH SERIES
    # pkl for EXAM
    # updating 2-4 database files (if exam has series with TE30 and series with TE135, it will update 4 files, otherwise it will update 2 files)
    # updating pickle object file
        # for first exam these files will be created


# each exam usually has a few csv - one for each series.

# adding a new MRS exam should include:

# 1. for each series - duplicate and add info:
        # duplicating the CSV twice - first is called spreadsheet_with_info, second is named with subject's ID and the series num and TE
        # the new file contains the following data:
            # patient info --> see info keys in "MRS_strings" script
            # series info --> see series keys in "MRS_strings" script
            # MRS results
    # using the script "add_info"

# 2. for each exam: create a pickle file that holds the PATIENT INFO + SERIES INFO for each of the series(plural) + MRS RESULTS for each of the series
        # each series has the info listed above
        # this pkl holds the patient info with all it's series
        # (see dictionary structure in   )
    # using the script "add_info"

# 3. for each exam: for each series: comparing to standard.
    # this is the all purpose of this project: provide a scala of standard and compare new exam to it
        # get TE value, age group, tissue type and location of this series and save them as comparision parameters.
                # using "filters" script
        # get the MRS results for this series
        # find all series in the database with the same TE, group age, tissue type and location -
            # only get ones that are qualified to set a standard (NORMAL = True)
        # compare the series all the other series with the same parameters

# 4. Adding to databases:
        # for each exam: for each series: adding the series (with all the data listed above) to the corresponding CSV database (fetus/child, TE30/TE135)
        # for each exam: for each series: cleaning the series from irrelevant MRS results (see cleaning definitions in "clean_series" script)
            # adding each clean series (including patient info and series info) to the corresponding CSV CLEAN database (fetus/child, TE30/TE135)
        # for each exam: for each series: adding the series to a pickle dictionary file (see dictionary structure in   )
    # using the script "add_to_database"





import os
import add_info as Add_info
import mrs_strings as Strings
import add_to_database as Add_to_database
import easygui as gui
import compare_exam_to_normal as Compare_exam_to_standard
from pydicom.filereader import dcmread
import pkl_functions as Pkl_func




# the csv file is located in a random folder, so the only way to find it is just to look in all the exam folder
def get_all_csvs_path_for_patient(exam_folder_path):
    all_csvs_path = []
    for root, dirs, files in os.walk(exam_folder_path):
        for file in files:
            if file.endswith('.dcm'):
                break   # csv file will never be inside dcms folder
            if file.endswith('.csv'):
                if root not in all_csvs_path:
                    all_csvs_path.append(root)
    return all_csvs_path



# RGB files are dicom files that are located inside a folder twith name contains RGB
# the dcm description does not indicate it's a rgb
# the rgb folder is located in a random folder, so the only way to find it is just to look in all the exam folder
def get_all_rgbs_for_patient(exam_folder_path):

    all_rgbs_path=[]

    for root, dirs, files in os.walk(exam_folder_path):
        if 'rgb' in root.lower():
            for sub_root, sub_dirs, sub_files in os.walk(root):
                for sub_file in sub_files:
                    if sub_file.endswith('.dcm'):
                        rgb_dcm_path = os.path.join(sub_root, sub_file)
                        rgb_dcm_info = dcmread(rgb_dcm_path)
                        if 'Ser' in rgb_dcm_info.ImageComments:
                            if rgb_dcm_path not in all_rgbs_path:
                                all_rgbs_path.append(rgb_dcm_path)

    return all_rgbs_path





def main(exam_folder = None, is_new_database = False, re_do_add_info = True):

    print ('Add New Exam')

    exam_folder = gui.diropenbox('select the patient\'s folder', '', Strings.MAIN_MRSS_FOLDER)

    all_csvs_path = get_all_csvs_path_for_patient(exam_folder)  # first we need to find all the files with the MRS results
    all_rgbs_path = get_all_rgbs_for_patient(exam_folder)       # need to find the RGB files so we can show the location image when adding the manual info (tissue type and location of MRS)

    pkl_path = os.path.join(exam_folder, 'MRS_data.pkl')        # define a path in which we will save the pkl file. should be in the root folder.

    exam_dict = { Strings.PATIENT_INFO:{}, Strings.ALL_SERIES:{} }
    # define the initial structure of the pkl exam object we will create.

    # eventually the exam dictionary structure will be:
    # exam_dict_=        {
    #                       Strings.PATIENT_INFO:{},
    #                       Strings.ALL_SERIES:
    #                       {
    #                           {SERIES_NUM:series_data}, (series_data include series_data and MRS data)
    #                           {SERIES_NUM:series_data},
    #                           {SERIES_NUM:series_data}
    #                       }
    #                    }
    # series_data = {TE:VALUE, Series_num:VALUE, tissue:VALUE, location:VALUE, metabolite1:VALUE, metaboliet2:VALUE.... last_metabolite1:VALUE}

    # Strings.PATIENT_INFO, Strings.ALL_SERIES - just names. given by me and can be changed.
    # SERIES_NUM - value of the series num according to DICOMS





    # finished creating a csv with the data for each series
    # the exam dict is now updated with this exam info, according to the structure defined above
    exam_dict = Add_info.main(exam_folder, all_csvs_path, all_rgbs_path, exam_dict)

    # save this dict to pickle file.
    Pkl_func.save_pickle(pkl_path, exam_dict)

    is_fetal = exam_dict[Strings.PATIENT_INFO][Strings.IS_FETAL]

    # After adding all the info to the exam and the series, we compare each series to the co-responding data in the database.
    # We plot and see where the exam is in comparison to the normal values.
    try:
        Compare_exam_to_standard.main(exam_folder, exam_dict, is_fetal)
    except:
        # handles the case of first exam, so the database doesn't exist yet
        print("No data to compare to yet")


    # now we add this exam to all the databases.
    # using "add_to_database" script
    Add_to_database.main(exam_dict, is_fetal)




if __name__ == '__main__':
    main()










###############################################################
# old not in use:

#
# def get_series_dict(series_folder_path):
#
#     series_csv_path = None
#     files = os.listdir(series_folder_path)
#     for file in files:
#         if Strings.CSV_WITH_INFO in file:
#             series_csv_path = os.path.join (series_folder_path, file)
#             break
#     if series_csv_path == None:
#         easygui.msgbox("Data is missing for this series. Please add the exam using \"Add New Exam\" before comparing this series.", "OK")
#         sys.exit()
#     series_dict = Read_csv.get_series_data_from_series_csv(series_csv_path)
#
#     return series_dict



# for series_num in exam_dict[Strings.ALL_SERIES].keys():
#     series_dict = exam_dict[Strings.PATIENT_INFO].copy()
#     series_values = exam_dict[Strings.ALL_SERIES][series_num].copy()
#     series_dict.update(series_values)
#     Compare_series_to_normal.main(series_dict, is_fetal)
