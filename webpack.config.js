const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
// const FaviconsWebpackPlugin = require('favicons-webpack-plugin');
const path = require('path');

const config = {
  mode: 'development',
  watch: true,
  entry: './src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1
            }
          },
          'postcss-loader'
        ]
      },
      {
        test: /\.ts(x)?$/,
        loader: 'ts-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(js|jsx)$/,
        use: 'babel-loader',
        exclude: /node_modules/
      },
      /* {
        test: /\.(png|jpg|gif|ico)$/,
        // use: [
        //   {
        //     loader: 'file-loader',
        // options: {
        //   name: '[name].[ext]',
        //   outputPath: 'assets/images/'

        // use: [
        //   {
        //     loader: 'file-loader',
        //     options: {
        //       name: '[name].[ext]',
        //       outputPath: 'assets/images/'
        //     }
        //   }
        // ]

        // options: {
        //   outputPath: 'assets/images/',
        // }

        type: 'asset/resource',

        // type: 'asset',

        // generator: {
        //   fromFile: 'src/assets/images/[name].[ext]',
        // }

        generator: {
          filename: (name) => {
            const path = name.filename.split('/').slice(1, -1).join('/');
            return `${path}/[name][ext]`;
          },
        },
      } */
      {
        test: /\.png$/,
        use: [
          {
            loader: 'url-loader',
            options: {
              mimetype: 'image/png'
            }
          }
        ]
      },
    ]
  },
  resolve: {
    extensions: [
      '.tsx',
      '.ts',
      '.js'
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html'
    }),
    // new FaviconsWebpackPlugin({
    //   logo: './src/assets/images/favicon.png',
    //   prefix: 'assets/images/favicons/',
    //   devMode: 'webapp',
    //   icons: {
    //     android: true,
    //     appleIcon: true,
    //     appleStartup: true,
    //     coast: false,
    //     favicons: true,
    //     firefox: true,
    //     opengraph: false,
    //     twitter: false,
    //     yandex: false,
    //     windows: false
    //   }
    // }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: './src/assets/images',
          to: 'assets/images'
        }
      ]
    })
  ],
};

module.exports = config;