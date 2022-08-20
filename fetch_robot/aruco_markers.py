import cv2
from aruco_utils import ARUCO_DICT, aruco_3d_cube
# import os
import pickle
import io


def single_aruco_create(dict_name, id, side_pixel, border_bits):
    aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_name])
    tag = cv2.aruco.drawMarker(aruco_dict, id, side_pixel, border_bits)
    return tag


def gridboard_aruco_create(n_markers_w, n_markers_h, dict_name, image_size, marker_side, marker_separation=0.1,
                           first_marker=0, padding_size=[20] * 4, padding_color=[255] * 3):
    aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_name])
    grid_board = cv2.aruco.GridBoard_create(markersX=n_markers_w, markersY=n_markers_h, markerLength=marker_side,
                                            markerSeparation=marker_separation, dictionary=aruco_dict,
                                            firstMarker=first_marker)
    img = grid_board.draw(image_size)
    img = cv2.copyMakeBorder(img, padding_size[0], padding_size[1], padding_size[2], padding_size[3],
                             cv2.BORDER_CONSTANT, value=padding_color)

    return img, grid_board


def gridboard_charuco_create(x_squares, y_squares, dict_name, image_size, square_length, marker_length,
                             padding_size=[20] * 4, padding_color=[255] * 3):
    aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_name])
    charuco_grid_board = cv2.aruco.CharucoBoard_create(squaresX=x_squares, squaresY=y_squares,
                                                       squareLength=square_length,
                                                       markerLength=marker_length, dictionary=aruco_dict)
    img = charuco_grid_board.draw(image_size)
    img = cv2.copyMakeBorder(img, padding_size[0], padding_size[1], padding_size[2], padding_size[3],
                             cv2.BORDER_CONSTANT, value=padding_color)

    return img, charuco_grid_board


def camera_calibration_charuco(video, dict_name, board, append_prev_calib):
    aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_name])
    # video = cv2.VideoCapture(0)
    # video.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    # video.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    all_corners = []
    all_ids = []
    counter1 = 1
    while True:
        ret, frame = video.read()
        if ret:
            tmp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # detected_frame = frame
            corners, ids, rejected = cv2.aruco.detectMarkers(tmp_frame, aruco_dict)
            if (ids is not None) and (ids.size > 0):
                retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(corners, ids, tmp_frame, board)
                if retval > 9:
                    frame = cv2.aruco.drawDetectedMarkers(frame, corners=corners, ids=ids)
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1000) & 0xFF == ord('p'):
                        print('image ' + str(counter1))
                        all_corners.append(charuco_corners)
                        all_ids.append(charuco_ids)
                        counter1 += 1
                else:
                    pass
            if cv2.waitKey(1) == 27:
                break
        else:
            print("waiting for the video")
    video.release()
    cv2.destroyAllWindows()

    new_calib = {'corners': all_corners, 'ids': all_ids}
    if append_prev_calib:
        calibration_file = io.open("calibration_data.pickle", "rb")
        prev_calib = pickle.load(calibration_file)
        new_calib['corners'] = new_calib['corners'] + prev_calib['corners']
        new_calib['ids'] = new_calib['ids'] + prev_calib['ids']
        calibration_file.close()

    calibration_file = io.open("calibration_data.pickle", "wb")
    pickle.dump(new_calib, calibration_file)
    calibration_file.close()

    try:
        cal = cv2.aruco.calibrateCameraCharucoExtended(charucoCorners=new_calib['corners'], charucoIds=new_calib['ids'],
                                                       board=board, imageSize=tmp_frame.shape, distCoeffs=None,
                                                       cameraMatrix=None)
        calibration_output = {'cameraMatrix': cal[1], 'distCoeffs': cal[2]}
        output_file = io.open("calibration_output.pickle", "wb")
        pickle.dump(calibration_output, output_file)
        output_file.close()
    except Exception:
        print('Calibration Error')


def detect_aruco(source, dict_name=None, aruco_dict=None, aruco_params=None, image_name=None,
                 frame=None, refine=False, board=None):
    if aruco_params is None:
        aruco_params = cv2.aruco.DetectorParameters_create()
    if aruco_dict is None:
        aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_name])
    if source == 0:
        image = cv2.imread(image_name)
    else:
        image = frame
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    if refine:
        corners, ids, rejected, recoveredIdxs = cv2.aruco.refineDetectedMarkers(gray, board=board,
                                                                                detectedCorners=corners,
                                                                                detectedIds=ids,
                                                                                rejectedCorners=rejected)
        # print(recoveredIdxs)
    detected_markers_image = cv2.aruco.drawDetectedMarkers(corners=corners, ids=ids, image=image)
    if ids is not None:
        all_ids = [item for id in ids for item in id]
    else:
        all_ids = ids
    markers_data = {'corners': corners, 'ids': all_ids, 'rejected': rejected}
    # cv2.imshow("Detected Markers", detected_markers_image)

    return detected_markers_image, markers_data


def aruco_position_estimate(frame, aruco_dict, aruco_params, board, camera_calib, real_marker_size):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_markers_image, markers_data = detect_aruco(source=1, frame=frame, aruco_dict=aruco_dict,
                                                        aruco_params=aruco_params, refine=True, board=board)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
    for nid, corner in enumerate(markers_data['corners']):
        markers_data[nid] = cv2.cornerSubPix(gray, corner, winSize=(3, 3), zeroZone=(-1, -1), criteria=criteria)
    # frame_markers = cv2.aruco.drawDetectedMarkers(frame, markers_data['corners'], markers_data['ids'])
    rvecs, tvecs, obj_point = cv2.aruco.estimatePoseSingleMarkers(corners=markers_data['corners'], markerLength=real_marker_size,
                                                       cameraMatrix=camera_calib['cameraMatrix'],
                                                       distCoeffs=camera_calib['distCoeffs'])

    if rvecs is not None:
        for i in range(len(tvecs)):
            detected_markers_image = cv2.drawFrameAxes(image=detected_markers_image, cameraMatrix=camera_calib['cameraMatrix'],
                                                        distCoeffs=camera_calib['distCoeffs'],
                                                        rvec=rvecs[i], tvec=tvecs[i], length=0.01)
            detected_markers_image = aruco_3d_cube(image=detected_markers_image, tvec=tvecs[i], rvec=rvecs[i],
                          camera_matrix=camera_calib['cameraMatrix'], dist_coeffs=camera_calib['distCoeffs'],
                          cube_side=real_marker_size)
    return detected_markers_image, tvecs, rvecs, markers_data['ids']
