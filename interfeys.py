import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import json

avtomobillar_list = []

# ==================== RANG SXEMASI ====================
BG_COLOR = "#1a1a2e"           # Asosiy fon rangi (to'q ko'k)
CARD_BG = "#16213e"            # Kartalar foni
ACCENT_COLOR = "#e94560"       # Aksent rang (qizil-pushti)
TEXT_COLOR = "#eaeaea"         # Matn rangi (oq)
ENTRY_BG = "#0f3460"           # Kiritish maydonlari foni
ENTRY_FG = "#ffffff"           # Kiritish maydonlari matni
SUCCESS_COLOR = "#00d9a0"      # Muvaffaqiyat rangi (yashil)
WARNING_COLOR = "#ffc107"      # Ogohlantirish rangi (sariq)
DANGER_COLOR = "#ff4757"       # Xavf rangi (qizil)

# ==================== KLASSLAR ====================
class Dvigatel:
    def __init__(self, ishlab_chiqaruvchi, ot_kuchi, dvigatel_turi):
        self.ishlab_chiqaruvchi = ishlab_chiqaruvchi
        self.ot_kuchi = ot_kuchi
        self.dvigatel_turi = dvigatel_turi

    def __repr__(self):
        return f"Ishlab chiqaruvchi: {self.ishlab_chiqaruvchi}, Kuch: {self.ot_kuchi} ot kuchi, Turi: {self.dvigatel_turi}"


class Avtomobil:
    def __init__(self, model, rang, yil, dvigatel):
        self.model = model
        self.rang = rang
        self.yil = yil
        self.dvigatel = dvigatel

    def __repr__(self):
        return (f"Avtomobil modeli: {self.model}\n"
                f"Rangi: {self.rang}\n"
                f"Yili: {self.yil}\n"
                f"Dvigatel brendi: {self.dvigatel.ishlab_chiqaruvchi}\n"
                f"Ot kuchi: {self.dvigatel.ot_kuchi}\n"
                f"Dvigatel turi: {self.dvigatel.dvigatel_turi}")


# ==================== UI FUNKSIYALARI ====================
def avtomobil_yaratish():
    try:
        model = entry_model.get().strip()
        rang = entry_rang.get().strip()
        yil = entry_yil.get().strip()
        dv_ishlab_chiqaruvchi = entry_dv_nomi.get().strip()
        dv_kuchi = entry_dv_kuchi.get().strip()
        dv_turi = combo_dv_turi.get()

        if not model or not rang or not yil or not dv_ishlab_chiqaruvchi or not dv_kuchi or not dv_turi:
            messagebox.showwarning("Diqqat", "Iltimos, barcha maydonlarni to'ldiring!")
            return

        try:
            yil = int(yil)
            ot_kuchi = int(dv_kuchi)
        except ValueError:
            messagebox.showwarning("Diqqat", "Yil va Ot kuchi maydonlariga faqat son kiriting!")
            return

        yangi_dvigatel = Dvigatel(dv_ishlab_chiqaruvchi, ot_kuchi, dv_turi)
        yangi_avto = Avtomobil(model, rang, yil, yangi_dvigatel)

        avtomobillar_list.append(yangi_avto)
        listbox_avtomobillar.insert(tk.END, f"{yangi_avto.model} ({yangi_avto.yil})")
        
        lbl_natija.config(text=str(yangi_avto))
        clear_entries()
        messagebox.showinfo("Muvaffaqiyat", f"{model} avtomobili yaratildi!")

    except Exception as e:
        messagebox.showerror("Xatolik", f"Xatolik yuz berdi: {e}")


def clear_entries():
    """Barcha kiritish maydonlarini tozalash"""
    entry_model.delete(0, tk.END)
    entry_rang.delete(0, tk.END)
    entry_yil.delete(0, tk.END)
    entry_dv_nomi.delete(0, tk.END)
    entry_dv_kuchi.delete(0, tk.END)
    combo_dv_turi.set(dvigatel_turlari[0])


