import time
import threading as th
import math

import cv2
import mediapipe as mp

# required variable
VideoData = []
CameraData = []

# get image
Video = cv2.VideoCapture('../Test Video/test_video.mp4')
Camera = cv2.VideoCapture(0)

# Tracking/Pose Settings
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Camera settings
Camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
Camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
Camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Some functions


def VideoCoordintations(VideoArray, SampleVideo):
    while Video.isOpened():
        _, frame = Video.read()
        try:
            frame = cv2.resize(frame, (1280, 720))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = pose.process(frame_rgb)
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if results.pose_world_landmarks:
                for l in results.pose_world_landmarks.landmark:
                    VideoArray += [f'{l.x},{-l.y},{l.z}']

            cv2.imshow("VideoTrack", frame)

        except Exception as ex:
            print(ex)
            break
        if(cv2.waitKey(1) == ord('q')):
            return VideoArray
            break

    Video.release()


def CameraCoordinations(CameraArray, WebCam):
    new_frame_time = 0
    prev_frame_time = 0
    while WebCam.isOpened():
        succes, image = WebCam.read()
        if not succes:
            print("Ignore empty camera frame")
            continue

        try:
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            font = cv2.FONT_HERSHEY_SIMPLEX

            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps = str(fps)
            cv2.putText(image, fps, (7, 70), font, 3,
                        (100, 255, 0), 3, cv2.LINE_AA)

            if results.pose_world_landmarks:
                for l in results.pose_world_landmarks.landmark:
                    CameraArray += [f'{l.x},{-l.y},{l.z}']
            cv2.imshow("CameraTrack", image)

        except Exception as ex:
            print(ex)
            break
        if(cv2.waitKey(1) == ord('w')):
            return CameraArray
            break


if __name__ == '__main__':
    integerCamer_XYZ = []
    integerVideo_XYZ = []

    for element in VideoCoordintations(VideoData, Video):
        Video_XYZ = element.split(',')
        for elem in Video_XYZ:
            integerVideo_XYZ.append(float(elem))

    for item in CameraCoordinations(CameraData, Camera):
        Camera_XYZ = item.split(',')
        for elem in Camera_XYZ:
            integerCamer_XYZ.append(float(elem))

    Similarity = math.sqrt((integerVideo_XYZ[0]-integerCamer_XYZ[0])**2+
        (integerVideo_XYZ[1]-integerCamer_XYZ[1])**2+
        (integerVideo_XYZ[2]-integerCamer_XYZ[2]) **2)
    print(f'Аккуратность повторения движений: {Similarity}')
