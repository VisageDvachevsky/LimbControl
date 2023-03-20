import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

video = cv2.VideoCapture('../Test Video/test_video.mp4')

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        ret, frame = cap.read()

        ret_v, frame_v = video.read()
        
        if not ret_v:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        image_v = cv2.cvtColor(frame_v, cv2.COLOR_BGR2RGB)
        image_v.flags.writeable = False
        results_v = pose.process(image_v)

        image.flags.writeable = True
        image_v.flags.writeable = True
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        mp_drawing.draw_landmarks(image_v, results_v.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        CameraArr = []
        VideoArr = []

        if results.pose_landmarks is not None:
            for i, landmark in enumerate(results.pose_landmarks.landmark):
                CameraArr.append([landmark.x, landmark.y, landmark.z])

        if results_v.pose_landmarks is not None:
            for i, landmark in enumerate(results_v.pose_landmarks.landmark):
                VideoArr.append([landmark.x, landmark.y, landmark.z])

        if len(CameraArr) != len(VideoArr):
            min_length = min(len(CameraArr), len(VideoArr))
            CameraArr = CameraArr[:min_length]
            VideoArr = VideoArr[:min_length]

        distance = 0
        percent = 0
        for i in range(len(CameraArr)):
            x1, y1, z1 = CameraArr[i]
            x2, y2, z2 = VideoArr[i]
            distance += math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
            percent = (1 - (distance / 100)) * 100


        flipped_image = cv2.flip(image, 1)
        flipped_image = cv2.cvtColor(flipped_image, cv2.COLOR_RGB2BGR)
        print(distance)
        cv2.putText(flipped_image, f"Accuracy in percent: {percent:.1f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('MediaPipe Pose', flipped_image)        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()