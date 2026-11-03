"""Testable computer-vision helpers for prediction visualization."""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

import cv2


def prediction_box(
    prediction: dict[str, Any], image_shape: tuple[int, ...]
) -> tuple[int, int, int, int] | None:
    """Convert center-based prediction coordinates to clipped pixel corners."""
    if len(image_shape) < 2:
        raise ValueError("image_shape must contain image height and width")

    try:
        center_x = float(prediction["x"])
        center_y = float(prediction["y"])
        box_width = float(prediction["width"])
        box_height = float(prediction["height"])
    except (KeyError, TypeError, ValueError):
        return None

    if box_width <= 0 or box_height <= 0:
        return None

    image_height, image_width = image_shape[:2]
    if image_height <= 0 or image_width <= 0:
        return None

    x1 = max(0, min(image_width - 1, int(round(center_x - box_width / 2))))
    y1 = max(0, min(image_height - 1, int(round(center_y - box_height / 2))))
    x2 = max(0, min(image_width - 1, int(round(center_x + box_width / 2))))
    y2 = max(0, min(image_height - 1, int(round(center_y + box_height / 2))))

    if x2 <= x1 or y2 <= y1:
        return None
    return x1, y1, x2, y2


def annotate_predictions(image, predictions: Iterable[dict[str, Any]]):
    """Return a copy of image with bounding boxes and class labels."""
    if image is None:
        raise ValueError("image cannot be None")

    annotated = image.copy()
    for prediction in predictions:
        box = prediction_box(prediction, annotated.shape)
        if box is None:
            continue

        label = str(prediction.get("class", "unknown"))
        try:
            confidence = float(prediction.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0

        normalized_label = label.casefold()
        if normalized_label == "filled":
            color = (0, 170, 0)
        elif normalized_label == "empty":
            color = (0, 0, 220)
        else:
            color = (0, 165, 255)

        x1, y1, x2, y2 = box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            annotated,
            f"{label} ({confidence:.2f})",
            (x1, max(18, y1 - 7)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2,
            cv2.LINE_AA,
        )
    return annotated


def count_classes(predictions: Iterable[dict[str, Any]]) -> dict[str, int]:
    """Count class labels while preserving their original spelling."""
    counts: Counter[str] = Counter(
        str(item.get("class", "unknown")) for item in predictions
    )
    return dict(sorted(counts.items()))
