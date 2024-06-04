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
import shutil
import argparse
import csv
import concurrent.futures
import traceback
import openai
import logging


# import the prompt definition
from prompt_med_man_mod_1 import _prompt
#from prompt_initial_visit import _prompt
from modules.output_struct import OutputStruct


#########################################################
##
#########################################################
def configure_logging(logfile_path):
 
    # Configure logging
    logging.basicConfig(filename=logfile_path, level=logging.INFO, force=True,
                        format='%(asctime)s - %(levelname)s - %(message)s')

#########################################################
##
#########################################################
def copy_files_from_list(file_list_path, source_directory, destination_directory):
    # Ensure the destination directory exists
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Read the file containing the list of file names
    with open(file_list_path, 'r') as file_list_string:
        file_list = list(file_list_string)
        #print(f"file list {file_list}")

        for file_name in file_list:
            # Strip any extra whitespace characters
            file_name = file_name.strip()

            # Strip any quotation marks characters
            file_name = file_name.replace('"', '')

            # Strip commas
            file_name = file_name.replace(',', '')

            file_path = os.path.join(source_directory,file_name)
            #file_path = '\'' + source_directory + file_name + '\''
            if os.path.isfile(file_path):
                try:
                    # Copy the file to the destination directory
                    shutil.copy(file_path, destination_directory)
                    logging.info(f"......Copied {file_path} to {destination_directory}")
                except Exception as e:
                    logging.info(f"......Failed to copy {file_path}: {e}")
            else:
                logging.info(f"......File {file_path} does not exist.")

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

            pdf_reader = pypdf.PdfReader(file,strict=False)
            for page in pdf_reader.pages:
                ret = page.extract_text(visitor_text=visitor_body, extraction_mode="plain" )
                page_contents.append(ret)
            
            document_content = "\n".join(page_contents)

            #print("exfp ==> ",document_content)
            return document_content
    except pypdf.errors.PdfReadError as pe:
        raise Exception("Failed to load file due to (1)", pe)
    except Exception as e:
        # print(e)
        raise ("Failed to load file due to (2)", e)
    
