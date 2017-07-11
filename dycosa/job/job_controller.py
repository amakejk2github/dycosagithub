import os
import time
try:
    from uasyncio import get_event_loop, open_connection, start_server, sleep_ms
except:
    from asyncio import get_event_loop, open_connection, start_server, sleep_ms
class JobController:
    """
    This class manages the job and execute them if necessary
    """
    JobDirectory = "job"
    timed_jobs = list()
    periodic_jobs = list()
    def __init__(self):
        if not os.path.exists(self.JobDirectory):
            os.makedirs(self.JobDirectory)

    def add_job(self):
        pass

    def delete_job(self):
        pass

    def list_jobs(self):
        pass

    def get_job(self):
        pass

    def run_periodically(self, period, func):
        self.periodic_jobs.append((func, period, time.now))

    def run_timed(self, time, func):
        self.timed_jobs.append((func, time))

    def add_restendpoint(self, jobname, endpoint, function):
        if hasattr(self, jobname):
            obj = getattr(self, jobname)
            setattr(obj, endpoint, function)
        else:
            obj = object()
            setattr(obj, endpoint, function)
            setattr(self, jobname, obj)

    def run(self):
        while True:
            for fnc in self.periodic_jobs:
                if time.time() + fnc[1] >= fnc[2]:
                    fnc[0]()
                    fnc[2] = time.now
            for fnc in self.timed_jobs:
                if time.time()== fnc[1]:
                    fnc[0]()


