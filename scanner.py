#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import platform
import socket
import threading
import time

# ضبط الترميز التلقائي لويندوز
if platform.system() == "Windows":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        os.system("chcp 65001 >nul")
    except Exception:
        pass

def launch_gui_interface():
    try:
        import customtkinter as ctk
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        root = ctk.CTk()
        root.geometry("720x530")
        root.title("FRNOKI Scanner - Cyber Dashboard v2.0")
        root.resizable(False, False)
        
        # إطار رئيسي
        main_frame = ctk.CTkFrame(root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # العنوان العلوي بالإنجليزية المنظمة
        title_label = ctk.CTkLabel(
            main_frame, 
            text="FRNOKI ADVANCED NETWORK SCANNER", 
            font=("Consolas", 18, "bold")
        )
        title_label.pack(pady=(0, 15))
        
        # إطار التحكم والإدخال
        control_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        control_frame.pack(fill="x", padx=0, pady=5)
        
        lbl_target = ctk.CTkLabel(control_frame, text="Target IP:", font=("Consolas", 13, "bold"))
        lbl_target.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        entry_target = ctk.CTkEntry(control_frame, width=300, height=38, placeholder_text="127.0.0.1", font=("Consolas", 13))
        entry_target.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        entry_target.insert(0, "127.0.0.1")
        
        btn_scan = ctk.CTkButton(
            control_frame, 
            text="Start Scan", 
            command=lambda: execute_gui_scan(),
            width=130,
            height=38,
            fg_color="#1f538d", 
            hover_color="#14375e",
            font=("Consolas", 13, "bold")
        )
        btn_scan.grid(row=0, column=2, padx=15, pady=15, sticky="e")
        control_frame.columnconfigure(1, weight=1)

        # شاشة المخرجات (Console Output)
        text_output = ctk.CTkTextbox(main_frame, width=670, height=290, font=("Consolas", 12))
        text_output.pack(pady=15, fill="both", expand=True)
        text_output.insert("0.0", "[*] System initialized successfully...\n[*] Ready to scan target ports.\n\n")
        
        def execute_gui_scan():
            target = entry_target.get().strip()
            if not target:
                target = "127.0.0.1"
            
            text_output.insert("end", f"[*] Starting port scan on target: {target}...\n")
            text_output.see("end")
            
            def background_scan():
                common_ports = [21, 22, 80, 443, 3306, 8080]
                found = []
                for p in common_ports:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.7)
                        if s.connect_ex((target, p)) == 0:
                            found.append(str(p))
                        s.close()
                    except:
                        pass
                
                if found:
                    result_str = f"[+] OPEN PORTS FOUND: {', '.join(found)}\n"
                else:
                    result_str = f"[-] No open ports detected on standard list.\n"
                
                text_output.insert("end", result_str + "----------------------------------------\n")
                text_output.see("end")
                
            threading.Thread(target=background_scan).start()

        root.mainloop()
        
    except Exception as err:
        print(f"[!] GUI Error: {err}")

if __name__ == "__main__":
    launch_gui_interface()