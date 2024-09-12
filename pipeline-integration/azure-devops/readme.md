# Introduction

All of these files are used to integrate AEP with Azure DevOps. 

The pipeline should be triggered by a push to the repository, or via a pull request trigger. 

## What each template does

### Get a PR Review
The `ado_pullrequest_reviewer.yml` template is used to add a review comment to your pull request based on the changes made.

### Get a PR Summary
The `ado_pullrequest_summarise.yml` template is used to summarise the changes made within the pull request by updating the PR description.

### Get a PR Review with Board Integration
The `ado_pullrequest_reviewer_boards.yml` template is used to add a review comment to your pull request, as well as provide an indication as to whether the pull request meets the criteria outlined in the linked work item.

### Get a PR Summary with Board Integration
The `ado_pullrequest_reviewer_boards.yml` template is used to summarise the changes made within the pull request by updating the PR description, as well as indicating the work that has been completed according to the linked work item.

## How to Set Up a Pull Request Trigger
This guide will take you through a typical set up for a pull request trigger within your repository.

1. Before you get started adding pipelines, remember to store your secrets securely in Azure DevOps. You can do this by creating a new variable group and adding your secrets there. Call the group 'AEP'.
   1. You can follow the Microsoft Documentation for this here: [Create a variable group](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/set-secret-variables?view=azure-devops&tabs=yaml%2Cbash#set-a-secret-variable-in-a-variable-group)
   2. Create two secrets using your AEP API Key and Consumer Key. Call them `X_API_KEY` and `X_API_CONSUMER` respectively.

2. Set up your AEP Template by copying the contents of the template e.g. `ado_pullrequest_reviewer.yml` into your templates repository, for this example - I've uploaded it to a 'devops-templates' repository in the root of the directory.

3. Now, create a 'GenAI-PR.yml' file in your target repository (i.e. where your code is), and add the following pipeline:
```yaml
trigger: none

resources:
  repositories:
    - repository: devops-templates
      type: git
      name: devops-templates

variables:
  - group: AEP

stages:  
  - template: ado_pullrequest_reviewer.yml@devops-templates
    parameters:
      x_api_consumer: $(X_API_CONSUMER)
      x_api_key: $(X_API_KEY)
```

4. Now, go to the Azure DevOps portal and create a new pipeline. Choose your existing file, selecting the repository where you've added the 'GenAI-PR.yml' file.

5. Next, go to your repository settings by:
   1. Clicking on the 'Cog' icon in the bottom left corner.
   2. Under 'Repos', click on 'Repositories'.
   3. Go to your repository (where you added the 'GenAI-PR.yml' file).
   4. Click on 'Policies'.
   5. Under 'Branch Policies', click on your 'main/master' branch.
   6. Add a 'Build Validation' by clicking the + icon.
   7. Select your 'GenAI-PR' pipeline as a build pipeline, with an automatic trigger, with an optional policy requirement.

6. Congrats, you've set up a pull request trigger! Now, whenever you create a pull request, the pipeline will run and add a review comment to your pull request based on the changes made. 