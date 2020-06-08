import streamlit as st
import time
import cv2
import datetime
import imutils
import time
import cv2
from phue import Bridge

# https://discovery.meethue.com/
b = Bridge("192.168.1.7")

st.title("Light controller")

st.header("Individual Control")

if st.checkbox("Manual control"):

    if st.checkbox("Sofa Living Room"):
        bri1 = st.slider("Birghtness", 0, 255, 255)
        b.set_light(1, "on", True)
        b.set_light(1, "bri", bri1)
    else:
        b.set_light(1, "on", False)

    if st.checkbox("Center Living Room"):
        bri2 = st.slider("Birghtness", 0, 255, 255)
        b.set_light(2, "on", True)
        b.set_light(2, "bri", bri2)
    else:
        b.set_light(2, "on", False)

    if st.checkbox("TV Living Room"):
        bri3 = st.slider("Birghtness", 0, 255, 255)
        b.set_light(3, "on", True)
        b.set_light(3, "bri", bri3)
    else:
        b.set_light(3, "on", False)

    st.header("Ambiance")

    if st.checkbox("TV Mode"):
        b.set_light(1, "on", False)
        b.set_light(2, "on", False)
        b.set_light(3, "on", False)

    if st.checkbox("Full light"):
        bri = 255
        b.set_light(1, "on", True)
        b.set_light(2, "on", True)
        b.set_light(3, "on", True)
        b.set_light(1, "bri", bri)
        b.set_light(2, "bri", bri)
        b.set_light(3, "bri", bri)

    if st.checkbox("Subdued"):
        bri = st.slider("Birghtness", 0, 255, 255)
        b.set_light(1, "on", True)
        b.set_light(2, "on", True)
        b.set_light(3, "on", True)
        b.set_light(1, "bri", bri)
        b.set_light(2, "bri", bri)
        b.set_light(3, "bri", bri)

elif st.checkbox("Control from video"):

    vs = cv2.VideoCapture(0)
    vs.set(cv2.CAP_PROP_FPS, 25)

    image_placeholder = st.empty()

    k = 0
    while True:
        success, frame = vs.read()
        text = "Unoccupied"

        if not success:
            break

        frame = imutils.resize(frame, width=900)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # firstFrame = gray
        if k == 0:
            firstFrame = gray

        k += 1
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < 1000:
                    continue
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"

            cv2.putText(
                frame,
                "Room Status: {}".format(text),
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                frame,
                datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (0, 0, 255),
                1,
            )

            bri = 255
            b.set_light(1, "on", True)
            b.set_light(2, "on", True)
            b.set_light(3, "on", True)
            b.set_light(1, "bri", bri)
            b.set_light(2, "bri", bri)
            b.set_light(3, "bri", bri)

        image_placeholder.image(frame, channels="BGR")
        time.sleep(3)
