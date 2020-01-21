

To set environment variables, see the documentation (here)[https://docs.microsoft.com/en-us/azure/virtual-machines/linux/terraform-install-configure?/azure/terraform/toc.json&bc=/azure/bread/toc.json].

```
#!/bin/sh
echo "Setting environment variables for Terraform"
export ARM_SUBSCRIPTION_ID=your_subscription_id
export ARM_CLIENT_ID=your_appId
export ARM_CLIENT_SECRET=your_password
export ARM_TENANT_ID=your_tenant_id

# Not needed for public, required for usgovernment, german, china
export ARM_ENVIRONMENT=public
```