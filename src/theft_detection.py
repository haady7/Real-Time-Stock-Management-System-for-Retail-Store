"""Run Roboflow inference over a webcam or video file.

Required .env values:
  ROBOFLOW_API_KEY
  THEFT_MODEL_ID

Predictions are review flags only and must not be treated as proof of wrongdoing.
"""

from __future__ import annotations

import argparse
import csv
import os
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient


def parse_source(value: str) -> int | str:
    return int(value) if value.isdigit() else value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag configured retail activity classes in a video."
    )
    parser.add_argument(
        "--source",
        default="0",
        help="Webcam index (0) or path to a video file.",
    )
    parser.add_argument(
        "--output",
        default="outputs/theft_detection.mp4",
        help="Path for the annotated video.",
    )
    parser.add_argument(
        "--log",
        default="outputs/theft_events.csv",
        help="CSV path for frame-level detections.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Display the annotated video while processing.",
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("ROBOFLOW_API_KEY")
    model_id = os.getenv("THEFT_MODEL_ID")
    api_url = os.getenv("ROBOFLOW_API_URL", "https://serverless.roboflow.com")
    if not api_key or not model_id:
        parser.error("Set ROBOFLOW_API_KEY and THEFT_MODEL_ID in your .env file.")

    client = InferenceHTTPClient(api_url=api_url, api_key=api_key)
    capture = cv2.VideoCapture(parse_source(args.source))
    if not capture.isOpened():
        parser.error(f"Could not open video source: {args.source}")

    fps = capture.get(cv2.CAP_PROP_FPS)
    fps = fps if fps and fps > 0 else 24.0
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        capture.release()
        parser.error("The video source did not provide valid frame dimensions.")

    output_path = Path(args.output)
    log_path = Path(args.log)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    if not writer.isOpened():
        capture.release()
        parser.error(f"Could not create output video: {output_path}")

    frame_number = 0
    try:
        with log_path.open("w", newline="", encoding="utf-8") as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(
                ["frame", "timestamp_utc", "class", "confidence"]
            )

            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                frame_number += 1

                # The inference SDK accepts an image path. Close the temporary
                # file before inference so this also works on Windows.
                fd, temp_path = tempfile.mkstemp(suffix=".jpg")
                os.close(fd)
                try:
                    if not cv2.imwrite(temp_path, frame):
                        raise RuntimeError("Could not encode a video frame.")
                    result = client.infer(temp_path, model_id=model_id)
                finally:
                    Path(temp_path).unlink(missing_ok=True)

                timestamp = datetime.now(timezone.utc).isoformat()
                for prediction in result.get("predictions", []):
                    label = str(prediction.get("class", "unknown"))
                    confidence = float(prediction.get("confidence", 0))
                    x = float(prediction.get("x", 0))
                    y = float(prediction.get("y", 0))
                    box_width = float(prediction.get("width", 0))
                    box_height = float(prediction.get("height", 0))
                    x1 = max(0, int(x - box_width / 2))
                    y1 = max(0, int(y - box_height / 2))
                    x2 = min(width - 1, int(x + box_width / 2))
                    y2 = min(height - 1, int(y + box_height / 2))

                    color = (0, 0, 220) if label.lower() == "shoplifting" else (0, 200, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        frame,
                        f"{label} ({confidence:.2f})",
                        (x1, max(18, y1 - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color,
                        2,
                    )
                    log_writer.writerow([frame_number, timestamp, label, confidence])

                    if label.lower() == "shoplifting":
                        print(
                            f"Review alert on frame {frame_number}: "
                            "model predicted Shoplifting; verify manually."
                        )

                writer.write(frame)
                if args.preview:
                    cv2.imshow("Retail activity review", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
    finally:
        capture.release()
        writer.release()
        if args.preview:
            cv2.destroyAllWindows()

    print(f"Annotated video saved to: {output_path}")
    print(f"Detection log saved to: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
