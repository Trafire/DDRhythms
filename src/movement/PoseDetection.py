#!/usr/bin/env python

import math
from collections import deque

import cv2 as cv


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
        self.points_list = deque([], maxlen=1000)
        self._person_height = None

    def distance(self, part_one: str, part_two: str, offset=1) -> int:
        a = self.get_body_part_location(part_one, offset)
        b = self.get_body_part_location(part_two, offset)
        if a and b:
            return math.dist(a, b)
        return None

    def get_points(self, offset):
        print(len(self.points_list))
        if len(self.points_list) > abs(offset):
            return self.points_list[offset]
        else:
            return [(0, 0)] * 19

    def get_body_part_location(self, part: str, offset=-1) -> None:
        """Returns value of location of body part
        Parameters
        ----------

        part: String in
        offset: index of points to use. [-1] is latest

        Returns float
        -------
        """

        index = VideoInput.BODY_PARTS.get(part, None)
        # error if body part is not in Body Part List
        assert index is not None
        return self.get_points(offset)[index]

    def get_height(self):
        if self._person_height is None:
            #     # LAnkle = self.get_body_part_location("LAnkle")
            #     # LShoulder = self.get_body_part_location("LShoulder")
            height = self.distance("LAnkle", "LShoulder")
            if height > 0:
                self._person_height = height
        return self._person_height

    def shoulder_width(self):

        return self.distance("LShoulder", "rShoulder")

    def leg_length(self, offset):
        pass

    def left_foot_position(self, offset=-1):

        pass

    def right_foot_position(self, offset):
        pass

    def change_right_in_foot_position(self, offset):
        pass

    def change_left_in_foot_position(self, offset):
        pass

    def left_knee(self, offset):
        pass

    def right_knee(self, offset):
        pass

    def hip_angle(self, offset):
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
            self.points_list.append(points)

            height = self.get_height()
            shoulder_width = self.shoulder_width()
            if height != None:
                print(shoulder_width)

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

            cv.imshow("OpenPose using OpenCV", frame)


v = VideoInput(r"data\test_video.mp4")
v.get()
