import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment

def generate_empty_audio(output_file, file_name):
    """
    生成一个无声的短音频文件，包含标准 MP3 元数据
    """
    try:
        # 创建 1 秒无声音频
        silent_audio = AudioSegment.silent(duration=1000)  # 1000 毫秒 = 1 秒
        # 设置必要的 MP3 元数据
        silent_audio.export(output_file, format="mp3", tags={
            "title": file_name,
            "artist": "Apermesa",
            "album": "Half Life 3",
            "year": "2024"
        })
        return True
    except Exception as e:
        messagebox.showerror("错误", f"生成空音频失败：{str(e)}")
        return False

def embed_image_in_audio(image_file):
    """
    将图片嵌入到生成的无声音频文件中
    """
    file_name = os.path.splitext(os.path.basename(image_file))[0]
    output_audio_file = os.path.join(os.path.dirname(image_file), "temp_silent.mp3")
    if not generate_empty_audio(output_audio_file, file_name):
        return

    output_file = os.path.join(os.path.dirname(image_file), file_name + "(embedded).mp3")
    try:
        with open(output_audio_file, "rb") as audio, open(image_file, "rb") as image:
            with open(output_file, "wb") as output:
                output.write(audio.read())  # 写入音频数据
                output.write(image.read())  # 写入图片数据
        os.remove(output_audio_file)  # 删除临时音频文件
        messagebox.showinfo("完成", f"图片已嵌入！文件保存为：{output_file}")
    except Exception as e:
        messagebox.showerror("错误", f"嵌入失败：{str(e)}")

def extract_image_from_file(input_file):
    """
    从伪装文件中提取图片，并生成图片文件
    """
    try:
        with open(input_file, "rb") as file:
            data = file.read()

        # 检测图片格式
        formats = {
            b'\xFF\xD8\xFF': ".jpg",  # JPG 文件头
            b'\x89PNG': ".png"          # PNG 文件头
        }

        start_index = -1
        file_extension = None
        for header, ext in formats.items():
            index = data.find(header)
            if index != -1:
                start_index = index
                file_extension = ext
                break

        if start_index == -1:
            messagebox.showerror("错误", "未找到支持的图片文件头，文件可能不包含图片。")
            return

        # 提取图片数据
        embedded_file_name = os.path.splitext(os.path.basename(input_file))[0].replace("(embedded)", "")
        output_image_file = os.path.join(os.path.dirname(input_file), f"{embedded_file_name}{file_extension}")
        with open(output_image_file, "wb") as image_file:
            image_file.write(data[start_index:])  # 保存从图片头开始的所有数据

        messagebox.showinfo("完成", f"图片已提取！文件保存为：{output_image_file}")
    except Exception as e:
        messagebox.showerror("错误", f"提取失败：{str(e)}")

def embed_action():
    """选择图片文件并嵌入到生成的无声音频中"""
    image_file = filedialog.askopenfilename(title="选择图片文件", filetypes=[("图片文件", "*.jpg;*.jpeg;*.png")])
    if not image_file:
        return

    embed_image_in_audio(image_file)

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
