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

## 收费模式（v1.23 起全站免费）

- **v1.23 已移除授权码月付**：英文卷、数学卷与其他模块全部免费开放，无需激活。
- `gen_license.py` 仍保留在仓库中但不再被构建引用；日后若重启收费，
  可按 v1.21 的做法重新接入（git 历史可查）。
- **商业化注意**：英文卷中 EDB「中国寓言系列」改编阅读题标注为"仅教学用途"，
  若重启收费，建议将该部分设为免费内容或替换，避免版权争议。
- 运营口径：免费为主，靠持续更新题库与内容积累家长信任；自愿支持通道
  （爱发电/打赏）可后挂，不设门槛。

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

仓库保持 private；对外分发方式：全站免费，把最新 `index_vX.Y.html` 直接发给家长
（微信文件即可），GitHub 只做版本管理，不对外托管。
