import cv2
from ultralytics import YOLO


class YOLOAI:
    def __init__(self):
        self.model = YOLO("yolo11n.pt")

        self.camera = cv2.VideoCapture(0)

        self.detected_objects = []

    def update(self):

        ret, frame = self.camera.read()

        if not ret:
            return []

        results = self.model(
            frame,
            verbose=False
        )

        objects = []

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])

                name = self.model.names[class_id]

                objects.append(name)

        self.detected_objects = list(set(objects))

        return self.detected_objects

    def release(self):

        self.camera.release()
        cv2.destroyAllWindows()