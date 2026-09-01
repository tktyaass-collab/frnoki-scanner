import os
import socket
import threading
import customtkinter as ctk

# Clean terminal encoding setup for the background terminal
if os.name == 'nt':
    os.system('chcp 65001 > nul')

def show_cli_banner():
    print("\n" + "="*50)
    print(" "*15 + "FRNOKI SCANNER")
    print("="*50)
    print("[+] Welcome to FRNOKI Network Scanner")
    print("[+] CLI initialized successfully")
    print("[+] Launching Arabic Graphical User Interface...")
    print("="*50 + "\n")

# GUI Theme Setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("أداة فحص الشبكة - FRNOKI")
        self.geometry("700x500")
        self.resizable(False, False)
        
        # العنوان الرئيسي
        self.title_label = ctk.CTkLabel(self, text="فاحص المنافذ والشبكات", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=15)
        
        # حقل إدخال الهدف (IP)
        self.target_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.target_frame.pack(pady=5, fill="x", padx=30)
        
        self.target_label = ctk.CTkLabel(self.target_frame, text=":عنوان الهدف (IP)", font=("Arial", 14))
        self.target_label.pack(side="right", padx=5)
        
        self.target_entry = ctk.CTkEntry(self.target_frame, width=350, justify="right", font=("Arial", 14))
        self.target_entry.pack(side="right", padx=5)
        self.target_entry.insert(0, "127.0.0.1")
        
        # زر بدء الفحص
        self.scan_btn = ctk.CTkButton(self, text="بدء الفحص", font=("Arial", 16, "bold"), fg_color="#2b9348", hover_color="#55a630", command=self.start_scan_thread)
        self.scan_btn.pack(pady=15)
        
        # صندوق عرض النتائج
        self.output_box = ctk.CTkTextbox(self, width=620, height=230, font=("Consolas", 12))
        self.output_box.pack(pady=5)
        self.output_box.insert("0.0", "جاهز لبدء عملية الفحص...\n")

    def log_message(self, message):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")

    def start_scan_thread(self):
        target = self.target_entry.get().strip()
        self.output_box.delete("0.0", "end")
        self.log_message(f"جاري فحص الهدف: {target} ...")
        
        threading.Thread(target=self.run_scan, args=(target,), daemon=True).start()

    def run_scan(self, target):
        ports = [21, 22, 23, 80, 443, 445, 3306, 8080]
        try:
            target_ip = socket.gethostbyname(target)
            for port in ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((target_ip, port))
                if result == 0:
                    self.log_message(f"[مفتوح] المنفذ {port}")
                else:
                    self.log_message(f"[مغلق] المنفذ {port}")
                s.close()
            self.log_message("\nتم الانتهاء من الفحص بنجاح.")
        except Exception as e:
            self.log_message(f"حدث خطأ: {e}")

if __name__ == "__main__":
    show_cli_banner()
    app = ScannerApp()
    app.mainloop()