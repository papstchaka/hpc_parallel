# High Performance Computing using <a href="https://www.open-mpi.org/" target="_blank">`OpenMPI`</a> in C++ for Asynchronous Value Iteration

## Content

- [`About the project`](#about-the-project)
- [`Repository structure`](#repository-structure)
- [`Communication protocols`](#communication-protocols)
- [`Adding communication protocols`](#adding-communication-protocols)
- [`Data import`](#data-import)
- [`Evaluation of implementations`](#evaluation-of-implementations)
- [`Run the project`](#run-the-project)
- [`Benchmark comparison`](#benchmark-comparison---8-processors)
- [`Variance of running time`](#variance-of-running-time)
- [`Install OpenMPI`](#install-openmpi)
- [`Group members`](#group-members)

---

## About the project

In this repository a `Asynchronous Value Iteration` is implemented using  <a href="https://www.open-mpi.org/" target="_blank">`OpenMPI`</a> for parallelization and performance boost. Therefor different strategies of communication are implemented and afterwards evaluated and compared to eachother.

---

## Repository structure

- <a href="data/" target="_blank">`data/`</a> - contains datasets
- <a href="install_files/" target="_blank">`install_files/`</a> - contains all needed debian pacakges to install <a href="https://www.open-mpi.org/" target="_blank">`OpenMPI`</a> `[Version 2.2.1]`
- <a href="lib/" target="_blank">`lib/`</a> - contains all required libraries
- <a href="results/" target="_blank">`results/`</a> - contains the results of the implementations
- <a href="src/" target="_blank">`src/`</a> - contains the C++ source code
- <a href="CMakeLists.txt" target="_blank">`CMakeLists.txt`</a> - responsible for creating the correct `Makefile` for code compiling
- <a href="Doxyfile" target="_blank">`Doxyfile`</a> - responsible for automatically creating the code documentation
- <a href="Makefile" target="_blank">`Makefile`</a> - responsible for all interactions with the project
- <a href="Project_Presentation.pdf" target="_blank">`Project_Presentation`</a> - contains results of the project for presentation purposes
- <a href="hostfile" target="_blank">`hostfile`</a> - contains all hosts on which parallel computing shall be runned
- <a href="main.cpp" target="_blank">`main.cpp`</a> - Main script, runs all implementations in <a href="src/" target="_blank">`src/`</a>, runs the task

---

## Communication protocols:

For simplification reasons - especially because the names of the implementations would get very long otherwise and confusing - the individual implementations are named numerically instead of the actual communication schemes. The following table shows which number is corresponding to which <a href="https://www.open-mpi.org/" target="_blank">`OpenMPI`</a> functionality.

| name                                                                                           | OpenMPI functionality                    |
| ---------------------------------------------------------------------------------------------- | ------------------------------------- |
| <a href="src/vi_processor_impl_distr_01.cpp" target="_blank">`VI_Processor_Impl_Distr_01`</a>  | `Allgatherv`, `Allreduce`, `Gatherv`  |
| <a href="src/vi_processor_impl_distr_02.cpp" target="_blank">`VI_Processor_Impl_Distr_02`</a>  | `Send`, `Recv`, `Bcast`               |
| <a href="src/vi_processor_impl_distr_03.cpp" target="_blank">`VI_Processor_Impl_Distr_03`</a>  | `Sendrecv`, `Gatherv`                 |
| <a href="src/vi_processor_impl_distr_04.cpp" target="_blank">`VI_Processor_Impl_Distr_04`</a>  | `Isend`, `Irecv`, `Ibcast`, `Igatherv`|
| <a href="src/vi_processor_impl_distr_05.cpp" target="_blank">`VI_Processor_Impl_Distr_05`</a>  | `Igatherv`, `Bcast`, `Gatherv`        |

An extensive documentation for possible <a href="https://www.open-mpi.org/" target="_blank">`OpenMPI`</a> communication protocols and their functionality: [`Princeton Bootcamp communication protocols`](https://princetonuniversity.github.io/PUbootcamp/sessions/parallel-programming/Intro_PP_bootcamp_2018.pdf) respectively <a href="https://www.open-mpi.org/doc/v2.1/" target="_blank">`official documentation of the used OpenMPI Version [2.1.1]`</a>. For comparison reasons <a href="src/vi_processor_impl_local.cpp" target="_blank">`VI_Processor_Impl_Local`</a> was implemented which is the implementation of the synchronous `Value Iteration`.

Further information about the individual implementation can be gleaned in <a href="src/" target="_blank">`src/`</a> respectively the scripts themselves.

---

## Adding communication protocols

We can add and evaluate different `VI implementations` and communication strategies by implementing a from <a href="src/vi_processor_base.h" target="_blank">` VI_Processor_Base`</a> derived class (see example <a href="src/vi_processor_impl_local.cpp" target="_blank">`VI_Processor_Impl_Local`</a> respectively <a href="src/vi_processor_impl_distr_01.cpp" target="_blank">`VI_Processor_Impl_Distr_01`</a>). 



---

## Data import

The dataset is converted from `.pickle`-format into `.npz`-format while compiling by the <a href="Makefile" target="_blank">`Makefile`</a> using <a href="data/convert_pickle.py" target="_blank">`convert_pickle.py`</a>. Those are afterwards read-in by <a href="https://github.com/rogersce/cnpy" target="_blank">`"cnpy" by Carl Rogers`</a> library.

---

## Evaluation of implementations

When a comparison of multiple implementations is desired, <a href="main.cpp" target="_blank">`main.cpp`</a> builds up a list containing multiple implementations. Afterwards the calculation time is iteratively measured (each ~20 times). The the mean calculation time is used to compare the implementations.

---

## Run the project

1. Clone the repository

```text
# clone repository
git clone https://github.com/papstchaka/hpc_parallel.git

# respectively pull to latest version (if project already cloned)
cd hpc_parallel
git pull origin master

# switch to master branch
git checkout master
```

-------------------------------------------------------------

2. Make sure that your <a href="hostfile" target="_blank">`hostfile`</a> respectively your `~/.ssh/config` are set up correctly/accordingly. Currently <a href="hostfile" target="_blank">`hostfile`</a> only contains the local machine, using 4 slots/processors.

`~/.ssh/config`:
```text
# Put this file in ~/.ssh/ with the name 'config'

# Matches <host1> <host2> and so on, %h gets the actual match, e.g. host6, and completes the host name, where <host1>, <host2> stand for the host names of your respective cluster computers

Host host1 host2 
  HostName %h.<rest_of_address>

# Configuration for all hosts (matches always)

Host *
  User <your_user_name>
  ForwardX11 yes
  Compression yes
```

<a href="hostfile" target="_blank">`hostfile`</a>:

```text
# All computers mpirun should use. You can use as much slots as desired (should be below physical number of processors - must be lower/equal to max-slots)
# Comments as in Python
# localhost slots=4 max-slots=4 --> local machine !
<host1>.<rest_of_address> slots=2 max-slots=2
<host2>.<rest_of_address> slots=2 max-slots=2
```

-------------------------------------------------------------

3. Compile and run the project. Therefor different possibilities exist.

```text

1. Running the project locally on current physical machine
   (number of started processors: 2 respectively 4)

1.1 make run_debug_local

-------------------------------------------------------------

2. Distributed computing on multiple physical devices
   (manual decision of used dataset).

2.1 make run_debug (start with "debug" dataset)

    or
  
2.2 make run_small (start with "small" dataset)

    or

2.3 make run_normal (start with "normal" dataset)

-------------------------------------------------------------

3. Distributed computing on multiple physical devices
   (all datasets will be processed sequentially)

3.1 make run_all

-------------------------------------------------------------

4. manual running

4.1 make compile

4.2 cd build

4.3 mpirun -np 6 -hostfile ../hostfile ./MPI_Project.exe "<path_to_data_folder>" "<path_to_results_folder>" <number_of_runs>

```
## Benchmark comparison - 8 processors

In the graphics below the benchmark comparison for all implemented communication protocols is shown for the different datasets.

<a href="data/data_debug-8/" target="_blank">`data_debug/`</a>

<h2 align="center">
  <img src="results/data_debug-8/benchmark_distr.png" alt="Benchmark Vergleich" width="800px" />
</h2>

<a href="data/data_small-8/" target="_blank">`data_small/`</a>

<h2 align="center">
  <img src="results/data_small-8/benchmark_distr.png" alt="Benchmark Vergleich" width="800px" />
</h2>

<a href="data/data_normal-8/" target="_blank">`data_normal/`</a>

<h2 align="center">
  <img src="results/data_normal-8/benchmark_distr.png" alt="Benchmark Vergleich" width="800px" />
</h2>

---

## Variance of running time

The graphic below is a variance plot. It shows the deviation of calculation times. It was only generated for [`data_debug`](data_debug/) dataset because [`data_small`](data_small/) dataset and [`data_normal`](data_normal/) dataset only ran once each. Thereafter no variance exists. 

<h2 align="center">
  <img src="results/data_debug-8/var_distr.png" alt="Varianz Vergleich" width="800px" />
</h2>

---

## Install OpenMPI

Installer files for <a href="https://www.open-mpi.org/" target="_blank">`OpenMPI`</a> are located in <a href="install_files/" target="_blank">`install_files/`</a>. They have to be installed in the following order (Linux environment: Ubuntu, WSL2, etc.). Afterwards version `2.2.1` is installed on the respective machine.
```cmd
1. cd install_files
2. sudo dpkg -i libhwloc5_1.11.9-1_amd64.deb
3. sudo dpkg -i libopenmpi2_2.1.1-8_amd64.deb
4. sudo dpkg -i openmpi-common_2.1.1-8_all.deb
5. sudo dpkg -i openmpi-bin_2.1.1-8_amd64.deb
```
---

## Group members

|                             |                             |
| --------------------------- | --------------------------- |
| Stümke, Daniel              | daniel.stuemke@tum.de       |
| Christoph, Alexander        | alexander.christoph@tum.de  |
| Kiechle, Johannes           | johannes.kiechle@tum.de     |
| Gottwald, Martin (Lecturer) | martin.gottwald@tum.de      |
| Hein, Alice (Lecturer)      | alice.hein@tum.de           |