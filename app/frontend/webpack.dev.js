const config = require('./webpack.config');
const { merge } = require('webpack-merge');

module.exports = merge(config, {
    mode: 'development',
    entry: './src/index.js',
    devServer: {
        port: 3000,
        proxy: { "/api/v1/**": { target: 'http://web:5000', secure: false } }
    },
    // Need for docker container reloading
    watchOptions: {
        poll: true
    }
});