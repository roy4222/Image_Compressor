import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
from tqdm import tqdm
import threading
from pathlib import Path
import logging

class ImageCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("圖片壓縮工具")
        self.root.geometry("800x600")  # 調整視窗大小
        
        # 設置樣式
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)
        
        # 創建主框架並添加padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置grid的權重，使其可以自適應縮放
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # 輸入資料夾選擇
        ttk.Label(main_frame, text="輸入資料夾:").grid(row=0, column=0, sticky=tk.W)
        self.input_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="瀏覽", command=self.select_input_folder).grid(row=0, column=2)
        
        # 輸出資料夾選擇
        ttk.Label(main_frame, text="輸出資料夾:").grid(row=1, column=0, sticky=tk.W)
        self.output_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="瀏覽", command=self.select_output_folder).grid(row=1, column=2)
        
        # 圖片品質設置
        ttk.Label(main_frame, text="壓縮品質 (1-100):").grid(row=2, column=0, sticky=tk.W)
        self.quality = tk.IntVar(value=80)
        quality_scale = ttk.Scale(main_frame, from_=1, to=100, variable=self.quality, orient=tk.HORIZONTAL)
        quality_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Label(main_frame, textvariable=self.quality).grid(row=2, column=2)
        
        # 最大寬度設置
        ttk.Label(main_frame, text="最大寬度 (像素):").grid(row=3, column=0, sticky=tk.W)
        self.max_width = tk.IntVar(value=1920)
        ttk.Entry(main_frame, textvariable=self.max_width, width=10).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # 輸出格式選擇
        ttk.Label(main_frame, text="輸出格式:").grid(row=4, column=0, sticky=tk.W)
        self.output_format = tk.StringVar(value="webp")
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=4, column=1, sticky=tk.W)
        ttk.Radiobutton(format_frame, text="WebP", variable=self.output_format, value="webp").grid(row=0, column=0)
        ttk.Radiobutton(format_frame, text="JPEG", variable=self.output_format, value="jpeg").grid(row=0, column=1)
        ttk.Radiobutton(format_frame, text="PNG", variable=self.output_format, value="png").grid(row=0, column=2)
        
        # 進度條
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)
        
        # 狀態標籤
        self.status_var = tk.StringVar(value="準備就緒")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=6, column=0, columnspan=3)
        
        # 開始按鈕
        self.start_button = ttk.Button(main_frame, text="開始壓縮", command=self.start_compression)
        self.start_button.grid(row=7, column=0, columnspan=3, pady=10)

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_path.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    def compress_image(self, input_path, output_path, quality, max_width, output_format):
        try:
            with Image.open(input_path) as img:
                # 轉換為RGB模式（如果是RGBA，則移除透明通道）
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # 調整圖片大小
                if img.size[0] > max_width:
                    ratio = max_width / img.size[0]
                    new_size = (max_width, int(img.size[1] * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)

                # 保存壓縮後的圖片
                img.save(output_path, format=output_format.upper(), quality=quality, optimize=True)
                return True
        except Exception as e:
            logging.error(f"處理圖片 {input_path} 時發生錯誤: {str(e)}")
            return False

    def start_compression(self):
        if not self.input_path.get() or not self.output_path.get():
            messagebox.showerror("錯誤", "請選擇輸入和輸出資料夾")
            return

        self.start_button.config(state='disabled')
        threading.Thread(target=self.compression_thread, daemon=True).start()

    def compression_thread(self):
        input_dir = self.input_path.get()
        output_dir = self.output_path.get()
        quality = self.quality.get()
        max_width = self.max_width.get()
        output_format = self.output_format.get()

        # 獲取所有圖片文件
        image_files = []
        for ext in ('*.jpg', '*.jpeg', '*.png', '*.webp'):
            image_files.extend(Path(input_dir).glob(ext))
            image_files.extend(Path(input_dir).glob(ext.upper()))

        total_files = len(image_files)
        if total_files == 0:
            self.status_var.set("未找到圖片文件")
            self.start_button.config(state='normal')
            return

        self.progress['maximum'] = total_files
        processed = 0
        success = 0

        for image_file in image_files:
            try:
                output_filename = f"{image_file.stem}.{output_format}"
                output_path = os.path.join(output_dir, output_filename)
                
                if self.compress_image(str(image_file), output_path, quality, max_width, output_format):
                    success += 1
                
                processed += 1
                self.progress['value'] = processed
                self.status_var.set(f"處理中... {processed}/{total_files}")
                self.root.update_idletasks()
            
            except Exception as e:
                logging.error(f"處理文件 {image_file} 時發生錯誤: {str(e)}")

        self.status_var.set(f"完成! 成功處理 {success}/{total_files} 個文件")
        self.start_button.config(state='normal')
        self.progress['value'] = 0
        
        messagebox.showinfo("完成", f"圖片壓縮完成!\n成功: {success}\n失敗: {total_files - success}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressor(root)
    root.mainloop()
