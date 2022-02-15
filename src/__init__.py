import os
import csv
import json
from datetime import datetime

# General flags
NO_ARG = 0
N_OUT = 1
Y_TXT = 2
M_TXT = 3
Y_SALES = 4
SRCH_SCHOOLDESC = 3
SRCH_PARID = 4

# Index of each position in the arguments list
POS_ARG_TYPE = 0
POS_ARG_KEY = 1
POS_ARG_OUT = 2
POS_ARG_PATH = 3

# Index of each column in the data created from the CSV file
POS_PARID = 0
POS_SCHOOLDESC = 12
POS_MAX = 24 # Number of columns

# Path of the CSV file.
# P. S.: This path should be absolute ou passed as a parameter to read_data. Here it is assumed that this
# application will be executed through main.py under the project root directory. 
CSV_PATH = os.getcwd() + "/input/property_sales_transactions.csv"

# to-do: implement a more intelligent, flexible parsing funcion
def parse_arg(arg):
    argum = {}
    # If the correct number of arguments was entered
    if  (len(arg) >= 2) and (len(arg) <= 4):
        if arg[POS_ARG_TYPE] == "--filter-school-desc":
            argum["srch_type_in"] = arg[POS_ARG_TYPE]
            argum["srch_key"] = arg[POS_ARG_KEY]
            argum["srch_type_code"] = SRCH_SCHOOLDESC                    
        elif arg[POS_ARG_TYPE] == "--find-pair-id":
            argum["srch_type_in"] = arg[POS_ARG_TYPE]
            argum["srch_key"] = arg[POS_ARG_KEY]
            argum["srch_type_code"] = SRCH_PARID
        else:
            argum["srch_type_code"] = NO_ARG
            return argum

        # If a option to save the results or to show then as a JSON may have been chosen
        if len(arg) > 2:
            # If the 'output' option was typed
            if (arg[POS_ARG_OUT] == "-o") or (arg[POS_ARG_OUT] == "--output"):
                # if the path may have been provided
                if len(arg) > 3:
                    argum["srch_out_path"] = arg[POS_ARG_PATH] # to-do: check for forbidden characters
                    argum["out"] = Y_TXT
                # Otherwise (len(arg) == 3) we report an error and tell the function caller
                # that the output path is missing
                else:
                    argum["srch_type_code"] = NO_ARG # This error turns the whole command invalid
                    argum["out"] = M_TXT # This flag tells the caller that the path is missing
            # if the --sale-summary option was chose (in this case, len(arg) must be equal to 3)
            elif (arg[POS_ARG_OUT] == "--sale-summary") and (len(arg) == 3):
                argum["out"] = Y_SALES
            # Otherwise the command is invalid
            else:
                argum["srch_type_code"] = NO_ARG
        # Otherwise (len(arg) == 2) the command is valid but the results shall not be saved
        else:
            argum["out"] = N_OUT  

    else:
        argum["srch_type_code"] = NO_ARG
    
    return argum

def read_data():
    # P.S.: We could have used Python's CSV module
    file_csv = open(CSV_PATH, 'r')

    data_in = []

    for line in file_csv:
        columns = line.strip().split(',')
        data_in.append(columns)

    file_csv.close()

    return data_in

def search_method(srch_method, data, keyword):
    
    results = []

    if srch_method == SRCH_PARID:
        pos_meth = POS_PARID
    elif srch_method == SRCH_SCHOOLDESC:
        pos_meth = POS_SCHOOLDESC
    else:
        return []
    
    # Make the search case insensitive
    l_keyword = keyword.casefold()

    for i in range(1, len(data)):
        # Make the search case insensitive
        tmp_data = data[i][pos_meth].casefold()
        if tmp_data.find(l_keyword) != -1:
            results.append(data[i])
    
    # Add the columns names
    if(len(results) > 0):
        results = [data[0]] + results

    return results

def export_results(res, exp_path):
    # Get the timestamp
    # to-do: configure the time zone
    date = datetime.now()

    # to-do: check exp_path for cases that the try/except block cannot catch.
    file_name = exp_path + "results-" + date.strftime('%Y-%m-%dT%H-%M-%S.%f%z') + ".txt"

    try:
        file_exp = open(file_name, 'w', newline='', encoding='utf-8')
        file_exp_writer = csv.writer(file_exp, delimiter=',')

        for i in range(0, len(res)):
            file_exp_writer.writerow(res[i])

        file_exp.close()

    except:
        print("\nInvalid path!\n")


# FER: this function is more complex than I thought. I'll do it later.
# def print_sales_sum(res_entry):


#     # Creating a dictionary to print in JSON format
#     entry_dic = {'PARID':res_entry[POS_PARID], 'SCHOOLDESC':res_entry[POS_PARID] \
#                  'VALID SALE': }
