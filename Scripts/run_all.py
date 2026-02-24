import subprocess
import sys
from pathlib import Path

def main():
    script_dir = Path(__file__).resolve().parent
    script_singbox = script_dir / 'list2singbox.py'
    script_mihomo = script_dir / 'list2mihomo.py'

    print("🚀 开始执行转换任务...\n")

    print("================ 转换至 sing-box 格式 ================")
    subprocess.run([sys.executable, str(script_singbox)], check=True)

    print("\n================ 转换至 mihomo 格式 ================")
    subprocess.run([sys.executable, str(script_mihomo)], check=True)

    print("\n✅ 所有转换任务已完成！")

if __name__ == "__main__":
    main()
