const config = require('./webpack.config');
const { merge } = require('webpack-merge');

module.exports = merge(config, {
    mode: 'development',
    entry: './src/index.js',
    devServer: {
        port: 3000,
        proxy: { "/**": { target: 'http://web:5000/api/v1', secure: false } }
    },
    // Need for docker container reloading
    watchOptions: {
        poll: true
    }
});