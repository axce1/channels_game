var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');


module.exports = {
  context: __dirname,
  entry: {lobby: './apps/templates/componets/lobby/index'},
  output: {
    path: path.resolve('./apps/static/bundles/'),
    filename: '[name]-bundle.js'
  },

  plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(), // don't reload if there is an error
        new BundleTracker({path: __dirname, filename: './webpack-stats.json'})
  ],

  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: /(node_modules)/,
        use: [{
          loader: 'babel-loader',
          options: {
            presets: ['es2015', 'react']
          }
        }],
      },
    ]
  },

  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
};
