#from pypdf import PdfReader
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from collections import OrderedDict

import pandas as pd
import pypdf
import json
import os
import time
import argparse
import csv
import concurrent.futures


# import the prompt definition
from prompt_med_man_mod_1 import _prompt
from modules.output_struct import OutputStruct
 
#########################################################
##
#########################################################
def is_valid_path(parser, arg):
#def is_valid_path(arg):
    if not os.path.exists(arg.strip()):
        #print ("The path %s does not exist!" % arg)
        parser.error("The path %s does not exist!" % arg)
    else:
        #print("valid")
        return arg

#########################################################
##
#########################################################
def visitor_body(text, cm, tm, fontDict, fontSize):
    y = tm[5]
    if text and 0 < y < 770:
        return text
    else:
        return None
    
#########################################################
##
#########################################################
def extract_text_from_pdf(pdf_file_path):
    try:
        with open(pdf_file_path, 'rb') as file:
            page_contents = []

            pdf_reader = pypdf.PdfReader(file)
            for page in pdf_reader.pages:
                ret = page.extract_text(visitor_text=visitor_body, extraction_mode="plain" )
                page_contents.append(ret)
            
            document_content = "\n".join(page_contents)

            #print("exfp ==> ",document_content)
            return document_content
    except pypdf.errors.PdfReadError as pe:
        raise Exception("Failed to load file due to (1)", pe)
    except Exception as e:
        raise ("Failed to load file due to (2)", e)
    
#########################################################
##
#########################################################
def convert_to_json(document_content):
    try:
        # prompt is defined in the prompt import file 
        system_message = _prompt
        with get_openai_callback() as cost:
            chat = ChatOpenAI(model_name='gpt-3.5-turbo-0125', temperature=0.0, max_tokens=4096)
            #chat = ChatOpenAI(model_name='gpt-4-turbo', temperature=0.0, max_tokens=4096)
            messages = [
                SystemMessage(
                    content=system_message
                ),
                HumanMessage(
                    content=document_content
                )
            ]
            answer = chat.invoke(messages)

        # Extract cost from response
        cost_dict = {
            'completion_tokens': cost.completion_tokens,
            'prompt_tokens' : cost.prompt_tokens,
            'total_tokens' : cost.total_tokens,
            'total_cost' : cost.total_cost,
            'successful_requests' : cost.successful_requests
        }
        return answer.content, cost_dict

    except Exception as e:
        return e, None


#########################################################
##
#########################################################
def flatten_json(y, prefix=''):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            out[name[:-1]] = ', '.join(map(str, x))
        else:
            out[name[:-1]] = x
    flatten(y, prefix)
    return out

#########################################################
##
#########################################################
def collect_keys(data):
    keys = set()
    for item in data:
        flat_item = flatten_json(item)
        keys.update(flat_item.keys())
    return keys

#########################################################
##
#########################################################
def convert_to_csv_alt(json_string,filename):
    try:
        data = json.loads(json_string)
        keys = collect_keys(data)

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(keys))
            writer.writeheader()
            for item in data:
                flat_item = flatten_json(item)
                writer.writerow(flat_item)

        return True

    except Exception as e:
        raise e

#########################################################
##
#########################################################
def convert_to_csv(json_string,filename):
    try:
        # Load JSON string
        data = json.loads(json_string)

        # Flatten JSON and create DataFrame
        #df = pd.json_normalize(data, max_level=2, sep='.')
        df = pd.json_normalize(data)

        # Write DataFrame to CSV
        df.to_csv(filename, index=False)

        return True

    except Exception as e:
        raise e
    

#########################################################
##
#########################################################
def output_json(filename):
    return True

#########################################################
##
#########################################################
def calculate_api_cost(cost_list):
    try:
        total_cost = 0.00
        for cost in cost_list:
            total_cost += cost["total_cost"]
        return total_cost
    
    except Exception as e:
        print(e)
        return e

#########################################################
##
#########################################################
def process_directory(file_toprocess_path, output_base_path=None):
    try:
        return True
    except Exception as e:
        print(e)
        return e

