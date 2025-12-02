import tkinter as tk
from tkinter import messagebox, ttk
import json


# ========== KLASSLAR ==========
class Dvigatel:
    def __init__(self, ishlab_chiqaruvchi, ot_kuchi, dvigatel_turi):
        self.ishlab_chiqaruvchi = ishlab_chiqaruvchi
        self.ot_kuchi = ot_kuchi
        self.dvigatel_turi = dvigatel_turi


class Avtomobil:
    def __init__(self, model, rang, yil, dvigatel):
        self.model = model
        self.rang = rang
        self.yil = yil
        self.dvigatel = dvigatel


# ========== GLOBAL ==========
avtomobillar = []
tanlangan_index = None


# ========== FUNKSIYALAR ==========
def qoshish():
    model = e_model.get().strip()
    rang = e_rang.get().strip()
    yil = e_yil.get().strip()
    dv_nomi = e_dv_nomi.get().strip()
    dv_kuchi = e_dv_kuchi.get().strip()
    dv_turi = combo_turi.get()

    if not all([model, rang, yil, dv_nomi, dv_kuchi]):
        messagebox.showerror("Xato", "Barcha maydonlarni to'ldiring!")
        return

    try:
        yil = int(yil)
        kuchi = int(dv_kuchi)
    except:
        messagebox.showerror("Xato", "Yil va kuch raqam bo'lishi kerak!")
        return

    dvigatel = Dvigatel(dv_nomi, kuchi, dv_turi)
    avto = Avtomobil(model, rang, yil, dvigatel)
    avtomobillar.append(avto)

    yangilash()
    tozalash()
    messagebox.showinfo("Tayyor", f"{model} qo'shildi!")


def ochirish():
    global tanlangan_index
    if tanlangan_index is None:
        messagebox.showerror("❌ Xato", "Avtomobilni tanlang!")
        return

    avto = avtomobillar[tanlangan_index]
    if messagebox.askyesno("Tasdiqlash", f"{avto.model} ni o'chirasizmi?"):
        avtomobillar.pop(tanlangan_index)
        tanlangan_index = None
        yangilash()
        tozalash()
        messagebox.showinfo("Tayyor", "O'chirildi!")


def tahrirlash():
    global tanlangan_index
    if tanlangan_index is None:
        messagebox.showerror("❌ Xato", "Avtomobilni tanlang!")
        return

    model = e_model.get().strip()
    rang = e_rang.get().strip()
    yil = e_yil.get().strip()
    dv_nomi = e_dv_nomi.get().strip()
    dv_kuchi = e_dv_kuchi.get().strip()
    dv_turi = combo_turi.get()

    if not all([model, rang, yil, dv_nomi, dv_kuchi]):
        messagebox.showerror("Xato", "Barcha maydonlarni to'ldiring!")
        return

    try:
        yil = int(yil)
        kuchi = int(dv_kuchi)
    except:
        messagebox.showerror("Xato", "Yil va kuch raqam bo'lishi kerak!")
        return

    avto = avtomobillar[tanlangan_index]
    avto.model = model
    avto.rang = rang
    avto.yil = yil
    avto.dvigatel.ishlab_chiqaruvchi = dv_nomi
    avto.dvigatel.ot_kuchi = kuchi
    avto.dvigatel.dvigatel_turi = dv_turi

    yangilash()
    messagebox.showinfo("Tayyor", "Yangilandi!")


def tanlash(event):
    global tanlangan_index
    widget = event.widget
    selection = widget.curselection()
    if selection:
        tanlangan_index = selection[0]
        avto = avtomobillar[tanlangan_index]

        e_model.delete(0, tk.END)
        e_model.insert(0, avto.model)
        e_rang.delete(0, tk.END)
        e_rang.insert(0, avto.rang)
        e_yil.delete(0, tk.END)
        e_yil.insert(0, avto.yil)
        e_dv_nomi.delete(0, tk.END)
        e_dv_nomi.insert(0, avto.dvigatel.ishlab_chiqaruvchi)
        e_dv_kuchi.delete(0, tk.END)
        e_dv_kuchi.insert(0, avto.dvigatel.ot_kuchi)
        combo_turi.set(avto.dvigatel.dvigatel_turi)

        # Ma'lumotlarni ko'rsatish
        info_text.config(state=tk.NORMAL)
        info_text.delete(1.0, tk.END)
        info_text.insert(tk.END, f"═══════════════════════════════\n", "header")
        info_text.insert(tk.END, f"    TANLANGAN AVTOMOBIL\n", "header")
        info_text.insert(tk.END, f"═══════════════════════════════\n\n", "header")
        info_text.insert(tk.END, f"Model: ", "label")
        info_text.insert(tk.END, f"{avto.model}\n\n", "value")
        info_text.insert(tk.END, f"Rang: ", "label")
        info_text.insert(tk.END, f"{avto.rang}\n\n", "value")
        info_text.insert(tk.END, f"Yil: ", "label")
        info_text.insert(tk.END, f"{avto.yil}\n\n", "value")
        info_text.insert(tk.END, f"Dvigatel brendi: ", "label")
        info_text.insert(tk.END, f"{avto.dvigatel.ishlab_chiqaruvchi}\n\n", "value")
        info_text.insert(tk.END, f"Kuchi: ", "label")
        info_text.insert(tk.END, f"{avto.dvigatel.ot_kuchi} hp\n\n", "value")
        info_text.insert(tk.END, f"Turi: ", "label")
        info_text.insert(tk.END, f"{avto.dvigatel.dvigatel_turi}\n", "value")
        info_text.config(state=tk.DISABLED)


