# SeleNet :: Network vizualiser

## First time

- Go to: https://ion.cesium.com/
- Create an account if you do not already have one.
- Open the **[Access Token section](https://ion.cesium.com/tokens)**, create a new token named `selenet` if you do not already have one, and copy it.
- Save the copied token into the `.token.selenet` text file.
- `npm install`: install all dependencies if they are not already installed (check that the node_modules folder exists).

Once you are in cesium Ion, you need to add the moon asset to your assets. 
Go to **[Asset Depot](https://ion.cesium.com/assetdepot/2684829?query=moon)**, and type `Moon` in the search bar. Add the **Cesium Moon** asset to your asses by clucking the "+"

It should then show up in the **My Assets** Tab, with ID **[2684829](https://ion.cesium.com/assetdepot/2684829?query=moon)**


## Build or rebuild the webpack

Use a recent version of Node (for instance, node v24.13.1 & npm v11.8.0). `[nvm](https://github.com/nvm-sh/nvm)` can help you to install a recent version.


```bash
npm run build
```

## Launch the application

```bash
TOKEN=$(cat .token.selenet) 
API_URL=$TOKEN npm start
```

