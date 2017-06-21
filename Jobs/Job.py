class Job:
    
    def __init__(self):
        pass

    def run(self):
        pass

    def restendpoint(self, func):
        self.jobhelper.add_restendpoint(func)
        return func

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