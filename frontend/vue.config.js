module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000/',
                changeOrigin: true
            }
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
