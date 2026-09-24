---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 550c777a310fec68d053917dc686d83d_15936f79b7eb11f1af5a525400ea19b7
    ReservedCode1: 8tQ4DARigLBOu68YtIh9YHKLB8GJ+9BHoa2BdxIj5KgWv/1mtai5/F0B52jGgbgLnUIwztnFXDIy/ot2z7IQkt0Lt/ffpdatxBDIgYCgFi3bevmLZjQc2avKEXo+JBKO5xlf3TTDREGOftSpxE7aAgiOo16HgPd4D6XyR9qGYgpFHG6D5+5/59zNyFU=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 550c777a310fec68d053917dc686d83d_15936f79b7eb11f1af5a525400ea19b7
    ReservedCode2: 8tQ4DARigLBOu68YtIh9YHKLB8GJ+9BHoa2BdxIj5KgWv/1mtai5/F0B52jGgbgLnUIwztnFXDIy/ot2z7IQkt0Lt/ffpdatxBDIgYCgFi3bevmLZjQc2avKEXo+JBKO5xlf3TTDREGOftSpxE7aAgiOo16HgPd4D6XyR9qGYgpFHG6D5+5/59zNyFU=
---



# 安装说明（INSTALL）

本仓库有两种用法：**作为 Agent Skill 安装**，或**当命令行脚本直接用**。任选其一，也可两者都要。

---

## 一、作为 Agent Skill 安装

适用于支持 `SKILL.md` 规范的 Agent（如 Marvis 自定义技能）。

### 1. 拿到文件

三选一：

- **网页下载**：打开仓库页面 → 绿色 `Code` 按钮 → `Download ZIP`；
- **命令行**：`git clone https://github.com/yechuyi0122-jpg/pdf-nup.git`
- **让 Agent 自己装**：把下面这句话复制给 Agent（需先给它仓库地址或本地包）：

  > 把 pdf-nup 技能装成自定义 skill，按仓库里的 INSTALL.md 落盘，装完重启。

### 2. 放到技能目录

Marvis 自定义技能目录（Windows）：

```
%APPDATA%\Tencent\Marvis\User\<你的用户ID>\skills\custom\pdf-nup\
```

最终目录结构必须是：

```
skills\custom\pdf-nup\
├── SKILL.md
├── meta.json
└── scripts\
    └── pdf_nup.py
```

> ⚠️ **目录名必须是 `pdf-nup`**。从 GitHub 下载的 ZIP 解压后目录名是 `pdf-nup-main`，**请先重命名**，否则技能不会被识别。

### 3. 装依赖

```bash
python -m pip install pymupdf
```

### 4. 重启 Marvis

自定义技能目录在启动时扫描，**必须重启**才会加载。

### 5. 验证

重启后对 Agent 说：

> 这份 PDF 做成 4-up 纵向并版并加页码

---

## 二、命令行直接使用

```bash
# 1) 取代码
git clone https://github.com/yechuyi0122-jpg/pdf-nup.git
cd pdf-nup

# 2) 装依赖
python -m pip install -r requirements.txt

# 3) 跑一下（先造个示例 PDF）
python examples/make_sample.py

# 4) 4-up 纵向 + 页码
python scripts/pdf_nup.py --input examples/sample-input.pdf --output examples/out/sample-4up.pdf --layout 4up --orientation portrait --page-badge
```

Windows 下若默认字体路径报错，加 `--badge-font` 指定字体：

```bash
python scripts/pdf_nup.py --input 源.pdf --output 出.pdf --layout 2up --page-badge --badge-font C:\Windows\Fonts\msyh.ttc
```

---

## 三、卸载

删除 `skills\custom\pdf-nup\` 整个目录（命令行方式则直接删掉 clone 下来的文件夹），重启 Agent 即可。
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
