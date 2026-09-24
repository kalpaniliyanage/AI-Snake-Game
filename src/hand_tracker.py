import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:

    def __init__(self):

        # ----------------------------------------------------
        # CAMERA
        # ----------------------------------------------------

        self.cap = cv2.VideoCapture(0)

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

        # ----------------------------------------------------
        # MEDIAPIPE MODEL
        # ----------------------------------------------------

        base_options = python.BaseOptions(
            model_asset_path="models/hand_landmarker.task"
        )

        options = vision.HandLandmarkerOptions(

            base_options=base_options,

            running_mode=vision.RunningMode.VIDEO,

            num_hands=1,

            min_hand_detection_confidence=0.6,

            min_hand_presence_confidence=0.6,

            min_tracking_confidence=0.6
        )

        self.detector = (
            vision.HandLandmarker.create_from_options(
                options
            )
        )

        self.timestamp = 0

        # ----------------------------------------------------
        # VIRTUAL JOYSTICK
        # ----------------------------------------------------

        self.center_x = 320
        self.center_y = 240

        # Dead zone
        self.dead_zone = 60

    # ========================================================
    # GET HAND DIRECTION
    # ========================================================

    def get_direction(self):

        ret, frame = self.cap.read()

        if not ret:

            return None, None

        # Mirror camera
        frame = cv2.flip(
            frame,
            1
        )

        height, width = frame.shape[:2]

        # ----------------------------------------------------
        # MEDIAPIPE IMAGE
        # ----------------------------------------------------

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        self.timestamp += 1

        result = self.detector.detect_for_video(
            mp_image,
            self.timestamp
        )

        direction = None

        # ----------------------------------------------------
        # DRAW VIRTUAL JOYSTICK
        # ----------------------------------------------------

        cv2.circle(
            frame,
            (
                self.center_x,
                self.center_y
            ),
            self.dead_zone,
            (100, 100, 100),
            2
        )

        cv2.circle(
            frame,
            (
                self.center_x,
                self.center_y
            ),
            7,
            (255, 0, 0),
            -1
        )

        # ----------------------------------------------------
        # HAND DETECTED
        # ----------------------------------------------------

        if result.hand_landmarks:

            hand = result.hand_landmarks[0]

            # ------------------------------------------------
            # DRAW LANDMARKS
            # ------------------------------------------------

            for landmark in hand:

                x = int(
                    landmark.x * width
                )

                y = int(
                    landmark.y * height
                )

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

            # ------------------------------------------------
            # HAND CONNECTIONS
            # ------------------------------------------------

            connections = [

                # Thumb
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 4),

                # Index finger
                (0, 5),
                (5, 6),
                (6, 7),
                (7, 8),

                # Middle finger
                (0, 9),
                (9, 10),
                (10, 11),
                (11, 12),

                # Ring finger
                (0, 13),
                (13, 14),
                (14, 15),
                (15, 16),

                # Pinky
                (0, 17),
                (17, 18),
                (18, 19),
                (19, 20),

                # Palm
                (5, 9),
                (9, 13),
                (13, 17)
            ]

            for start, end in connections:

                x1 = int(
                    hand[start].x * width
                )

                y1 = int(
                    hand[start].y * height
                )

                x2 = int(
                    hand[end].x * width
                )

                y2 = int(
                    hand[end].y * height
                )

                cv2.line(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (255, 255, 255),
                    2
                )

            # ------------------------------------------------
            # PALM CENTER
            # ------------------------------------------------

            # Use several palm landmarks
            palm_points = [
                hand[0],
                hand[5],
                hand[9],
                hand[13],
                hand[17]
            ]

            palm_x = int(
                sum(
                    point.x for point in palm_points
                )
                / len(palm_points)
                * width
            )

            palm_y = int(
                sum(
                    point.y for point in palm_points
                )
                / len(palm_points)
                * height
            )

            # ------------------------------------------------
            # DRAW PALM CENTER
            # ------------------------------------------------

            cv2.circle(
                frame,
                (
                    palm_x,
                    palm_y
                ),
                14,
                (0, 0, 255),
                -1
            )

            # ------------------------------------------------
            # LINE TO JOYSTICK CENTER
            # ------------------------------------------------

            cv2.line(
                frame,
                (
                    self.center_x,
                    self.center_y
                ),
                (
                    palm_x,
                    palm_y
                ),
                (255, 0, 255),
                3
            )

            # ------------------------------------------------
            # CALCULATE DISTANCE
            # ------------------------------------------------

            dx = palm_x - self.center_x

            dy = palm_y - self.center_y

            # ------------------------------------------------
            # VIRTUAL JOYSTICK LOGIC
            # ------------------------------------------------

            if (
                abs(dx) <= self.dead_zone
                and
                abs(dy) <= self.dead_zone
            ):

                # Hand is inside dead zone
                direction = None

            else:

                # Horizontal movement is stronger
                if abs(dx) > abs(dy):

                    if dx > self.dead_zone:

                        direction = "RIGHT"

                    elif dx < -self.dead_zone:

                        direction = "LEFT"

                # Vertical movement
                else:

                    if dy > self.dead_zone:

                        direction = "DOWN"

                    elif dy < -self.dead_zone:

                        direction = "UP"

            # ------------------------------------------------
            # DISPLAY PALM POSITION
            # ------------------------------------------------

            cv2.putText(
                frame,
                f"Palm: ({palm_x}, {palm_y})",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        else:

            cv2.putText(
                frame,
                "NO HAND DETECTED",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # ----------------------------------------------------
        # CAMERA TITLE
        # ----------------------------------------------------

        cv2.putText(
            frame,
            "VIRTUAL JOYSTICK",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

        # ----------------------------------------------------
        # CURRENT DIRECTION
        # ----------------------------------------------------

        if direction:

            cv2.putText(
                frame,
                f"DIRECTION: {direction}",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

        return direction, frame

    # ========================================================
    # RELEASE
    # ========================================================

    def release(self):

        self.cap.release()

        self.detector.close()

        cv2.destroyAllWindows()
        