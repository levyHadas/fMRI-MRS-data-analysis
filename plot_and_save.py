# we need to see each exam in comparison to other exam with the same parameters.
# Since each exam has a few series which differ in the location and tissue type, we need to plot each series separately.
# the parameters are: age_group, tissue_type and location. These might change in the future and are all saved in the MRS-strings script.
# each parameter has a few optional values and each series matches one of the values.
# the user can chose to force the parameters, so he will see not only the data that correspond to the series params,
# but also to other params




import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import os
import mrs_strings as Strings





# called from "compare_series_to_normal" func in "cpmpare_exam_to_normal" script
# INPUT =  series_data_set = DICT,  database_data_set = DICT, series_main_data
# OUTPUT = shows plots of each series in comparision to database
# OUTPUT = saves .png images of the plots in the main exam folder inside folder calles "plots".
def main(series_data_set, database_data_set, series_main_data, exam_folder_path):

    plots_folder = os.path.join(exam_folder_path, 'plots')
    if not os.path.isdir( plots_folder ):
        os.mkdir(plots_folder)
    plot_file_name = 'series'+series_main_data[Strings.SERIES_NUM]+'TE'+series_main_data[Strings.TE]+'ID'+series_main_data[Strings.PATIENT_ID]+'.png'
    figure_save_path = os.path.join(plots_folder, plot_file_name)

    figure_title = 'Plotting:   patient ' + series_main_data[Strings.PATIENT_NAME] + ', ' + series_main_data[Strings.PATIENT_ID] + ', Series ' + series_main_data[Strings.SERIES_NUM] + '\n with Database TE' + series_main_data[Strings.TE]
    plt.figure(1, figsize=(10, 10))

    plt.title(figure_title)

    plt.yticks(np.arange(0, 4, 0.05))
    plt.tick_params(length=8, width=2, labelsize=7)

    violin = sb.violinplot(data=database_data_set.values(), showmeans=True, orient='v', legend_out=True, saturation=1, linewidth=1, inner = "stick", color='#89afec')
    violin.axes.set_xticklabels(database_data_set.keys())
    violin.axes.grid(color='#c3c3c3', axis='both', linewidth=0.2)

    plt.scatter(x=series_data_set.keys(), y=series_data_set.values(), color='#EC2F5E', marker='x', s=80)
    # now plot the current series

    plt.savefig(figure_save_path)
    plt.show()





if __name__ == '__main__':
    main()

