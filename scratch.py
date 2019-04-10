import numpy as np
from mpl_toolkits.mplot3d import axes3d
import socket, time
import flatbuffers as fb
from IMU0 import *
from PX4Data import PX4Data
def main():
    imu = PX4Data()
    while (True):
        #print(imu.acc.x, imu.acc.y,imu.acc.z )
        #print(imu.gyr.x, imu.gyr.y, imu.gyr.z)
        #print(imu.gps.x, imu.gps.y, imu.gps.z)
        #print(imu.quat.x, imu.quat.y, imu.quat.z, imu.quat.w)
        print(imu.vel.x, imu.vel.y, imu.vel.z)
        time.sleep(0.1)


    # serverIP = ''
    # server_address = (serverIP, 1111)
    #
    #
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect(server_address)
    #
    # while (True):
    #     buf = sock.recv(1024)
    #     if fb.Table.HasFileIdentifier(buf, "IMU0".encode()):
    #         imu = IMU0.GetRootAsIMU0(buf, 0)
    #         type = imu.Type()
    #         x = imu.X()
    #         y = imu.Y()
    #         z = imu.Z()
    #         w = imu.W()
    #         print(type)
    #         print(x, y, z, w)



if __name__ == '__main__':
    main()