#<ETS2DLCManager>
#Copyright (C) Gavin
#Email:gavintwt@gmail
#Discord:gavin.g
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.


from cmath import e
import sys
import logging
import urllib.request
import json
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk

class DLCManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ETS2 DLC 管理器")

        # 默认 DLC 文件夹路径
        self.default_dlc_folder_path = self.find_ets2_folder()
        self.dlc_folder_path = tk.StringVar(value=self.default_dlc_folder_path)

        # 默认目标文件夹路径
        self.default_target_folder_path = r"C:\ETS2DLC"
        self.target_folder_path = tk.StringVar(value=self.default_target_folder_path)

        # 备份 DLC 文件夹路径
        self.backup_dlc_folder_path = r"C:\ETS2DLC2"

        # 进度条变量
        self.progress_var = tk.DoubleVar()
        self.progress_var.set(0.0)

        # 创建 UI 元素
        self.create_widgets()

        # 应用主题化的样式
        self.apply_theme()

        # 打开软件时清空 C:\ETS2DLC 文件夹中的所有文件
        #self.clear_target_folder()

        # 打开软件时创建备份 DLC 文件夹和默认目标文件夹
        self.create_backup_and_default_folders()

    def create_widgets(self):

        # 创建一个ttk.Style对象
        style = ThemedStyle(self.master)

        # 设置按钮样式
        style.configure('TButton', padding=10, font=('Helvetica', 12))

        tk.Label(self.master, text="DLC文件夹路径:").pack(pady=10)
        ttk.Label(self.master, textvariable=self.dlc_folder_path).pack(pady=5)  # 使用ttk.Label

        tk.Label(self.master, text="目标文件夹路径:").pack(pady=10)
        ttk.Label(self.master, textvariable=self.target_folder_path).pack(pady=5)  # 使用ttk.Label

        # 使用 ThemedStyle 设置按钮样式
        ttk.Button(self.master, text="一键禁用DLC", command=self.move_dlc, style='TButton').pack(pady=10)
        ttk.Button(self.master, text="一键启用DLC", command=self.restore_dlc, style='TButton').pack(pady=10)

        tk.Label(self.master, text="版本:V0.0.1\n欢迎使用ETS2 DLC 管理器\n由果果开发/维护", fg="red").pack(side="bottom")

        # 进度条
        self.progress_bar = ttk.Progressbar(self.master, variable=self.progress_var, length=300, mode="determinate")
        self.progress_bar.pack(pady=10)
    
    def apply_theme(self):
        style = ttk.Style(self.master)
        style.theme_use("yaru")  # 选择你想要的主题  

    def browse_dlc_folder(self):
        dlc_folder_path = filedialog.askdirectory(title="选择 DLC 文件夹")
        self.dlc_folder_path.set(dlc_folder_path)

    def move_dlc(self):
        source_ets2_folder = self.find_ets2_folder()
        target_dlc_folder = self.target_folder_path.get()


        specific_dlc_files = [
            "dlc_it.scs",
            "dlc_north.scs",
            "dlc_east.scs",
            "dlc_balt.scs",
            "dlc_fr.scs",
            "dlc_balkan_e.scs",
            "dlc_balkan_w.scs",  
            "dlc_iberia.scs",
            "dlc_heavy_cargo.scs",
            "dlc_schwarzmuller.scs",
            "dlc_krone.scs",
            "dlc_feldbinder.scs",
            "dlc_wielton.scs",
            "dlc_tirsan.scs",
            "dlc_volvo_construction.scs"
        ]

        self.move_dlc_to_folder(source_ets2_folder, target_dlc_folder, specific_dlc_files)

    def restore_dlc(self):
        source_dlc_folder = r"C:\ETS2DLC"
        target_folder_path = self.dlc_folder_path.get()

        print(f"Source DLC Folder: {source_dlc_folder}")
        print(f"Target Folder Path: {target_folder_path}")

        error_message = None

        try:
            if not os.path.exists(target_folder_path):
                raise FileNotFoundError(f"目标文件夹 '{target_folder_path}' 不存在。")

            # 执行还原操作
            self.restore_dlc_files(source_dlc_folder, target_folder_path)
        except Exception as e:
            error_message = f"还原 DLC 时发生错误: {e}"
            print(error_message)
            self.show_error_message(error_message)

    def show_error_message(self, message):
        messagebox.showerror("错误", message)

    def move_dlc_to_folder(self, source_folder, target_folder, files_to_move):
        try:
            if not os.path.exists(source_folder):
                messagebox.showerror("错误", f"源文件夹 '{source_folder}' 不存在。")
                return

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            total_files = len(files_to_move)
            progress_step = 100 / total_files
            current_progress = 0

            for file_name in files_to_move:
                source_file_path = os.path.join(source_folder, file_name)
                target_file_path = os.path.join(target_folder, file_name)

                if os.path.exists(source_file_path):
                    shutil.move(source_file_path, target_file_path)

                current_progress += progress_step
                self.progress_var.set(current_progress)
                self.master.update_idletasks()

            messagebox.showinfo("完成", "DLC 操作已成功完成。")

        except Exception as e:
            messagebox.showerror("错误", f"处理 DLC 时发生错误: {str(e)}")

    def restore_dlc_files(self, source_dlc_folder, target_folder_path):
        try:
            if not os.path.exists(source_dlc_folder):
                messagebox.showerror("错误", f"DLC 文件夹 '{source_dlc_folder}' 不存在。")
                return

            total_files = len(os.listdir(source_dlc_folder))
            progress_step = 100 / total_files
            current_progress = 0

            for file_name in os.listdir(source_dlc_folder):
                file_path = os.path.join(source_dlc_folder, file_name)
                target_file_path = os.path.join(target_folder_path, file_name)

                if os.path.exists(file_path):
                    shutil.copy2(file_path, target_file_path)
                    # 不再删除源文件，因为这是备份操作
                    # os.remove(file_path)

                current_progress += progress_step
                self.progress_var.set(current_progress)
                self.master.update_idletasks()

            messagebox.showinfo("完成", "DLC 操作已成功完成。")

        except Exception as e:
            messagebox.showerror("错误", f"处理 DLC 时发生错误: {str(e)}")

    def change_default_path(self):
        new_default_path = filedialog.askdirectory(title="选择新的默认路径")
        if new_default_path:
            self.default_target_folder_path = new_default_path
            self.target_folder_path.set(new_default_path)

    def create_backup_and_default_folders(self):
        try:
            # 如果备份文件夹不存在，则创建它
            if not os.path.exists(self.backup_dlc_folder_path):
                os.makedirs(self.backup_dlc_folder_path)
                messagebox.showinfo("完成", f"备份 DLC 文件夹 '{self.backup_dlc_folder_path}' 已创建。")
                
                # 在第一次启动时，将特定 DLC 复制到备份文件夹
                self.copy_specific_dlc_to_backup()
            
            # 如果默认目标文件夹不存在，则创建它
            if not os.path.exists(self.default_target_folder_path):
                os.makedirs(self.default_target_folder_path)
                messagebox.showinfo("完成", f"目标文件夹 '{self.default_target_folder_path}' 已创建。")
        except Exception as e:
            messagebox.showerror("错误", f"创建备份和默认目标文件夹时发生错误: {str(e)}")

    def copy_specific_dlc_to_backup(self):
        source_ets2_folder = self.find_ets2_folder()
        backup_dlc_folder = self.backup_dlc_folder_path

        specific_dlc_files = [
            "dlc_it.scs",
            "dlc_north.scs",
            "dlc_east.scs",
            "dlc_balt.scs",
            "dlc_fr.scs",
            "dlc_balkan_e.scs",
            "dlc_balkan_w.scs",  
            "dlc_iberia.scs",
            "dlc_heavy_cargo.scs",
            "dlc_schwarzmuller.scs",
            "dlc_krone.scs",
            "dlc_feldbinder.scs",
            "dlc_wielton.scs",
            "dlc_tirsan.scs",
            "dlc_volvo_construction.scs"
        ]

        self.copy_dlc_to_folder(source_ets2_folder, backup_dlc_folder, specific_dlc_files)

    def copy_dlc_to_folder(self, source_folder, target_folder, files_to_copy):
        try:
            if not os.path.exists(source_folder):
                messagebox.showerror("错误", f"源文件夹 '{source_folder}' 不存在。")
                return

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            total_files = len(files_to_copy)
            progress_step = 100 / total_files
            current_progress = 0

            for file_name in files_to_copy:
                source_file_path = os.path.join(source_folder, file_name)
                target_file_path = os.path.join(target_folder, file_name)

                if os.path.exists(source_file_path):
                    shutil.copy2(source_file_path, target_file_path)

                current_progress += progress_step
                self.progress_var.set(current_progress)
                self.master.update_idletasks()

            messagebox.showinfo("完成", "DLC 备份操作已成功完成。")

        except Exception as e:
            messagebox.showerror("错误", f"处理 DLC 备份时发生错误: {str(e)}")

    def clear_target_folder(self):
        # 清空目标文件夹中的所有文件
        target_folder_path = self.default_target_folder_path

        if os.path.exists(target_folder_path):
            for file_name in os.listdir(target_folder_path):
                file_path = os.path.join(target_folder_path, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"清空目标文件夹时发生错误: {e}")

    def run(self):
        # 运行主循环
        self.master.mainloop()

    def find_ets2_folder(self):
        # 在所有盘符中查找 ETS2 文件夹
        possible_paths = [
            r"Steam\steamapps\common\Euro Truck Simulator 2",
            r"SteamLibrary\steamapps\common\Euro Truck Simulator 2",
            r"steamapps\common\Euro Truck Simulator 2",
            r"common\Euro Truck Simulator 2",
            r"Program Files\Steam\steamapps\common\Euro Truck Simulator 2",
            r"Program Files\SteamLibrary\steamapps\common\Euro Truck Simulator 2",
            r"Program Files\steamapps\common\Euro Truck Simulator 2",
            r"Program Files\common\Euro Truck Simulator 2",
            r"Program Files (x86)\Steam\steamapps\common\Euro Truck Simulator 2",
            r"Program Files (x86)SteamLibrary\steamapps\common\Euro Truck Simulator 2",
            r"Program Files (x86)\steamapps\common\Euro Truck Simulator 2",
            r"Program Files (x86)\common\Euro Truck Simulator 2"
        ]

        for drive in range(ord('A'), ord('Z') + 1):
            drive = chr(drive)
            for path in possible_paths:
                ets2_folder_path = os.path.join(drive + ":", path)
                if os.path.exists(ets2_folder_path):
                    return ets2_folder_path
        return "未找到 ETS2 文件夹"


def run_application():
    root = tk.Tk()
    app = DLCManagerApp(root)
    app.run()


run_application()
