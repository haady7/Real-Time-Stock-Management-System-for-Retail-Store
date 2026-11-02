# Advanced Image Recognition for Retail Stock Management

## Overview

This project applies computer vision to two retail tasks:

1. **Shelf stock monitoring** — classify shelf sections as `Filled` or `Empty` so staff can identify areas that may need restocking.
2. **Retail security monitoring** — detect visual classes associated with customer/product activity (for example, `Product-Picked`, `Customer-Bagpack`, and `Shoplifting`) and flag events for staff review.

The academic report describes a workflow built around Roboflow-trained YOLOv8 models, OpenCV video processing, and a Google Colab/edge-device deployment approach.

## Objectives

- Reduce reliance on manual shelf checks.
- Monitor shelf availability and support restocking decisions.
- Check product placement against predefined shelf layouts (planograms).
- Flag potentially suspicious visual events for human review.
- Save detection details and annotated footage for later inspection.

## Architecture and workflow

1. **Capture:** read shelf or store-camera images/video.
2. **Preprocess:** extract frames with OpenCV, resize and normalize inputs for model inference.
3. **Stock inference:** classify shelf regions as `Filled` or `Empty`.
4. **Security inference:** identify configured product/customer activity classes.
5. **Output:** draw bounding boxes, count detections, and record event metadata.
6. **Review and iteration:** review false positives/false negatives and add suitable examples to the training data.

The report also discusses alerting (audible alarms and SMS/email), inventory/ERP integration, edge deployment, and an active-learning feedback loop as parts of the proposed system.

## Technology stack

- Python
- YOLOv8
- Roboflow and Roboflow Inference
- OpenCV
- Google Colab
- NVIDIA Jetson Nano (described as an edge deployment target)
- OpenPose/posture estimation (described in the report for behavioral analysis)

## Dataset and training approach described in the report

- More than 10,000 shelf images for the stock-management task.
- More than 5,000 video clips for the theft-detection task.
- Shelf labels include `Filled` and `Empty`.
- Security labels include `Shoplifting`, `Product-Picked`, and `Customer-Bagpack`.
- A 70% / 20% / 10% training, validation, and test split.
- Image resizing to 640 × 640 and augmentation such as rotation, brightness changes, and blur.

These are details stated in the submitted academic report; the repository does not include the original datasets.

## Results stated in the academic report

| Measure | Figure stated in report |
|---|---:|
| Stock classification precision | 92% |
| Theft-detection accuracy | 85% |
| Edge processing speed | 30+ FPS |
| Detection-to-alert latency | Below 500 ms |
| Planogram adherence | 95% |
| Stockout reduction in the described pilot | 35% |
| Theft-incident reduction in the described pilot | 50% |

**Important:** These are figures reported in the academic document. They have not been independently reproduced or benchmarked by the cleaned scripts in this repository. Treat them as reported project results, not as a verified production guarantee.

## Code in this repository

The `src/` scripts are cleaned, configurable implementations of the image and video inference workflows described in the report. They require valid Roboflow model IDs and an API key supplied through environment variables. They are not a copy of a complete production deployment, and the optional SMS/email and ERP integrations described in the report are not implemented here.

See the root [README](../README.md) for setup and usage.

## Privacy, security, and responsible use

- Do not commit Roboflow API keys, tokens, passwords, private datasets, or private CCTV footage.
- Configure credentials locally using a `.env` file copied from `.env.example`.
- Keep camera use lawful and transparent, minimize retained footage, and apply appropriate access controls.
- A model prediction is only an alert for human review. It is **not proof that a person committed theft**; false positives can occur.
- The source report contained hard-coded API credentials in its code appendix. Those values have been removed from the public-safe report copy and are intentionally not reproduced here. Rotate those credentials in Roboflow before using the project again.

## Source

Prepared from the supplied academic project report, *Advanced Image Recognition for Retail Stock Management* (B.E. CSE – AI & ML, 2024–25), including its proposed architecture, methodology, results discussion, and Appendix II code workflow.
