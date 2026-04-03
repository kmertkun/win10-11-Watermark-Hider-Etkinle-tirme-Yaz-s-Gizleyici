"""
Windows 10/11 Watermark Hider / Etkinleştirme Yazısı Gizleyici
--------------------------------------------------------------
Author: zPeaw (Main: https://github.com/zPeaw)
        kmertkun (New Active: https://github.com/kmertkun)

A standalone Python GUI tool to hide the "Activate Windows" watermark 
by securely disabling the 'svsvc' registry service.

Features:
- Auto UAC Administrator Elevation
- Auto-Language Selection (English/Turkish)
- Classic UI with Dark Theme Tkinter GUI
- Self-Hiding Console Window

Use at your own risk. This does not activate Windows illegally, it only hides the watermark.
"""

import winreg
import ctypes
import sys
import os
import time
import tkinter as tk
from tkinter import messagebox

# Arka plandaki siyah CMD (konsol) penceresini gizlemek için:
try:
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
except Exception:
    pass

def get_system_lang():
    """Bilgisayarın varsayılan Windows dilini tespit eder (tr veya en)."""
    try:
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        primary_lang = lang_id & 0x3ff
        # Turkish primary language ID is 0x1f (31)
        if primary_lang == 0x1f:
            return "tr"
    except:
        pass
    return "en" # Varsayılan olarak İngilizce

# Dil tercihini tespit et
LANG = get_system_lang()

# Metinlerin her iki dildeki karşılıkları
TEXTS = {
    "tr": {
        "TITLE": "WIN10-11 KEY ETKİNLEŞTİRME",
        "SUBTITLE": "ETKİNLEŞTİRME",
        "FEAT_TITLE": "ÖZELLİKLER",
        "BTN_APPLY": "Filigranı Gizle (svsvc)",
        "BTN_RESTART": "Bilgisayarı Yeniden Başlat (Anında)",
        "APPLY_SUCCESS_TITLE": "BAŞARILI",
        "APPLY_SUCCESS_MSG": "İşlem başarılı, su izi (watermark) gizlendi.\n\nEtkili olması için lütfen bilgisayarınızı yeniden başlatın.",
        "APPLY_ERR_TITLE": "HATA",
        "APPLY_ERR_MSG": "Kayıt defteri değiştirilemedi:\n",
        "RESTART_TITLE": "UYARI!",
        "RESTART_MSG": "Sisteminiz bekletilmeden hemen yeniden başlatılacak. Kaydedilmemiş açık belgeleriniz silinecektir.\nDevam edilsin mi?",
        "SPLASH_LOAD": "ORTAM YÜKLENİYOR...",
        "SPLASH_INIT": "ETKİNLEŞTİRME PROTOKOLLERİ BAŞLATILIYOR..."
    },
    "en": {
        "TITLE": "WIN10-11 KEY ACTIVATION",
        "SUBTITLE": "ACTIVATION",
        "FEAT_TITLE": "FEATURES",
        "BTN_APPLY": "Remove Watermark (svsvc)",
        "BTN_RESTART": "System Restart (Immediate)",
        "APPLY_SUCCESS_TITLE": "SUCCESS",
        "APPLY_SUCCESS_MSG": "Action successful, watermark has been hidden.\n\nPlease restart your computer to apply changes.",
        "APPLY_ERR_TITLE": "ERROR",
        "APPLY_ERR_MSG": "Registry modification failed:\n",
        "RESTART_TITLE": "WARNING!",
        "RESTART_MSG": "Your system will be restarted immediately. Any unsaved data will be lost.\nDo you want to proceed?",
        "SPLASH_LOAD": "LOADING ENVIRONMENT...",
        "SPLASH_INIT": "INITIALIZING ACTIVATION PROTOCOLS..."
    }
}

