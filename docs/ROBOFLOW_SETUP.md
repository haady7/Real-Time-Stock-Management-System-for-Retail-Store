# Roboflow setup

The inference scripts use a Roboflow-hosted model through the Inference SDK.

## 1. Prepare your models

In your Roboflow workspace, make sure you have trained and deployed the relevant object-detection model versions. You need a model ID for the stock-monitoring task and (if using video activity mode) a model ID for the activity task.

Model ID format:

```text
workspace-name/project-name/version-number
```

The actual workspace, project names, and version numbers are specific to your account and are not included in this repository.

## 2. Create local configuration

Copy .env.example to .env and fill in:

- ROBOFLOW_API_KEY: a private API key from your Roboflow account.
- ROBOFLOW_API_URL: defaults to the serverless inference endpoint.
- STOCK_MODEL_ID: your shelf-stock model ID.
- THEFT_MODEL_ID: your retail activity model ID.

Never commit .env. The example file contains placeholders only.

## 3. Run local inference

Install the repository:

```bash
pip install -e .
```

Then run one of the commands in the root README.

## 4. Confirm class names

The scripts display class labels returned by your model. The stock model should return the shelf classes expected by your dataset (for example, Filled and Empty). The activity model should return the classes used in the dataset you trained.

The script does not create a theft-behavior classifier, perform posture estimation, or infer intent. It only displays and logs the labels returned by the configured model.

## Troubleshooting

- Check that the API key is valid and has access to the project.
- Confirm the workspace, project, and version in each model ID.
- Confirm that the model endpoint is deployed and available.
- Check that your input image/video can be read by OpenCV.
- Use a small image/video sample while testing to avoid unnecessary inference calls.
