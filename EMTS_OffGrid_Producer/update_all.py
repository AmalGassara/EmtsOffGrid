from threading import Thread
import time
import test1
class update_all(Thread):
    def  __init__(self):
        Thread.__init__(self)
        self.deamon=True
    def run(self):
        while True:
            currentForm=test1.Exchange.getInstance()
            currentForm.weather_data()
            currentForm.relay_state()
            currentForm.vedirect_connect()
            if (currentForm.battery == ''):
                currentForm.battery_from_solarcharger()
            else:
                currentForm.vedirect_battery()
            if (currentForm.solarcharger != ''):
                currentForm.vedirect_solarcharger()
            else:
                pass
            time.sleep(20) 