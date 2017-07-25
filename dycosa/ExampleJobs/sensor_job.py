from dycosa.job import Job
class SensorJob(Job):

    @Job.run_periodically("5m")
    def check_temp(self):
        sens = self.jobHelper.get_node_by_id("00:28:f8:67:f3:7a")
        fans = self.jobHelper.get_nodes_by_driver("Fan")
        for fan in fans:
            if sens.get_temperature() > 30:
                fan.pwm(100)
            else:
                fan.pwm(0)

    @Job.run_timed("10:00")
    def print_time(self):
        print("It's 10:00")