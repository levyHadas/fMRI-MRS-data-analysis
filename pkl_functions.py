
import os
import pickle








def read_pkl(pkl_path):
    input_pkl_file = open(pkl_path, 'rb')
    input_data = pickle.load(input_pkl_file)
    input_pkl_file.close()
    print(input_data)
    return input_data




def save_pickle (pkl_path, data):
    output_pkl_file = open(pkl_path, 'wb')
    pickle.dump(data, output_pkl_file)
    print(data)
    output_pkl_file.close()







