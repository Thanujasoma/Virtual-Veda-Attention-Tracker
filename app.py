import cv2
import dlib
import time
import numpy as np
import pandas as pd
import os
import mediapipe as mp
from scipy.spatial import distance
from imutils import face_utils

# -------------------------------
# FUNCTIONS
# -------------------------------

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[2], mouth[10])
    B = distance.euclidean(mouth[4], mouth[8])
    C = distance.euclidean(mouth[0], mouth[6])
    return (A + B) / (2.0 * C)

# -------------------------------
# INITIALIZATION
# -------------------------------

EAR_THRESHOLD = 0.25
MAR_THRESHOLD = 0.6
YAWN_FRAMES = 10

blink_count = 0
blink_frames = 0
yawn_count = 0
yawn_frames = 0

score = 50

last_logged_time = time.time()
LOG_INTERVAL = 5  # seconds

# Excel setup
excel_file = "attention_report.xlsx"

if not os.path.exists(excel_file):
    df_init = pd.DataFrame(columns=[
        "Time", "Name", "Status", "Score", "Hand Raised"
    ])
    df_init.to_excel(excel_file, index=False)

# CSV log
log_data = []

# -------------------------------
# LOAD MODELS
# -------------------------------

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

face_net = cv2.dnn.readNetFromCaffe(
    "deploy.prototxt",
    "res10_300x300_ssd_iter_140000.caffemodel"
)

# Mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# -------------------------------
# LOAD STUDENTS
# -------------------------------

orb = cv2.ORB_create()
known_faces = {}
attendance_data = {}

IMAGE_FOLDER = "student image"

for file in os.listdir(IMAGE_FOLDER):
    if file.endswith(("jpg", "png", "jpeg")):
        path = os.path.join(IMAGE_FOLDER, file)
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        kp, des = orb.detectAndCompute(image, None)
        if des is not None:
            name = file.split(".")[0]
            known_faces[name] = des
            attendance_data[name] = "Not Raised"

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# -------------------------------
# CAMERA
# -------------------------------

cap = cv2.VideoCapture(0)

(lStart, lEnd) = (42, 48)
(rStart, rEnd) = (36, 42)
(mStart, mEnd) = (48, 68)

with mp_hands.Hands(min_detection_confidence=0.7,
                    min_tracking_confidence=0.7) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # -------------------------------
        # HAND DETECTION
        # -------------------------------
        results = hands.process(rgb_frame)
        hand_raised_flag = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist_y = hand_landmarks.landmark[
                    mp_hands.HandLandmark.WRIST].y
                index_tip_y = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                if index_tip_y < wrist_y:
                    hand_raised_flag = True

                mp_draw.draw_landmarks(frame, hand_landmarks,
                                       mp_hands.HAND_CONNECTIONS)

        # -------------------------------
        # FACE DETECTION
        # -------------------------------
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0))
        face_net.setInput(blob)
        detections = face_net.forward()

        for i in range(detections.shape[2]):
            if detections[0, 0, i, 2] > 0.6:

                box = detections[0, 0, i, 3:7] * \
                      np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")

                face_roi = gray[y1:y2, x1:x2]

                # Face recognition
                kp, des = orb.detectAndCompute(face_roi, None)
                name = "Unknown"
                best_matches = 0

                for student_name, known_des in known_faces.items():
                    if des is not None:
                        matches = bf.match(known_des, des)
                        if len(matches) > best_matches:
                            best_matches = len(matches)
                            name = student_name

                # Landmarks
                rect = dlib.rectangle(x1, y1, x2, y2)
                landmarks = predictor(gray, rect)
                landmarks = face_utils.shape_to_np(landmarks)

                leftEye = landmarks[lStart:lEnd]
                rightEye = landmarks[rStart:rEnd]
                mouth = landmarks[mStart:mEnd]

                ear = (eye_aspect_ratio(leftEye) +
                       eye_aspect_ratio(rightEye)) / 2.0
                mar = mouth_aspect_ratio(mouth)

                # Blink
                if ear < EAR_THRESHOLD:
                    blink_frames += 1
                else:
                    if blink_frames >= 3:
                        blink_count += 1
                    blink_frames = 0

                # Yawn
                if mar > MAR_THRESHOLD:
                    yawn_frames += 1
                else:
                    if yawn_frames >= YAWN_FRAMES:
                        yawn_count += 1
                    yawn_frames = 0

                # Head pose
                nose = landmarks[30]
                left_eye = landmarks[36]
                right_eye = landmarks[45]
                center = (left_eye[0] + right_eye[0]) // 2

                if nose[0] < center - 15:
                    attention_status = "Looking Left"
                elif nose[0] > center + 15:
                    attention_status = "Looking Right"
                else:
                    attention_status = "Looking Center"

                # Final status
                status = "Attentive"
                if ear < EAR_THRESHOLD:
                    status = "Drowsy"
                elif mar > MAR_THRESHOLD:
                    status = "Yawning"
                elif attention_status != "Looking Center":
                    status = "Distracted"

                # Score
                if ear < EAR_THRESHOLD:
                    score -= 2
                else:
                    score += 1

                if mar > MAR_THRESHOLD:
                    score -= 3

                if attention_status != "Looking Center":
                    score -= 1

                if hand_raised_flag:
                    score += 5
                    attendance_data[name] = "Raised"

                score = max(0, min(score, 100))

                # -------------------------------
                # LOG EVERY 5 SECONDS
                # -------------------------------
                current_time = time.time()

                if current_time - last_logged_time >= LOG_INTERVAL:
                    timestamp = time.strftime("%H:%M:%S")
                    hand_status = "Yes" if hand_raised_flag else "No"

                    # Excel append
                    new_row = pd.DataFrame([{
                        "Time": timestamp,
                        "Name": name,
                        "Status": status,
                        "Score": score,
                        "Hand Raised": hand_status
                    }])

                    with pd.ExcelWriter(excel_file, mode='a',
                                        engine='openpyxl',
                                        if_sheet_exists='overlay') as writer:
                        new_row.to_excel(writer, index=False,
                                         header=False,
                                         startrow=writer.sheets['Sheet1'].max_row)

                    # CSV log
                    log_data.append({
                        "Time": timestamp,
                        "Name": name,
                        "Status": status,
                        "Score": score,
                        "Hand Raised": hand_status
                    })

                    last_logged_time = current_time

                # Display
                cv2.rectangle(frame, (x1, y1), (x2, y2),
                              (0,255,0), 2)

                cv2.putText(frame, name, (x1, y1 - 10),
                            0, 0.7, (0,255,0), 2)

                cv2.putText(frame, f"Status: {status}",
                            (10, 30), 0, 0.7, (255,255,0), 2)

                cv2.putText(frame, f"Score: {score}",
                            (10, 60), 0, 0.7, (0,255,0), 2)

                cv2.putText(frame, f"Blinks: {blink_count}",
                            (10, 90), 0, 0.7, (0,255,255), 2)

                cv2.putText(frame, f"Yawns: {yawn_count}",
                            (10, 120), 0, 0.7, (0,255,255), 2)

                if hand_raised_flag:
                    cv2.putText(frame, "Hand Raised!",
                                (x1, y2 + 30),
                                0, 0.7, (0,255,0), 2)

        cv2.imshow("Virtual Veda", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# -------------------------------
# SAVE CSV
# -------------------------------
cap.release()
cv2.destroyAllWindows()

df = pd.DataFrame(log_data)
df.to_csv("session_log.csv", index=False)

print("✅ Excel + CSV saved successfully!")