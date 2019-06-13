# -*- coding: cp1255 -*-

SERIES_NUM = 'series/acq'
CSV_PATH = 'path'
TE = 'TE'
TISSUE_TYPE = 'tissue'
LOCATION = 'location'


SCAN_DATE = 'date of scan'
PATIENT_NAME = 'Name'
PATIENT_ID = 'ID'
PATIENT_AGE = 'Age (months)'
MOTHER_AGE = 'Mother Age'
FETUS_AGE = 'Fetus age (weeks)'
PATIENT_BIRTH_DATE = 'date of birth'
MOTHER_BIRTH_DATE = 'Mother Date of Birth'
FETUS_BIRTH_DATE = 'due date'
PATIENT_GENDER = 'gender'
FETUS_GENDER = 'Fetus gender'
PATIENT_WEIGHT = 'weight'
MOTHER_WEIGHT = 'Mother Weight'
DIAGNOSIS = 'diagnosis'
NORMAL = 'normal?'
MORE_DIAG = 'addtional diagnosis'
NOTES = 'notes'
IS_FETAL = 'Fetal?'

CSV_WITH_INFO = 'spreadsheet_with_info.csv'
CSV_WITH_INFO_BACKUP = 'spreadsheet_with_info_backup.csv'
CSV_ORIG = 'spreadsheet.csv'

SHORT_TE = '30'
SHORT_TE_35 = '35' #in rare case the TE will be 35. We need to address it as if it was 30
LONG_TE_130 = '130' #in rare cases the TE will be 130. We nned to address it as if it was 135
LONG_TE = '135'
CHILD = 'children'
FETAL = 'fetals'
CLEAN = 'clean'
FULL = 'full'
PATIENT_INFO = 'Patient Info'
ALL_SERIES = 'All Series'

LACTAT_METABOLIT = ' Lac/Cr+PCr'
LACTAT_SD = ' Lac %SD'

NORMALIZATION_STRING = '/Cr+PCr'
SD_STRING = '%SD'

AGE_GROUP_NAME = 'age_group'



#all the above are just names, in order to not use strings in the code itself
#if we ever need to change any name, like file name, or any header, we can change the string here and it will change in any place in the code.










INFO_KEYS_CHILD = [SCAN_DATE, PATIENT_NAME, PATIENT_ID,
                           PATIENT_AGE, PATIENT_BIRTH_DATE, PATIENT_GENDER,
                             PATIENT_WEIGHT, DIAGNOSIS, NORMAL, MORE_DIAG, NOTES, IS_FETAL]
INFO_KEYS_FETAL = [SCAN_DATE, PATIENT_NAME, PATIENT_ID,
                           MOTHER_AGE, FETUS_AGE, MOTHER_BIRTH_DATE, FETUS_BIRTH_DATE, FETUS_GENDER,
                             MOTHER_WEIGHT, DIAGNOSIS, NORMAL, MORE_DIAG, NOTES, IS_FETAL]

INFO_KEYS = {True:INFO_KEYS_FETAL, False:INFO_KEYS_CHILD}

#info keys = data that is unique for this subject and is not unique for a series.
    #the info keys are different for a fetus or a child 
    #(fetus contain info about the mother as well as the fetus)
#in order to avoid constant check if the current subject is a child or a fetus, the info keys are arranged in a dictionary. 
    #Keys for this dict are True and False (as answer to "is_fetal")
    #dict[True] holds info keys for fetal. Dict[False] holds info keys for child.




SERIES_KEYS = [CSV_PATH, SERIES_NUM, TE, TISSUE_TYPE, LOCATION]
#series keys = data that is unique for a series – things like the sample tissus and location and the TE value.
    # series keys are the same for a fetus and child 






#there are a few files that we create and access:

#csv databases files: 8 files
    #csv databases with full data:
            #csv database for children
                    #csv database for TE30 (and 35)
                    #csv database for TE135 (and 130) 
            #csv database for fetuses 
                    #csv database for TE30 (and 35)
                    #csv database for TE135 (and 130) 
    #csv databases with clean data – 
        #only holds the data that was defined by Dafna and Moran as relevant:
        # 4 files – same as the full database files