def is_admin():
    """Uygulamanın yönetici izinlerine sahip olup olmadığını kontrol eder."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def disable_svsvc():
    """svsvc hizmetinin Start değerini 4 (Devre Dışı) olarak değiştirir."""
    try:
        key_path = r"SYSTEM\CurrentControlSet\Services\svsvc"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 4)
        winreg.CloseKey(key)
        return True, ""
    except Exception as e:
        return False, str(e)

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(TEXTS[LANG]["TITLE"])
        self.root.geometry("850x650")
        self.root.configure(bg="#0c0c0c")
        self.root.resizable(False, False)
        self.center_window(self.root, 850, 650)
        
        # ========== BAŞLIK ALANI ==========
        lbl_title1 = tk.Label(self.root, text="win10-11", font=("Courier New", 45, "bold"), fg="#cc0000", bg="#0c0c0c")
        lbl_title1.pack(pady=(30, 0))
        
        lbl_title2 = tk.Label(self.root, text="key", font=("Courier New", 55, "bold"), fg="#cc0000", bg="#0c0c0c")
        lbl_title2.pack()

        lbl_subtitle = tk.Label(self.root, text=TEXTS[LANG]["SUBTITLE"], font=("Courier New", 14, "bold"), fg="#00ff00", bg="#0c0c0c")
        lbl_subtitle.pack(pady=(15, 20))

        # ========== ÖZELLİKLER PANELİ ==========
        frame_features = tk.Frame(self.root, bg="#151515", bd=1, relief=tk.SOLID, highlightbackground="#333333", highlightcolor="#333333", highlightthickness=1)
        frame_features.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        lbl_feat_title = tk.Label(frame_features, text=TEXTS[LANG]["FEAT_TITLE"], font=("Courier New", 9), fg="#666666", bg="#151515")
        lbl_feat_title.place(x=20, y=10)

        # İŞLEMLER (Klasik Tasarımlı Butonlar)
        btn_apply = tk.Button(frame_features, text=TEXTS[LANG]["BTN_APPLY"], font=("Courier New", 11, "bold"),
                              bg="#006400", fg="#ffffff", relief=tk.RAISED, bd=3,
                              command=self.on_apply, cursor="hand2", width=45, height=2)
        btn_apply.pack(pady=(30, 20))

        btn_restart = tk.Button(frame_features, text=TEXTS[LANG]["BTN_RESTART"], font=("Courier New", 11, "bold"),
                                bg="#8b0000", fg="#ffffff", relief=tk.RAISED, bd=3,
                                command=self.on_restart, cursor="hand2", width=45, height=2)
        btn_restart.pack(pady=10)

    def center_window(self, win, width, height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/2))
        win.geometry(f"{width}x{height}+{x}+{y}")

    def on_apply(self):
        success, msg = disable_svsvc()
        if success:
            messagebox.showinfo(TEXTS[LANG]["APPLY_SUCCESS_TITLE"], TEXTS[LANG]["APPLY_SUCCESS_MSG"], parent=self.root)
        else:
            messagebox.showerror(TEXTS[LANG]["APPLY_ERR_TITLE"], TEXTS[LANG]["APPLY_ERR_MSG"] + msg, parent=self.root)

    def on_restart(self):
        ans = messagebox.askyesno(TEXTS[LANG]["RESTART_TITLE"], TEXTS[LANG]["RESTART_MSG"], parent=self.root)
        if ans:
            os.system("shutdown /r /t 0")

def show_splash():
    """Program ilk çalıştığında gösterilecek havalı açılış (Splash) ekranı"""
    splash = tk.Tk()
    splash.overrideredirect(True)
    
    width, height = 500, 300
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))
    splash.geometry(f"{width}x{height}+{x}+{y}")
    splash.configure(bg="#050505")

    frame = tk.Frame(splash, bg="#050505", highlightbackground="#00aa00", highlightthickness=1)
    frame.pack(fill=tk.BOTH, expand=True)

    lbl_main = tk.Label(frame, text=TEXTS[LANG]["SPLASH_LOAD"], font=("Courier New", 18, "bold"), fg="#00ff00", bg="#050505")
    lbl_main.pack(expand=True)
    
    lbl_sub = tk.Label(frame, text=TEXTS[LANG]["SPLASH_INIT"], font=("Courier New", 10), fg="#444444", bg="#050505")
    lbl_sub.pack(side=tk.BOTTOM, pady=20)

    splash.update()
    time.sleep(2.5)
    splash.destroy()

if __name__ == "__main__":
    if is_admin():
        show_splash()
        root = tk.Tk()
        app = AppGUI(root)
        root.mainloop()
    else:
        try:
            script_path = sys.argv[0]
            exe = sys.executable
            if exe and exe.lower().endswith("python.exe"):
                exe_dir = os.path.dirname(exe)
                pyw = os.path.join(exe_dir, "pythonw.exe")
                if os.path.exists(pyw):
                    exe = pyw
                    
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, f'"{script_path}"', None, 1)
        except Exception:
            pass
