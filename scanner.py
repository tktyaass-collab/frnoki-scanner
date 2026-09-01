import sys
import io
import os
import socket
import threading
from datetime import datetime

# فرض ترميز UTF-8 لمنع ظهور علامات الاستفهام في ويندوز
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
except Exception:
    pass

# محاولة استيراد مكتبات الواجهة الرسومية وتعديل النصوص العربية
try:
    import customtkinter as ctk
    from arabic_reshaper import reshape
    from bidi.algorithm import get_display
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

def ar(text):
    """دالة لمعالجة النصوص العربية لتدعم العرض السليم"""
    try:
        reshaped_text = reshape(text)
        return get_display(reshaped_text)
    except Exception:
        return text

def print_banner():
    banner = r"""
███████╗██████╗ ███╗   ██╗ ██████╗ ██╗  ██╗██╗
██╔════╝██╔══██╗████╗  ██║██╔═══██╗██║ ██╔╝██║
█████╗  ██████╔╝██╔██╗ ██║██║   ██║█████╔╝ ██║
██╔══╝  ██╔══██╗██║╚██╗██║██║   ██║██╔═██╗ ██║
██║     ██║  ██║██║ ╚████║╚██████╔╝██║  ██╗██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝
    [ FRNOKI PROFESSIONAL NETWORK SCANNER ]
    """
    print(banner)
    print("=" * 60)
    print(ar("  مرحباً بك في أداة فحص الشبكات والمنافذ المطورة بواسطة فرنوكي"))
    print("=" * 60)

def scan_port(target_ip, port, results_list):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            results_list.append(port)
        s.close()
    except Exception:
        pass

def cli_scanner():
    print("\n" + "=" * 40)
    target = input(ar(" أدخل عنوان آي بي الهدف (Target IP) أو الموقع: ")).strip()
    if not target:
        print(ar("[-] لم يتم إدخال عنوان صحيح!"))
        return

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(ar("[-] عذراً، لم يتم العثور على النطاق المطلوب!"))
        return

    print(ar(f"\n[+] جاري بدء الفحص على الآي بي: {target_ip}"))
    print(ar("[+] يرجى الانتظار...\n"))

    open_ports = []
    threads = []
    
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080]
    
    for port in common_ports:
        t = threading.Thread(target=scan_port, args=(target_ip, port, open_ports))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("=" * 40)
    print(ar(" نتائج الفحص (Open Ports):"))
    print("=" * 40)
    if open_ports:
        for p in sorted(open_ports):
            print(ar(f" [✔] البورت مفتوح: {p}"))
    else:
        print(ar("[-] لم يتم العثور على منافذ مفتوحة في النطاق المحدد."))
    print("=" * 40)

def run_gui():
    if not GUI_AVAILABLE:
        print(ar("[-] مكتبات الواجهة الرسومية (customtkinter) غير مثبتة! يرجى تثبيتها أولاً."))
        return

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("FRNOKI Scanner")
    root.geometry("500x450")

    title_label = ctk.CTkLabel(root, text="FRNOKI Network Scanner", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    target_entry = ctk.CTkEntry(root, placeholder_text="أدخل الآي بي أو الرابط هنا...", width=350, height=40)
    target_entry.pack(pady=10)

    result_box = ctk.CTkTextbox(root, width=400, height=200)
    result_box.pack(pady=10)

    def start_gui_scan():
        target = target_entry.get().strip()
        result_box.delete("0.0", "end")
        if not target:
            result_box.insert("end", "الرجاء إدخال هدف صحيح!\n")
            return
        
        result_box.insert("end", f"جاري فحص: {target}...\n")
        
        def background_scan():
            try:
                ip = socket.gethostbyname(target)
                ports = [21, 22, 23, 25, 53, 80, 443, 3306, 3389]
                open_p = []
                for p in ports:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.4)
                    if s.connect_ex((ip, p)) == 0:
                        open_p.append(p)
                    s.close()
                
                result_box.insert("end", f"تم الانتهاء من الفحص للآي بي: {ip}\n")
                if open_p:
                    result_box.insert("end", f"المنافذ المفتوحة: {open_p}\n")
                else:
                    result_box.insert("end", "لا توجد منافذ شائعة مفتوحة.\n")
            except Exception as e:
                result_box.insert("end", f"حدث خطأ: {str(e)}\n")

        threading.Thread(target=background_scan).start()

    scan_btn = ctk.CTkButton(root, text="بدء الفحص", command=start_gui_scan, width=200, height=35)
    scan_btn.pack(pady=10)

    root.mainloop()

def show_help():
    print("\n" + "=" * 50)
    print(ar(" دليل الاستخدام وطريقة تشغيل الأداة (Guide):"))
    print("=" * 50)
    print(ar("1. تثبيت المتطلبات أول مرة:"))
    print("   pip install customtkinter arabic-reshaper python-bidi")
    print(ar("2. تشغيل الأداة من التيرمنال:"))
    print("   python scanner.py")
    print(ar("3. الخيارات المتاحة:"))
    print(ar("   - [1] تشغيل الواجهة الرسومية (GUI)"))
    print(ar("   - [2] تشغيل الفاحص السريع (CLI)"))
    print(ar("   - [3] عرض دليل المساعدة أو الخروج"))
    print("=" * 50)

def interactive_cli():
    print_banner()
    while True:
        print("\n" + ar("اختر وضع التشغيل:"))
        print(ar(" [1] فتح الواجهة الرسومية (GUI)"))
        print(ar(" [2] فحص الشبكة عبر الأوامر (CLI Scan)"))
        print(ar(" [3] عرض دليل المساعدة وتثبيت المتطلبات (Help)"))
        print(ar(" [4] خروج (Exit)"))
        
        choice = input(ar(" أدخل رقم الخيار [1-4]: ")).strip()
        
        if choice == "1":
            run_gui()
        elif choice == "2":
            cli_scanner()
        elif choice == "3":
            show_help()
        elif choice == "4":
            print(ar("شكراً لاستخدامك أداة فرنوكي. إلى اللقاء!"))
            break
        else:
            print(ar("[-] خيار غير صحيح، يرجى اختيار رقم من 1 إلى 4."))

if __name__ == "__main__":
    interactive_cli()