import tkinter as tk
import random
import time
import threading

# 状態管理用グローバル変数
popup_enabled = True
popup_showing = False  # 現在ポップアップが表示中かどうか

start_time = time.time()  # アプリ起動時刻（秒）

def toggle_popup():
    global popup_enabled
    popup_enabled = not popup_enabled
    status_label.config(text=f"ポップアップ表示: {'ON' if popup_enabled else 'OFF'}")
    toggle_btn.config(text="OFFにする" if popup_enabled else "ONにする")

def stop_app():
    root.destroy()  # アプリケーションを完全に終了

def show_popup():
    global popup_showing
    if not popup_enabled or popup_showing:
        return

    popup_showing = True  # 表示中フラグON
    popup = tk.Toplevel()
    popup.title("作業に戻りたいですか？")
    popup.geometry("400x200")
    popup.configure(bg='white')
    

    msg = tk.Label(popup, text="作業に戻りたいですか？", font=("Notosansjp", 18), bg='white')
    msg.pack(pady=10)
# 経過時間の計算（秒 → 分秒）
    elapsed = int(time.time() - start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    timer_text = f"起動してから {minutes}分 {seconds}秒 経過"

    timer_label = tk.Label(popup, text=timer_text, font=("Notosansjp", 14), bg='white')
    timer_label.pack(pady=10)


    def on_click():
        global popup_showing
        popup_showing = False
        popup.destroy()

    btn = tk.Button(popup, text="Yes", font=("Notosansjp", 12), bg="#00bfff", fg="white", command=on_click)
    btn.pack(pady=10)

    # ポップアップを閉じたときもフラグを戻す
    popup.protocol("WM_DELETE_WINDOW", lambda: (popup.destroy(), set_popup_closed()))

def set_popup_closed():
    global popup_showing
    popup_showing = False

def run_timer():
    while True:
        wait_time = random.randint(10, 30)
        time.sleep(wait_time)
        root.after(0, show_popup)  # UIスレッドでポップアップ表示

# メイン設定ウィンドウ
root = tk.Tk()
root.title("ポップアップ制御アプリ")
root.geometry("300x180")

status_label = tk.Label(root, text="ポップアップ表示: ON", font=("Helvetica", 12))
status_label.pack(pady=10)

toggle_btn = tk.Button(root, text="OFFにする", font=("Helvetica", 12), command=toggle_popup)
toggle_btn.pack(pady=5)

exit_btn = tk.Button(root, text="アプリを終了", font=("Helvetica", 12), command=stop_app, fg="red")
exit_btn.pack(pady=15)

# バックグラウンドスレッドでタイマー起動
threading.Thread(target=run_timer, daemon=True).start()

root.mainloop()
