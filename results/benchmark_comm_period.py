'''
opens the results given by the project and makes a benchmark comparison plot showing the influence of the different communication periods. These periods indicate the number of epochs that each processor runs before the resulting J is updated by the master.
'''
## Imports
import os, glob, re, argparse
import numpy as np
import matplotlib.pyplot as plt

def atoi(text:str) -> int:
    '''
    converts string into integer
    Parameters:
        - text: text to convert [String]
    Returns:
        - text: converted text, if text can be converted to integer [Integer]
    '''
    return int(text) if text.isdigit() else text

def natural_keys(text:str) -> list:
    '''
    alist.sort(key=natural_keys) sorts in human order - http://nedbatchelder.com/blog/200712/human_sorting.html (See Toothy's implementation in the comments)
    Parameters:
        - text: name of file [String]
    Returns:
        - list: list containing the names of the files in integer format [List]
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

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
    ## get all files with .npz ending, sorted
    filenames = sorted(glob.glob(os.path.join(path, "*.npz")), key = natural_keys)
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

def autolabel(ax:object, rects:list) -> None:
    '''
    goes through the barplots and changes the respective annotations of the bars
    Parameters:
        - ax: subplot where the bars are located in [object]
        - rects: list containing the respective bars [List]
    Returns:
        - None
    '''
    ## go through the barplots
    for rect in rects:
        ## get actual height
        height = rect.get_height()
        ## change annotation: size, significant numbers and location
        ax.annotate('{:.4f}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

def plot_mean_exec_time(mean_times:dict, x:np.array, width:float, path:str, comm:np.array, met:float) -> None:
    '''
    makes the plot containing the values of the mean execution times
    Parameters:
        - mean_times: dictionary containing the values of the mean execution times [Dictionary]
        - x: dummy array containing numbers up to amount of bars [numpy.array]
        - width: width of bars [Float]
        - path: path where result plot shall be saved [String]
        - comm: array containing the different communication periods [numpy.array]
        - met: mean execution time of local implementation [Float]
    Returns:
        - None
    '''
    ## init plots, set labelsize of x- and y-axis
    fig, ax = plt.subplots(figsize=(16,8))
    plt.rcParams['xtick.labelsize']=16
    plt.rcParams['ytick.labelsize']=16
    ## init bars
    rects = []
    ## go through all mean times
    for i in range(mean_times.keys().__len__()):
        ## add barplot
        rects.append(ax.bar(x + (i * 0.12 - 0.24), mean_times[list(mean_times.keys())[i]].values(), width, label='Scheme: ' + list(mean_times.keys())[i]))
    ## add horizontal line to indicate mean execution time of local implementation
    ax.axhline(y = met, label = "Local implementation", color = "black")
    ## set ylabel, title, xticks, xticklabels, legend
    ax.set_ylabel('Mean execution time (in seconds)', fontsize=16)
    ax.set_title('Benchmark comparison among communication schemes', fontsize=20)
    ax.set_xticks(x)
    ax.set_xticklabels(comm)
    ax.set_xlabel('Communication frequency (in epochs)', fontsize=16)
    ax.legend(fontsize='x-large')    
    ## go through all barplots
    for rect in rects:
        ## update annotation
        autolabel(ax, rect)
    ## minor plot change
    fig.tight_layout()
    plt.grid()
    ## save plot
    plt.savefig(os.path.join(path, 'benchmark_distr.png'))
    print("[INFO] The benchmark visualization plot was successfully stored to: " + path)

def plot_var_exec_time(var_times:dict, x:np.array, width:float, path:str, comm:np.array, vet:float):
    '''
    makes the plot containing the values of the variance of the execution times
    Parameters:
        - var_times: dictionary containing the values of the variance of the execution times [Dictionary]
        - x: dummy array containing numbers up to amount of bars [numpy.array]
        - width: width of bars [Float]
        - path: path where result plot shall be saved [String]
        - comm: array containing the different communication periods [numpy.array]
        - vet: variance of execution time of local implementation [Float]
    Returns:
        - None
    '''
    ## init plots, set labelsize of x- and y-axis
    fig, ax = plt.subplots(figsize=(16,8))
    plt.rcParams['xtick.labelsize']=16
    plt.rcParams['ytick.labelsize']=16
    ## init bars
    rects = []
    ## go through all mean times
    for i in range(var_times.keys().__len__()):
        ## add barplot
        rects.append(ax.bar(x + (i * 0.12 - 0.24), var_times[list(var_times.keys())[i]].values(), width, label='Scheme: ' + list(var_times.keys())[i]))
    ## add horizontal line to indicate variance of execution time of local implementation
    ax.axhline(y = vet, label = "Local implementation", color = "black")
    ## set ylabel, title, xticks, xticklabels, legend
    ax.set_ylabel('Variance of execution time (in milliseconds)', fontsize=16)
    ax.set_title('Variance execution time comparison among communication schemes', fontsize=20)
    ax.set_xticks(x)
    ax.set_xticklabels(comm)
    ax.set_xlabel('Communication frequency (in epochs)', fontsize=16)
    ax.legend(fontsize='x-large')    
     ## go through all barplots
    for rect in rects:
        ## update annotation
        autolabel(ax, rect)
    ## minor plot change
    fig.tight_layout()
    plt.grid()
    ## save plot
    plt.savefig(os.path.join(path, 'var_distr.png'))
    print("[INFO] The variance visualization plot was successfully stored to: " + path)
        
def visualize(path:str, data:dict) -> None:
    '''
    visualizes mean execution time and variance of execution times
    Parameters:
        - path: path to store result in [String]
        - data: dictionary containing respective data [Dictionary]
    Returns:
        - None
    '''
    ## init mean execution times and variance of execution times
    mean_times = {}
    var_times = {}
    ## init communication periods list and labels
    comm = []
    labels = []
    ## go through keys
    for label in list(data.keys()):
        ## get implementation name and communication period
        result = label.split("-")
        ## skip the local implementation       
        if any(x in label for x in ["Local", "local"]):
            continue
        else:                
            ## add communication period
            comm.append(result[-1])
            ## init respective mean execution time and variance of execution time of given implementation
            mean_times[result[0]] = {}
            var_times[result[0]] = {}
    ## make sure we have a numpy array, sort it naturally
    comm = np.array(comm)
    comm = sorted(np.unique(comm), key = natural_keys)
    ## make list of keys
    labels = list(mean_times.keys())    
    ## go through data keys
    for label in list(data.keys()):
        ## get implementation name and communication period
        scheme = label.split("-")[0]
        freq = label.split("-")[-1]
        ## skip the local implementation (when both values are the same -> indicates no comm_period exists)
        if(scheme == freq):
            continue
        ## add respective mean execution time and variance of execution time of given implementation, multiply variance with 1000 (too low otherwise)
        mean_times[scheme][freq] = data[label]['mean_execution_time'][0]
        var_times[scheme][freq] = data[label]['var_execution_time'][0] * 1000
    ## set dummy array containing numbers up to amount of bars and width of bars
    x = np.arange(len(comm))
    width = 0.1
    ## plot mean execution times and variance of execution times
    plot_mean_exec_time(mean_times, x, width, path, comm, data["Local"]["mean_execution_time"][0])
    plot_var_exec_time(var_times, x, width, path, comm, data["Local"]["var_execution_time"][0])   
    
def main() -> None:
    '''
    main function, runs all other functions, makes and saves plot
    Parameters:
        - None
    Returns:
        - None
    '''
    ## init argument parse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    args = parser.parse_args()    
    ## get respective folder where results shall be stored in
    result_dir = os.path.join(os.getcwd(), args.path)
    ## get data, make plots
    data = load_data(result_dir)
    visualize(result_dir, data)
    
if __name__ == "__main__":
    main()