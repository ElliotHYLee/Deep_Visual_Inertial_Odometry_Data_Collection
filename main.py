import numpy as np
import pyzed.sl as sl
import cv2
from PX4Data import PX4Data

def main():
    imu = PX4Data()
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_PERFORMANCE
    init_params.camera_resolution = sl.RESOLUTION.RESOLUTION_VGA  # Use HD1080 video mode
    init_params.camera_fps = 120  # Set fps at 60
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.COORDINATE_SYSTEM_RIGHT_HANDED_Z_UP_X_FWD
    init_params.coordinate_units = sl.UNIT.UNIT_METER  # Set units in meters

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)


    # Enable positional tracking with default parameters
    py_transform = sl.Transform()  # First create a Transform object for TrackingParameters object
    tracking_parameters = sl.TrackingParameters(init_pos=py_transform)
    err = zed.enable_tracking(tracking_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Capture 50 frames and stop
    i = 0
    image = sl.Mat()
    zed_pose = sl.Pose()
    zed_imu = sl.IMUData()
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.sensing_mode = sl.SENSING_MODE.SENSING_MODE_STANDARD  # Use STANDARD sensing mode
    prevTimeStamp = 0
    file = open('data/data.txt', 'w')
    key = 0
    depth = sl.Mat()
    point_cloud = sl.Mat()
    pcList = []
    while key != 113:
        # Grab an image, a RuntimeParameters object must be given to grab()
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS: # A new image is available if grab() returns SUCCESS
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.TIME_REFERENCE_CURRENT)  # Get the timestamp at the time the image was
            dt = (timestamp - prevTimeStamp) * 1.0 / 10 ** 9
            if dt > 0.03:
                # Get the pose of the left eye of the camera with reference to the world frame
                zed.get_position(zed_pose, sl.REFERENCE_FRAME.REFERENCE_FRAME_WORLD)

                # Display the translation and timestamp
                py_translation = sl.Translation()
                gnd_pos = zed_pose.get_translation(py_translation).get()
                tx = round(gnd_pos[0], 3)
                ty = round(gnd_pos[1], 3)
                tz = round(gnd_pos[2], 3)
                print("Translation: Tx: {0}, Ty: {1}, Tz {2}, Timestamp: {3}\n".format(tx, ty, tz, zed_pose.timestamp))

                # Display the orientation quaternion
                py_orientation = sl.Orientation()
                quat = zed_pose.get_orientation(py_orientation).get()
                ox = round(quat[0], 3)
                oy = round(quat[1], 3)
                oz = round(quat[2], 3)
                ow = round(quat[3], 3)
                print("Orientation: Ox: {0}, Oy: {1}, Oz {2}, Ow: {3}\n".format(ox, oy, oz, ow))

                zed.retrieve_image(image, sl.VIEW.VIEW_LEFT)
                img = image.get_data()
                cv2.imwrite('data/images/' + str(timestamp) + '.png', img)

                zed.retrieve_measure(depth, sl.MEASURE.MEASURE_DEPTH)
                # Retrieve colored point cloud. Point cloud is aligned on the left image.
                zed.retrieve_measure(point_cloud, sl.MEASURE.MEASURE_XYZRGBA)
                print(point_cloud.get_data().shape)
                pc = np.reshape(point_cloud.get_data(), (1, 376, 672, 4))
                pcList.append(pc)

                cv2.imshow("ZED", img)
                key = cv2.waitKey(1)

                prevTimeStamp = timestamp
                print(dt)
                print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image.get_width(), image.get_height(), timestamp))

                file.write('%d '
                           '%.4f %.4f %.4f '
                           '%.4f %.4f %.4f %.4f '
                           '%.4f %.4f %.4f '
                           '%.4f %.4f %.4f '
                           '%.4f %.4f %.4f '
                           '%.4f %.4f %.4f '
                           '%.4f %.4f %.4f %.4f \n' % (timestamp, tx, ty, tz, ox, oy, oz, ow,
                                                       imu.acc.x, imu.acc.y, imu.acc.z,
                                                       imu.gyr.x, imu.gyr.y, imu.gyr.z,
                                                       imu.gps.x, imu.gps.y, imu.gps.z,
                                                       imu.vel.x, imu.vel.y, imu.vel.z,
                                                       imu.quat.x, imu.quat.y, imu.quat.z, imu.quat.w))
                i = i + 1

    # Close the camera
    pc = np.concatenate(pcList, axis=0)
    np.save('pc', pc)
    zed.close()
    file.close()
    imu.close()


if __name__ == '__main__':
    main()
