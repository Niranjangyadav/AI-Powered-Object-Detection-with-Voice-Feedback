import cv2 as cv
import numpy as np

def detectObject(model, layer_names, h, w, image, colors, labels):
    blob = cv.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    model.setInput(blob)
    outputs = model.forward(layer_names)

    boxes, confidences, class_ids = [], [], []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                box = detection[0:4] * np.array([w, h, w, h])
                center_x, center_y, width, height = box.astype("int")
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    idxs = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    classes = []

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in colors[class_ids[i]]]
            cv.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = f"{labels[class_ids[i]]}: {confidences[i]:.2f}"
            cv.putText(image, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            classes.append(labels[class_ids[i]])

    return image, classes, boxes, confidences, class_ids, idxs


def displayImage(img):
    cv.imshow("Detected Image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
