# GitHub Actions Configuration

This folder contains two GitHub Actions workflows. Select a workflow below to view its details:
- [gha_pullrequest_reviewer.yml](https://github.com/KainosSoftwareLtd/ai-enhanced-platform/blob/main/pipeline-integration/github-actions/gha_pullrequest_reviewer.yml) - Workflow using OpenAI for reviewing pull requests.

<details>
<summary>gha_pullrequest_reviewer.yml</summary>

This workflow is triggered when a pull request is opened or updated on the 'master' branch, or manually triggered using the workflow_dispatch event.

## Configuration Values

- **X_API_KEY**: The API key for the system. This is stored as a secret in the GitHub repository settings.
- **X_API_CONSUMER**: The consumer UUID for the system. This is also stored as a secret in the GitHub repository settings.
- **API_HOST**: The URL of the API host. Currently, it is set to "https://app-aep-api-s-latest-uksouth.azurewebsites.net/".
- **WORKING_DIRECTORY**: The working directory for the pipeline. It is set to the `${{ github.workspace }}/` directory in the current GitHub workspace.

</details>

- [gha_pullrequest_summarise.yml](https://github.com/KainosSoftwareLtd/ai-enhanced-platform/blob/feature/main/pipeline-integration/github-actions/gha_pullrequest_summarise.yml) - Workflow using OpenAI for summarising pull requests.

<details>
<summary>gha_pullrequest_summarise.yml</summary>

This workflow is also triggered when a pull request is opened or updated on the 'master' branch, or manually triggered using the workflow_dispatch event.

## Configuration Values

- **X_API_KEY**: The API key for the system. This is stored as a secret in the GitHub repository settings.
- **X_API_CONSUMER**: The consumer UUID for the system. This is also stored as a secret in the GitHub repository settings.
- **API_HOST**: The URL of the API host. Currently, it is set to "https://app-aep-api-s-latest-uksouth.azurewebsites.net/".
- **WORKING_DIRECTORY**: The working directory for the pipeline. It is set to the `pipeline-integration/github-actions/` directory in the current GitHub workspace.

</details>

## Updating Configuration Values

To update these values, you can change them directly in the respective `.yml` files. However, for the `X_API_KEY` and `X_API_CONSUMER`, you should update the secrets in the GitHub repository settings.

## Master Branch Reference

These configurations are typically used in the context of the `master` branch. If your repository uses a different default branch (like `main`), you may need to update any branch references in your workflows.