#pickel databases: 4 files
    #pkl databases for fetuses - full and clean
        #pkl database for TE30 (and 35)
        #pkl database for TE135 (and 130)
    #pkl databases for children - full and clean
        #same stractur as fetuses


MAIN_MRSS_FOLDER = '//fmri-df1/users/MRS_Pediatric/Siemense'

children_dataBase_shortTE_path = 'M:\\clinica\Hadas\\MRS\\databases\\children.MRS.dataBase.shortTE.csv'
children_dataBase_longTE_path = 'M:\\clinica\\Hadas\\MRS\\databases\\children.MRS.dataBase.longTE.csv'
fetal_dataBase_shortTE_path = 'M:\\clinica\Hadas\\MRS\\databases\\fetal.MRS.dataBase.shortTE.csv'
fetal_dataBase_longTE_path = 'M:\\clinica\\Hadas\\MRS\\databases\\fetal.MRS.dataBase.longTE.csv'



CSV_FULL_DATABASE_PATH = {      True:{  SHORT_TE:fetal_dataBase_shortTE_path,
                                        LONG_TE:fetal_dataBase_longTE_path  },
                                False:{ SHORT_TE:children_dataBase_shortTE_path,
                                        LONG_TE:children_dataBase_longTE_path}
                        }


fetal_clean_dataBase_shortTE_path = 'M:\\clinica\\Hadas\\MRS\\databases\\fetal.MRS.dataBase.shortTE.CLEANED.csv'
fetal_clean_dataBase_longTE_path = 'M:\\clinica\\Hadas\\MRS\\databases\\fetal.MRS.dataBase.longTE.CLEANED.csv'
children_clean_dataBase_shortTE_path = 'M:\\clinica\\Hadas\\MRS\\databases\\children.MRS.dataBase.shortTE.CLEANED.csv'
children_clean_dataBase_longTE_path = 'M:\\clinica\\Hadas\\MRS\\databases\\children.MRS.dataBase.longTE.CLEANED.csv'

CSV_CLEAN_DATABASE_PATH = {      True:{  SHORT_TE:fetal_clean_dataBase_shortTE_path,
                                         LONG_TE:fetal_clean_dataBase_longTE_path  },
                                False:{ SHORT_TE:children_clean_dataBase_shortTE_path,
                                        LONG_TE:children_clean_dataBase_longTE_path}
                        }

#in order to have easy access to the relevant database, the **paths** are arranged in a dictionary:
#one dict for full databases and one for clean database. - they have the same stracture
    #Keys for these dict are True and False (as answer to "is_fetal")
    #dict[True] holds paths to databases for fetal. Dict[False] holds paths to databases for child.
        #inside each dict the keys are: SHORT_TE and LONG_TE
            #dict[SHORT_TE] holds the path to the database of all the series with TE=30/35
            #dict[LONG_TE] holds the path to the database of all the series with TE=135/130




CHILDREN_DATABASE_PKL_PATH_SHORT_TE = 'M:\\clinica\\Hadas\\MRS\\databases\\children_database_pkl_shortTE.pkl'
CHILDREN_DATABASE_PKL_PATH_LONG_TE = 'M:\\clinica\\Hadas\\MRS\\databases\\children_database_pkl_longTE.pkl'
FETAL_DATABASE_PKL_PATH_SHORT_TE = 'M:\\clinica\\Hadas\\MRS\\databases\\children_database_pkl_shortTE.pkl'
FETAL_DATABASE_PKL_PATH_LONG_TE = 'M:\\clinica\\Hadas\\MRS\\databases\\children_database_pkl_longTE.pkl'

PKL_FULL_DATABASE_PATH = {      True:{  SHORT_TE:FETAL_DATABASE_PKL_PATH_SHORT_TE,
                                        LONG_TE:FETAL_DATABASE_PKL_PATH_LONG_TE  },
                                False:{ SHORT_TE:CHILDREN_DATABASE_PKL_PATH_SHORT_TE,
                                        LONG_TE:CHILDREN_DATABASE_PKL_PATH_LONG_TE}
                        }

#in order to have easy access to the relevant database, the **paths** are arranged in a dictionary:
    #Keys for this dict are True and False (as answer to "is_fetal")
    #dict[True] holds paths to databases for fetal. Dict[False] holds paths to databases for child.
        #inside each dict the keys are: SHORT_TE and LONG_TE
            #dict[SHORT_TE] holds the path to the database of all the series with TE=30/35
            #dict[LONG_TE] holds the path to the database of all the series with TE=135/130

