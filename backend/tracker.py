from time import perf_counter
from numba import jit, cuda
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import torch
import os
import os

class Detector:
    def __init__(self, model_name) -> None:
        self.model = YOLO(model_name)
        self.model.info(False)
        # self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # print("Using Device: ", self.device)

    def get_detections(self, frame):
        result = self.model(frame)[0]

        detections = []
        for r in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            if class_id == 0:
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
                score = int(score)
                detections.append([(x1, y1, abs(x2-x1), abs(y2-y1)), score, class_id])

        return detections

@jit(target_backend='cuda')
def mainTracker(video_name):
    print(video_name)
    cap = cv2.VideoCapture(video_name)
    scale_factor = 0.4
    # video_out_path = os.path.join('.', 'out.mp4')
    ret, frame = cap.read()
    # cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'MP4V'), cap.get(cv2.CAP_PROP_FPS),
    #                       (frame.shape[1], frame.shape[0]))
    model = Detector(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'models','boxes.pt'))
    tracker = DeepSort(max_age=5,
                    n_init=5,
                    nms_max_overlap=1.0,
                    max_cosine_distance=0.3,
                    nn_budget=None,
                    override_track_class=None,
                    embedder="mobilenet",
                    half=True,
                    bgr=True,
                    embedder_gpu=True,
                    embedder_model_name=True,
                    embedder_wts=None,
                    polygon=False,
                    today=None)

    boxes_dict = {}
    color = (0, 255, 0)
    count = 0
    print(ret)
    while count < 1500 and ret:
        h, w, _ = frame.shape
        frame = cv2.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)

        start = perf_counter()
        detections = model.get_detections(frame)

        tracks = tracker.update_tracks(detections, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            boxes_dict[track_id] = boxes_dict.get(track_id, 0) + 1

            ltrb = track.to_ltrb()

            x1, y1, x2, y2 = ltrb
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, "ID: " + str(track_id), (int(x1), int(y1-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)

        end = perf_counter()
        total_time = end - start
        fps = 1 / total_time
        cv2.putText(frame, "FPS: "+str(int(fps)), (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(frame, "Counter: "+str(int(len(boxes_dict))), (20, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
        # cap_out.write(frame)
        cv2.imshow("Video", frame)

        key = cv2.waitKey(30)

        if key == 27:
            break

        ret, frame = cap.read()
        count += 1

    cap.release()
    # cap_out.release()
    cv2.destroyAllWindows()
    return str(len(boxes_dict))


mainTracker("C:/Users/aweso/Desktop/Side Projects/SmarTrack/smarTrack/files/demo_video.mp4")