# Security policy

## Reporting a vulnerability

Do not publish credentials, API keys, private retail footage, or personal data in a public issue. Contact the repository owner privately through their GitHub profile.

## Credential handling

- Store Roboflow credentials only in a local .env file.
- Keep .env out of version control.
- Rotate any API key exposed in a report, notebook, screenshot, or commit.
- Do not hard-code API keys in source code.

## Surveillance data

Use CCTV data only with authorization and appropriate notice. Minimize collection and retention, and protect access to recorded footage.

## Model limitations

A prediction labelled Shoplifting is a model output, not a verified finding. It must not be treated as proof of wrongdoing or used as the sole basis for action against a person.
