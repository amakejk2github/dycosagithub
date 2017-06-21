import os
try:
    from uasyncio import get_event_loop, open_connection, start_server, sleep_ms
except:
    from asyncio import get_event_loop, open_connection, start_server, sleep_ms
class JobController:
    """
    This class manages the jobs and execute them if necessary
    """
    JobDirectory = "Jobs"
    def __init__(self):
        self.queued_jobs = queue.Queue()
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

    def call_job(self, name, method, payload):
        pass

    def run(self):
        while True:
            if not self.queued_jobs.empty():
                job = self.queued_jobs.get()
                myJob = __import__(job.name)[0]
                jobObj = myJob()
                #ToDo Add job to uasyncip queue



