const webpack = require('webpack');

module.exports = {
    plugins: [
        new webpack.DefinePlugin({
            $ENV: {
                API_DOMAIN: JSON.stringify(process.env['API_DOMAIN']),
            }
        })
    ]
};