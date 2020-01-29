# Terraform Setup
This project makes use of Terraform and Azure Pipelines in order to create infrastructure as code, and automatically deploy infrastructure as code is committed to the repository. 




To initialize Terraform locally, without running through Azure Pipelines, the following command can be used once the corresponding environment Variables have been set.

` terraform init -backend-config="resource_group_name=$TF_VAR_BACKEND_RG" -backend-config="storage_account_name=$TF_VAR_BACKEND_ACCOUNT" -backend-config="container_name=$TF_VAR_BACKEND_CONTAINER" -backend-config="key=$TF_VAR_BACKEND_KEY" `