#the pkl database dict structur is:
# {full:{
#       True(as answer to is_fetal):
#                {
#                   SHORT_TE:   {series_num:{series_data_as_dict}, series_num:{series_data_as_dict}.....},
#                   LONG_TE:    {series_num:{series_data_as_dict}, series_num:{series_data_as_dict}.....}
#                },
#       False:
#                {
#                   SHORT_TE:   {series_num:{series_data_as_dict}, series_num:{series_data_as_dict}.....},
#                   LONG_TE:    {series_num:{series_data_as_dict}, series_num:{series_data_as_dict}.....}
#                }
#       },
#  clean:        
#       True(as answer to is_fetal):
#                {
#                   SHORT_TE:   {series_num:{series_data_as_dict}, series_num:{series_data_as_dict}.....},
#                   LONG_TE:    {series_num:{series_data_as_dict}, series_num:{series_data_as_dict}.....}
#                },
#       False:
#                {
#                   SHORT_TE:   {series_num:{series_data_as_dict}, series_num:{series_data_as_dict}.....},
#                   LONG_TE:    {series_num:{series_data_as_dict}, series_num:{series_data_as_dict}.....}
#                }
#       }}



METABOLITS_SHORT_TE = ['Row', ' Col', ' Ala', ' Ala %SD', ' Ala/Cr+PCr', ' Asp', ' Asp %SD', ' Asp/Cr+PCr',
                    ' Cr', ' Cr %SD', ' Cr/Cr+PCr', ' PCr', ' PCr %SD', ' PCr/Cr+PCr', ' GABA', ' GABA %SD',
                    ' GABA/Cr+PCr', ' Glc', ' Glc %SD', ' Glc/Cr+PCr', ' Gln', ' Gln %SD', ' Gln/Cr+PCr',
                    ' Glu', ' Glu %SD', ' Glu/Cr+PCr', ' GPC', ' GPC %SD', ' GPC/Cr+PCr', ' PCh', ' PCh %SD',
                    ' PCh/Cr+PCr', ' GSH', ' GSH %SD', ' GSH/Cr+PCr', ' Ins', ' Ins %SD', ' Ins/Cr+PCr',
                    ' Lac', ' Lac %SD', ' Lac/Cr+PCr', ' NAA', ' NAA %SD', ' NAA/Cr+PCr', ' NAAG', ' NAAG %SD',
                    ' NAAG/Cr+PCr', ' Scyllo', ' Scyllo %SD', ' Scyllo/Cr+PCr', ' Tau', ' Tau %SD', ' Tau/Cr+PCr', ' -CrCH2',
                    ' -CrCH2 %SD', ' -CrCH2/Cr+PCr', ' GPC+PCh', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG', ' NAA+NAAG %SD',
                    ' NAA+NAAG/Cr+PCr', ' Cr+PCr', ' Cr+PCr %SD', ' Cr+PCr/Cr+PCr', ' Glu+Gln', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr',
                    ' Lip13a', ' Lip13a %SD', ' Lip13a/Cr+PCr', ' Lip13b', ' Lip13b %SD', ' Lip13b/Cr+PCr', ' Lip09',
                    ' Lip09 %SD', ' Lip09/Cr+PCr', ' MM09', ' MM09 %SD', ' MM09/Cr+PCr', ' Lip20', ' Lip20 %SD',
                    ' Lip20/Cr+PCr', ' MM20', ' MM20 %SD', ' MM20/Cr+PCr', ' MM12', ' MM12 %SD', ' MM12/Cr+PCr',
                    ' MM14', ' MM14 %SD', ' MM14/Cr+PCr', ' MM17', ' MM17 %SD',' MM17/Cr+PCr', ' Lip13a+Lip13b',
                    ' Lip13a+Lip13b %SD', ' Lip13a+Lip13b/Cr+PCr', ' MM14+Lip13a+L', ' MM14+Lip13a+L %SD',
                    ' MM14+Lip13a+L/Cr+PCr', ' MM09+Lip09', ' MM09+Lip09 %SD', ' MM09+Lip09/Cr+PCr', ' MM20+Lip20',
                    ' MM20+Lip20 %SD',' MM20+Lip20/Cr+PCr']

