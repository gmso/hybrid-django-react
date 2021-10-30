const path = require('path');

module.exports = {
  entry: './frontend/index.js',  // path to our input file
  output: {
    filename: 'index-bundle.js',  // output bundle file name
    path: path.resolve(__dirname, './static'),  // path to our Django static directory
  },
  mode: 'development',
  watch: true,
  watchOptions: {
    aggregateTimeout: 500, // delay before reloading
    poll: 1000 // enable polling since fsevents are not supported in docker
  },
  devServer: {
    port: 80, // use any port suitable for your configuration
    host: '0.0.0.0', // to accept connections from outside container
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: { presets: ["@babel/preset-env", "@babel/preset-react"] }
      },
    ]
  }
};