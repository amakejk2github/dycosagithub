import os
import time
import asyncio
from base64 import b64decode, b64encode
from dycosa.drivers import Driver
class JobController(Driver):
    """
    This class manages the job and execute them if necessary
    """
    JobDirectory = "job"
    timed_jobs = list()
    periodic_jobs = list()
    jobs = list()
    def __init__(self):
        if not os.path.exists(self.JobDirectory):
            os.makedirs(self.JobDirectory)

    def add_job(self, name, jobfile):
        filename = os.path.join(self.JobDirectory, name + ".py")
        if os.path.isfile(filename):
            raise Exception("There is already a job called {job}".format(job=name))
        file = open(filename, 'w')
        file.write(b64decode(jobfile).decode("ascii"))
        file.close()
        return[]

    def delete_job(self, name):
        filename = os.path.join(self.JobDirectory, name + ".py")
        if not os.path.isfile(filename):
            raise Exception("There is no job called {job}".format(job=name))
        os.remove(filename)

    def list_jobs(self):
        return [y[:-3] for y in os.listdir(self.JobDirectory)]

    def get_job(self, name):
        filename = os.path.join(self.JobDirectory, name + ".py")
        if not os.path.isfile(filename):
            raise Exception("There is no job called {job}".format(job=name))
        file = open(filename, 'r')
        job = file.read()
        file.close()
        return {"name" : name, "jobfile" : b64encode(job.encode("ascii")).decode("ascii")}

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

    @asyncio.coroutine
    def run(self):
        print("Job-Controller: controller is running")
        while True:
            yield from asyncio.sleep(1)
            for fnc in self.periodic_jobs:
                if time.time() + fnc[1] >= fnc[2]:
                    fnc[0]()
                    fnc[2] = time.now
            for fnc in self.timed_jobs:
                if time.time()== fnc[1]:
                    fnc[0]()