METABOLITS_LONG_TE = ['Row', ' Col', ' Ala', ' Ala %SD', ' Ala/Cr+PCr', ' Cr', ' Cr %SD', ' Cr/Cr+PCr', ' PCr',
                   ' PCr %SD', ' PCr/Cr+PCr',' Gln', ' Gln %SD', ' Gln/Cr+PCr', ' Glu', ' Glu %SD',
                   ' Glu/Cr+PCr', ' GPC', ' GPC %SD', ' GPC/Cr+PCr', ' PCh',' PCh %SD', ' PCh/Cr+PCr',
                   ' GSH', ' GSH %SD', ' GSH/Cr+PCr', ' Ins', ' Ins %SD', ' Ins/Cr+PCr', ' Lac', ' Lac %SD',
                   ' Lac/Cr+PCr', ' NAA', ' NAA %SD', ' NAA/Cr+PCr', ' NAAG', ' NAAG %SD', ' NAAG/Cr+PCr',
                   ' Scyllo', ' Scyllo %SD', ' Scyllo/Cr+PCr', ' -CrCH2', ' -CrCH2 %SD', ' -CrCH2/Cr+PCr',
                   ' GPC+PCh', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr',' NAA+NAAG', ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr',
                   ' Cr+PCr', ' Cr+PCr %SD', ' Cr+PCr/Cr+PCr', ' Glu+Gln',' Glu+Gln %SD', ' Glu+Gln/Cr+PCr',
                   ' Lip13a', ' Lip13a %SD', ' Lip13a/Cr+PCr', ' Lip13b', ' Lip13b %SD',' Lip13b/Cr+PCr',' Lip20',
                   ' Lip20 %SD', ' Lip20/Cr+PCr', ' Lip13a+Lip13b', ' Lip13a+Lip13b %SD',' Lip13a+Lip13b/Cr+PCr']

METABOLITS_ALL = {SHORT_TE:METABOLITS_SHORT_TE, LONG_TE:METABOLITS_LONG_TE}

#in order to make sure we are wrting each series to the right TE database, we predefine the metabolits names:
#since they are different to TE30 and TE135, this is a test that we always write to the right one.




RELEVANT_METABOLITS_SHORT_TE = [' Glu %SD', ' Glu/Cr+PCr', ' GPC %SD', ' GPC/Cr+PCr', ' Ins %SD', ' Ins/Cr+PCr',
                         ' Lac %SD', ' Lac/Cr+PCr', ' NAA %SD', ' NAA/Cr+PCr', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr',
                         ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' MM09+Lip09 %SD',
                         ' MM09+Lip09/Cr+PCr', ' MM20+Lip20 %SD', ' MM20+Lip20/Cr+PCr']

RELEVANT_METABOLITS_LONG_TE = [' Glu %SD', ' Glu/Cr+PCr', ' GPC %SD', ' GPC/Cr+PCr', ' Ins %SD', ' Ins/Cr+PCr',
                         ' Lac %SD', ' Lac/Cr+PCr', ' NAA %SD', ' NAA/Cr+PCr', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr',
                         ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' MM09+Lip09 %SD',
                         ' MM09+Lip09/Cr+PCr', ' MM20+Lip20 %SD', ' MM20+Lip20/Cr+PCr']

RELEVANT_METABOLITS_ALL = {SHORT_TE:RELEVANT_METABOLITS_SHORT_TE, LONG_TE:RELEVANT_METABOLITS_LONG_TE}

  








METABOLITS_TO_COMPARE_LONG = [' Glu/Cr+PCr', ' GPC/Cr+PCr', ' Ins/Cr+PCr', ' Lac/Cr+PCr', ' NAA/Cr+PCr',
                        ' GPC+PCh/Cr+PCr', ' NAA+NAAG/Cr+PCr', ' Glu+Gln/Cr+PCr']
METABOLITS_TO_COMPARE_SHORT = METABOLITS_TO_COMPARE_LONG + [' MM09+Lip09/Cr+PCr', ' MM20+Lip20/Cr+PCr']

METABOLITS_TO_COMPARE = {SHORT_TE : METABOLITS_TO_COMPARE_SHORT ,LONG_TE : METABOLITS_TO_COMPARE_LONG}


