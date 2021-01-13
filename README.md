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

``` bash
export AZ_RESOURCE_GROUP="frnhr-aztest1-group"
export AZ_REGISTRY="frnhrregistry"
export AZ_PLAN="frnhr-aztest1-plan"
export AZ_APP="frnhr-aztest1-docker"
export AZ_IMAGE="aztest1"
export AZ_IMAGE_VERSION="0.1.0"
```

``` bash
az group create -l northeurope -n  $AZ_RESOURCE_GROUP
az acr create --resource-group  $AZ_RESOURCE_GROUP --name $AZ_REGISTRY --sku Basic
```

Take note of the `lloginServer` value in the response.

``` bash
az acr login --name $AZ_REGISTRY
```

Build and tag an image:
``` bash
docker build . -t $AZ_IMAGE:$AZ_IMAGE_VERSION -t $AZ_IMAGE:latest
```

Push the image to Azure:
``` bash 
docker tag $AZ_IMAGE:$AZ_IMAGE_VERSION $AZ_REGISTRY.azurecr.io/$AZ_IMAGE:$AZ_IMAGE_VERSION
docker tag $AZ_IMAGE:latest $AZ_REGISTRY.azurecr.io/$AZ_IMAGE:latest
docker push $AZ_REGISTRY.azurecr.io/$AZ_IMAGE:$AZ_IMAGE_VERSION
docker push $AZ_REGISTRY.azurecr.io/$AZ_IMAGE:latest
```

Configure:
``` bash
az appservice plan create --name $AZ_PLAN --resource-group $AZ_RESOURCE_GROUP --is-linux
az webapp create --resource-group $AZ_RESOURCE_GROUP --plan $AZ_PLAN --name $AZ_APP --deployment-container-image-name $AZ_REGISTRY.azurecr.io/$AZ_IMAGE:latest
az webapp config appsettings set --resource-group $AZ_RESOURCE_GROUP --name $AZ_APP --settings WEBSITES_PORT=8000
AZ_PRINCIPAL_ID=$(az webapp identity assign --resource-group $AZ_RESOURCE_GROUP --name $AZ_APP --query principalId --output tsv)
AZ_SUBSCRIPTION_ID=$(az account show --query id --output tsv)
az role assignment create --assignee $AZ_PRINCIPAL_ID --scope /subscriptions/$AZ_SUBSCRIPTION_ID/resourceGroups/$AZ_RESOURCE_GROUP/providers/Microsoft.ContainerRegistry/registries/$AZ_REGISTRY --role "AcrPull"
az acr update -n $AZ_REGISTRY --admin-enabled true
```

Deploy:
``` bash
az webapp config container set --name $AZ_APP --resource-group $AZ_RESOURCE_GROUP --docker-custom-image-name $AZ_REGISTRY.azurecr.io/$AZ_IMAGE:latest --docker-registry-server-url https://$AZ_REGISTRY.azurecr.io
echo "https://$AZ_APP.azurewebsites.net/"
```

Docs:
 - https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli
 - https://docs.microsoft.com/en-us/azure/app-service/quickstart-custom-container?pivots=container-linux

