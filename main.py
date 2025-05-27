import cv2 as cv
import numpy as np
import os
from object_detection import detectObject, displayImage
from text_to_speech import speak, delete_directory

playcount = 0
class_labels = []
cnn_model = None
cnn_layer_names = []

def load_libraries():
    global class_labels, cnn_model, cnn_layer_names
    class_labels = open('model/yolov3-labels.txt').read().strip().split('\n')
    cnn_model = cv.dnn.readNetFromDarknet('model/yolov3.cfg', 'model/yolov3.weights')
    layer_names = cnn_model.getLayerNames()
    cnn_layer_names = [layer_names[i[0] - 1] for i in cnn_model.getUnconnectedOutLayers()]

def detect_from_video():
    global playcount
    label_colors = np.random.randint(0, 255, size=(len(class_labels), 3), dtype='uint8')
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Unable to load video")

    frame_height, frame_width = None, None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_width is None or frame_height is None:
            frame_height, frame_width = frame.shape[:2]

        frame, cls, _, _, _, _ = detectObject(
            cnn_model, cnn_layer_names, frame_height, frame_width, frame, label_colors, class_labels
        )

        if cls:
            data = ", ".join(set(cls))  # unique detected classes
            speak("Detected Objects: " + data, playcount)
            playcount += 1

        cv.imshow("Detected Objects", frame)
        if cv.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    os.makedirs('play', exist_ok=True)
    load_libraries()
    delete_directory()
    detect_from_video()
