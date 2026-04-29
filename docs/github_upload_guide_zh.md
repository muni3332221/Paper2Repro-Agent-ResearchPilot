# GitHub 上传指南

## 推荐方式：解压后用 Git 上传

不要直接把 zip 文件上传成仓库主体。GitHub 仓库应该展示项目里的源码文件、README、docs、tests 等内容，而不是只有一个压缩包。

### 1. 新建仓库

在 GitHub 点击 **New repository**，仓库名可以用：

```text
paper2repro-agent
```

建议勾选 Public。不要勾选自动生成 README，因为项目里已经有 README.md。

### 2. 本地解压项目

下载 zip 后解压，进入项目目录：

```bash
cd paper2repro-agent
```

### 3. 初始化 Git 并提交

```bash
git init
git add .
git commit -m "Initial commit: Paper2Repro Agent"
```

### 4. 绑定远程仓库

把下面的地址换成你自己的 GitHub 仓库地址：

```bash
git branch -M main
git remote add origin https://github.com/YOUR_NAME/paper2repro-agent.git
git push -u origin main
```

## 网页上传方式

也可以在 GitHub 仓库页面点击 **Add file → Upload files**，把解压后的所有文件和文件夹拖进去。不要只上传 zip 文件。

## 上传后建议检查

- README.md 是否自动显示在仓库首页。
- `src/`、`docs/`、`tests/` 是否都在仓库里。
- `.env` 不要上传，`.env.example` 可以上传。
- GitHub Actions 是否能运行测试。
