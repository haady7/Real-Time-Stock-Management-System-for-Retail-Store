# Project overview

## Source project

*Advanced Image Recognition for Retail Stock Management* (B.E. Computer Science and Engineering – Artificial Intelligence & Machine Learning, 2024–25), M. H. Saboo Siddik College of Engineering, University of Mumbai.

## Problem statement

The report identifies manual inventory checks as time-consuming and vulnerable to human error. It discusses stockouts, overstocking, difficulty checking shelf layout compliance, and the challenge of identifying theft or misplaced items without automated monitoring.

## Objectives

- Improve stock-monitoring accuracy and efficiency.
- Identify shelf sections that may be empty and need restocking.
- Support planogram checks.
- Flag retail activity classes for security staff review.
- Maintain detection logs and annotated visual output.

## Proposed system in the report

The report describes two YOLOv8 models hosted through Roboflow:

1. A stock model for Filled and Empty shelf classes.
2. A theft/activity model for classes and behaviors described in the report.

OpenCV is used to capture video frames and prepare them for inference. The report also discusses alerting, centralized inventory systems, ERP connectivity, posture estimation, edge deployment, and a feedback loop for model improvement.

## Implementation represented in this repository

The current code provides:
- Roboflow inference for an individual shelf image.
- Roboflow inference over webcam or video frames.
- Bounding-box drawing and confidence labels.
- CSV logging of video predictions.
- Environment-variable configuration and basic tests.

This implementation is a cleaned, configurable reference workflow. It is not a complete production retail platform and does not implement all features mentioned in the report.

## Dataset and model availability

No original dataset or model weights are distributed here. The user must configure model IDs from a Roboflow workspace to run inference.

## Metrics reported by the academic document

The report states 92% precision for stock classification, 85% accuracy for theft detection, 30+ FPS on the described edge setup, below 500 ms detection-to-alert latency, 95% planogram adherence, and pilot reductions of 35% in stockouts and 50% in theft incidents.

Those figures are reported by the academic document. The datasets, detailed evaluation protocol, and independent reproduction are not included with this repository; therefore these figures should not be presented as independently verified benchmarks.

## Important interpretation

Computer-vision detections can be wrong. A model output labelled Shoplifting is only an automated prediction and must be reviewed by an authorized human. It is not proof that an individual committed theft.
