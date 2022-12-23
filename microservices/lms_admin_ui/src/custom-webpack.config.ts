const webpack = require('webpack');

module.exports = {
    plugins: [
        new webpack.DefinePlugin({
            $ENV: {
                API_URL: JSON.stringify(process.env['API_URL'])
            }
        })
    ]
};