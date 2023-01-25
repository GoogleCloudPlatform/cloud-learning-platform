const webpack = require('webpack');

module.exports = {
    plugins: [
        new webpack.DefinePlugin({
            $ENV: {
                API_DOMAIN: JSON.stringify(process.env['API_DOMAIN']),
                FIREBASE_API_KEY: JSON.stringify(process.env['FIREBASE_API_KEY']),
                FIREBASE_AUTH_DOMAIN: JSON.stringify(process.env['FIREBASE_AUTH_DOMAIN']),
                FIREBASE_PROJECT_ID: JSON.stringify(process.env['FIREBASE_PROJECT_ID']),
                FIREBASE_STORAGE_BUCKET: JSON.stringify(process.env['FIREBASE_STORAGE_BUCKET']),
                FIREBASE_APP_ID: JSON.stringify(process.env['FIREBASE_APP_ID'])
            }
        })
    ]
};