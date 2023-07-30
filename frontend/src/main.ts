import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import SuperTokens from "supertokens-auth-react";
import "./assets/main.css";
import { SuperTokensConfig } from "./config";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';

SuperTokens.init(SuperTokensConfig);

const app = createApp(App);

app.use(router);

app.mount("#app");
