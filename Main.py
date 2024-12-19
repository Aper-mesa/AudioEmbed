import os
import tkinter as tk
from tkinter import filedialog, messagebox

def embed_image_in_audio(audio_file, image_file):
    """
    将图片嵌入到音频文件中，并生成嵌入后的文件
    """
    output_file = os.path.join(os.path.dirname(audio_file), "embedded.mp3")
    try:
        with open(audio_file, "rb") as audio, open(image_file, "rb") as image:
            with open(output_file, "wb") as output:
                output.write(audio.read())  # 写入音频数据
                output.write(image.read())  # 写入图片数据
        messagebox.showinfo("完成", f"图片已嵌入！文件保存为：{output_file}")
    except Exception as e:
        messagebox.showerror("错误", f"嵌入失败：{str(e)}")

def extract_image_from_file(input_file):
    """
    从伪装文件中提取图片，并生成图片文件
    """
    output_image_file = os.path.join(os.path.dirname(input_file), "extracted_image.jpg")
    try:
        with open(input_file, "rb") as file:
            data = file.read()

        # 搜索 JPG 文件头
        jpg_start = data.find(b'\xFF\xD8\xFF')  # JPG 的文件头
        if jpg_start == -1:
            messagebox.showerror("错误", "未找到 JPG 文件头，文件可能不包含图片。")
            return

        # 提取图片数据
        with open(output_image_file, "wb") as image_file:
            image_file.write(data[jpg_start:])  # 保存从图片头开始的所有数据

        messagebox.showinfo("完成", f"图片已提取！文件保存为：{output_image_file}")
    except Exception as e:
        messagebox.showerror("错误", f"提取失败：{str(e)}")

def embed_action():
    """选择音频和图片文件并嵌入图片"""
    audio_file = filedialog.askopenfilename(title="选择音频文件", filetypes=[("音频文件", "*.mp3")])
    if not audio_file:
        return

    image_file = filedialog.askopenfilename(title="选择图片文件", filetypes=[("图片文件", "*.jpg;*.jpeg;*.png")])
    if not image_file:
        return

    embed_image_in_audio(audio_file, image_file)

def extract_action():
    """选择伪装文件并提取图片"""
    input_file = filedialog.askopenfilename(title="选择伪装文件", filetypes=[("音频文件", "*.mp3")])
    if not input_file:
        return

    extract_image_from_file(input_file)

# 创建主界面
root = tk.Tk()
root.title("音频图片嵌入与提取工具")
root.geometry("400x200")

# 嵌入按钮
embed_button = tk.Button(root, text="嵌入图片到音频", command=embed_action, height=2, width=20)
embed_button.pack(pady=20)

# 提取按钮
extract_button = tk.Button(root, text="提取图片从音频", command=extract_action, height=2, width=20)
extract_button.pack(pady=20)

# 运行主循环
root.mainloop()
