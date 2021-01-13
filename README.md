## Deployment to Azure


### Install Azure CLI

``` bash
brew brew install azure-cli
```

This takes ages to complete, installs Python 3.9 and 3.8 and a bunch of other dependencies. 

Then:
``` bash
az login
```


### Web app

On Azure web panel, go to Home / "All resources", find the App Service entry (not App Service Plan).
Click on "Configuration" under "Settings" in the sidebar. Add a new application setting with:

 - name: `WEBSITES_PORT`  
 - value: `5000`


``` bash
az webapp config set --resource-group <resource-group-name> --name <app-name> --linux-fx-version "PYTHON|3.8"

az webapp up --sku F1 --name <app-name>
```

This deploys the app to Azure and also creates the `.azure/config` file. Subsequent updates can be applied with just `az webapp up`.

Behind the scene, the code is being containerized. So we might do that ourselves, see next section.


### Docker

