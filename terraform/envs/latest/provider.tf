terraform {

  # The backend configuration defines the Terraform State files need to be stored.
  backend "azurerm" {
    key = "stable-backend.tfstate"
  }

  required_version = ">= 0.14"

  # Terraform configurations must declare which providers they require, so that Terraform can install and use them.
  # Provider requirements are declared in a required_providers block.

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.106.1"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "2.50.0"
    }
  }
}
provider "azuread" {
}
provider "azurerm" {
  skip_provider_registration = true
  features {}
}
