import os

#########################################################
##
#########################################################
class OutputStruct:
    def __init__(self,init_path, file_prefix):
        try:
            self.init_path = init_path
            self.file_prefix = file_prefix
            self.session_output = self.init_path + "/output_" + self.file_prefix 

            self.json = "/json"
            self.logs = "/logs"
            self.files_processed = "/files_processed"
            self.files_failed = "/files_failed"
            self.costs = "/costs"
            self.csv = "/csv"
        except Exception as e:
            print(e)
            raise e

    def init_output_dir(self):
        try:
            print("session_output ", self.session_output)

            if not os.path.exists(self.init_path):
                os.mkdir(self.init_path)

            os.mkdir(self.session_output)

            os.mkdir(self.session_output + self.costs)
            os.mkdir(self.session_output + self.csv)
            os.mkdir(self.session_output + self.json)
            os.mkdir(self.session_output + self.files_failed)
            os.mkdir(self.session_output + self.files_processed)
            os.mkdir(self.session_output + self.logs)

            return self.session_output
        except Exception as e:
            print(e)
            raise e
    
    def get_costs_full_path(self):
        return self.session_output + self.costs
    def get_csv_full_path(self):
        return self.session_output + self.csv
    def get_processed_full_path(self):
        return self.session_output + self.files_processed
    def get_failed_full_path(self):
        return self.session_output + self.files_failed
    def get_json_full_path(self):
        return self.session_output + self.json
    def get_logs_full_path(self):
        return self.session_output + self.logs
