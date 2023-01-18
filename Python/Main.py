# default library
import time
from threading import Thread

# custom library
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
Camera.set(cv2.CAP_PROP_FRAME_WIDTH, 854)
Camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Threading return class
class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

# Some functions


def VideoCoordintations(VideoArray, SampleVideo):
    """
    { conclusion coordinates from video }

    :param      VideoArray:   The video array
    :type       VideoArray:   { List }
    :param      SampleVideo:  The sample video
    :type       SampleVideo:  { cv2 video }

    :returns:   { return list with video coordinates }
    :rtype:     { array }
    """
    # check video state
    while Video.isOpened():
        _, frame = Video.read()
        try:
            # change video size
            frame = cv2.resize(frame, (854, 480))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = pose.process(frame_rgb)
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            # parse landmarks
            if results.pose_world_landmarks:
                for l in results.pose_world_landmarks.landmark:
                    VideoArray += [f'{l.x},{-l.y},{l.z}']

            cv2.imshow("VideoTrack", frame)

        except Exception as ex:
            print(str(ex))
            break
        if(cv2.waitKey(1) == ord('w')):
            return VideoArray
            break

    Video.release()


def CameraCoordinations(CameraArray, WebCam):
    """
    { conclution coordinates from camera }

    :param      CameraArray:  The camera array
    :type       CameraArray:  { list }
    :param      WebCam:       The web camera
    :type       WebCam:       { cv2 camera }

    :returns:   { return list with camera coordinates }
    :rtype:     { array }
    """
    # fps config
    new_frame_time = 0
    prev_frame_time = 0
    # check camera state
    while WebCam.isOpened():
        succes, image = WebCam.read()
        if not succes:
            print("Ignore empty camera frame")
            continue

        try:
            # tracking settings
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
            # fps settings
            font = cv2.FONT_HERSHEY_SIMPLEX

            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps = str(fps)
            cv2.putText(image, fps, (7, 70), font, 3,
                        (100, 255, 0), 3, cv2.LINE_AA)
            # parse landmarks
            if results.pose_world_landmarks:
                for l in results.pose_world_landmarks.landmark:
                    CameraArray += [f'{l.x},{-l.y},{l.z}']
            cv2.imshow("CameraTrack", image)

        except Exception as ex:
            print(str(ex))
            break
        if(cv2.waitKey(1) == ord('w')):
            return CameraArray
            break


if __name__ == '__main__':
    # Thread object
    twrv = ThreadWithReturnValue(target=VideoCoordintations, args=(VideoData, Video,))
    twrv1 = ThreadWithReturnValue(target=CameraCoordinations, args=(CameraData, Camera,))
    # Thread Start
    twrv.start()
    twrv1.start()