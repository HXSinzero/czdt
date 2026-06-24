import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { getPublicAssetUrl } from './config'
import './styles.css'

const fontStyle = document.createElement('style')
fontStyle.textContent = `
@font-face {
  font-family: "zydt";
  src: url("${getPublicAssetUrl('fonts/智勇大同体.ttf')}") format("truetype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
`
document.head.appendChild(fontStyle)

createApp(App).use(router).mount('#app')
