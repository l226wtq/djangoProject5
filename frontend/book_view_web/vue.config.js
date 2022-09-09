const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false,
  publicPath:'./',

  // build: {
  //   // Template for index.html
  //   index: path.resolve(__dirname, '../dist/index.html'),

  //   // Paths
  //   assetsRoot: path.resolve(__dirname, '../dist'),
  //   assetsSubDirectory: 'static',
  //   // assentsPublicPath原值'/'改为'./'
  //   // 如果是vue3.0,则assetsDir: './' 
  //   assetsPublicPath: './', 
  // }
})
