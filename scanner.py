import sys
import socket
import threading
import customtkinter as ctk
import arabic_reshaper
from bidi.algorithm import get_display

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

def ar(text):
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text

def print_banner():
    print(r"""
███████╗██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗██╗
██╔════╝██╔══██╗████╗  ██║██╔═══██╗██║ ██╔╝██║
█████╗  ██████╔╝██╔██╗ ██║██║   ██║█████╔╝ ██║
██╔══╝  ██╔══██╗██║╚██╗██║██║   ██║██╔═██╗ ██║
██║     ██║  ██║██║ ╚████║╚██████╔╝██║  ██╗██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝
""")
    print("=" * 65)
    print(ar("             FRNOKI SCANNER - لوحة التحكم والإرشادات"))
    print("=" * 65)

def print_help():
    print_banner()
    print(ar(" [دليل الاستخدام والأوامر المتاحة في ويندوز]:"))
    print(ar("  1. تشغيل الواجهة الرسومية المباشرة:"))
    print("     python scanner.py")
    print(ar("  2. فتح دليل المساعدة مباشرة:"))
    print("     python scanner.py help")
    print(ar("  3. شرح طريقة الاستخدام:"))
    print(ar("     - قم بإدخال هدف الفحص (مثل 192.168.1.1 أو اسم الموقع)."))
    print(ar("     - اضغط زر 'بدء الفحص' أو مفتاح Enter."))
    print(ar("     - سيتم تفريغ خانة الإدخال تلقائياً وعرض حالة المنافذ."))
    print("=" * 65 + "\n")

def run_scanner(target_input, text_area):
    if not target_input:
        text_area.insert("end", ar("خطأ: يرجى إدخال الهدف أولاً!") + "\n")
        return
    
    text_area.delete("0.0", "end")
    text_area.insert("end", f"[*] {ar('جاري فحص الهدف')}: {target_input}...\n")
    print(f"[!] جاري فحص الهدف: {target_input}")
    
    try:
        target_ip = socket.gethostbyname(target_input)
    except socket.gaierror:
        text_area.insert("end", f"[-] {ar('خطأ: تعذر التعرف على العنوان.')}\n")
        print(f"[-] خطأ: تعذر التعرف على الهدف {target_input}")
        return

    text_area.insert("end", f"[+] Target IP: {target_ip}\n")
    text_area.insert("end", "=" * 65 + "\n")
    text_area.insert("end", f"{'PORT':<10} | {'SERVICE':<15} | {'STATE'}\n")
    text_area.insert("end", "=" * 65 + "\n")

    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS",
        445: "SMB", 3306: "MySQL", 8080: "HTTP-Proxy"
    }

    for port, service in common_ports.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            result = s.connect_ex((target_ip, port))
            s.close()
            
            if result == 0:
                text_area.insert("end", f"{port:<10} | {service:<15} | 🟢 {ar('مفتوح')}\n")
            else:
                text_area.insert("end", f"{port:<10} | {service:<15} | 🔴 {ar('مقفول')}\n")
        except Exception:
            pass

    text_area.insert("end", "=" * 65 + "\n")
    text_area.insert("end", f"[+] {ar('تم إتمام الفحص بنجاح بواسطة فرنوكي')}.\n")
    print(f"[+] تم إتمام الفحص بنجاح للهدف: {target_ip}\n")

def start_scan_thread(entry_widget, text_area):
    target = entry_widget.get().strip()
    if target:
        entry_widget.delete(0, "end")
    threading.Thread(target=run_scanner, args=(target, text_area), daemon=True).start()

class FrnokiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FRNOKI SCANNER")
        self.geometry("900x780")
        self.config(bg="#090a0f")

        ascii_title = (
            "███████╗██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗██╗\n"
            "██╔════╝██╔══██╗████╗  ██║██╔═══██╗██║ ██╔╝██║\n"
            "█████╗  ██████╔╝██╔██╗ ██║██║   ██║█████╔╝ ██║\n"
            "██╔══╝  ██╔══██╗██║╚██╗██║██║   ██║██╔═██╗ ██║\n"
            "██║     ██║  ██║██║ ╚████║╚██████╔╝██║  ██╗██║\n"
            "╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝"
        )

        self.title_label = ctk.CTkLabel(
            self, 
            text=ascii_title, 
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"), 
            text_color="#00ffcc",
            justify="center"
        )
        self.title_label.pack(pady=(20, 15))

        self.frame_top = ctk.CTkFrame(self, fg_color="#121624", corner_radius=15, border_color="#00ffcc", border_width=1)
        self.frame_top.pack(fill="x", padx=25, pady=10)

        label_text = ar("الهدف:")
        self.label_ip = ctk.CTkLabel(self.frame_top, text=label_text, font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
        self.label_ip.pack(side="right", padx=15, pady=15)

        self.entry_target = ctk.CTkEntry(
            self.frame_top, 
            placeholder_text="FRNOKI", 
            font=ctk.CTkFont(size=13), 
            width=350, 
            fg_color="#1a2035", 
            text_color="white", 
            border_color="#00ffcc",
            justify="right"
        )
        self.entry_target.pack(side="right", padx=10, pady=15)
        self.entry_target.bind("<Return>", lambda event: start_scan_thread(self.entry_target, self.text_output))

        btn_text = ar("بدء الفحص 🚀")
        self.btn_scan = ctk.CTkButton(
            self.frame_top, 
            text=btn_text, 
            font=ctk.CTkFont(size=13, weight="bold"), 
            fg_color="#00ffcc", 
            text_color="#090a0f", 
            hover_color="#00b38f", 
            command=lambda: start_scan_thread(self.entry_target, self.text_output)
        )
        self.btn_scan.pack(side="left", padx=15, pady=15)

        self.text_output = ctk.CTkTextbox(
            self, 
            font=ctk.CTkFont(family="Consolas", size=12), 
            fg_color="#0d1117", 
            text_color="#00ff66", 
            corner_radius=15, 
            border_color="#1f2937", 
            border_width=2
        )
        self.text_output.pack(fill="both", expand=True, padx=25, pady=15)

def interactive_cli():
    print_banner()
    print(ar(" اختر من القائمة:"))
    print(ar(" [1] تشغيل واجهة الأداة الرسومية (GUI)"))
    print(ar(" [2] عرض دليل المساعدة وطريقة الاستخدام (Help)"))
    print(ar(" [3] خروج"))
    
    choice = input(ar("\nادخل رقم الخيار [1-3]: ")).strip()
    
    if choice == "1":
        print(ar("[+] جاري إطلاق الواجهة الرسومية..."))
        app = FrnokiApp()
        app.mainloop()
    elif choice == "2" or choice.lower() == "help":
        print_help()
        input(ar("اضغط على مفتاح Enter للعودة أو إغلاق النافذة..."))
    else:
        print(ar("إلى اللقاء!"))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["help", "--help", "-h"]:
            print_help()
        else:
            app = FrnokiApp()
            app.mainloop()
    else:
        interactive_cli()