def select_avtomobil(event):
    selected_index = listbox_avtomobillar.curselection()
    if selected_index:
        index = selected_index[0]
        selected_avto = avtomobillar_list[index]
        lbl_natija.config(text=str(selected_avto))
        
        entry_model.delete(0, tk.END)
        entry_model.insert(0, selected_avto.model)
        
        entry_rang.delete(0, tk.END)
        entry_rang.insert(0, selected_avto.rang)
        
        entry_yil.delete(0, tk.END)
        entry_yil.insert(0, selected_avto.yil)
        
        entry_dv_nomi.delete(0, tk.END)
        entry_dv_nomi.insert(0, selected_avto.dvigatel.ishlab_chiqaruvchi)
        
        entry_dv_kuchi.delete(0, tk.END)
        entry_dv_kuchi.insert(0, selected_avto.dvigatel.ot_kuchi)
        
        combo_dv_turi.set(selected_avto.dvigatel.dvigatel_turi)


def avtomobil_ochirish():
    selected_index = listbox_avtomobillar.curselection()
    if selected_index:
        index = selected_index[0]
        ochiriladigan_avto = avtomobillar_list[index]
        if messagebox.askyesno("Tasdiqlash", f"{ochiriladigan_avto.model} avtomobilini o'chirmoqchimisiz?"):
            listbox_avtomobillar.delete(index)
            avtomobillar_list.pop(index)
            lbl_natija.config(text="Avtomobil tanlanmagan...")
            clear_entries()
            messagebox.showinfo("Muvaffaqiyat", f"{ochiriladigan_avto.model} avtomobili o'chirildi.")
    else:
        messagebox.showwarning("Diqqat", "Iltimos, o'chirish uchun avtomobilni tanlang!")


def save_data():
    data_to_save = []
    for avto in avtomobillar_list:
        data_to_save.append({
            "model": avto.model,
            "rang": avto.rang,
            "yil": avto.yil,
            "dvigatel": {
                "ishlab_chiqaruvchi": avto.dvigatel.ishlab_chiqaruvchi,
                "ot_kuchi": avto.dvigatel.ot_kuchi,
                "dvigatel_turi": avto.dvigatel.dvigatel_turi
            }
        })
    try:
        with open("avtomobillar_data.json", "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Muvaffaqiyat", "Ma'lumotlar muvaffaqiyatli saqlandi!")
    except Exception as e:
        messagebox.showerror("Xatolik", f"Ma'lumotlarni saqlashda xatolik yuz berdi: {e}")


