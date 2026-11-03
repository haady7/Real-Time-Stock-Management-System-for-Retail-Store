import numpy as np

from retail_vision.vision import annotate_predictions, count_classes, prediction_box


def test_prediction_box_converts_center_coordinates():
    prediction = {"x": 50, "y": 40, "width": 20, "height": 10}
    assert prediction_box(prediction, (100, 100, 3)) == (40, 35, 60, 45)


def test_prediction_box_clips_to_image_bounds():
    prediction = {"x": 5, "y": 5, "width": 20, "height": 20}
    assert prediction_box(prediction, (50, 50, 3)) == (0, 0, 15, 15)


def test_prediction_box_rejects_invalid_coordinates():
    assert prediction_box({"x": "invalid"}, (50, 50, 3)) is None


def test_count_classes_handles_missing_label():
    predictions = [{"class": "Filled"}, {"class": "Empty"}, {}]
    assert count_classes(predictions) == {
        "Empty": 1,
        "Filled": 1,
        "unknown": 1,
    }


def test_annotate_predictions_returns_new_image():
    image = np.zeros((80, 100, 3), dtype=np.uint8)
    prediction = {
        "class": "Filled",
        "confidence": 0.92,
        "x": 50,
        "y": 40,
        "width": 20,
        "height": 10,
    }
    result = annotate_predictions(image, [prediction])
    assert result.shape == image.shape
    assert not np.array_equal(result, image)
