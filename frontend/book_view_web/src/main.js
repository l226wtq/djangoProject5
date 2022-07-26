import { createApp } from 'vue'
import App from './App.vue'
import 'devextreme/dist/css/dx.light.css';
import { createRouter, createWebHashHistory } from 'vue-router'

import VueClipboard from 'vue3-clipboard'

import "highlight.js/styles/vs.css"
import "highlight.js/lib/common"
import hljsVuePlugin from "@highlightjs/vue-plugin";

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


//中文界面或提示（翻译不全）
import zhMessages from "devextreme/localization/messages/zh.json";
import { loadMessages, locale } from "devextreme/localization";
loadMessages(zhMessages);
locale(navigator.language);
// // 货币
// import config from "devextreme/core/config";
// config({
//     //ui组件显示顺序  true 为把样式都改倒了 从右往左
//     rtlEnabled:false,
//     //货币配置
//     defaultCurrency: 'RMB'
// });

// import PSIcheckoutMainView from "./components/PSIcheckoutMainView.vue"
const PSIcheckoutMainView = () => import("./components/PSIcheckoutMainView.vue")
// import PSIwarehousingMainView from "./components/PSIwarehousingMainView.vue"
const PSIwarehousingMainView = () => import("./components/PSIwarehousingMainView.vue")
// import PSImainListView from "./components/PSImainListView.vue"
const PSImainListView = () => import("./components/PSImainListView.vue")

const PSIwarehousingPurchaseMainView = () => import("./components/PSIwarehousingPurchaseMainView.vue")
const PSIwarehousingPorductMainView = () => import("./components/PSIwarehousingPorductMainView.vue")
const dbExportBackup = () => import("./components/dbExportBackup.vue")
const sqlDocumentMainView = () => import("./components/sqlDocumentMainView.vue")
const homepage = () => import("./components/PSIhomePage.vue")
// 2. 定义一些路由
// 每个路由都需要映射到一个组件。
// 我们后面再讨论嵌套路由。
const routes = [
    
    { path: '', component: homepage },
    { path: '/homepage', component: homepage },
    { path: '/warehousing', component: PSIwarehousingMainView },
    { path: '/warehousingpurchase', component: PSIwarehousingPurchaseMainView },
    { path: '/warehousingproduct', component: PSIwarehousingPorductMainView },
    { path: '/checkout', component: PSIcheckoutMainView },
    { path: '/mainlist', component: PSImainListView },
    { path: '/dbexportbackup', component: dbExportBackup },
    { path: '/sqldocument', component: sqlDocumentMainView },
    { path: '/sqldocument/:sysType', component: sqlDocumentMainView },
]
// 3. 创建路由实例并传递 `routes` 配置
// 你可以在这里输入更多的配置，但我们在这里
// 暂时保持简单
const router = createRouter({
    // 4. 内部提供了 history 模式的实现。为了简单起见，我们在这里使用 hash 模式。
    history: createWebHashHistory(),
    routes, // `routes: routes` 的缩写
})

const app = createApp(App)
app.use(router)
app.use(VueClipboard, {
    autoSetContainer: true,
    appendToBody: true,
})
app.use(hljsVuePlugin)
app.use(ElementPlus)

app.mount('#app')