#########################################################
##
#########################################################
def convert_to_json(document_content):

    max_retries = 5  # Maximum number of retries
    retry_delay = 1  # Initial delay between retries (in seconds)

    # prompt is defined in the prompt import file 
    system_message = _prompt
    for attempt in range(max_retries):
        try:
            if attempt > 1:
                #print(f"......Retrying request. Attempt: {attempt} after a {retry_delay} second retry delay.")
                logging.info(f"......Retrying request. Attempt: {attempt} after a {retry_delay} second retry delay.")

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
        
        except openai.RateLimitError as rle:
            # Print the error and retry with exponential backoff
            if attempt < max_retries - 1:
                logging.info(f"......Rate limit exceeded. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logging.info("......Max retries reached. This file will fail.")
                #return rle, None
                raise Exception('m:convert_to_json: {}'.format(rle)) from rle

        except Exception as e:
            #return e, None
            print(f"......<convert_to_json>")
            raise e 

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
        logging.info(e)
        return e


#########################################################
##
#########################################################
def process_file(file_toprocess_path, output_base_path=None):
    try:
        logging.info( f"...Processing ==> {file_toprocess_path}")
        json_obj = None
        cost = None

        # Start the timer
        pstart_time = time.time()

        document_content = extract_text_from_pdf(file_toprocess_path)
        #print(document_content)

        try:
            json_string, cost = convert_to_json(document_content)
        
        except Exception as ie:
            logging.info(f"m:inner(_1):process_file ===> {ie}")
            logging.exception('Got exception on ie handler')

            return ie,  None

        if output_base_path:
            output_file_name = os.path.basename(file_toprocess_path) + ".json"
            output_file_path = output_base_path + "/" + output_file_name

            with open(output_file_path, "w") as outfile:
                outfile.write(json_string)

        # convert to object
        try:
            json_obj = json.loads(json_string)

        except Exception as ie2:
            logging.info(f"m:inner(_2):process_file ===> {ie2}")
            logging.exception('Got exception on ie2 handler')
            return ie2,  None

        #print(cost)
        return json_obj, cost
    
    except Exception as e:
        logging.info(f"......m:process_file ===> {e}") 
        logging.exception('Got exception on main handler')
        #logging.info("......", traceback.format_exc())
        return e, None
    
    finally:
        # Stop the timer
        pend_time = time.time()

        # Calculate the total time taken
        ptotal_time = pend_time - pstart_time

        # Print the total time taken
        logging.info("......Total time taken: {} seconds".format(ptotal_time))
    
#########################################################
##
#########################################################
def submit_tasks(executor, pdf_file_path, files, output_struct):
    """
    Submits tasks to the executor and returns a dictionary of futures.
    """
    futures = {}
    for file in files:
        future = executor.submit(process_file, pdf_file_path + file, output_struct.get_json_full_path())
        futures[future] = file
    return futures

#########################################################
##
#########################################################
def handle_futures(futures):
    """
    Handles the futures and collects their results and file names.
    """
    results = []
    files = []
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            results.append(result)
            files.append(futures[future])  # Store the corresponding file name
        except Exception as e:
            logging.info(f"Exception occurred while processing file: {futures[future]}")
            logging.info(e)

    return results, files  # Return both results and file names

#########################################################
##
#########################################################
def after_processing(results, files):
    """
    Function to execute after all files have been processed.
    Processes the collected results.
    """
    try:
        logging.info("All files have been processed. Performing post-processing steps...")
        logging.info("Collected results:")

        # Lists for processed file
        json_list = []
        cost_list = [] 
        pfiles_list = []
        ffiles_list = []

        for file_name, (json_obj, cost) in zip(files, results):
            if cost is None:
                ffiles_list.append(file_name)
                logging.info(f"... failed to process: {file_name}" )
            else:   
                pfiles_list.append(file_name)
                json_list.append(json_obj)
                cost_list.append(cost)

        return json_list, cost_list, pfiles_list, ffiles_list

    except Exception as e:
        logging.info(f"Exception occurred after processing:")
        logging.info(e)

#########################################################
##
#########################################################
def process_directory(file_toprocess_path, output_base_path=None):
    try:
        return True
    except Exception as e:
        logging.info(e)
        return e


#########################################################
##
#########################################################
def main(pdf_file_path):
    """Main function to process PDF, vectorize text, and interact with OpenAI."""
    try:
        # date time for filenames
        now = datetime.now() # current date and time
        date_time = now.strftime("%Y%m%d_%H%M")

        # Start the timer
        start_time = time.time()
        logging.info(f"starting: {date_time}")

        # Prepare output directories
        # TODO: Clean this up
        output_base = "./output"
        output_struct = OutputStruct(output_base, date_time)
        session_output_base_path = output_struct.init_output_dir()

        # Initialize logging
        print(f"log file: {output_struct.get_logfile_full_path()}")
        configure_logging(output_struct.get_logfile_full_path())

        # Lists for processed file
        json_list = []
        cost_list = [] 
        pfiles_list = []
        ffiles_list = []

        # Filters for files to be processed
        file_type = ".pdf"
        #pattern = r'med[\s_]man'

        #
        logging.info(f"Processing Starts: date and time {date_time}")
        logging.info(f"Results output will be written to {session_output_base_path}")
        logging.info(f"Log file: {output_struct.get_logs_full_path()}")


        # Check if the path is a directory
        if os.path.isdir(pdf_file_path):
            #print("The path is a directory.")

            # Get the list of files in the current directory
            files = os.listdir(pdf_file_path)
            
            # Filter the list to only include files that end with .pdf
            pdf_files = [f for f in files if f.endswith(file_type)]


            # Use ThreadPoolExecutor to process files in multiple threads
            max_threads = 5
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
                # Submit tasks to the executor
                futures = submit_tasks(executor, pdf_file_path, pdf_files, output_struct)

            # Handle futures and collect results
            results, files = handle_futures(futures)

            # Execute after all threads have completed
            json_list, cost_list, pfiles_list, ffiles_list = after_processing(results, files)

        else:
            json_obj, cost = process_file(pdf_file_path, output_struct.get_json_full_path())
            if cost is  None:
                ffiles_list.append(pdf_file_path)
            else:   
                pfiles_list.append(pdf_file_path)
                json_list.append(json_obj)
                cost_list.append(cost)

        # Create the output file
        output_file = date_time + "output.csv"
        json_string = json.dumps(json_list)
        convert_to_csv_alt(json_string,output_struct.get_csv_full_path() + "/" + output_file)

        # write files processed
        fproc_file_path = output_struct.get_processed_full_path() + "/" + "files_processed.json"
        with open(fproc_file_path, "w") as outfile:
            outfile.write(json.dumps(pfiles_list,indent=4))

        # write files failed to processed
        fproc_file_path = output_struct.get_failed_full_path() + "/" + "files_failed_to_process.json"
        with open(fproc_file_path, "w") as outfile:
            outfile.write(json.dumps(ffiles_list,indent=4))

        # write Open AI costs per call
        costs_file_path = output_struct.get_costs_full_path() + "/" + "ai_costs.json"
        with open(costs_file_path, "w") as outfile:
            outfile.write(json.dumps(cost_list,indent=4))

        # Calculate Tokens and Cost estimate 
        total_cost = calculate_api_cost(cost_list)
        logging.info (f"api cost >>> {total_cost}")

        return True

    except Exception as e:
        logging.info("Exception thrown ===>", e)
        logging.info(traceback.format_exc())
        #print("Exception thrown ===>", e)
        #print(traceback.format_exc())
        return e
    
    finally:
        # Stop the timer
        end_time = time.time()

        # Calculate the total time taken
        total_time = end_time - start_time

        # Print the total time taken
        logging.info("Total time taken: {} seconds".format(total_time))
    
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


    # Call the main procedure
    rc = main(pdf_file_path)
