// The path to the CesiumJS source code
const cesiumSource = "node_modules/cesium/Source";
const cesiumWorkers = "../Build/Cesium/Workers";
const CopyWebpackPlugin = require("copy-webpack-plugin");
const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  context: __dirname,
  entry: {      
    moon: "./src/moon.js",
    // app: "./src/index.js"
        
  },
  // output: {
  //   filename: "app.js",
  //   path: path.resolve(__dirname, "dist"),
  //   sourcePrefix: "",
  // },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].bundle.js",
    clean: true,
  },
  amd: {
    // Enable webpack-friendly use of require in Cesium
    toUrlUndefined: true,
  },
  resolve: {
    alias: {
      cesium: path.resolve(__dirname, cesiumSource),
    },
    mainFiles: ["module", "main", "Cesium"],
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(png|gif|jpg|jpeg|svg|xml|czml|json)$/,
        use: ["url-loader"],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "src/moon.html",
    }),
    // new HtmlWebpackPlugin({
    //   filename: "moon.html",
    //   template: "./src/moon/moon.html",
    //   chunks: ["moon"],
    // }),
    // new HtmlWebpackPlugin({
    //   filename: "earth.html",
    //   template: "./src/earth/earth.html",
    //   chunks: ["earth"],
    // }),
    // Copy Cesium Assets, Widgets, and Workers to a static directory
    new CopyWebpackPlugin({
      patterns: [
        { from: path.join(cesiumSource, cesiumWorkers), to: "Workers" },
        { from: path.join(cesiumSource, "Assets"), to: "Assets" },
        { from: path.join(cesiumSource, "Widgets"), to: "Widgets" },
      ],
    }),
    new webpack.DefinePlugin({
      // Define relative base path in cesium for loading assets
      CESIUM_BASE_URL: JSON.stringify("/"),
    }),
    new webpack.DefinePlugin({
      "process.env.API_URL": JSON.stringify(process.env.API_URL)
    })
  ],
  mode: "development",
};