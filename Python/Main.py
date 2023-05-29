import cv2
import mediapipe as mp
import math

def calculate_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

video_path = 'video.mp4'

cap = cv2.VideoCapture(video_path)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    webcam = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Не удалось прочитать видео")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(image)

        image = cv2.resize(image, (640, 480))

        # mp_drawing.draw_landmarks(
        #     image,
        #     results.pose_landmarks,
        #     mp_pose.POSE_CONNECTIONS,
        #     mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        #     mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
        # )

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            keypoints_file = [
                (landmarks[mp_pose.PoseLandmark.NOSE].x, landmarks[mp_pose.PoseLandmark.NOSE].y, landmarks[mp_pose.PoseLandmark.NOSE].z),
                (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].z),
                (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].z)
            ]

            while len(keypoints_file) < 3:
                keypoints_file.append((0, 0, 0))

        _, webcam_frame = webcam.read()

        webcam_image = cv2.cvtColor(webcam_frame, cv2.COLOR_BGR2RGB)
        webcam_results = pose.process(webcam_image)

        # mp_drawing.draw_landmarks(
        #     webcam_frame,
        #     webcam_results.pose_landmarks,
        #     mp_pose.POSE_CONNECTIONS,
        #     mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        #     mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
        # )

        if webcam_results.pose_landmarks:
            webcam_landmarks = webcam_results.pose_landmarks.landmark

            keypoints_webcam = [
                (webcam_landmarks[mp_pose.PoseLandmark.NOSE].x, webcam_landmarks[mp_pose.PoseLandmark.NOSE].y, webcam_landmarks[mp_pose.PoseLandmark.NOSE].z),
                (webcam_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, webcam_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y, webcam_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].z),
                (webcam_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, webcam_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y, webcam_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].z)
            ]

            while len(keypoints_webcam) < 3:
                keypoints_webcam.append((0, 0, 0))

            distance = calculate_distance(
                keypoints_file[0][0], keypoints_file[0][1], keypoints_file[0][2],
                keypoints_webcam[0][0], keypoints_webcam[0][1], keypoints_webcam[0][2]
            )
            cv2.putText(webcam_frame, f"Distance: {distance}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


        cv2.imshow('Pose Estimation', webcam_frame)
        cv2.imshow('Pose Estimation with file', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    webcam.release()
    cv2.destroyAllWindows()
