import cv2
import numpy as np

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    # "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    # "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    # "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    # "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}


def aruco_display(corners, ids, rejected, image):
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
            # compute and draw the center (x, y)-coordinates of the ArUco
            # marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
            # draw the ArUco marker ID on the image
            cv2.putText(image, str(markerID), (topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            print("[Inference] ArUco marker ID: {}".format(markerID))
        # show the output image
    return image


def aruco_3d_cube(image, rvec, tvec, camera_matrix, dist_coeffs, cube_side):
    half_size = cube_side / 2
    object_points = np.empty((8, 3), dtype=np.float32)

    object_points[0, 0] = -half_size
    object_points[0, 1] = -half_size
    object_points[0, 2] = 0
    object_points[4, 0] = -half_size
    object_points[4, 1] = -half_size
    object_points[4, 2] = cube_side

    object_points[1, 0] = -half_size
    object_points[1, 1] = half_size
    object_points[1, 2] = 0
    object_points[5, 0] = -half_size
    object_points[5, 1] = half_size
    object_points[5, 2] = cube_side

    object_points[2, 0] = half_size
    object_points[2, 1] = half_size
    object_points[2, 2] = 0
    object_points[6, 0] = half_size
    object_points[6, 1] = half_size
    object_points[6, 2] = cube_side

    object_points[3, 0] = half_size
    object_points[3, 1] = -half_size
    object_points[3, 2] = 0
    object_points[7, 0] = half_size
    object_points[7, 1] = -half_size
    object_points[7, 2] = cube_side

    image_points = cv2.projectPoints(objectPoints=object_points, rvec=rvec, tvec=tvec, cameraMatrix=camera_matrix,
                                     distCoeffs=dist_coeffs)[0]
    image_points = np.round(image_points)
    image_points = image_points.astype(int)
    image_points = image_points.tolist()
    image_points = [tuple(image_points[i][0]) for i in range(len(image_points))]

    for i in range(4):
        image = cv2.line(image, image_points[i], image_points[(i + 1) % 4], (255, 255, 0), 2)
    for i in range(4):
        image = cv2.line(image, image_points[i + 4], image_points[4 + (i + 1) % 4], (255, 255, 0), 2)
    for i in range(4):
        image = cv2.line(image, image_points[i], image_points[i + 4], (255, 255, 0), 2)

    return image
