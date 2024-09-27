import cv2
import numpy as np

class LaneDetector:
    def __init__(self, config):
        self.canny_threshold1 = config['canny_threshold1']
        self.canny_threshold2 = config['canny_threshold2']
        self.roi_vertices = config['roi_vertices']
    
    def detect_lanes(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, self.canny_threshold1, self.canny_threshold2)
        mask = np.zeros_like(edges)
        vertices = np.array(self.roi_vertices, dtype=np.int32)
        cv2.fillPoly(mask, vertices, 255)
        masked_edges = cv2.bitwise_and(edges, mask)
        lines = cv2.HoughLinesP(masked_edges, 1, np.pi/180, 50, minLineLength=100, maxLineGap=50)
        return lines
