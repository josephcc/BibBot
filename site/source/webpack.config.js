var webpack = require("webpack");
var path = require('path');

module.exports = {
  entry: {
    app: './app/app.jsx',
  },
  output: {
    path: '../dist',
    filename: '[name].js'
  },
  module: {
    loaders: [
      {
        test: /\.jsx$/,
        loader: "babel-loader",
        include: path.join(__dirname, 'app'),
        query: {
          stage: 0
        }
      }
    ]
  },
  plugins: [
    new webpack.optimize.DedupePlugin(),
    new webpack.PrefetchPlugin("react"),
    new webpack.PrefetchPlugin("react/lib/ReactComponentBrowserEnvironment")
  ]
}