DIAGNOSIS1_healthy = '1. Healthy'  #TAKIN
DIAGNOSIS2_developmental_disability = '2. Developmental Disability' #ICHUR ITPATHUTI
DIAGNOSIS3_metabolic_disease = '3. Metabolic Disease'
DIAGNOSIS4_preemie = '4. Preemie'
DIAGNOSIS5_autism = '5. Autism'
DIAGNOSIS6_epilepsy = '6. Epilepsy'
DIAGNOSIS7_CMV = '7. CMV'
DIAGNOSIS8_IUGR = '8. IUGR'
DIAGNOSIS9_genetic_syndrome = '9. Genetic Syndrome'
DIAGNOSIS10_lesion = '10. Lesion'
DIAGNOSIS11_other = '11. Other'


DIAGNOSES = [DIAGNOSIS1_healthy, DIAGNOSIS2_developmental_disability, DIAGNOSIS3_metabolic_disease, DIAGNOSIS4_preemie, DIAGNOSIS5_autism,
             DIAGNOSIS6_epilepsy, DIAGNOSIS7_CMV, DIAGNOSIS8_IUGR, DIAGNOSIS9_genetic_syndrome, DIAGNOSIS10_lesion, DIAGNOSIS11_other]



MY_PATH = 'M:\\clinica\\Hadas\\MRS'

AGE_GROUPS = {'age_group1':{'min':0,'max': 25}, 'age_group2':{'min':25,'max': 1200} } #25 because range does not includ the max value


TISSUE1 = 'White Matter' #ONCE WE HAVE THE DATA, THIS SHOULD BE WM
TISSUE2 = 'Lesion'
TISSUE3 = 'Nuclei'
TISSUE4 = 'Cerebellum'
TISSUE5 = 'Other'

TISSUES = [TISSUE1, TISSUE2, TISSUE3, TISSUE4, TISSUE5]



TISSUE1_LOCATION1 = 'Frontal'
TISSUE1_LOCATION2 = 'Occipital'

TISSUE2_LOCATION1 = 'White Matter'
TISSUE2_LOCATION2 = 'Brainstem'
TISSUE2_LOCATION3 = 'Cerebellum'

OTHER_TISSUES_LOCATIONS = 'Other'


LOCATIONS = {TISSUE1:[TISSUE1_LOCATION1, TISSUE1_LOCATION2], TISSUE2:[TISSUE2_LOCATION1, TISSUE2_LOCATION2, TISSUE2_LOCATION3],
             TISSUE3:[OTHER_TISSUES_LOCATIONS], TISSUE4:[OTHER_TISSUES_LOCATIONS], TISSUE5:[OTHER_TISSUES_LOCATIONS]}

















########     old, not in use                  ##################

#RELEVANT_MATABOLITS_AND_SD =[' Glu %SD', ' Glu/Cr+PCr', ' GPC %SD', ' GPC/Cr+PCr', ' Ins %SD', ' Ins/Cr+PCr', ' Lac %SD',
#                      ' Lac/Cr+PCr', ' NAA %SD', ' NAA/Cr+PCr', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG %SD',
#                      ' NAA+NAAG/Cr+PCr', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' MM09+Lip09 %SD', ' MM09+Lip09/Cr+PCr',
#                      ' MM20+Lip20 %SD', ' MM20+Lip20/Cr+PCr']

