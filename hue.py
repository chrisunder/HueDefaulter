# !/usr/bin/python

from phue import Bridge
import time
import json
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "HueDefaulter"
    _svc_display_name_ = "Hue Defaulter"


    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                          servicemanager.PYS_SERVICE_STARTED,
                          (self._svc_name_,''))
        self.main()

    def main(self):
        default_temp = 366
        ideal_temp = 240  # Enter the desired colour temp here.
        bridge_ip = '192.168.86.22'  # Enter bridge IP here.
        room_name = 'Upstairs'
        b = Bridge(bridge_ip)

        # If running for the first time, press button on bridge and run with b.connect() uncommented
        b.connect()

        lights = b.get_light_objects()
        while True:
            for light in lights:
                if room_name in str(light.name):
                    if light.on:
                        if light.colortemp == default_temp:
                            print('Fixing: ', light.name)
                            light.colortemp = ideal_temp
            time.sleep(0.25)
        

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
