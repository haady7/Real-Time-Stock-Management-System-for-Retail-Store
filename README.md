# Real-Time Stock Management System for Retail Store

An academic computer-vision project exploring automated retail shelf monitoring and activity flagging with **YOLOv8, Roboflow, Python, and OpenCV**.

The project report describes two computer-vision workflows: classifying shelf sections as `Filled` or `Empty`, and flagging configured visual activity classes (such as `Product-Picked` and `Shoplifting`) for staff review.

## Project goals

- Monitor shelf availability from images or video.
- Highlight shelf areas classified as filled or empty.
- Annotate detections with bounding boxes and confidence scores.
- Log model predictions for review.
- Explore a second inference workflow for retail activity monitoring.

## Repository contents

```text
.
├── docs/
│   └── PROJECT_REPORT_SUMMARY.md
├── src/
│   ├── stock_detection.py
│   └── theft_detection.py
├── .env.example
├── .gitignore
├── requirements.txt
├── output.png
└── README.md
```

- `docs/PROJECT_REPORT_SUMMARY.md` — cleaned overview of the submitted academic report, including its objectives, described architecture, dataset approach, and reported results.
- `src/stock_detection.py` — configurable Roboflow image inference for shelf stock classes.
- `src/theft_detection.py` — configurable video inference with annotated output and CSV event logging.
- `output.png` — an existing sample output image in this repository.

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Application scripting |
| YOLOv8 | Object detection model family described in the report |
| Roboflow | Dataset annotation, model hosting, and inference |
| OpenCV | Image/video capture, drawing, and export |
| Google Colab | Reported development and experimentation environment |

## Setup

**Requirements:** Python 3.9+ and a valid Roboflow model/API key.

1. Clone this repository:

   ```bash
   git clone https://github.com/haady7/Real-Time-Stock-Management-System-for-Retail-Store.git
   cd Real-Time-Stock-Management-System-for-Retail-Store
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your own Roboflow credentials:

   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env
   # macOS/Linux
   cp .env.example .env
   ```

   Edit `.env` and set `ROBOFLOW_API_KEY`, `STOCK_MODEL_ID`, and `THEFT_MODEL_ID` using values from your own Roboflow workspace. Never commit the populated `.env` file.

## Run stock detection on one image

```bash
python src/stock_detection.py --image path/to/shelf.jpg
```

The annotated image is saved to `outputs/stock_detection.jpg` by default. To choose another output path:

```bash
python src/stock_detection.py --image path/to/shelf.jpg --output outputs/my_result.jpg
```

## Run activity detection on a video

Use a video file:

```bash
python src/theft_detection.py --source path/to/store_video.mp4 --preview
```

Or use the default webcam:

```bash
python src/theft_detection.py --source 0 --preview
```

The annotated video and CSV log are saved under `outputs/` by default. Press `q` in the preview window to stop processing.

## Reported results

The academic report states the following figures. They are **reported in the submitted document and have not been independently reproduced by the cleaned scripts in this repository**.

| Metric | Value stated in report |
|---|---:|
| Stock classification precision | 92% |
| Theft-detection accuracy | 85% |
| Edge processing speed | 30+ FPS |
| Detection-to-alert latency | Below 500 ms |
| Planogram adherence | 95% |
| Stockout reduction in the described pilot | 35% |
| Theft-incident reduction in the described pilot | 50% |

For context and qualifications, see [the project report summary](docs/PROJECT_REPORT_SUMMARY.md).

## Important limitations and responsible use

- The scripts require your own valid Roboflow credentials and model IDs. The original project dataset and trained model weights are not included.
- Optional integrations discussed in the academic report (such as SMS/email notifications, ERP synchronization, and a production dashboard) are not implemented by these scripts.
- Model outputs can be wrong. A `Shoplifting` class prediction is only a signal for trained staff to review; it is **not proof of theft or wrongdoing**.
- Use surveillance footage only with appropriate authorization, notice, privacy safeguards, and retention controls.
- The submitted report appendix contained hard-coded Roboflow API credentials. Those credentials are intentionally not included in this public repository. **Revoke/rotate them in Roboflow before reusing the project**, and use environment variables for new credentials.

## Project report

The cleaned project overview is available in [docs/PROJECT_REPORT_SUMMARY.md](docs/PROJECT_REPORT_SUMMARY.md). The original PDF has not been added here because its appendix contained exposed API credentials; a redacted local copy was prepared separately.

## Author and academic context

Based on the B.E. Computer Science and Engineering (Artificial Intelligence & Machine Learning) project, *Advanced Image Recognition for Retail Stock Management* (2024–25), submitted at M. H. Saboo Siddik College of Engineering, University of Mumbai.

