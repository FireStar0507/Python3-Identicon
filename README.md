# Identicon Generator | 唯一性图标生成器
*by [FireStar0507](github.com/FireStar0507)*

**支持Python3.8+以上版本！**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Generate unique identicons from any string input!**  
**通过任意字符串生成独特的标识符图标！**

---

## 🌟 Features | 功能亮点

- **CLI Support** | **命令行支持**  
  Generate icons via simple commands with customizable size, path, and display options.  
  通过简单命令生成图标，支持自定义大小、保存路径和显示选项。

- **String-Driven** | **字符串驱动**  
  Use any string (emails, IDs, phrases) to generate stable unique icons.  
  支持任意字符串（邮箱、ID、短语）生成唯一性图标。

- **Colorful & Dynamic** | **多彩动态**  
  Auto-generate colors based on hash values.  
  基于哈希值自动生成颜色。

- **Lightweight** | **轻量化**  
  Pure Python with zero external dependencies except Pillow.  
  纯 Python 实现，除 Pillow 外无额外依赖。

---

## 🚀 Quick Start | 快速开始

### Installation | 安装依赖
```bash
pip install Pillow
```

### Basic Usage | 基础用法
```bash
# 生成图标并保存（默认路径为哈希值命名）
python identicon.py -c "hello@world.com"

# 生成图标并直接显示
python identicon.py -c "user123" -r

# 指定大小和保存路径
python identicon.py -c "admin" -s 64 -f ~/Downloads/admin_icon.png
```

---

## ⚙️ CLI Options | 命令行参数

| Option | 参数           | Description | 描述                  |
|--------|----------------|-------------|-----------------------|
| `-c`   | `--code`       | **Required** Input string/number | **必填** 输入字符串或数字 |
| `-s`   | `--size`       | Patch size (default: 24) | 块大小（默认24）      |
| `-f`   | `--file`       | Custom save path | 自定义保存路径        |
| `-r`   | `--show`       | Display image immediately | 直接显示图像          |
| `-n`   | `--no-save`    | Disable auto-saving | 禁止自动保存          |

---

## 🎨 Customization | 高级定制

### 1. Extend Renderers
```python
class CustomRenderer(DonRenderer):
    def decode(self, code):
        # Override color logic
        _, _, _, fore_color, back_color = super().decode(code)
        fore_color = (255, 0, 0)  # Force red foreground
        return middle, corner, side, fore_color, back_color

# Usage
img = render_identicon("test", 24, renderer=CustomRenderer)
```

### 2. Modify Path Shapes
Edit the `PATH_SET` in `DonRenderer` class to create new patterns.  
修改 `DonRenderer` 类中的 `PATH_SET` 来定义新形状。

---

## 🤝 Contributing | 贡献指南

1. Fork the repository.  
   点击 Fork 按钮创建分支。
2. Create a feature branch.  
   创建新分支开发功能：`git checkout -b feat/awesome`
3. Commit changes.  
   提交代码：`git commit -m 'Add awesome feature'`
4. Push to the branch.  
   推送到仓库：`git push origin feat/awesome`
5. Open a Pull Request.  
   提交 Pull Request。

---

## 📄 License | 许可证

MIT License | MIT 许可证  
Copyright (c) [FireStar0507]  
For details, see [LICENSE](LICENSE).


---

## 🖼️ Example | 示例

![Identicon Example1](image/91d18344e6a1592703700a67abb29c66f8b334badd0fcdad9e0e13bb82a37653.png)
![Identicon Example2](image/18885f27b5af9012df19e496460f9294d5ab76128824c6f993787004f6d9a7db.png)
![Identicon Example3](image/de32fcf24e63494b38c40a2cc5a175f837f55ab4ed6c04551e0361dd123ee679.png)
![Identicon Example4](image/f911e414cf6bdfc595532ab166b5ba0f63d73c021452fcdacbda363dda6ad8fb.png)
*示例图标（实际效果以生成为准）*

---

**Enjoy generating your unique identicons!** 🎨  
**尽情生成你的专属图标吧！** 🎨

