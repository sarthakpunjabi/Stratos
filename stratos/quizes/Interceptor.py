"""This creates a singleton object of our application for Logging."""
from abc import abstractclassmethod, abstractmethod
import logging
from multiprocessing import get_logger
import os
import datetime
from django.conf import settings


class Interceptor:
    def __init__(self) -> None:
        self.logger = None

    class Concrete_Interceptor:
        def __init__(self) -> None:
            pass
        
        @abstractmethod
        def get_logger(self):
            pass

class Context_object():
    def __init__(self,get_response):
        self.get_response = get_response
        self.command = []
        

    def __call__(self,request):
        request.log = Concrete_Interceptor().get_logger()
        response = self.get_response(request)
        # print(response)
        return response
        

    def process_view(self,request, view_func, view_args, view_kwargs):
        pass

    def process_exception(self,request, exception):
        pass

    def process_execution(self,request,response):
        pass

    
    

class Concrete_Interceptor(Interceptor,Context_object):
    """
    This creates a logger instance of quiz application.
    It is used for demonstrating interceptor implementation.
    """
    _logger = None

    def __init__(self):
        if not self._logger:
            print("Logging Initialized...")
            self._logger = logging.getLogger("crumbs")
            self._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s'
            )
            now = datetime.datetime.now()
            dir_name = settings.LOG_LOCATION

            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)

            file_handler = logging.FileHandler(
                str(dir_name) + "/log_" + now.strftime("%Y-%m-%d") + ".log"
            )
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
            

    def get_logger(self):
        """
        Getter for returning the interceptor object.
        """
        return self._logger