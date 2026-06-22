# 发布与部署指南（MkDocs + GitHub Pages）

> 本文是「怎么把书发布成网站」的操作手册。工具链与架构决策的背景见 `PLAN.md §9`。
> 现阶段处于**框架定型**，本文是**到部署阶段照着做**的 checklist；正文写作期不必执行。

---

## 1. 总体架构

**一个学科 = 一个仓库 = 一个站点；同学科的「指南」「综述」是同站点下的两个路径区。**

```
ttzg.site                        根域名（你已有）
└─ ebook.ttzg.site               电子书门户：列出所有学科        [独立仓库：ebook]
   ├─ quant.ebook.ttzg.site      量化学科站                      [仓库：quant ← 本项目]
   │   ├─ /guide/                量化教学指南
   │   └─ /survey/               量化技术综述
   ├─ <学科2>.ebook.ttzg.site    以后的学科，结构同上            [仓库：<学科2>]
   └─ ...
```

为什么不是「指南、综述各一个独立项目」：两书互相高频引用、需要同源互跳，且学科要写进域名。把学科做成子域名（一仓库一站点）、两书做成 `/guide/`、`/survey/` 路径区，可同时满足：①「量化」在域名里 ②一个网站、点一下就互跳 ③ N 个学科只要 N 个仓库（不是 2N）。

---

## 2. 域名方案

| 层级 | 域名 | 承载内容 | 仓库 |
|---|---|---|---|
| 根域名 | `ttzg.site` | 你的主域名 | — |
| 一级子域名 | `ebook.ttzg.site` | 电子书**门户**（学科索引页） | `ebook`（可选，建议有） |
| 二级子域名 | `quant.ebook.ttzg.site` | **量化学科**站（本项目） | `quant` |
| 路径区 | `…/guide/`、`…/survey/` | 量化指南、量化综述 | 同上仓库内 |

> `quant.ebook.ttzg.site` 共 21 字符，远低于 GitHub Pages 证书要求的 64 字符上限；且全部是子域名（无需操作根域名的 A 记录），DNS 全用 CNAME，最省心。

---

## 3. 仓库怎么管理

**结论：本项目就是「量化」这一个仓库，不拆成两个项目。** 指南与综述在同一仓库、同一站点、不同路径区。门户 `ebook` 是另一个独立的小仓库（只放一个学科索引页，可选）。

**命名约定（关键，便于扩展）：仓库名 = 学科 slug = 子域名 label。**

| 仓库 | 自定义域名 | DNS CNAME 记录 |
|---|---|---|
| `quant` | `quant.ebook.ttzg.site` | `quant.ebook` → `w3903771.github.io` |
| `ebook` | `ebook.ttzg.site` | `ebook` → `w3903771.github.io` |
| 未来 `<slug>` | `<slug>.ebook.ttzg.site` | `<slug>.ebook` → `w3903771.github.io` |

- 所有仓库的 CNAME 都指向**同一个** `w3903771.github.io`；GitHub 按访问的域名（Host）匹配到「声明了该自定义域名」的那个仓库，不会混淆。
- 全部学科仓库挂在固定 GitHub 账号 `w3903771` 下；若想集中管理也可建一个 Organization。
- 本项目本地目录与远端仓库均命名为 `quant`（与子域名 `quant.ebook.ttzg.site` 一致）。

---

## 4. 一次性配置（每个学科仓库做一遍）

以 `quant` 仓库为例。

### 4.1 DNS：在 `ttzg.site` 的域名解析处加记录

| 主机记录 / Host | 类型 | 记录值 | 用途 |
|---|---|---|---|
| `quant.ebook` | CNAME | `w3903771.github.io` | 量化学科站 |
| `ebook` | CNAME | `w3903771.github.io` | 门户（部署门户仓库时加） |
| `_github-pages-challenge-w3903771` | TXT | （GitHub 给的校验串） | **账户级域名验证**，见 4.3 |

> 不同服务商「主机记录」写法：阿里云/DNSPod/Cloudflare 等在 `ttzg.site` 的解析里填 `quant.ebook` 即可（系统自动补上 `.ttzg.site`）。**不要**给这些子域名再加任何 A/AAAA 记录，只留一条 CNAME，否则证书签发会失败。

### 4.2 仓库 Pages 设置

1. 仓库 **Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**（本项目用 Actions 部署，不是从分支部署）。
2. 同页 **Custom domain** 填 `quant.ebook.ttzg.site`，保存。GitHub 会做 DNS 检查（需 4.1 生效，通常几分钟到一小时）。
3. 检查通过后，勾选 **Enforce HTTPS**（证书签发前该项灰显，耐心等）。

> 本项目的 workflow（`.github/workflows/deploy.yml`）已在产物里写入 `_site/CNAME`，与 Settings 里的 Custom domain 双保险，避免每次部署后域名丢失。