def load_data():
    try:
        with open("avtomobillar_data.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        avtomobillar_list.clear()
        listbox_avtomobillar.delete(0, tk.END)

        for item in loaded_data:
            dvigatel_data = item["dvigatel"]
            dvigatel_obj = Dvigatel(dvigatel_data["ishlab_chiqaruvchi"], dvigatel_data["ot_kuchi"], dvigatel_data["dvigatel_turi"])
            avtomobil_obj = Avtomobil(item["model"], item["rang"], item["yil"], dvigatel_obj)
            avtomobillar_list.append(avtomobil_obj)
            listbox_avtomobillar.insert(tk.END, f"{avtomobil_obj.model} ({avtomobil_obj.yil})")
        
        if loaded_data:
            messagebox.showinfo("Muvaffaqiyat", f"{len(loaded_data)} ta avtomobil yuklandi!")
    except FileNotFoundError:
        pass  # Fayl topilmasa, hech narsa qilmaymiz
    except Exception as e:
        messagebox.showerror("Xatolik", f"Ma'lumotlarni yuklashda xatolik yuz berdi: {e}")


def search_avtomobillar(query):
    listbox_avtomobillar.delete(0, tk.END)
    if not query:
        for avto in avtomobillar_list:
            listbox_avtomobillar.insert(tk.END, f"{avto.model} ({avto.yil})")
        return

    query = query.lower()
    found = False
    for avto in avtomobillar_list:
        if (query in avto.model.lower() or
            query in avto.rang.lower() or
            query in str(avto.yil).lower() or
            query in avto.dvigatel.ishlab_chiqaruvchi.lower() or
            query in str(avto.dvigatel.ot_kuchi).lower() or
            query in avto.dvigatel.dvigatel_turi.lower()):
            listbox_avtomobillar.insert(tk.END, f"{avto.model} ({avto.yil})")
            found = True
    
    if not found:
        lbl_natija.config(text="Qidiruv bo'yicha hech narsa topilmadi...")


def reset_search():
    entry_search.delete(0, tk.END)
    listbox_avtomobillar.delete(0, tk.END)
    for avto in avtomobillar_list:
        listbox_avtomobillar.insert(tk.END, f"🚗 {avto.model} ({avto.yil})")
    lbl_natija.config(text="Avtomobil tanlanmagan...")


def update_avtomobil():
    selected_index = listbox_avtomobillar.curselection()
    if not selected_index:
        messagebox.showwarning("Diqqat", "Iltimos, yangilash uchun avtomobilni tanlang!")
        return
    
    index = selected_index[0]
    avto_to_update = avtomobillar_list[index]

    try:
        new_model = entry_model.get().strip()
        new_rang = entry_rang.get().strip()
        new_yil = entry_yil.get().strip()
        new_dv_ishlab_chiqaruvchi = entry_dv_nomi.get().strip()
        new_dv_kuchi = entry_dv_kuchi.get().strip()
        new_dv_turi = combo_dv_turi.get()

        if not new_model or not new_rang or not new_yil or not new_dv_ishlab_chiqaruvchi or not new_dv_kuchi or not new_dv_turi:
            messagebox.showwarning("Diqqat", "Iltimos, barcha maydonlarni to'ldiring!")
            return
        
        try:
            new_yil = int(new_yil)
            new_ot_kuchi = int(new_dv_kuchi)
        except ValueError:
            messagebox.showwarning("Diqqat", "Yil va Ot kuchi maydonlariga faqat son kiriting!")
            return
        
        avto_to_update.model = new_model
        avto_to_update.rang = new_rang
        avto_to_update.yil = new_yil
        avto_to_update.dvigatel.ishlab_chiqaruvchi = new_dv_ishlab_chiqaruvchi
        avto_to_update.dvigatel.ot_kuchi = new_ot_kuchi
        avto_to_update.dvigatel.dvigatel_turi = new_dv_turi
        
        listbox_avtomobillar.delete(index)
        listbox_avtomobillar.insert(index, f"{new_model} ({new_yil})")
        
        lbl_natija.config(text=str(avto_to_update))
        messagebox.showinfo("Muvaffaqiyat", f"{new_model} avtomobili yangilandi!")

    except Exception as e:
        messagebox.showerror("Xatolik", f"Ma'lumotlarni yangilashda xatolik yuz berdi: {e}")


# ==================== ASOSIY OYNA ====================
root = tk.Tk()
root.title("Avtomobil Parki Boshqaruv Tizimi")
root.geometry("900x700")
root.configure(bg=BG_COLOR)
root.resizable(True, True)

# ==================== SARLAVHA ====================
header_frame = tk.Frame(root, bg=ACCENT_COLOR, pady=15)
header_frame.pack(fill="x")

tk.Label(
    header_frame, 
    text="AVTOMOBIL PARKI BOSHQARUV TIZIMI", 
    font=("Helvetica", 18, "bold"),
    bg=ACCENT_COLOR,
    fg="white"
).pack()

# ==================== ASOSIY KONTEYNER ====================
main_container = tk.Frame(root, bg=BG_COLOR)
main_container.pack(fill="both", expand=True, padx=20, pady=15)

# ==================== CHAP PANEL (FORMA) ====================
left_panel = tk.Frame(main_container, bg=CARD_BG, padx=20, pady=20)
left_panel.pack(side="left", fill="y", padx=(0, 10))

# Avtomobil ma'lumotlari sarlavhasi
tk.Label(
    left_panel, 
    text="Avtomobil Ma'lumotlari", 
    font=("Helvetica", 14, "bold"),
    bg=CARD_BG,
    fg=ACCENT_COLOR
).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

# Umumiy label va entry stili
label_style = {"bg": CARD_BG, "fg": TEXT_COLOR, "font": ("Helvetica", 11)}
entry_style = {"bg": ENTRY_BG, "fg": ENTRY_FG, "font": ("Helvetica", 11), "insertbackground": "white", "relief": "flat", "width": 20}

# Model
tk.Label(left_panel, text="Model:", **label_style).grid(row=1, column=0, sticky="w", pady=8)
entry_model = tk.Entry(left_panel, **entry_style)
entry_model.grid(row=1, column=1, padx=10, pady=8, ipady=5)

# Rang
tk.Label(left_panel, text="Rang:", **label_style).grid(row=2, column=0, sticky="w", pady=8)
entry_rang = tk.Entry(left_panel, **entry_style)
entry_rang.grid(row=2, column=1, padx=10, pady=8, ipady=5)

# Yil
tk.Label(left_panel, text="Yil:", **label_style).grid(row=3, column=0, sticky="w", pady=8)
entry_yil = tk.Entry(left_panel, **entry_style)
entry_yil.grid(row=3, column=1, padx=10, pady=8, ipady=5)

# Dvigatel bo'limi
tk.Label(
    left_panel, 
    text="Dvigatel Ma'lumotlari", 
    font=("Helvetica", 14, "bold"),
    bg=CARD_BG,
    fg=ACCENT_COLOR
).grid(row=4, column=0, columnspan=2, pady=(20, 15), sticky="w")

# Dvigatel Brendi
tk.Label(left_panel, text="Dvigatel Brendi:", **label_style).grid(row=5, column=0, sticky="w", pady=8)
entry_dv_nomi = tk.Entry(left_panel, **entry_style)
entry_dv_nomi.grid(row=5, column=1, padx=10, pady=8, ipady=5)

# Ot kuchi
tk.Label(left_panel, text="Ot kuchi:", **label_style).grid(row=6, column=0, sticky="w", pady=8)
entry_dv_kuchi = tk.Entry(left_panel, **entry_style)
entry_dv_kuchi.grid(row=6, column=1, padx=10, pady=8, ipady=5)

# Dvigatel turi
tk.Label(left_panel, text="Dvigatel turi:", **label_style).grid(row=7, column=0, sticky="w", pady=8)
dvigatel_turlari = ["Benzin", "Dizel", "Elektr", "Gibrid"]

style = ttk.Style()
style.theme_use('clam')
style.configure("Custom.TCombobox", 
                fieldbackground=ENTRY_BG, 
                background=ENTRY_BG,
                foreground=ENTRY_FG,
                arrowcolor=TEXT_COLOR)

combo_dv_turi = ttk.Combobox(left_panel, values=dvigatel_turlari, state="readonly", width=18, style="Custom.TCombobox")
combo_dv_turi.set(dvigatel_turlari[0])
combo_dv_turi.grid(row=7, column=1, padx=10, pady=8, ipady=5)

# ==================== TUGMALAR (CHAP PANEL) ====================
buttons_frame = tk.Frame(left_panel, bg=CARD_BG)
buttons_frame.grid(row=8, column=0, columnspan=2, pady=20)

btn_style = {"font": ("Helvetica", 10, "bold"), "relief": "flat", "cursor": "hand2", "width": 18, "height": 2}

btn_yaratish = tk.Button(buttons_frame, text="Yaratish", command=avtomobil_yaratish, 
                          bg=SUCCESS_COLOR, fg="white", **btn_style)
btn_yaratish.grid(row=0, column=0, padx=5, pady=5)

btn_yangilash = tk.Button(buttons_frame, text="Yangilash", command=update_avtomobil, 
                           bg=WARNING_COLOR, fg="black", **btn_style)
btn_yangilash.grid(row=0, column=1, padx=5, pady=5)

btn_ochirish = tk.Button(buttons_frame, text="O'chirish", command=avtomobil_ochirish, 
                          bg=DANGER_COLOR, fg="white", **btn_style)
btn_ochirish.grid(row=1, column=0, padx=5, pady=5)

btn_tozalash = tk.Button(buttons_frame, text="Tozalash", command=clear_entries, 
                          bg="#6c757d", fg="white", **btn_style)
btn_tozalash.grid(row=1, column=1, padx=5, pady=5)

# Saqlash va Yuklash tugmalari
file_buttons_frame = tk.Frame(left_panel, bg=CARD_BG)
file_buttons_frame.grid(row=9, column=0, columnspan=2, pady=5)

btn_saqlash = tk.Button(file_buttons_frame, text="Saqlash", command=save_data, 
                         bg="#17a2b8", fg="white", **btn_style)
btn_saqlash.grid(row=0, column=0, padx=5, pady=5)

btn_yuklash = tk.Button(file_buttons_frame, text="Yuklash", command=load_data, 
                         bg="#fd7e14", fg="white", **btn_style)
btn_yuklash.grid(row=0, column=1, padx=5, pady=5)

# ==================== O'NG PANEL ====================
right_panel = tk.Frame(main_container, bg=CARD_BG, padx=20, pady=20)
right_panel.pack(side="right", fill="both", expand=True)

# Qidiruv bo'limi
search_frame = tk.Frame(right_panel, bg=CARD_BG)
search_frame.pack(fill="x", pady=(0, 15))

tk.Label(search_frame, text="Qidirish:", bg=CARD_BG, fg=TEXT_COLOR, 
         font=("Helvetica", 11)).pack(side="left", padx=(0, 10))

entry_search = tk.Entry(search_frame, bg=ENTRY_BG, fg=ENTRY_FG, font=("Helvetica", 11),
                        insertbackground="white", relief="flat", width=25)
entry_search.pack(side="left", padx=5, ipady=5)

btn_qidirish = tk.Button(search_frame, text="Qidirish", 
                          command=lambda: search_avtomobillar(entry_search.get()),
                          bg=ACCENT_COLOR, fg="white", font=("Helvetica", 10, "bold"),
                          relief="flat", cursor="hand2", padx=15)
btn_qidirish.pack(side="left", padx=5)

btn_reset = tk.Button(search_frame, text="Tozalash", command=reset_search,
                       bg="#6c757d", fg="white", font=("Helvetica", 10, "bold"),
                       relief="flat", cursor="hand2", padx=15)
btn_reset.pack(side="left", padx=5)

# Avtomobillar ro'yxati
tk.Label(
    right_panel, 
    text="Mavjud Avtomobillar", 
    font=("Helvetica", 14, "bold"),
    bg=CARD_BG,
    fg=ACCENT_COLOR
).pack(anchor="w", pady=(10, 10))

# Listbox uchun frame (scrollbar bilan)
listbox_frame = tk.Frame(right_panel, bg=CARD_BG)
listbox_frame.pack(fill="both", expand=True, pady=5)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side="right", fill="y")

