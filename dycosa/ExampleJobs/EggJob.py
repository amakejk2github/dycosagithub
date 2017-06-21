from Jobs import Job
class EggJob(Job):
    
    def __init__(self):
        self.time = self.jobHelper.get_value("jobs/eggJob/getTime")['current_time']
        if self.time is None:
            self.time = 0
        self.value = self.jobHelper.drivers["encoder0"].value
        self.jobHelper.run_periodically("5m", self.check_temp)
        self.jobHelper.run_by_call("addjust_time", self.print_time)

    def run(self):
        while True:
            new_value = self.jobHelper.drivers['encode0'].value
            if new_value != self.value:
                delta = new_value - self.value
                self.value = new_value
                nodes = self.jobHelper.get_nodes_by_job("EggJob")
                for node in nodes:
                    node.jobs.eggJob.addjustTime(delta)

    def get_time(self):
        return {'current_time':self.time}

    def addjustTime(self, timeDelta):
        self.time = self.time + timeDelta
        self.jobHelper.drivers["timeRing0"].setTime(self.time)