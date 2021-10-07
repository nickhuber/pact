module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://pact-backend:8000/',
                changeOrigin: true
            }
        },
        hot: true,
        watchOptions: {
            poll: 100
        }
    },
    configureWebpack: {
        optimization: {
            splitChunks: {
                minSize: 10000,
                maxSize: 250000,
            }
        }
    }
}
