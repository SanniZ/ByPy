#!/usr/bin/env python

import sys
import cv2

class FaceRecognization(object):
    def __init__(self, vc_id=0):
        self._vc = cv2.VideoCapture(vc_id)
        if not self._vc:
            print("Error, it is failed to get Video device!")
            sys.exit(-1)

    def get_face_frame(self):
        return self._vc.read()

    def __exit__(self):
        if self._vc:
            self._vc.release()
            self._vc = None
        print("exit!")

    def run(self):
        while True:
            # get face.
            rc, frame = self.get_face_frame()
            if not rc:
                print("Error, it is failed to get face data!")
                break
            print("rc = {}".format(rc))


if __name__ == '__main__':
    fr = FaceRecognization()
    fr.run()
