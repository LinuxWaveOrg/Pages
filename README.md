# LinuxWave
MacWave for Linux.

> **Site notice**: the official website has moved to **[linuxwave.org](https://linuxwave.org)** (previously `linuxwave.macwave.org`).

## TODO

- 安装命令将来改用 Release 资产（**先记录，暂不改**）：
  `https://github.com/LinuxWaveOrg/LinuxWave/releases/latest/download/install.sh`
  比现在的 `raw.githubusercontent.com/.../HEAD/lib/install.sh` 稳定 —— 前者按版本冻结，
  后者会跟着开发分支走。

- `foreword/` 下的两个 HTML 是**生成产物**：源文件在 LinuxWave 仓库的
  `Foreword/Foreword-zh.md` 与 `Foreword/Foreword-en.md`，改内容请改那边再重新生成
  （本站没有 Jekyll，`.md` 会以纯文本返回，所以这里存的是 HTML）。重新生成：

  ```bash
  python3 scripts/build_foreword.py ../LinuxWave/Foreword/Foreword-zh.md \
      foreword/foreword-zh.html zh "MacWave / LinuxWave 使用手册" "返回 LinuxWave 首页"
  python3 scripts/build_foreword.py ../LinuxWave/Foreword/Foreword-en.md \
      foreword/foreword.html en "MacWave / LinuxWave Handbook" "Back to LinuxWave"
  ```
