# Academic project report summary

**Source:** *Advanced Image Recognition for Retail Stock Management*, B.E. Computer Science and Engineering (Artificial Intelligence & Machine Learning), 2024–25, M. H. Saboo Siddik College of Engineering, University of Mumbai.

The submitted report lists three student contributors and describes a retail computer-vision system based on Roboflow and YOLOv8. This summary preserves the report's claims while distinguishing them from the cleaned implementation currently included in this repository.

## Abstract and motivation

The report proposes using image recognition to automate retail inventory monitoring, reduce manual shelf checks, identify empty shelf areas, support planogram compliance, and flag suspicious retail activity. It describes using webcam or recorded video, real-time frame processing, event logging, and annotated video export.

## Problem statement and objectives

Traditional inventory checks are described as labor-intensive and prone to human error. The report identifies stockouts, overstocking, difficulty verifying shelf layouts, and loss prevention as target problems.

The stated objectives are to:

- Improve accuracy and efficiency in stock tracking.
- Monitor shelf levels and help prevent stockouts/overstocking.
- Support planogram compliance.
- Improve loss prevention by flagging misplaced or missing items.

## System design described in the report

The proposed architecture contains two YOLOv8 models hosted using Roboflow:

1. A stock-management model intended to classify shelf regions as Filled or Empty.
2. A theft/activity model intended to detect visual classes and activity cues such as Shoplifting, Product-Picked, and Customer-Bagpack.

OpenCV is described as the video-frame processing component. The report also discusses posture estimation, audible alarms, SMS/email alerts, video export, ERP/inventory integration, edge deployment on NVIDIA Jetson Nano, and an active-learning feedback loop. Those additional integrations are not all implemented in the cleaned code currently in this repository.

## Dataset and training details stated in the report

- 10,000+ retail shelf images for the stock-management task.
- 5,000+ annotated video clips for the theft/activity task.
- Shelf labels include Filled and Empty.
- Activity labels mentioned include Shoplifting, Product-Picked, and Customer-Bagpack.
- Training/validation/testing split: 70% / 20% / 10%.
- Input resizing: 640 × 640 pixels.
- Augmentation examples: rotations and brightness adjustments.
- Reported training settings include batch size 16 and learning rate 0.001.
- The report describes transfer learning from pretrained COCO weights.

The source datasets and model weights were not supplied with this public repository.

## Results stated in the report

| Metric | Value stated in report |
|---|---:|
| Stock model precision | 92% |
| Theft model accuracy | 85% |
| Theft model F1-score | 0.83 |
| Planogram adherence | 95% |
| Edge processing speed | 30+ FPS |
| Detection-to-alert latency | Below 500 ms |
| Stockout reduction in a described four-week pilot | 35% |
| Theft-incident reduction in a described four-week pilot | 50% |

These numbers are **claims recorded in the academic report**. The corresponding source datasets, evaluation scripts, and independent reproduction are not included here. They must not be described as independently validated by the scripts in this repository.

## Software currently included in this repository

The maintained Python package provides configurable Roboflow inference for:
- One shelf image using the stock model.
- A video file or webcam using the activity model.

It annotates predictions with bounding boxes, exports the processed video, and records video predictions to CSV. Tests cover basic bounding-box conversion, class counting, and annotation.

## Limitations and responsible use

- The original datasets and trained Roboflow models are not included.
- Model IDs and a valid API key must be supplied by the user.
- SMS/email notifications, ERP integration, production dashboards, and posture estimation are described in the report but are not implemented by this repository's current scripts.
- An automated Shoplifting label is a model prediction only. It is not proof that a person committed theft and requires appropriate human review.
- CCTV use must be authorized, transparent, proportionate, and subject to access and retention safeguards.
- The report appendix contained hard-coded Roboflow API credentials. Those values are intentionally omitted from this public repository. Any exposed keys should be revoked and rotated in Roboflow.

## Report organization

The report includes an introduction and motivation, literature survey, problem statement/objectives, proposed architecture, framework and algorithm, experimental setup, results and discussion, conclusion/future scope, references, progress reports, and an appendix containing code and project material.
