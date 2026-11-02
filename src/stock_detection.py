"""Run Roboflow stock-shelf inference on one image.

Required .env values:
  ROBOFLOW_API_KEY
  STOCK_MODEL_ID
"""

from __future__ import annotations

import argparse
import os
from collections import Counter
from pathlib import Path

import cv2
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient


def get_client() -> tuple[InferenceHTTPClient, str]:
    load_dotenv()
    api_key = os.getenv("ROBOFLOW_API_KEY")
    model_id = os.getenv("STOCK_MODEL_ID")
    api_url = os.getenv("ROBOFLOW_API_URL", "https://serverless.roboflow.com")

    if not api_key or not model_id:
        raise RuntimeError(
            "Set ROBOFLOW_API_KEY and STOCK_MODEL_ID in your .env file."
        )

    return InferenceHTTPClient(api_url=api_url, api_key=api_key), model_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect filled/empty shelf areas.")
    parser.add_argument("--image", required=True, help="Path to the input image.")
    parser.add_argument(
        "--output",
        default="outputs/stock_detection.jpg",
        help="Path for the annotated output image.",
    )
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.is_file():
        parser.error(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        parser.error(f"OpenCV could not read image: {image_path}")

    try:
        client, model_id = get_client()
        result = client.infer(str(image_path), model_id=model_id)
    except Exception as exc:
        raise SystemExit(f"Roboflow inference failed: {exc}") from exc

    counts: Counter[str] = Counter()
    for prediction in result.get("predictions", []):
        label = str(prediction.get("class", "unknown"))
        counts[label] += 1

        # Roboflow object-detection coordinates are center x/y plus width/height.
        x = float(prediction.get("x", 0))
        y = float(prediction.get("y", 0))
        width = float(prediction.get("width", 0))
        height = float(prediction.get("height", 0))
        x1 = max(0, int(x - width / 2))
        y1 = max(0, int(y - height / 2))
        x2 = min(image.shape[1] - 1, int(x + width / 2))
        y2 = min(image.shape[0] - 1, int(y + height / 2))

        color = (0, 200, 0) if label.lower() == "filled" else (0, 0, 220)
        confidence = float(prediction.get("confidence", 0))
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            image,
            f"{label} ({confidence:.2f})",
            (x1, max(18, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2,
        )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), image):
        raise SystemExit(f"Could not write output image: {output_path}")

    print("Detection counts:")
    for label, count in sorted(counts.items()):
        print(f"  {label}: {count}")
    print(f"Annotated image saved to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
