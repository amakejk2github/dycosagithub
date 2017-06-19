class SensorJob(Job):
    
    def __init__(self):
        self.jobHelper.run_periodically("5m", self.check_temp)
        self.jobHelper.run_timed("10:00", self.print_time)
        pass

    def check_temp(self):
        sens = self.jobHelper.get_node_by_id("00:28:f8:67:f3:7a")
        fans = self.jobHelper.get_nodes_by_driver("Fan")
        for fan in fans:
            if sens.get_temperature() > 30:
                fan.pwm(100)
            else:
                fan.pwm(0)

    def print_time(self):
        print("It's 10:00")