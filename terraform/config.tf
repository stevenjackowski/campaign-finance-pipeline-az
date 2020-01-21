variable "backend_rg" {
  type        = string
  description = "Resource group name "
}

variable "backend_account" {
  type        = string
  description = "The id of the machine image (AMI) to use for the server."
}

variable "backend_container" {
  type        = string
  description = "The id of the machine image (AMI) to use for the server."
}

variable "backend_key" {
  type        = string
  description = "The id of the machine image (AMI) to use for the server."
}


terraform {
  backend "azurerm" {
    resource_group_name  = var.backend_rg
    storage_account_name = var.backend_account
    container_name       = var.backend_container
    key                  = var.backend_key
  }
}


resource "azurerm_resource_group" "rg" {
    name     = "CFPRg-1SJ"
    location = "westus"

    tags = {
        environment = "dev"
        project = "campaign-finance"
    }
}

# Create vnet
resource "azurerm_virtual_network" "net" {
    name                = "CFPNet-1SJ"
    address_space       = ["10.0.0.0/16"]
    location            = "westus"
    resource_group_name = azurerm_resource_group.rg.name

    tags = {
        environment = "dev"
        project = "campaign-finance"
    }
}

# Create subnet
resource "azurerm_subnet" "subnet" {
    name                 = "CFPSubnet-1SJ"
    resource_group_name  = azurerm_resource_group.rg.name
    virtual_network_name = azurerm_virtual_network.net.name
    address_prefix       = "10.0.1.0/24"
    service_endpoints    = ["Microsoft.Storage"]
}

# Create storage account
resource "azurerm_storage_account" "store" {
  name                = "cfpstorageaccount1sj"
  resource_group_name = azurerm_resource_group.rg.name

  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind              = "StorageV2"

    tags = {
        environment = "dev"
        project = "campaign-finance"
    }
}

# Create BLOB Container
resource "azurerm_storage_container" "container" {
  name                  = "control-blobs"
  resource_group_name   = azurerm_resource_group.rg.name
  storage_account_name  = azurerm_storage_account.store.name
  container_access_type = "private"

}

# Add the initial control JSON which includes candidate names
resource "azurerm_storage_blob" "blob" {
  name                   = "etl-control.json"
  resource_group_name    = azurerm_resource_group.rg.name
  storage_account_name   = azurerm_storage_account.store.name
  storage_container_name = azurerm_storage_container.container.name
  type                   = "Block"
  source                 = "etl-control-init.json"
  access_tier            = "Hot"

}

# 
resource "azurerm_storage_container" "container2" {
  name                  = "raw-data"
  resource_group_name   = azurerm_resource_group.rg.name
  storage_account_name  = azurerm_storage_account.store.name
  container_access_type = "private"

}

# Create Data Factory
resource "azurerm_data_factory" "datafactory" {
  name                = "cfpdatafactory1SJ"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  identity {
      type = "SystemAssigned"
  }

    tags = {
        environment = "dev"
        project = "campaign-finance"
    }

}

# TODO - Azure Functions

# TODOs
# Add role to Data Factory for Storage Account (Data Contributor)