# 职页成长指引

基于 Vue 3 + Vite 的职业成长指引展示站点。当前版本包含成长阶段、能力概览、本周行动和资源中心，后续可逐步接入真实 API。

## 开发

```bash
npm install
npm run dev
```

默认开发地址为 `http://localhost:5173/`。

## 构建

```bash
npm run build
```

构建产物会输出到 `dist` 目录。

## 部署到子目录

如果网站所有者提供的部署目录是 `https://xxx.yyy.com/zzz/`，请在 `.env.production` 中设置：

```ini
VITE_BASE_PATH=/zzz/
VITE_API_BASE_URL=/zzz/api
```

然后执行：

```bash
npm run build
```

Vite 会按 `VITE_BASE_PATH` 生成静态资源引用路径，页面中的接口根地址可通过 `src/config.js` 中的 `appConfig.apiBaseUrl` 读取。

## 目录说明

- `vite.config.js`：读取 `VITE_BASE_PATH`，控制静态资源基础路径。
- `src/config.js`：统一暴露 `basePath` 与 `apiBaseUrl`。
- `src/services/growthGuide.js`：成长指引数据服务，当前使用本地数据，后续可替换为真实接口。
- `src/App.vue`：站点主界面。
