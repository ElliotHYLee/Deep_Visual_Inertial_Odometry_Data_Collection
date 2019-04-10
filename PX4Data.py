import numpy as np
from mpl_toolkits.mplot3d import axes3d
import socket, time
import flatbuffers as fb
from IMU0 import *
from threading import Thread

class IMUVector:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0



class PX4Data:
    def __init__(self):
        serverIP = ''
        server_address = (serverIP, 1111)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_address)
        self.acc = IMUVector()
        self.gyr = IMUVector()
        self.quat = IMUVector()
        self.gps = IMUVector()
        self.vel = IMUVector()
        self.stop = False
        th = Thread(target = self.listen)
        th.start()


    def close(self):
        self.stop = True

    def listen(self):
        while (not self.stop):
            buf = self.sock.recv(1024)
            if fb.Table.HasFileIdentifier(buf, "IMU0".encode()):
                imu = IMU0.GetRootAsIMU0(buf, 0)
                typeName = imu.Type().decode()
                x = imu.X()
                y = imu.Y()
                z = imu.Z()
                w = imu.W()
                if typeName == 'gps':
                    self.gps.x = x
                    self.gps.y = y
                    self.gps.z = z
                elif typeName == 'acc':
                    self.acc.x = x
                    self.acc.y = y
                    self.acc.z = z
                elif typeName == 'gyr':
                    self.gyr.x = x
                    self.gyr.y = y
                    self.gyr.z = z
                elif typeName == 'vel':
                    self.vel.x = x
                    self.vel.y = y
                    self.vel.z = z
                elif typeName == 'quat':
                    self.quat.x = x
                    self.quat.y = y
                    self.quat.z = z
                    self.quat.w = w
                #print(type)
                # print(x, y, z, w)


if __name__ == '__main__':
    m = PX4Data()
