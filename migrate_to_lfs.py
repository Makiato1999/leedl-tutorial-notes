import os
import subprocess
import sys

def run(cmd):
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"命令失败: {cmd}")
        sys.exit(result.returncode)

def main():
    # 1. 检查 git-lfs 是否安装
    try:
        subprocess.run("git lfs version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("❌ 没有安装 git-lfs，请先在终端执行: brew install git-lfs")
        sys.exit(1)

    # 2. 初始化 git-lfs
    run("git lfs install")

    # 3. 跟踪图片文件
    run('git lfs track "*.png" "*.jpg" "*.jpeg" "*.gif" "*.webp"')

    # 4. 提交 .gitattributes
    run("git add .gitattributes")
    run('git commit -m "chore: track images with Git LFS" || true')

    # 5. 重写历史，把图片迁移到 LFS
    run('git lfs migrate import --include="*.png,*.jpg,*.jpeg,*.gif,*.webp"')

    # 6. 本地清理
    run("git gc --prune=now --aggressive")
    run("git count-objects -vH")

    # 7. 推送
    run("git push origin --force-with-lease --all")
    run("git push origin --force-with-lease --tags")

if __name__ == "__main__":
    main()
