from flask import Flask, render_template, Response
import cv2
import numpy as np
import mss

app = Flask(__name__)

# Route to render the viewer.html page
@app.route('/')
def index():
        return render_template('viewer.html')


# Video feed generator for screen capture
def generate_screen_feed():
    with mss.mss() as sct:
        # Define the monitor to capture (0 for the primary monitor)
        monitor = sct.monitors[1]  # Change index if needed
        while True:
            # Capture the screen
            img = sct.grab(monitor)
            # Convert the raw pixel data to an array
            frame = np.array(img)
            # Convert BGRA to BGR (OpenCV uses BGR format)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield the frame in the proper format for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_screen_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
