import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_qemu_img_path():
    return resource_path(os.path.join("qemu", "qemu-img.exe"))

def convert_img(source_img, dest_img, format_type):
    qemu_img = get_qemu_img_path()
    cmd = [
        qemu_img,
        "convert",
        "-O", format_type,
        source_img,
        dest_img
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def log_message(msg):
    log_text.configure(state='normal')
    log_text.insert(tk.END, msg + '\n')
    log_text.see(tk.END)
    log_text.configure(state='disabled')

def run_conversion():
    file_path = filedialog.askopenfilename(
        title="选择 OpenWRT 的 .img 文件",
        filetypes=[("Image Files", "*.img")]
    )
    if not file_path:
        return

    format_key = format_var.get()
    format_type = format_key.split()[0]

    filename_base = os.path.basename(file_path).replace(".img", "")
    output_dir = os.path.join(os.getcwd(), "convert")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{filename_base}.{format_type}")

    log_message(f"开始转换: {file_path}")
    log_message(f"目标格式: {format_type}")
    log_message("转换中，请稍候...")

    result = convert_img(file_path, output_file, format_type)

    if result.returncode == 0:
        log_message(f"✅ 转换成功: {output_file}")
        messagebox.showinfo("完成", f"转换成功，文件保存到:\n{output_file}")
    else:
        log_message("❌ 转换失败")
        log_message(result.stderr)
        messagebox.showerror("错误", "转换失败，请查看日志。")

def center_window(win, width=520, height=350):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
root.title("OpenWRT 镜像格式转换工具")

center_window(root)

root.resizable(False, False)

style = ttk.Style(root)
style.theme_use('clam')

main_frame = ttk.Frame(root, padding=15)
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(main_frame, text="OpenWRT 镜像格式转换", font=("Segoe UI", 16, "bold"))
title_label.pack(pady=(0, 15))

format_var = tk.StringVar()
format_var.set("qcow2 (QEMU/KVM)")

format_options = [
    "qcow2 (QEMU/KVM)",
    "raw (嵌入式设备等通用)",
    "vmdk (VMware)",
    "vdi (VirtualBox)",
    "vhdx (Hyper-V)"
]

format_label = ttk.Label(main_frame, text="选择目标格式：", font=("Segoe UI", 11))
format_label.pack(anchor=tk.W)

format_menu = ttk.Combobox(main_frame, textvariable=format_var, values=format_options, state="readonly", font=("Segoe UI", 11))
format_menu.pack(fill=tk.X, pady=(0, 20))

convert_button = ttk.Button(main_frame, text="选择文件并转换", command=run_conversion)
convert_button.pack(fill=tk.X, pady=(0, 20))

log_label = ttk.Label(main_frame, text="转换日志：", font=("Segoe UI", 11))
log_label.pack(anchor=tk.W)

log_text = tk.Text(main_frame, height=8, state='disabled', font=("Consolas", 10), bg="#f5f5f5")
log_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()
