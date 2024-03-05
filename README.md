# File Parser

## Overview
This project parses an input file, formats the data to a proper structure and generates an output file with the cleaned up data in delimited format. The project has two different ways of performing its task:
- Parsing with Pandas library
- Parsing with Python native libraries

## Getting Started

### Prerequisites
- Python 3.9+
- Virtualenv

### Installation Steps
1. Create a virtual environment.
    ```sh
    virtualenv venv
    ```
    
2. Activate virtual env.

    For MacOS:
    ```sh
    source venv/bin/activate
    ```

    For Windows:
    ```sh
    venv/Scripts/activate
    ```

3. Install python modules from requirements.txt file using pip. (Required only for parsing with Pandas library)
    ```sh
    pip install -r requirements.txt
    ```

### Running the project
- To parse with pandas library, run the project using the following command:
    ```sh
    python clean_parsing_using_pandas.py
    ```

- To parse with python native libraries, run the project using the following command:
    ```sh
    python clean_parsing.py
    ```

### Input/Output file:
    Input Filename: forParsing_task.xls
    Output Filename: result_using_pandas.csv / result.csv

## Notes
- The main reason for choosing Pandas library to perform file parsing is because it has great features for reading and writing files of multiple formats and provides good functionalities for data handling and management.

- 'timeit' module has been used for run time calculations instead of 'datetime' module, as it returns result directly in seconds which is more preferred in this case rather than a clock time format.

- After multiple runs, it has been noticed from the program info logs that the execution time for script using pandas library was a little bit more than that of script using native libaries by a few milliseconds . Hence, parsing with native libraries performed better than pandas library.

        Script run time with Pandas library: 0.0085 seconds
        Script run time with native libaries: 0.0045 seconds
    This data is as per measured on system specs: Windows 10 16GB RAM i7-13th Gen