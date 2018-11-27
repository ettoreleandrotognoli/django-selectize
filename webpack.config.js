const path = require('path');

module.exports = {
  entry: './src/typescript/index.ts',
  devtool: 'inline-source-map',
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/
      }
    ]
  },
  resolve: {
    extensions: [ '.ts', '.js' ]
  },
  output: {
    filename: 'selectize.js',
    path: path.resolve(__dirname, 'src/python/selectize/static/')
  }
};