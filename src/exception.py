import sys


def get_error_details(error,error_details:sys):
    _,_,ex_tab = error_details.exc_info()
    file_name = ex_tab.tb_frame.f_code.co_filename
    error_message = "The error occured in the file name [{}] at the line number [{}] with the error message [{}]".format(file_name,ex_tab.tb_lineno,str(error))

    return error_message


class CustomException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)
        self.error_message = get_error_details(error_message,error_details)

    def __str__(self):
        return self.error_message
