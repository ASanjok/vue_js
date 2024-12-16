const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      fallback: {
        querystring: require.resolve('querystring-es3'),
        stream: require.resolve('stream-browserify'),
        assert: require.resolve('assert'),
        util: require.resolve('util/'),
        net: false, 
        tls: false, 
      },
    },
  },
});
