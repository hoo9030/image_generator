# image_watcher.py — WebUI 이미지 생성 감지 → 후처리 자동 실행
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from main_postprocess import postprocess_webui_image

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".png"):
            print(f"[감지] 새 이미지 생성됨: {event.src_path}")
            try:
                postprocess_webui_image()
            except Exception as e:
                print(f"[오류] 후처리 실패: {e}")

if __name__ == "__main__":
    watch_path = os.path.join("outputs", "txt2img-images")
    observer = Observer()
    observer.schedule(ImageHandler(), path=watch_path, recursive=True)
    observer.start()

    print(f"[실행 중] '{watch_path}' 폴더 감시 시작 (Ctrl+C로 종료)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
