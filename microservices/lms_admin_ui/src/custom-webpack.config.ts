const webpack = require('webpack');

module.exports = {
    plugins: [
        new webpack.DefinePlugin({
            $ENV: {
                API_DOMAIN: JSON.stringify(process.env['API_DOMAIN']),
                FIREBASE_API_KEY: JSON.stringify(process.env['FIREBASE_API_KEY']),
                FIREBASE_APP_ID: JSON.stringify(process.env['FIREBASE_APP_ID']),
                PROJECT_ID: JSON.stringify(process.env['PROJECT_ID'])
            }
        })
    ]
};