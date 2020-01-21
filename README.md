# campaign-finance-pipeline-az

## Overview
This project is a learning/experimental app to load FEC campaign finance data and present it in a dashboard, using Azure technologies. The app will contain a data pipeline to load the latest Presidential campaign committee report information for selected presidential candidates, store this data in an Azure BLOB, and serve it to a simple dashboard so users can visualize the candidates' quarterly contributions, spend, and burndown rate (to see when they would run out of cash if they continue at their current spend). 

Some of the principles employed in this app design include:
* Data transformation logic will be written and Python, with Data Factory used as an orchestration engine
* All infrastructure will be written as code using Terraform
* In order to keep costs as low as possible, the cheapest storage options will be selected (e.g. Azure BLOB Storage)