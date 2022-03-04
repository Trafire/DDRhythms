#!/usr/bin/env python

import cv2 as cv


# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "--input", help="Path to image or video. Skip to capture frames from camera"
# )
# parser.add_argument(
#     "--thr", default=0.2, type=float, help="Threshold value for pose parts heat map"
# )
# parser.add_argument(
#     "--width", default=368, type=int, help="Resize input to specific width."
# )
# parser.add_argument(
#     "--height", default=368, type=int, help="Resize input to specific height."
# )
# # parser.add_argument('--scale', default=368, type=int, help='Resize input to specific height.')
#
# args = parser.parse_args()


class VideoInput:
    BODY_PARTS = {
        "Nose": 0,
        "Neck": 1,
        "RShoulder": 2,
        "RElbow": 3,
        "RWrist": 4,
        "LShoulder": 5,
        "LElbow": 6,
        "LWrist": 7,
        "RHip": 8,
        "RKnee": 9,
        "RAnkle": 10,
        "LHip": 11,
        "LKnee": 12,
        "LAnkle": 13,
        "REye": 14,
        "LEye": 15,
        "REar": 16,
        "LEar": 17,
        "Background": 18,
    }

    POSE_PAIRS = [
        ["Neck", "RShoulder"],
        ["Neck", "LShoulder"],
        ["RShoulder", "RElbow"],
        ["RElbow", "RWrist"],
        ["LShoulder", "LElbow"],
        ["LElbow", "LWrist"],
        ["Neck", "RHip"],
        ["RHip", "RKnee"],
        ["RKnee", "RAnkle"],
        ["Neck", "LHip"],
        ["LHip", "LKnee"],
        ["LKnee", "LAnkle"],
        ["Neck", "Nose"],
        ["Nose", "REye"],
        ["REye", "REar"],
        ["Nose", "LEye"],
        ["LEye", "LEar"],
    ]

    def __init__(self, input=0, width=200, height=200, scale=200, thr=0.2):
        self.thr = thr
        self.input = input
        self.in_width = width
        self.in_height = height
        self.scale = scale
        self.net = cv.dnn.readNetFromTensorflow("src/movement/graph_opt.pb")
        self.cap = cv.VideoCapture(self.input)
        self.calc_timestamps = [0.0]

    def get_height(self, points):
        pass

    def get(self):
        while cv.waitKey(1) < 0:
            hasFrame, frame = self.cap.read()
            if not hasFrame:
                cv.waitKey()
                break

            frameWidth = frame.shape[1]
            frameHeight = frame.shape[0]

            self.net.setInput(
                cv.dnn.blobFromImage(
                    frame,
                    1.0,
                    (self.in_width, self.in_height),
                    (127.5, 127.5, 127.5),
                    swapRB=True,
                    crop=False,
                )
            )
            out = self.net.forward()
            out = out[
                :, :19, :, :
            ]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

            assert len(VideoInput.BODY_PARTS) == out.shape[1]

            points = []
            for i in range(len(VideoInput.BODY_PARTS)):
                # Slice heatmap of corresponging body's part.
                heatMap = out[0, i, :, :]

                # Originally, we try to find all the local maximums. To simplify a sample
                # we just find a global one. However only a single pose at the same time
                # could be detected this way.
                _, conf, _, point = cv.minMaxLoc(heatMap)
                x = (frameWidth * point[0]) / out.shape[3]
                y = (frameHeight * point[1]) / out.shape[2]
                # Add a point if it's confidence is higher than threshold.
                points.append((int(x), int(y)) if conf > self.thr else None)

            print(points)
            height = self.get_height(points)

            for pair in VideoInput.POSE_PAIRS:
                partFrom = pair[0]
                partTo = pair[1]
                assert partFrom in VideoInput.BODY_PARTS
                assert partTo in VideoInput.BODY_PARTS

                idFrom = VideoInput.BODY_PARTS[partFrom]
                idTo = VideoInput.BODY_PARTS[partTo]

                if points[idFrom] and points[idTo]:
                    cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                    cv.ellipse(
                        frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED
                    )
                    cv.ellipse(
                        frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED
                    )

            t, _ = self.net.getPerfProfile()
            freq = cv.getTickFrequency() / 1000
            cv.putText(
                frame,
                "%.2fms" % (t / freq),
                (10, 20),
                cv.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
            )

            self.calc_timestamps.append(int(self.cap.get(cv.CAP_PROP_POS_MSEC)))
            print(points)
            print(self.calc_timestamps[-1])
            cv.imshow("OpenPose using OpenCV", frame)


v = VideoInput("data/test_video.mp4")
v.get()

#
#
#
#
# # inScale = args.scale
#
# net = cv.dnn.readNetFromTensorflow(r"C:\Users\Antoine\PycharmProjects\DDRhythms\src\movement\graph_opt.pb")
#
# # args.input = 0
#
# cap = cv.VideoCapture(args.input if args.input else 0)
#
# if cap.isOpened() == False:
#     print("Error opening video stream or file")
#
# while cv.waitKey(1) < 0:
#     hasFrame, frame = cap.read()
#     if not hasFrame:
#         cv.waitKey()
#         break
#
#     frameWidth = frame.shape[1]
#     frameHeight = frame.shape[0]
#
#     net.setInput(
#         cv.dnn.blobFromImage(
#             frame,
#             1.0,
#             (in_weight, in_height),
#             (127.5, 127.5, 127.5),
#             swapRB=True,
#             crop=False,
#         )
#     )
#     out = net.forward()
#     out = out[
#           :, :19, :, :
#           ]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements
#
#     assert len(BODY_PARTS) == out.shape[1]
#
#     points = []
#     for i in range(len(BODY_PARTS)):
#         # Slice heatmap of corresponging body's part.
#         heatMap = out[0, i, :, :]
#
#         # Originally, we try to find all the local maximums. To simplify a sample
#         # we just find a global one. However only a single pose at the same time
#         # could be detected this way.
#         _, conf, _, point = cv.minMaxLoc(heatMap)
#         x = (frameWidth * point[0]) / out.shape[3]
#         y = (frameHeight * point[1]) / out.shape[2]
#         # Add a point if it's confidence is higher than threshold.
#         points.append((int(x), int(y)) if conf > args.thr else None)
#
#     for pair in POSE_PAIRS:
#         partFrom = pair[0]
#         partTo = pair[1]
#         assert partFrom in BODY_PARTS
#         assert partTo in BODY_PARTS
#
#         idFrom = BODY_PARTS[partFrom]
#         idTo = BODY_PARTS[partTo]
#
#         if points[idFrom] and points[idTo]:
#             cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
#             cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
#             cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
#
#     t, _ = net.getPerfProfile()
#     freq = cv.getTickFrequency() / 1000
#     cv.putText(
#         frame, "%.2fms" % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0)
#     )
#
#     cv.imshow("OpenPose using OpenCV", frame)
