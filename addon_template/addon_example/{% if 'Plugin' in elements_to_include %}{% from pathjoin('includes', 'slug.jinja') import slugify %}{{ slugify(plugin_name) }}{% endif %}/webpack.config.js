const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const resolve = (...paths) => path.resolve(__dirname, ...paths);

module.exports = (env, argv) => {
  const config = {
    context: resolve('src'),
    entry: resolve('src', 'index.tsx'),
    module: {
      rules: [{
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader'
      }, {
        test: [/\.s[ac]ss$/],
        use: ['style-loader', 'css-loader', 'sass-loader'],
      }, {
        test: [/\.css$/],
        use: ['style-loader', 'css-loader'],
      }]
    },
    resolve: {
      extensions: ['.js', '.jsx', '.ts', '.tsx']
    },
    output: {
      path: resolve('dist'),
      filename: 'bundle.js'
    },
    plugins: [
      new CleanWebpackPlugin(),
      new CopyWebpackPlugin({
        patterns: [
          resolve('src', 'index.html'),
          resolve('src', 'plugin.json'),
        ]
      })
    ]
  };

  if (argv.mode === 'production') {
    Object.assign(config, {
      devtool: 'source-map'
    });
  }
  if (argv.mode === 'development') {
    Object.assign(config, {
      devtool: 'eval-source-map'
    });
  }
  return config;
};
