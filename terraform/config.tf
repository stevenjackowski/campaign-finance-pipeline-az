provider "azurerm" {
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

  network_rules {
    default_action             = "Deny"
    ip_rules                   = ["100.0.0.1"]
    virtual_network_subnet_ids = [azurerm_subnet.subnet.id]
  }

    tags = {
        environment = "dev"
        project = "campaign-finance"
    }
}

# Create Data Factory
resource "azurerm_data_factory" "example" {
  name                = "example"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

    tags = {
        environment = "dev"
        project = "campaign-finance"
    }

}

# TODO - Azure Functions