import os
class JobController:
    """
    This class manages the jobs and execute them if necessary
    """
    JobDirectory = "Jobs"
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