def saqlash():
    data = []
    for a in avtomobillar:
        data.append({
            "model": a.model, "rang": a.rang, "yil": a.yil,
            "dvigatel": {
                "ishlab_chiqaruvchi": a.dvigatel.ishlab_chiqaruvchi,
                "ot_kuchi": a.dvigatel.ot_kuchi,
                "dvigatel_turi": a.dvigatel.dvigatel_turi
            }
        })

    with open("avtomobillar.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    messagebox.showinfo("Tayyor", "Ma'lumotlar saqlandi!")


def yuklash():
    global tanlangan_index
    try:
        with open("avtomobillar.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        avtomobillar.clear()
        for item in data:
            dv = item["dvigatel"]
            dvigatel = Dvigatel(dv["ishlab_chiqaruvchi"], dv["ot_kuchi"], dv["dvigatel_turi"])
            avto = Avtomobil(item["model"], item["rang"], item["yil"], dvigatel)
            avtomobillar.append(avto)

        tanlangan_index = None
        yangilash()
        tozalash()
        messagebox.showinfo("Tayyor", "Ma'lumotlar yuklandi!")
    except FileNotFoundError:
        messagebox.showinfo("Axborot", "Saqlangan fayl topilmadi")


def yangilash():
    listbox.delete(0, tk.END)
    for i, avto in enumerate(avtomobillar, 1):
        listbox.insert(tk.END, f"{i}. {avto.model} ({avto.rang}, {avto.yil})")

    # Statistika yangilash
    jami_label.config(text=f"Jami avtomobillar: {len(avtomobillar)}")


def tozalash():
    global tanlangan_index
    e_model.delete(0, tk.END)
    e_rang.delete(0, tk.END)
    e_yil.delete(0, tk.END)
    e_dv_nomi.delete(0, tk.END)
    e_dv_kuchi.delete(0, tk.END)
    combo_turi.set("Benzin")
    tanlangan_index = None

    info_text.config(state=tk.NORMAL)
    info_text.delete(1.0, tk.END)
    info_text.insert(tk.END, "\n\n\n")
    info_text.insert(tk.END, "      Avtomobilni tanlang\n\n", "center")
    info_text.insert(tk.END, "   Ma'lumotlar shu yerda\n", "center")
    info_text.insert(tk.END, "   ko'rsatiladi", "center")
    info_text.config(state=tk.DISABLED)


# ========== ASOSIY OYNA ==========
root = tk.Tk()
root.title("AVTOMOBIL BOSHQARUV TIZIMI")
root.geometry("1100x700")
root.configure(bg="#1a1a2e")

# ========== SARLAVHA ==========
header = tk.Frame(root, bg="#16213e", height=80)
header.pack(fill=tk.X, padx=0, pady=0)

tk.Label(header, text="AVTOMOBIL BOSHQARUV TIZIMI",
         font=("Arial", 26, "bold"), bg="#16213e", fg="#00ff88").pack(pady=20)

# ========== ASOSIY KONTEYNER ==========
main_container = tk.Frame(root, bg="#1a1a2e")
main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# ========== CHAP: FORMA ==========
left_frame = tk.Frame(main_container, bg="#0f3460", bd=3, relief=tk.RAISED)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

tk.Label(left_frame, text="MA'LUMOTLARNI KIRITING",
         font=("Arial", 16, "bold"), bg="#0f3460", fg="#ffffff").pack(pady=20)

form = tk.Frame(left_frame, bg="#0f3460")
form.pack(padx=30, pady=10)

fields = [
    ("Model:", "e_model"),
    ("Rang:", "e_rang"),
    ("Yil:", "e_yil"),
    ("Dvigatel brendi:", "e_dv_nomi"),
    ("Ot kuchi:", "e_dv_kuchi"),
]

for i, (label_text, var_name) in enumerate(fields):
    tk.Label(form, text=label_text, font=("Arial", 13, "bold"),
             bg="#0f3460", fg="#00d9ff", anchor="w").grid(row=i, column=0, sticky="w", pady=12, padx=5)

    entry = tk.Entry(form, font=("Arial", 12), width=20, bg="#1a1a2e", fg="white",
                     insertbackground="white", bd=2, relief=tk.SOLID)
    entry.grid(row=i, column=1, pady=12, padx=10)
    globals()[var_name] = entry

tk.Label(form, text="Dvigatel turi:", font=("Arial", 13, "bold"),
         bg="#0f3460", fg="#00d9ff", anchor="w").grid(row=5, column=0, sticky="w", pady=12, padx=5)

combo_turi = ttk.Combobox(form, values=["Benzin", "Dizel", "Elektr", "Gibrid"],
                          state="readonly", font=("Arial", 12), width=18)
combo_turi.set("Benzin")
combo_turi.grid(row=5, column=1, pady=12, padx=10)

# TUGMALAR
btn_frame = tk.Frame(left_frame, bg="#0f3460")
btn_frame.pack(pady=30)

tugmalar = [
    ("QO'SHISH", qoshish, "#00ff88", "#000000", 0, 0),
    ("TAHRIRLASH", tahrirlash, "#ffaa00", "#000000", 0, 1),
    ("O'CHIRISH", ochirish, "#ff4444", "#ffffff", 1, 0),
    ("TOZALASH", tozalash, "#6c5ce7", "#ffffff", 1, 1),
    ("SAQLASH", saqlash, "#00d9ff", "#000000", 2, 0),
    ("YUKLASH", yuklash, "#a29bfe", "#000000", 2, 1),
]

for text, cmd, bg, fg, r, c in tugmalar:
    tk.Button(btn_frame, text=text, command=cmd, font=("Arial", 11, "bold"),
              bg=bg, fg=fg, width=14, height=2, bd=0, cursor="hand2",
              activebackground=bg, activeforeground=fg).grid(row=r, column=c, padx=8, pady=8)

# ========== O'RTA: RO'YXAT ==========
middle_frame = tk.Frame(main_container, bg="#0f3460", bd=3, relief=tk.RAISED)
middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

tk.Label(middle_frame, text="AVTOMOBILLAR RO'YXATI",
         font=("Arial", 16, "bold"), bg="#0f3460", fg="#ffffff").pack(pady=20)

list_container = tk.Frame(middle_frame, bg="#0f3460")
list_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

scrollbar = tk.Scrollbar(list_container, bg="#1a1a2e")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(list_container, font=("Courier New", 13), bg="#1a1a2e", fg="#00ff88",
                     selectbackground="#00d9ff", selectforeground="#000000", bd=0,
                     yscrollcommand=scrollbar.set, highlightthickness=0)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox.yview)
listbox.bind("<<ListboxSelect>>", tanlash)

jami_label = tk.Label(middle_frame, text="Jami avtomobillar: 0",
                      font=("Arial", 12, "bold"), bg="#0f3460", fg="#ffaa00")
jami_label.pack(pady=10)

# ========== O'NG: MA'LUMOTLAR ==========
right_frame = tk.Frame(main_container, bg="#0f3460", bd=3, relief=tk.RAISED, width=300)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

tk.Label(right_frame, text="BATAFSIL MA'LUMOT",
         font=("Arial", 16, "bold"), bg="#0f3460", fg="#ffffff").pack(pady=20)

info_text = tk.Text(right_frame, font=("Arial", 12), bg="#1a1a2e", fg="white",
                    bd=0, wrap=tk.WORD, highlightthickness=0, padx=15, pady=15)
info_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

info_text.tag_config("header", foreground="#00ff88", font=("Arial", 13, "bold"), justify="center")
info_text.tag_config("label", foreground="#00d9ff", font=("Arial", 12, "bold"))
info_text.tag_config("value", foreground="#ffffff", font=("Arial", 12))
info_text.tag_config("center", foreground="#6c5ce7", font=("Arial", 13, "bold"), justify="center")

tozalash()
yuklash()

root.mainloop()