listbox_avtomobillar = tk.Listbox(
    listbox_frame, 
    height=10, 
    bg=ENTRY_BG, 
    fg=TEXT_COLOR,
    font=("Helvetica", 12),
    selectbackground=ACCENT_COLOR,
    selectforeground="white",
    relief="flat",
    highlightthickness=0,
    yscrollcommand=scrollbar.set
)
listbox_avtomobillar.pack(fill="both", expand=True)
scrollbar.config(command=listbox_avtomobillar.yview)
listbox_avtomobillar.bind('<<ListboxSelect>>', select_avtomobil)

# Natija maydoni
tk.Label(
    right_panel, 
    text="Tanlangan Avtomobil Ma'lumotlari", 
    font=("Helvetica", 14, "bold"),
    bg=CARD_BG,
    fg=ACCENT_COLOR
).pack(anchor="w", pady=(15, 10))

lbl_natija = tk.Label(
    right_panel, 
    text="Avtomobil tanlanmagan...", 
    justify="left",
    anchor="nw",
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    font=("Helvetica", 12),
    relief="flat",
    padx=15,
    pady=15,
    wraplength=350
)
lbl_natija.pack(fill="both", expand=True, pady=5)

# ==================== FOOTER ====================
footer_frame = tk.Frame(root, bg=CARD_BG, pady=10)
footer_frame.pack(fill="x", side="bottom")

tk.Label(
    footer_frame, 
    text="© 2024 Avtomobil Parki Boshqaruv Tizimi | Kompozitsiya: Avtomobil + Dvigatel", 
    font=("Helvetica", 9),
    bg=CARD_BG,
    fg="#888888"
).pack()

# ==================== DASTURNI ISHGA TUSHIRISH ====================
load_data()
root.mainloop()
