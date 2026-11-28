> **🌊 迁移提示：LinuxWave 已并入 Summerwave。官网 <https://linuxwave.org> 已 301 跳转到 <https://summerwave.org/>；本仓库已归档，开发转到 <https://github.com/SummerwaveOrg/Summerwave>。**
> **🌊 Migration notice: LinuxWave has merged into Summerwave. The site <https://linuxwave.org> now 301-redirects to <https://summerwave.org/>. This repository is archived — development continues at <https://github.com/SummerwaveOrg/Summerwave>.**
>
> # 🚚 This repository is archived — LinuxWave is now part of **Summerwave**
>
> **New home: <https://github.com/SummerwaveOrg/Summerwave>**
> **Website: <https://summerwave.org/>** (`linuxwave.org` 301 → here)
>
> - **Existing installs keep working.** `wave`, `wave install` and `wave selfupdate` are
>   unaffected — you do not need to do anything, and this repository stays readable and its
>   releases stay downloadable.
> - **New installs, issues and pull requests go to the new repository.** This one is read-only:
>   no pushes, no issues, no pull requests.
> - Summerwave merges MacWave and LinuxWave into one codebase, one release line and one data
>   layout. LinuxWave's 4.x line ends at 4.6.x; security fixes, if any are ever needed, would be
>   cut here after a temporary unarchive.

---

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
