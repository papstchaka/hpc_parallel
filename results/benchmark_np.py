'''
opens the results given by the project and makes a benchmark comparison plot showing the influence of the different amount of used processors.
'''
## Imports
import os, sys, glob, re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def load_data(path:str) -> dict:
    '''
    reads in all the .npz files in given path, returns a dictionary with desired content
    Parameters:
        - path: path where files are located [String]
    Returns:
        - database: dictionary containing desired information [Dictionary]
    '''
    ## init database
    database = {}
    ## get all files with .npz ending
    filenames = glob.glob(os.path.join(path, "*.npz"))
    ## go through them
    for file in filenames:
        ## load file
        data = np.load(file)
        ## strip filename to get desired key - being the number of processors -> "2" in case of "26VI_Processor_Impl_Distr_01-2"
        key = file.split("/")[-1]
        key = key.split(".")[0]
        key = key.split("\\")[-1]
        key = key.split("_")[-1]
        database[key] = {}
        ## add all available properties to given key
        for count, properties in enumerate(data.files):
            value = data[properties].astype(float)
            database[key][properties] = value
    return database

def extend_database(folder:str, database:list) -> list:
    '''
    extends already existing database with new data from given folder
    Parameters:
        - folder: folder to search in for data [String]
    Returns:
        - database: list containing the data [List]
    '''
    ## init name of database
    dataset_name = ""
    ## strip name of dataset and number of processes from given folder -> dataset_name = "data_debug", np = 2 for "data_debug-2"
    m = re.search(r'/(.+?)-(\d+)/$', folder)
    dataset_name = m.group(1)
    np = int(m.group(2))
    ## load data from folder
    dataset = load_data(folder)
    ## if data in given folder (-> if not empty)
    if bool(dataset):
        ## extend database with data from local implementation
        database = [
            *database,
            {
                'dataset': dataset_name,
                'np': 1,
                'impl_name': "Local",
                'exec_time': dataset["Local"]["mean_execution_time"][0]
            }
        ]
        ## delete that data (that it is not accidentially used afterwards)
        del dataset["Local"]
        ## search for fasted implementation, extend database with respective data
        (best_impl_name,best_impl) = min(dataset.items(), key=lambda x: x[1]['mean_execution_time'][0])
        database = [ 
            *database,
            {
                'dataset': dataset_name,
                'np': np, 
                'impl_name': best_impl_name,
                'exec_time': best_impl['mean_execution_time'][0]
            }
        ]
    return database

def main() -> None:
    '''
    main function, runs all other functions, makes and saves plot
    Parameters:
        - None
    Returns:
        - None
    '''
    ## provided folder (usually "results/")
    parent_folder = sys.argv[1]
    ## search all folders in parent folder
    child_folders = glob.glob(os.path.join(parent_folder, "*/"))
    ## init database
    database = []
    ## go through all datafolders in parent folder
    for child_folder in child_folders:
        database = extend_database(child_folder, database)
    ## convert dictionary to pandas.DataFrame
    dataframe = pd.DataFrame(database)
    ## calculate log2 of execution time (that all data fit into one single plot)
    dataframe['exec_time_us_log'] = np.log2(dataframe['exec_time'] * 1e9)
    ## init plot
    plt.figure()
    ## make catplot with data
    g = sns.catplot(
        data=dataframe, kind="bar",
        x="dataset", y="exec_time_us_log", hue="np",
        order=['data_debug','data_small','data_normal'],
        palette="dark", alpha=.6, height=6,
        legend_out=True
    )
    ## update axis labels, legend and title
    g.set_axis_labels("", "log2 of mean execution time (us)")
    g.legend.set_title("Number of processes")
    g._legend.set_bbox_to_anchor((1.2, .7))
    ## save figure
    g.savefig(os.path.join(parent_folder,"benchmark_np.png"))
    ## unique the dataset names
    dataset_names = dataframe['dataset'].unique()
    ## init speedup column
    dataframe['speedup'] = [0.0] * len(dataframe)
    ## go through all dataset names
    for dataset_name in dataset_names:
        ## get the values of the local implementations
        dataset_local = dataframe[(dataframe['dataset'] == dataset_name) & (dataframe['np'] == 1)]
        ## get minimum local time
        min_local_exec_time = dataset_local['exec_time'].min()
        ## copy the sub dataset
        dataset_copy = dataframe[dataframe['dataset'] == dataset_name].copy()
        ## calculate the speedup in comparison to the local minimum execution time
        dataset_copy['speedup'] = (dataset_copy['exec_time'] / min_local_exec_time)**-1
        ## set the result into the main dataframe
        dataframe[dataframe['dataset'] == dataset_name] = dataset_copy
    ## get all data that is not from the local implementation
    dataframe_wo_local = dataframe[dataframe['np'] != 1]
    ## init plot
    plt.figure()
    ## make plot of speedup comparisons
    g = sns.lineplot(
        x='np', y='speedup', hue='dataset', hue_order=['data_debug','data_small','data_normal'],
        data=dataframe_wo_local
    ).get_figure()
    ## save figure
    g.savefig(os.path.join(parent_folder,"benchmark_np_speedup.png"))
    
if __name__ == "__main__":
    main()