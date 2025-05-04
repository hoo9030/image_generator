# git_sync.py — Git 자동 커밋 및 푸시
import subprocess

def push_changes():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "auto: upload new image and metadata"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("[Git] 변경 사항 푸시 완료")
    except subprocess.CalledProcessError as e:
        print(f"[Git] 오류 발생: {e}")
