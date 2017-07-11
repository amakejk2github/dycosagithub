class JobHelper:

    def __init__(self, job_controller):
        self.job_controller = job_controller

    def run_periodically(self, period, func):
        pass

    def run_timed(self, time, func):
        pass

    def add_restendpoint(self, jobname, endpoint, func):
        self.job_controller.add_restendpoint(jobname, endpoint, func)