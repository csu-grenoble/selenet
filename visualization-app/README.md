# SeleNet :: Network vizualiser

## First time

- Go to: https://ion.cesium.com/
- Create an account if you do not already have one.
- Open the **[Access Token section](https://ion.cesium.com/tokens)**, create a new token named `selenet` if you do not already have one, and copy it.
- `npm install`: install all dependencies if they are not already installed (check that the node_modules folder exists).

Once you are in cesium Ion, you need to add the moon asset to your assets. 
Go to **[Asset Depot](https://ion.cesium.com/assetdepot/2684829?query=moon)**, and type `Moon` in the search bar. Add the **Cesium Moon** asset to your asses by clucking the "+"

It should then show up in the **My Assets** Tab, with ID **[2684829](https://ion.cesium.com/assetdepot/2684829?query=moon)**


## Build or rebuild the webpack

```bash
npm run build
```

## Launch the application

```bash
`API_URL=my_selenet_token npm start
```
