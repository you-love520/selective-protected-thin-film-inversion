# 用于薄膜厚度反演的选择性受保护精修（Selective Protected Refinement）

本仓库包含核心算法实现、冻结的配置、与稿件一致的汇总表格，以及支持 Stage33 / 最终 A+B 版本方法的验证脚本。

## 与稿件结果的对应信息

- 开发随机种子：`20260426`
- 独立验证随机种子：`20260508`
- 独立验证设计：`3 种材料 x 3 个厚度 x 4 种污染场景 x 200 个观测 = 7200 个观测`
- 鲁棒锚点：E3 鲁棒多盆地（multibasin）轮廓
- 最终方法：选择性受保护精修（reported as Final A+B）
- 自适应保护：`eta2 = C2`
- B 路由阈值：最大相对盆地间隙（relative basin gap）为 `5.0`；最小局部可辨识性得分（local-identifiability score）为 `0.82`

## 主要验证结果（摘要）

| 指标 | 数值 |
|---|---:|
| E3 平均绝对误差 | 0.223465 nm |
| Final A+B 平均绝对误差 | 0.194634 nm |
| 仅 A 的接受精修次数 | 2976 |
| 仅 A 的改进 / 受损 | 2053 / 923 |
| Final A+B 的接受精修次数 | 2410 |
| Final A+B 的改进 / 受损 | 1915 / 495 |
| 精确 E3 回退次数 | 4790 |
| 平均 Final A+B 减 E3 | -0.028831 nm |
| 平均 Final A+B 减 A-only | -0.021967 nm |

## 仓库结构

```text
src/stage33_anchor/     鲁棒锚点和前向模型源模块
src/final_ab/           选择性受保护精修源模块
configs/                冻结的 Final A+B 参数和路由阈值
data/optical_constants/ 材料 B 和 C 使用的冻结光学常数表
tables/                 稿件表格的源 CSV 文件
figures/                生成的图形
analysis/               验证、表格构建、图形构建和阈值选择脚本
environment/            Python 依赖锁定文件
provenance/             校验和清单
```

## 软件环境与依赖

该实现针对 Python 3.12 准备。公开包指定了七个直接的 Python 依赖，用于数值优化、结构化数据处理、运行时监控和可视化。

### 直接依赖

| 包 | 版本 | 在计算流程中的作用 |
|---|---:|---|
| NumPy | 2.5.1 | 数组运算、数值线性代数、光谱处理和有种子随机数生成 |
| SciPy | 1.18.0 | 有界优化、标量最小化、线性最小二乘和高斯光谱响应滤波 |
| pandas | 2.2.2 | 表格结果处理与基于 CSV 的分析 |
| Matplotlib | 3.9.1 | 科学绘图与矢量/光栅图导出 |
| PyArrow | 17.0.0 | 列式数据交换与 Parquet 兼容的数据处理 |
| psutil | 7.2.2 | 运行时与系统资源监控 |
| Polars | 1.42.1 | 高效处理较大结构化结果表格 |

核心光学模型、鲁棒多盆地锚点和受保护精修实现主要依赖于 NumPy 与 SciPy。其余包用于结果表格处理、运行时分析、列式数据操作和科学可视化。

### 安装

在安装依赖前请先创建隔离的 Python 环境。

在 Windows PowerShell 下：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

在 Linux 或 macOS 下：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

固定版本依赖列表在以下位置提供：

```text
requirements.txt
environment/requirements-lock.txt
```

在复现实验报告的软件环境时，建议使用固定版本。


## 阈值选择复现实验

运行：

```bash
python analysis/select_b_thresholds.py --input configs/THRESHOLD_SELECTION_INPUT.json --output analysis/THRESHOLD_SELECTION_REPRODUCED_CHECK.json
```

该命令复现了来自开发网格的确定性 B 路由阈值选择。

## 许可证

本仓库原创源代码和文档采用 MIT License 发布，详见 `LICENSE`。

仓库中使用的第三方光学性质数据和已发表色散参数保留其原始来源、
署名和适用条款，详见 `THIRD_PARTY_NOTICES.md`。

## 引用

本软件版本的引用信息见 `CITATION.cff`。

## 第三方数据与来源

前向模型使用的部分光学性质数据来源于 KLA/Filmetrics 数据库记录以及
Zenodo 数据集 `10.5281/zenodo.15055400`。详细来源与署名信息见
`THIRD_PARTY_NOTICES.md`。