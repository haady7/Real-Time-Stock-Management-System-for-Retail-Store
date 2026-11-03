# Data directory

The original image dataset and video clips are not included in this public repository.

Suggested local organization:

```text
data/
├── raw/
│   ├── shelf-images/
│   └── retail-video/
└── processed/
    ├── stock-dataset/
    └── activity-dataset/
```

Keep private or licensed datasets on authorized storage. Local raw and processed folders are excluded by .gitignore.

See [Dataset Guide](../docs/DATASET_GUIDE.md) for the labels and split approach described in the academic report.
