"""Roboflow image and video inference runners."""

from __future__ import annotations

import csv
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import cv2
from inference_sdk import InferenceHTTPClient

from retail_vision.config import Settings
from retail_vision.vision import annotate_predictions, count_classes


def build_client(settings: Settings) -> InferenceHTTPClient:
    return InferenceHTTPClient(
        api_url=settings.api_url,
        api_key=settings.api_key,
    )


def infer_image(client: InferenceHTTPClient, image_path: Path, model_id: str):
    result = client.infer(str(image_path), model_id=model_id)
    predictions = result.get("predictions", [])
    if not isinstance(predictions, list):
        raise RuntimeError("Unexpected inference response: predictions is not a list")
    return predictions


def run_stock_image(
    image_path: Path,
    output_path: Path,
    settings: Settings,
) -> dict[str, int]:
    """Run stock-model inference on one image and save annotated output."""
    if not image_path.is_file():
        raise FileNotFoundError(f"Input image does not exist: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"OpenCV could not read image: {image_path}")

    client = build_client(settings)
    predictions = infer_image(client, image_path, settings.stock_model_id)
    annotated = annotate_predictions(image, predictions)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), annotated):
        raise OSError(f"Could not write annotated image: {output_path}")

    return count_classes(predictions)


def parse_video_source(source: str) -> int | str:
    """Treat numeric source strings as camera indices."""
    return int(source) if source.isdigit() else source


def run_video(
    source: str,
    output_path: Path,
    log_path: Path,
    settings: Settings,
    preview: bool = False,
) -> int:
    """Run activity inference on a video/webcam, saving MP4 and CSV output."""
    capture = cv2.VideoCapture(parse_video_source(source))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")

    fps = capture.get(cv2.CAP_PROP_FPS)
    fps = fps if fps and fps > 0 else 24.0
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        capture.release()
        raise RuntimeError("Video source did not provide valid frame dimensions")

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
        raise OSError(f"Could not create output video: {output_path}")

    client = build_client(settings)
    frame_number = 0
    try:
        with log_path.open("w", newline="", encoding="utf-8") as log_file:
            fields = [
                "frame", "timestamp_utc", "class", "confidence",
                "x", "y", "width", "height",
            ]
            log_writer = csv.DictWriter(log_file, fieldnames=fields)
            log_writer.writeheader()

            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                frame_number += 1

                # Close the temporary file before inference for Windows support.
                fd, temp_name = tempfile.mkstemp(suffix=".jpg")
                os.close(fd)
                temp_path = Path(temp_name)
                try:
                    if not cv2.imwrite(str(temp_path), frame):
                        raise OSError("Could not encode a video frame")
                    predictions = infer_image(
                        client, temp_path, settings.theft_model_id
                    )
                finally:
                    temp_path.unlink(missing_ok=True)

                annotated = annotate_predictions(frame, predictions)
                timestamp = datetime.now(timezone.utc).isoformat()
                for prediction in predictions:
                    log_writer.writerow(
                        {
                            "frame": frame_number,
                            "timestamp_utc": timestamp,
                            "class": prediction.get("class", "unknown"),
                            "confidence": prediction.get("confidence", ""),
                            "x": prediction.get("x", ""),
                            "y": prediction.get("y", ""),
                            "width": prediction.get("width", ""),
                            "height": prediction.get("height", ""),
                        }
                    )
                    if str(prediction.get("class", "")).casefold() == "shoplifting":
                        print(
                            f"Review required: model predicted Shoplifting on "
                            f"frame {frame_number}. This is not proof of theft."
                        )

                writer.write(annotated)
                if preview:
                    cv2.imshow("Retail activity review - press q to stop", annotated)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
    finally:
        capture.release()
        writer.release()
        if preview:
            cv2.destroyAllWindows()

    return frame_number
