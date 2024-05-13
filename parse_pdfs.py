#from pypdf import PdfReader
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback

import pandas as pd
import pypdf
import json
import os
import time
#import re
import argparse

# import the prompt definition
from prompt_med_man import _prompt

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
            pdf_reader = pypdf.PdfReader(file)

            page_contents = []

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
            chat = ChatOpenAI(model_name='gpt-3.5-turbo-0125', temperature=0.1, max_tokens=4096)
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
def convert_to_csv(_json,filename):
    try:
        # Flatten the nested JSON data
        df = pd.json_normalize(_json)

        # Specify the path where you want to save the CSV file
        csv_file_path = filename

        # Convert the DataFrame to a CSV file
        df.to_csv(csv_file_path, mode="w", index=False)

        return True

    except Exception as e:
        return e
    
#########################################################
##
#########################################################
def prepare_output_dirs(init_path, prefix):
    try:
        session_output = init_path + "/output_" + prefix # + "/"
        print("session_output ", session_output)

        if not os.path.exists(init_path):
            os.mkdir(init_path)

        json_output = session_output + "/json"
        csv_output = session_output + "/csv"
        pfile_output = session_output + "/files_processed"
        ffile_output = session_output + "/files_failto_process"
        costs_output = session_output + "/costs"

        os.mkdir(session_output)
        os.mkdir(json_output)
        os.mkdir(csv_output)
        os.mkdir(pfile_output)
        os.mkdir(ffile_output)
        os.mkdir(costs_output)

        return session_output
    except Exception as e:
        print(e)
        return e


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
def process_file(file_toprocess_path, output_base_path=None):
    try:
        document_content = extract_text_from_pdf(file_toprocess_path)

        json_string, cost = convert_to_json(document_content)

        if output_base_path:
            output_file_name = os.path.basename(file_toprocess_path) + ".json"
            output_file_path = output_base_path + "/" + output_file_name

            with open(output_file_path, "w") as outfile:
                outfile.write(json_string)

        # convert to object
        json_obj = json.loads(json_string)
        
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
        pattern = r'med[\s_]man'

        # date time for filenames
        now = datetime.now() # current date and time
        date_time = now.strftime("%Y%m%d_%H%M")
        print("date and time", date_time)

        # Prepare output directories
        # TODO: Clean this up
        output_base = "./output"
        session_output_base_path = prepare_output_dirs(output_base, date_time)
        json_output = session_output_base_path + "/json"
        csv_output = session_output_base_path + "/csv"
        pfile_output = session_output_base_path + "/files_processed"
        ffile_output = session_output_base_path + "/files_failto_process"
        costs_output = session_output_base_path + "/costs"

        # Check if the path is a directory
        if os.path.isdir(pdf_file_path):
            #print("The path is a directory.")

            # Get the list of files in the current directory
            files = os.listdir(pdf_file_path)

            # Iterate over the files
            for file in files:
                if file.lower().endswith(file_type):
                    #if re.search(pattern, file, re.IGNORECASE):
                    print ( "Processing  > ", file)
                    
                    json_obj, cost = process_file(pdf_file_path + file, json_output)
                    if cost is None:
                        ffiles_list.append(file)
                        print("... failed to process: ", file )
                    else:   
                        pfiles_list.append(file)
                        json_list.append(json_obj)
                        cost_list.append(cost)

        else:
            json_obj, cost = process_file(pdf_file_path, json_output)
            if cost is not None:
                pfiles_list.append(pdf_file_path)
                json_list.append(json_obj)
                cost_list.append(cost)

        # Create the output file
        output_file = date_time + "output.csv"
        convert_to_csv(json_list,csv_output + "/" + output_file)

        # write files processed
        print("1")
        fproc_file_path = pfile_output + "/" + "files_processed.json"
        with open(fproc_file_path, "w") as outfile:
            outfile.write(json.dumps(pfiles_list,indent=4))

        # write files failed to processed
        fproc_file_path = ffile_output + "/" + "files_failed_to_process.json"
        with open(fproc_file_path, "w") as outfile:
            outfile.write(json.dumps(ffiles_list,indent=4))

        # write Open AI costs per call
        costs_file_path = costs_output + "/" + "ai_costs.json"
        with open(costs_file_path, "w") as outfile:
            outfile.write(json.dumps(cost_list,indent=4))

        # Convert result dictionary to JSON
        json_result = json.dumps(json_list, indent=4)
        
        # Calculate Tokens and Cost estimate 
        total_cost = calculate_api_cost(cost_list)
        print ("api cost >>>", total_cost)

        return json_list, cost_list, pfiles_list

    except Exception as e:
        return e, None, None

#########################################################
##
#########################################################
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process PDFs to parse contents into menaingful fields and values.')
    parser.add_argument('path',metavar='path',type=str, #is_valid_path, 
                    help='File name OR path to a list of files to parse.')
    parser.add_argument('-l', '--logfile',help="Logfile name")  
    args = parser.parse_args()

    pdf_file_path = args.path
    if pdf_file_path is None:
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/med_man/Ayala.Mark Med Man.pdf'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/med_man/Cabral.Christine Med man.pdf'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/med_man/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/med_man_test/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/initial_list/history/batch_4/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/initial_list/med_mgt/batch_4/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/initial_list/therapy_note/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/initial_list/med_mgt/batch_2/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/initial_list/med_mgt/batch_3/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/initial_list/med_mgt/batch_4/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/initial_list/med_mgt/batch_5/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/initial_list/med_mgt/batch_6/'
        #pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/initial_list/med_mgt/batch_7/'
        pdf_file_path = f'/Users/epl/projects/enigma-33/solace_bh/data/pdf/process/exception_list/initial_list/'
    #print(pdf_file_path)
    #is_valid_path(pdf_file_path)
    
    # TODO: 
    # 1.    X Add single file or directory processing logic
    # 2.    X Add output of json for each document (create directory and write .json based on file name)
    # 3.    X Modify the token and cost calculator to be accurate
    # 4.    X Add output of costs per document as well as a cumulative total.
    # 5.    Add vectorization or security for PHI files. !!! 
    # 6.    Create a prompt for the Initial Eval Old System
    # 7.    X Find a way to make a consistent CSV file (or JSON schema which will ensure the csv consistency)
    # 8.    Accept file pattern as main argument
    # 9.    Accept prompt file name as argument and load dynamically??
    # 10.   # Add proper exception handling
    # 11.   Clean up code
    # 12.   Add logging to file
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
