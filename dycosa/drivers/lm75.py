from machine import Pin,I2C

class LM75:
    def __init__(self, SDA,SCL, adress,freq=400000):
        self.SDA = SDA
        self.SCL = SCL
        self.adress = adress
        self.freq = freq

    def readTemp(self):
        I2C.init(SCL,SDA,FREQ)
        I2C.start()
        temp = I2C.readfrom(self.adress,1)
        // I2C.deinit()
        return temp

if __name__ == "__main__":
    lm75 = lm75(4,5,72)
    for i in range(0,100)
        print(readTemp())