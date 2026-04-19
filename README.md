# 🎓 Virtual Veda – Student Attentiveness Monitoring System

## 📌 Project Overview

**Virtual Veda** is a computer vision-based intelligent system designed to monitor and evaluate student attentiveness during virtual learning sessions. The system uses real-time webcam input to analyze behavioral patterns such as eye blinking, yawning, head movement, and hand gestures.

It provides a **dynamic attentiveness score**, real-time feedback, and logs data for further analysis, helping improve engagement and accountability in online education.

---

## 🚀 Features

* Real-time video processing using webcam
* Face detection and student recognition
* Blink detection using **Eye Aspect Ratio (EAR)**
* Yawn detection using **Mouth Aspect Ratio (MAR)**
* Head pose estimation (focus detection)
* Hand raise detection using **MediaPipe**
* Dynamic attentiveness scoring (0–100)
* Automated attendance tracking
* Data logging in **Excel (.xlsx)** and **CSV (.csv)**
* Real-time display of status, score, and activity

---

## 🧠 Technologies Used

* Python
* OpenCV – Image processing & face detection
* Dlib – Facial landmark detection (68 points)
* MediaPipe – Hand gesture recognition
* NumPy – Numerical computations
* Pandas – Data handling and logging
* SciPy – Distance calculations
* Imutils – Utility functions
* OpenPyXL – Excel file handling

---

## 📂 Project Structure

```
Virtual-Veda/
│
├── student image/              # Dataset for face recognition
├── shape_predictor_68_face_landmarks.dat
├── deploy.prototxt
├── res10_300x300_ssd_iter_140000.caffemodel
│
├── app.py                     # Main implementation file
├── attention_report.xlsx       # Generated Excel report
├── session_log.csv             # Generated CSV log
│
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

---

## ⚙️ Installation

### Step 1: Clone the Repository

```
git clone https://github.com/your-username/virtual-veda.git
cd virtual-veda
```

---

### Step 2: Install Dependencies

```
pip install -r requirements.txt
```

---

### ⚠️ Important (Dlib Installation)

If `dlib` fails to install:

```
pip install dlib
```

For Windows users, you may need precompiled wheels.

---

### Step 3: Download Required Models

Download and place the following files in the project directory:

* `shape_predictor_68_face_landmarks.dat`
* `deploy.prototxt`
* `res10_300x300_ssd_iter_140000.caffemodel`

---

## ▶️ How to Run

```
python main.py
```

Press **`q`** to exit the application.

---

## 🧾 Output

### 📊 Excel Report (`attention_report.xlsx`)

* Timestamp
* Student Name
* Status (Attentive/Drowsy/Yawning/Distracted)
* Score
* Hand Raise Status

### 📁 CSV Log (`session_log.csv`)

* Session-wise detailed logs for analysis

---

## 🖥️ Sample Output Display

* Face detection with name
* Live attentiveness status
* Score (0–100)
* Blink count
* Yawn count
* Hand raise notification

---

## 📈 Attentiveness Scoring Logic

| Behavior     | Score Impact |
| ------------ | ------------ |
| Eye closed   | -2           |
| Yawning      | -3           |
| Looking away | -1           |
| Hand raised  | +5           |

Score is maintained between **0 and 100**.


# Outputs

#  Student in Attentive State


<img width="564" height="505" alt="image" src="https://github.com/user-attachments/assets/fa8cc0ea-ccfa-4bbc-b910-d6bd3e76ab1f" />

#  Student in Drowsy State


<img width="708" height="505" alt="image" src="https://github.com/user-attachments/assets/4808de91-97c0-4d9b-8b66-c7582b4a375b" />


#  Yawning Detection Output


<img width="579" height="535" alt="image" src="https://github.com/user-attachments/assets/69daf97e-88a7-4ff4-8bd4-deaac249a9b9" />


#  Distracted State Detection Output

<img width="425" height="361" alt="image" src="https://github.com/user-attachments/assets/1e6ffd71-f587-4194-8187-dbd7562bbe71" />
<img width="402" height="367" alt="image" src="https://github.com/user-attachments/assets/9bc7e33d-faa7-4d47-b8db-5ff6d72f8f6d" />


# Attention Report

<img width="510" height="715" alt="image" src="https://github.com/user-attachments/assets/cff1c202-c4b0-45c7-ade1-1dd6fb3aba80" />
<img width="460" height="722" alt="image" src="https://github.com/user-attachments/assets/61f9e4a8-b84c-4ce4-8ad1-e6d4ddddd73d" />


#  Session log 

<img width="397" height="646" alt="image" src="https://github.com/user-attachments/assets/270602ac-7a2a-4e34-a742-b6afad94d2c6" />
<img width="452" height="650" alt="image" src="https://github.com/user-attachments/assets/b6f1f67d-807f-4f22-845d-81e59d42eb5b" />

---

## ⚠️ Limitations

* Sensitive to lighting conditions
* Accuracy depends on camera quality
* Cannot detect mental focus (only physical behavior)
* May fail with occlusions (mask, glasses, etc.)
* Works best for single-user tracking

---

## 🔮 Future Enhancements

* Emotion detection using deep learning
* Multi-student tracking system
* Cloud-based analytics dashboard
* Mobile/web-based integration
* Voice and audio interaction analysis

---

## 🎯 Conclusion

Virtual Veda provides a smart and automated solution for monitoring student engagement in virtual classrooms. By combining multiple computer vision techniques, it enhances accountability, improves learning outcomes, and supports educators with real-time insights.

---

## 👩‍💻 Author

**Thanuja S,K Neha Sree,M Upendranath Reddy**
**@G.Pulla Reddy Engineering College**

---

## ⭐ Support

If you like this project:

* Star ⭐ the repository
* Share with others
* Contribute for improvements

---