#########################################################
##
#########################################################
def process_file(file_toprocess_path, output_base_path=None):
    try:
        print ( "...Processing  > ", file_toprocess_path)

        # Start the timer
        pstart_time = time.time()

        document_content = extract_text_from_pdf(file_toprocess_path)
        #print(document_content)

        json_string, cost = convert_to_json(document_content)

        if output_base_path:
            output_file_name = os.path.basename(file_toprocess_path) + ".json"
            output_file_path = output_base_path + "/" + output_file_name

            with open(output_file_path, "w") as outfile:
                outfile.write(json_string)

        # convert to object
        json_obj = json.loads(json_string)

        # Stop the timer
        pend_time = time.time()

        # Calculate the total time taken
        ptotal_time = pend_time - pstart_time

        # Print the total time taken
        print("......Total time taken: {} seconds".format(ptotal_time))

        #print(cost)
        return json_obj, cost
    except Exception as e:
        print(e)
        return e, None

#########################################################
##
#########################################################
def main(pdf_file_path):
    """Main function to process PDF, vectorize text, and interact with OpenAI."""
    try:
        # Lists for processed file
        json_list = []
        cost_list = [] 
        pfiles_list = []
        ffiles_list = []

        # Filters for files to be processed
        file_type = ".pdf"
        #pattern = r'med[\s_]man'

        # date time for filenames
        now = datetime.now() # current date and time
        date_time = now.strftime("%Y%m%d_%H%M")
        print("date and time", date_time)

        # Prepare output directories
        # TODO: Clean this up
        output_base = "./output"
        output = OutputStruct(output_base, date_time)
        session_output_base_path = output.init_output_dir()

        # Check if the path is a directory
        if os.path.isdir(pdf_file_path):
            #print("The path is a directory.")

            # Get the list of files in the current directory
            files = os.listdir(pdf_file_path)

            # Iterate over the files
            for file in files:
                if file.lower().endswith(file_type):
                    #if re.search(pattern, file, re.IGNORECASE):
                    
                    json_obj, cost = process_file(pdf_file_path + file, output.get_json_full_path())
                    if cost is None:
                        ffiles_list.append(file)
                        print("... failed to process: ", file )
                    else:   
                        pfiles_list.append(file)
                        json_list.append(json_obj)
                        cost_list.append(cost)

        else:
            json_obj, cost = process_file(pdf_file_path, output.get_json_full_path())
            if cost is  None:
                ffiles_list.append(pdf_file_path)
            else:   
                pfiles_list.append(pdf_file_path)
                json_list.append(json_obj)
                cost_list.append(cost)

        # Create the output file
        output_file = date_time + "output.csv"
        json_string = json.dumps(json_list)
        convert_to_csv_alt(json_string,output.get_csv_full_path() + "/" + output_file)

        # write files processed
        fproc_file_path = output.get_processed_full_path() + "/" + "files_processed.json"
        with open(fproc_file_path, "w") as outfile:
            outfile.write(json.dumps(pfiles_list,indent=4))

        # write files failed to processed
        fproc_file_path = output.get_failed_full_path() + "/" + "files_failed_to_process.json"
        with open(fproc_file_path, "w") as outfile:
            outfile.write(json.dumps(ffiles_list,indent=4))

        # write Open AI costs per call
        costs_file_path = output.get_costs_full_path() + "/" + "ai_costs.json"
        with open(costs_file_path, "w") as outfile:
            outfile.write(json.dumps(cost_list,indent=4))

        # Calculate Tokens and Cost estimate 
        total_cost = calculate_api_cost(cost_list)
        print ("api cost >>>", total_cost)

        return json_list, cost_list, pfiles_list

    except Exception as e:
        print("Exception thrown ===>", e)
        return e, None, None

#########################################################
##
#########################################################
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process PDFs to parse contents into meaningful fields and values.')
    parser.add_argument('path',metavar='path',type=str, #is_valid_path, 
                    help='File name OR path to a list of files to parse.')
    parser.add_argument('-l', '--logfile',help="Logfile name")  
    args = parser.parse_args()

    pdf_file_path = args.path
    if pdf_file_path is None:
        pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/exception_list/initial_list/'
    #print(pdf_file_path)
    #is_valid_path(pdf_file_path)
    
    # TODO: 
    # 1.    Add vectorization for security of PHI files. !!! 
    # 2.    Create a prompt for the Initial Eval Old System
    # 3.    Accept prompt file name as argument and load dynamically??
    # 4.    Clean up code
    # 5.    Add logging to file
    #

    # Start the timer
    start_time = time.time()

    # Call the main procedure
    json_list, cost_list, files_list = main(pdf_file_path)

    # Stop the timer
    end_time = time.time()

    # Calculate the total time taken
    total_time = end_time - start_time

    # Print the total time taken
    print("Total time taken: {} seconds".format(total_time))