# RELEVANT_METABOLITS_SHORT_TE = [' Glu/Cr+PCr', ' GPC/Cr+PCr', ' Ins/Cr+PCr', ' Lac/Cr+PCr', ' NAA/Cr+PCr',
#                        ' GPC+PCh/Cr+PCr', ' NAA+NAAG/Cr+PCr', ' Glu+Gln/Cr+PCr',' MM09+Lip09/Cr+PCr', ' MM20+Lip20/Cr+PCr']
#
# RELEVANT_METABOLITS_LONG_TE = [' Glu/Cr+PCr', ' GPC/Cr+PCr', ' Ins/Cr+PCr', ' Lac/Cr+PCr', ' NAA/Cr+PCr',
#                        ' GPC+PCh/Cr+PCr', ' NAA+NAAG/Cr+PCr', ' Glu+Gln/Cr+PCr']
#
#
# HEADERS_NO_RAW_SHORT_TE = ['Row', ' Col', ' Ala %SD', ' Ala/Cr+PCr', ' Asp %SD', ' Asp/Cr+PCr', ' Cr %SD',
#                            ' Cr/Cr+PCr', ' PCr %SD', ' PCr/Cr+PCr', ' GABA %SD', ' GABA/Cr+PCr', ' Glc %SD',
#                            ' Glc/Cr+PCr', ' Gln %SD', ' Gln/Cr+PCr', ' Glu %SD', ' Glu/Cr+PCr', ' GPC %SD',
#                            ' GPC/Cr+PCr', ' PCh %SD', ' PCh/Cr+PCr', ' GSH %SD', ' GSH/Cr+PCr', ' Ins %SD',
#                            ' Ins/Cr+PCr', ' Lac %SD', ' Lac/Cr+PCr', ' NAA %SD', ' NAA/Cr+PCr', ' NAAG %SD',
#                            ' NAAG/Cr+PCr', ' Scyllo %SD', ' Scyllo/Cr+PCr', ' Tau %SD', ' Tau/Cr+PCr', ' -CrCH2 %SD',
#                            ' -CrCH2/Cr+PCr', ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr',
#                            ' Cr+PCr %SD', ' Cr+PCr/Cr+PCr', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' Lip13a %SD',
#                            ' Lip13a/Cr+PCr', ' Lip13b %SD', ' Lip13b/Cr+PCr', ' Lip09 %SD', ' Lip09/Cr+PCr',
#                            ' MM09 %SD', ' MM09/Cr+PCr', ' Lip20 %SD', ' Lip20/Cr+PCr', ' MM20 %SD', ' MM20/Cr+PCr',
#                            ' MM12 %SD', ' MM12/Cr+PCr', ' MM14 %SD', ' MM14/Cr+PCr', ' MM17 %SD', ' MM17/Cr+PCr',
#                            ' Lip13a+Lip13b %SD', ' Lip13a+Lip13b/Cr+PCr', ' MM14+Lip13a+L %SD', ' MM14+Lip13a+L/Cr+PCr',
#                            ' MM09+Lip09 %SD', ' MM09+Lip09/Cr+PCr', ' MM20+Lip20 %SD', ' MM20+Lip20/Cr+PCr'] + INFO_KEYS
#
# HEADERS_NO_RAW_LONG_TE = ['Row', ' Col', ' Ala %SD', ' Ala/Cr+PCr', ' Cr %SD', ' Cr/Cr+PCr', ' PCr %SD',
#                           ' PCr/Cr+PCr', ' Gln %SD', ' Gln/Cr+PCr', ' Glu %SD', ' Glu/Cr+PCr', ' GPC %SD',
#                           ' GPC/Cr+PCr', ' PCh %SD', ' PCh/Cr+PCr', ' GSH %SD', ' GSH/Cr+PCr', ' Ins %SD',
#                           ' Ins/Cr+PCr', ' Lac %SD', ' Lac/Cr+PCr', ' NAA %SD', ' NAA/Cr+PCr', ' NAAG %SD',
#                           ' NAAG/Cr+PCr', ' Scyllo %SD', ' Scyllo/Cr+PCr', ' -CrCH2 %SD', ' -CrCH2/Cr+PCr',
#                           ' GPC+PCh %SD', ' GPC+PCh/Cr+PCr', ' NAA+NAAG %SD', ' NAA+NAAG/Cr+PCr', ' Cr+PCr %SD',
#                           ' Cr+PCr/Cr+PCr', ' Glu+Gln %SD', ' Glu+Gln/Cr+PCr', ' Lip13a %SD', ' Lip13a/Cr+PCr',
#                           ' Lip13b %SD', ' Lip13b/Cr+PCr', ' Lip20 %SD', ' Lip20/Cr+PCr', ' Lip13a+Lip13b %SD',
#                           ' Lip13a+Lip13b/Cr+PCr'] + INFO_KEYS
#
#


#SIDE1 = 'left'
#SIDE2 = 'right'
#SIDE3 = 'middle'
#SIDE4 = 'Not Relevant'
#SIDES = [SIDE1, SIDE2, SIDE3, SIDE4]





#this path is a general pth for all the scripts data. I son't know yet what it should be.
