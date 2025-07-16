import tkinter as tk
from tkinter import filedialog, messagebox
import vlc
import subprocess
import sys

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("名前どうしよう,,,")
        self.root.geometry("800x600")

        # python-vlcのインストールチェック
        self.check_and_install_vlc()

        # VLCインスタンスとメディアプレーヤー
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # 動画表示用のフレーム
        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        # コントロールパネル
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X, pady=5)

        # ボタン
        tk.Button(self.control_frame, text="ファイルを開く", command=self.open_file).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="再生", command=self.play).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="一時停止", command=self.pause).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="停止", command=self.stop).pack(side=tk.LEFT, padx=5)

        # 音量スライダー
        self.volume_scale = tk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                   label="音量", command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack(side=tk.LEFT, padx=5)

        # 動画のキャンバス
        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def check_and_install_vlc(self):
        try:
            import vlc
        except ImportError:
            response = messagebox.askyesno("ライブラリ未インストール", 
                                         "python-vlcが見つかりません。インストールしますか？")
            if response:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-vlc"])
                    messagebox.showinfo("成功", "python-vlcをインストールしました。")
                except subprocess.CalledProcessError:
                    messagebox.showerror("エラー", "python-vlcのインストールに失敗しました。")
                    self.root.quit()
            else:
                messagebox.showerror("エラー", "python-vlcが必要です。プログラムを終了します。")
                self.root.quit()

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")]
        )
        if file_path:
            self.media = self.instance.media_new(file_path)
            self.player.set_media(self.media)
            self.player.set_hwnd(self.canvas.winfo_id())  # Windows用
            # Mac/Linuxの場合は以下をコメント解除
            # self.player.set_xwindow(self.canvas.winfo_id())

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_volume(self, val):
        self.player.audio_set_volume(int(val))

    def __del__(self):
        self.player.stop()
        self.instance.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()