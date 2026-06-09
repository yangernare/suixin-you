# 随心游 - 智能旅行助手

## 项目背景

"随心游"是一个面向国内旅游场景的智能旅行助手 Web 应用，聚焦云南省（昆明、大理等城市）。核心目标是为游客提供**一站式旅行规划体验**：地图导览、路线规划、天气联动、穿搭建议、预算估算、景点打卡、旅行翻译、AI 智能问答等功能融为一体。

项目定位为前端主导的单页应用（SPA），后端仅提供数据查询和 AI 对话代理，大部分业务逻辑和 UI 渲染均在前端完成。

## 技术栈

### 前端

- **单文件架构**：前端代码集中在 `qianduan.html`（主页面）一个文件中，`3d-terrain.html` 为独立的 Mapbox 高级版本
- **地图引擎**：高德地图 JS API 2.0（主页面，含 3D 地形、卫星图层、交通图层、行政区绘制、多种路线规划插件）
- **3D 地形（主页面）**：MapLibre GL JS v4.1.1（开源免费），底图使用 ArcGIS 卫星瓦片，DEM 使用 AWS Terrarium 地形瓦片，以全屏覆盖层形式叠加在高德地图之上
- **3D 地形（独立页面）**：Mapbox GL JS v2（`3d-terrain.html`），更高质量的卫星底图和地形效果，需用户自行配置 Mapbox token
- **AI 模型**：通义千问（qwen-turbo）通过阿里云 DashScope OpenAI 兼容接口直连前端
- **语音合成**：Web Speech API（浏览器原生 TTS，中文语音朗读景点讲解）
- **样式方案**：原生 CSS（CSS 变量主题色、渐变、毛玻璃、动画）
- **无前端框架**：纯原生 JavaScript，无 React/Vue/Angular

### 后端
- **Web 框架**：Flask + flask-cors
- **数据库**：SQLite（`travel.db`），存储景点信息（地名、类别、经度、纬度）
- **AI 代理**：通过火山引擎 Ark API（豆包模型）提供 `/api/chat` 接口（备用通道）
- **语言**：Python 3

### 外部服务
- **高德地图**：地图展示、天气查询（AMap.Weather）、路线规划（Driving/Walking/Riding/Transfer）、定位（Geolocation）、行政区搜索（DistrictSearch）
- **阿里云 DashScope**：通义千问大模型 API（前端直连）
- **火山引擎 Ark**：豆包大模型 API（后端代理）
- **ArcGIS 卫星瓦片**：3D 地形覆盖层底图（`server.arcgisonline.com`，免费无需 token）
- **AWS Terrarium DEM**：3D 地形高程数据（`s3.amazonaws.com/elevation-tiles-prod/terrarium/`，免费无需 token）

## 项目结构

```
随心游/
├── qianduan.html          # 主前端文件（HTML+CSS+JS 全内联，含 3D 地形覆盖层）
├── 3d-terrain.html        # 3D地形独立页面（Mapbox GL JS 高级版本，需 token）
├── 后端服务.py             # Flask 后端，提供景点查询、AI 聊天和讲解接口
├── SHUJUKU.py             # 数据库初始化脚本（创建 locations 表）
├── chaxun.py              # 数据导入脚本（从 CSV 导入 POI 数据到 SQLite）
├── travel.db              # SQLite 数据库文件
└── 随心游—地图端UI/        # 早期 UI 原型/参考
    ├── map_ui.html
    └── TourProject/
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/locations` | GET | 获取全部景点数据 |
| `/api/search?keyword=xxx` | GET | 关键词模糊搜索景点 |
| `/api/chat` | POST | AI 聊天（火山引擎代理） |
| `/api/guide` | POST | AI 景点讲解（接收 `{name, city, desc}`，返回 `{content}`） |

后端默认运行在 `http://127.0.0.1:5000`。

## 核心功能模块

1. **主题路线推荐**：慢享人文、自然野趣、美食漫游、轻量休闲四大主题
2. **3D 地图导览**：高德 3D 地形视图 + 行政区边界 + 景点标注
3. **智能路线规划**：支持步行/骑行/驾车/公交，AI 结合天气推荐出行方式
4. **实时天气 + 穿搭建议**：高德天气 API + 规则引擎 + AI 个性化建议
5. **预算估算**：按天数/类别（餐饮/门票/交通/住宿）估算，AI 优化方案
6. **景点打卡进度**：记录游玩状态和时间
7. **旅行翻译助手**：常用短句 + 自定义翻译
8. **景点评分与点评**：星级评分 + 文字评论 + 图片上传
9. **UGC 景点添加**：用户可在地图上点击添加自定义景点
10. **AI 聊天助手**：悬浮聊天窗口，支持快捷提问，上下文感知当前景点
11. **3D 地形可视化**：主页面集成 MapLibre GL JS，点击 "3D地形" 按钮切换全屏覆盖层，展示苍山、轿子山、大牯牛山的真实 DEM 地形和徒步路线；独立页面 `3d-terrain.html` 提供 Mapbox 高级版本
12. **AI 语音导游**：人文景点弹窗内置讲解按钮，后端 `/api/guide` 接口生成讲解词 + 浏览器 Web Speech API 中文朗读

## 项目约定

- **单文件优先**：前端所有代码保持在 `qianduan.html` 中，不拆分模块
- **中文界面**：所有 UI 文案使用中文
- **城市数据硬编码**：昆明和大理的景点数据直接写在 JS 的 `cityData` 对象中
- **坐标系**：使用 GCJ-02 坐标系（高德/国内标准）
- **配色方案**：主色 `#409EFF`（Element UI 蓝），四主题色分别为橙/绿/红/青
- **弹窗交互**：所有功能面板使用 `.modal-overlay` 模态弹窗实现

## 沟通偏好

- 用户使用中文交流，代码注释为中文
- 用户为个人开发者/学生项目，偏好直接有效的解决方案
- 修改代码时保持现有代码风格，不引入额外框架或依赖

## 禁止事项

- **不要**将前端拆分为多个文件或引入构建工具（webpack/vite 等）
- **不要**引入前端框架（React/Vue/Angular）
- **不要**删除或修改高德地图 API Key 和安全密钥
- **不要**删除或修改 AI API Key（DashScope / 火山引擎）
- **不要**硬编码 Mapbox token（`3d-terrain.html` 中用户通过页面输入框自行配置，存 localStorage；主页面使用 MapLibre 无需 token）
- **不要**修改已有的城市景点数据坐标
- **不要**将 SQLite 替换为其他数据库
- **不要**添加英文界面或多语言支持