### 4.3（推荐）账户级域名验证，防子域名被抢注

GitHub 个人头像 → **Settings → Pages → Verify domains** → 输入 `ttzg.site` → 按提示在 DNS 加一条 `_github-pages-challenge-w3903771` 的 TXT 记录 → Verify。
验证后，`*.ttzg.site` 下的自定义域名只能被你的账号使用，杜绝他人占用导致的子域名劫持。

---

## 5. 日常：本地预览与构建

```bash
# 装文档工具链（并入独立 uv 环境）
uv sync --group docs

# 预览指南（默认 http://127.0.0.1:8000 ）
uv run mkdocs serve -f mkdocs.guide.yml

# 同时预览综述，换个端口
uv run mkdocs serve -f mkdocs.survey.yml -a 127.0.0.1:8001

# 本地构建（产物 _site/guide、_site/survey；正常用 CI 构建，本地一般只需 serve）
uv run mkdocs build -f mkdocs.guide.yml
uv run mkdocs build -f mkdocs.survey.yml
```

部署：把仓库推到 GitHub 的 `main` 分支，Actions 自动构建并发布。`workflow_dispatch` 也支持在 Actions 页手动触发。

> CI **不跑任何量化/深度学习代码**——图表是你本地预先跑好、以静态图（PNG/SVG）提交进仓库的，所以 CI 只装 `mkdocs-material + jieba`，构建极快、无需 GPU。这正是「代码本地跑、结果图静态内嵌」方案的红利。

---

## 6. 写作约定（与本架构配套）

- **同书内链接**用相对路径（MkDocs 默认生成相对链接，换域名不受影响）。
- **跨书链接**用根相对路径：综述里引指南写 `[…](/guide/chXX/)`，指南里引综述写 `[…](/survey/0X/)`。两书同源，换域名也不用改正文。
- **图片**：本地脚本出图 → 存进仓库（如 `guide/img/`，与正文就近）→ 正文相对引用 `![](img/xxx.png)`。
- **数学**：行内 `$...$`、块级 `$$...$$` 直接写（已配 arithmatex + MathJax）。下标 `r_{t}` 等无需转义。
- **提示框**：用 `!!! note` / `!!! warning` / `!!! tip`（admonition）。
- **每本书要有 `index.md`** 作为站点首页（已为指南/综述各建一个）。
- **正式产物（会发布的网页内容）一律不出现 "d2l" 字样**；写作风格描述用中性表述。

---

## 7. 常见坑

- **HTTPS 证书要等**：DNS 生效后 GitHub 才签发 Let's Encrypt 证书，最长约 1 小时；期间 `Enforce HTTPS` 不可勾、浏览器可能告警，属正常。
- **子域名只留一条 CNAME**：多余的 A/AAAA/ANAME 会阻止证书签发。
- **CAA 记录**：若 `ttzg.site` 设过 CAA，必须包含 `letsencrypt.org`，否则签不出证书；没设 CAA 则不受影响。
- **自定义域名全 GitHub 唯一占用**：一个域名只能被一个仓库声明；做了 4.3 的域名验证可防被抢。
- **`.nojekyll`**：Material 产物用 `assets/` 目录（无下划线），通常不需要；workflow 仍 `touch` 一个，零成本防坑。
- **两次 build 不互相覆盖**：`mkdocs build` 的 `--clean` 只清自己的 `site_dir`（`_site/guide` 或 `_site/survey`），CNAME / index.html / .nojekyll 在两次 build 之后再写入 `_site` 根目录。

---

## 8. 新增一个学科的 checklist

1. 用本仓库做模板，新建仓库 `<slug>`（如 `dl`、`stat`）。
2. 改两套 `mkdocs.*.yml` 的 `site_name` / `site_url`（`https://<slug>.ebook.ttzg.site/guide|survey/`）。
3. 改 `.github/workflows/deploy.yml` 里的 `_site/CNAME` 为 `<slug>.ebook.ttzg.site`。
4. 改 `home/index.html` 的文案与两张卡片链接。
5. DNS 加 `<slug>.ebook` CNAME → `w3903771.github.io`。
6. 仓库 Settings → Pages：Source=Actions，Custom domain 填 `<slug>.ebook.ttzg.site`。
7. 门户 `ebook` 仓库首页加一张该学科卡片。

---

## 9. 门户站 `ebook.ttzg.site`（可选）

门户是一个独立小仓库，首页列出所有学科卡片，每张卡片链到对应 `<slug>.ebook.ttzg.site`。最简做法：把本项目 `home/index.html` 改成「学科列表」版即可，部署方式与上文相同（Source=Actions 或直接放一个 `index.html` 从分支部署）。学科还少时也可以先不做门户，直接用各学科子域名。
