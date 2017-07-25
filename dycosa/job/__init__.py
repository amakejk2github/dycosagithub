class Job:
    def __init__(self, jobhelper):
        self.jobhelper = jobhelper

    def restendpoint(self, endpoint):
        def wrapper(func):
            self.jobhelper.add_restendpoint(self.__name__, endpoint, func)
            return func

        return wrapper

    def run_periodically(self, period):
        def wrapper(func):
            self.jobhelper.add_periodic_run(period, func)
            return func

        return wrapper

    def run_timed(self, time):
        def wrapper(func):
            self.jobhelper.add_timed(time, func)
            return func

        return wrapper

class JobHelper:

    def __init__(self, job_controller):
        self.job_controller = job_controller

    def run_periodically(self, period, func):
        pass

    def run_timed(self, time, func):
        pass

    def add_restendpoint(self, jobname, endpoint, func):
        self.job_controller.add_restendpoint(jobname, endpoint, func)