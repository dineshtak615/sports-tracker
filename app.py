
import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("/content/input_video.mp4")

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter("/content/output_tracked.mp4",
      cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

frame_num  = 0
unique_ids = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_num += 1

    results = model.track(frame, persist=True,
                          tracker="bytetrack.yaml",
                          conf=0.4, classes=[0],
                          verbose=False)[0]

    annotated = frame.copy()
    if results.boxes.id is not None:
        for box, tid in zip(results.boxes, results.boxes.id):
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            pid = int(tid)
            unique_ids.add(pid)
            cv2.rectangle(annotated, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(annotated, f"ID {pid}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.putText(annotated, f"Players: {len(results.boxes)}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    out.write(annotated)

    if frame_num % 100 == 0:
        print(f"Processed {frame_num} frames...")

cap.release()
out.release()
print(f"\n✅ Done!")
print(f"Total frames  : {frame_num}")
print(f"Unique players: {len(unique_ids)}")
print(f"Saved to /content/output_tracked.mp4")
