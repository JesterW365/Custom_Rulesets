# 读取 .\Custom_Rules\*.list
# 输出 .\Generated_Rules\mihomo\*.yaml
# 移除 空行、注释行(#、//开头)、仅包含空格的行
# 检查 行内不能有空格，如行中有空格，则移除改行并写入log日志中

# domain类型yaml格式：第一行为'payload: '，之后逐行添加list文件中的内容'  - {list文件中的内容}'

import logging
from datetime import datetime
from pathlib import Path

# ── 路径配置（相对于本脚本所在目录的上级，即项目根目录）──────────────────────
_ROOT = Path(__file__).resolve().parent.parent
_INPUT_DIR = _ROOT / "Custom_Rules"
_OUTPUT_DIR = _ROOT / "Generated_Rulesets" / "mihomo"
_LOG_FILE = Path(__file__).resolve().parent / "list2mihomo.log"

# ── 日志配置 ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    filename=_LOG_FILE,
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_logger = logging.getLogger(__name__)


def process_list_file(list_path: Path) -> None:
    """将单个 .list 文件转换为 mihomo 格式的 .yaml 文件。

    Args:
        list_path: 输入的 .list 文件路径。
    """
    valid_lines: list[str] = []
    skipped: list[tuple[int, str]] = []  # (行号, 原始内容)

    with list_path.open(encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.rstrip("\r\n")

            # 移除空行、仅含空格的行
            if not line.strip():
                continue

            # 移除注释行（# 或 // 开头）
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue

            # 检查行内是否含有空格（规则条目本身不应包含空格）
            if " " in stripped:
                skipped.append((lineno, line))
                continue

            valid_lines.append(stripped)

    # 将含空格的异常行写入 log
    if skipped:
        for lineno, content in skipped:
            _logger.warning(
                "[%s] 第 %d 行含有空格，已跳过：%s",
                list_path.name,
                lineno,
                content,
            )

    # 生成输出文件
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = _OUTPUT_DIR / f"{list_path.stem}.yaml"

    with out_path.open("w", encoding="utf-8") as f:
        f.write("payload:\n")
        for item in valid_lines:
            f.write(f"  - \"{item}\"\n")

    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] "
        f"{list_path.name} → {out_path.name}  "
        f"({len(valid_lines)} 条规则，跳过 {len(skipped)} 行)"
    )


def main() -> None:
    """入口：遍历 Custom_Rules 目录下所有 .list 文件并逐一转换。"""
    list_files = sorted(_INPUT_DIR.glob("*.list"))
    if not list_files:
        print(f"未在 {_INPUT_DIR} 中找到任何 .list 文件。")
        return

    for list_path in list_files:
        process_list_file(list_path)

    print("全部转换完成。")


if __name__ == "__main__":
    main()
