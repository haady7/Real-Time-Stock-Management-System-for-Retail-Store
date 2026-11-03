# Dataset guide

This guide records the dataset approach described in the submitted academic report. The original datasets are not part of this repository.

## Tasks and labels described in the report

### Shelf stock monitoring

- Input: images of retail shelves.
- Labels: Filled and Empty.
- Purpose: identify shelf areas that may require restocking.

### Retail activity / theft detection

- Input: retail video clips or extracted frames.
- Labels mentioned in the report include Shoplifting, Product-Picked, and Customer-Bagpack.
- Purpose: flag visual predictions for subsequent staff review.

## Preparation approach described in the report

- Resize images to 640 × 640 pixels.
- Normalize images for model input.
- Apply augmentation such as rotation and brightness changes.
- Split the data into 70% training, 20% validation, and 10% testing.

## Recommended dataset hygiene

- Keep train, validation, and test sets separate.
- Avoid placing adjacent frames from the same recording in different splits; that can cause data leakage.
- Check class balance and label quality.
- Review false positives and false negatives before retraining.
- Keep source permissions, consent/notice, and retention requirements documented.
- Do not commit private CCTV footage or licensed datasets to this repository.

The recommendations above are general engineering guidance; the listed labels and 70/20/10 split are drawn from the project report.
