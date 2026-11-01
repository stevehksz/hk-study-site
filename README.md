# 香港插班学习站（hk-study-site）

为内地家庭快速了解并跟上香港教学（中文 · 英文 · 数学）的单文件 HTML 学习站：
古诗词 185 首（拼音/粤拼）、港小生字 335、词表 1465、数学中↔英术语表、
英文卷（P1–P6 + 综合卷，本地随机出题 + AI 换题）、数学卷（双语对照 P1–P6）、
默写填空、朗读、打卡火焰、成就徽章、闪卡、单词贪吃蛇、升学规划。
数据全部存 localStorage，不上传。

## 构建

```bash
python generate_html.py        # 生成 index_vX.Y.html + index.html 副本
node verify2.js                # jsdom 全量断言（当前 171 项）
```

首次构建会自动生成 `license_secret.txt`（授权码密钥）。

## 授权码月付（v1.21 起）

- **付费模块**：英文卷 + 数学卷（智能出卷）。
- **免费模块**：速览指南、术语表、港小生字、词表、古诗词、进度、游戏。
- **发码**（收款后手动执行）：

```bash
python gen_license.py 陈太太 3            # 3 个月
python gen_license.py 陈太太 2026-12-31   # 指定到期日
```

激活码格式 `HKSS-YYYYMMDD-XXXXXXXX`，发码记录自动追加到 `licenses_issued.csv`
（含客户信息，已 gitignore，绝不入库）。用户在锁定面板输入激活码即解锁，
到期后输入新码续期。

- **安全级别声明**：防君子级——密钥随页面分发，读源码者可自制码。
  月付模式的真正护城河是**持续更新的题库与内容**，不是技术封锁。
- **商业化注意**：英文卷中 EDB「中国寓言系列」改编阅读题标注为"仅教学用途"，
  若正式收费，建议将该部分设为免费内容或替换，避免版权争议。

## 版本规范

- 每次功能改动递增 `v1.x`（版本号写在 generate_html.py 副标题"公开版 vX.Y"，
  为单一真相源）。
- 产物自动命名 `index_vX.Y.html`，同时保留 `index.html` 副本
  （verify2.js 与部署入口依赖）。

## 上传 GitHub（私有仓库）

```bash
git remote add origin https://github.com/stevehksz/hk-study-site.git
git push -u origin main
```

仓库保持 private；对外分发方式：把最新 `index_vX.Y.html` 直接发给付费家长
（微信文件即可），GitHub 只做版本管理，不对外托管。
