from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import time

app = Flask(__name__)

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

with open("coco.names", "r") as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture(0)   # change to 1 if external camera

RED_TIME = 5
YELLOW_TIME = 3
GREEN_TIME = 7

current_signal = "R"
signal_start_time = time.time()
car_count = 0
timer_value = 0

def generate_frames():
    global current_signal, signal_start_time, car_count, timer_value

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape

        blob = cv2.dnn.blobFromImage(frame, 1/255, (416,416), (0,0,0), True, crop=False)
        net.setInput(blob)
        output_layers = net.getUnconnectedOutLayersNames()
        detections = net.forward(output_layers)

        boxes = []
        confidences = []

        for output in detections:
            for detect in output:
                scores = detect[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if classes[class_id] == "car" and confidence > 0.5:
                    cx = int(detect[0] * width)
                    cy = int(detect[1] * height)
                    w = int(detect[2] * width)
                    h = int(detect[3] * height)

                    x = int(cx - w / 2)
                    y = int(cy - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        car_count = len(indexes)

        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        elapsed = int(time.time() - signal_start_time)

        if current_signal == "R" and elapsed >= RED_TIME:
            if car_count > 0:
                current_signal = "Y"
                signal_start_time = time.time()

        elif current_signal == "Y" and elapsed >= YELLOW_TIME:
            if car_count >= 4:
                current_signal = "G"
            else:
                current_signal = "R"
            signal_start_time = time.time()

        elif current_signal == "G" and elapsed >= GREEN_TIME:
            current_signal = "R"
            signal_start_time = time.time()

        if current_signal == "R":
            timer_value = max(0, RED_TIME - elapsed)
            color = (0,0,255)
        elif current_signal == "Y":
            timer_value = max(0, YELLOW_TIME - elapsed)
            color = (0,255,255)
        else:
            timer_value = max(0, GREEN_TIME - elapsed)
            color = (0,255,0)

        cv2.putText(frame, f"Signal: {current_signal}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    return jsonify({
        "cars": car_count,
        "signal": current_signal,
        "timer": timer_value
    })

if __name__ == "__main__":
    # ⭐ THIS IS THE IMPORTANT CHANGE ⭐
    app.run(host="0.0.0.0", port=5000, debug=True)
