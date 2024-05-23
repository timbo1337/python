import tkinter as tk
from tkinter import messagebox, simpledialog
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random

# Absztrakt Szoba osztály
class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
        self.foglalasok = []

    @abstractmethod
    def __str__(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 10000)

    def __str__(self):
        return f"Egyágyas szoba - Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft"

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 15000)

    def __str__(self):
        return f"Kétágyas szoba - Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft"

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if datum in szoba.foglalasok:
                    return False
                else:
                    szoba.foglalasok.append(datum)
                    return szoba.ar
        return False

    def lemondas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if datum in szoba.foglalasok:
                    szoba.foglalasok.remove(datum)
                    return True
        return False

    def foglalasok_listazasa(self):
        foglalasok = []
        for szoba in self.szobak:
            for datum in szoba.foglalasok:
                foglalasok.append((szoba.szobaszam, datum))
        return foglalasok

class Foglalas:
    def __init__(self, szalloda, szobaszam, datum):
        self.szalloda = szalloda
        self.szobaszam = szobaszam
        self.datum = datum

class SzallodaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Szállodai Szobafoglaló Rendszer")

        self.szalloda = Szalloda("Hotel Python")
        self.szalloda.szoba_hozzaadas(EgyagyasSzoba(101))
        self.szalloda.szoba_hozzaadas(KetagyasSzoba(102))
        self.szalloda.szoba_hozzaadas(EgyagyasSzoba(103))

        self.szobak_listbox = tk.Listbox(root, height=10, width=50, font=("Arial", 12))
        self.szobak_listbox.pack()

        self.frissit_szobak_listbox()

        self.szobak_listazasa_gomb = tk.Button(root, text="Szobák listázása", command=self.frissit_szobak_listbox)
        self.szobak_listazasa_gomb.pack()

        self.foglalas_gomb = tk.Button(root, text="Foglalás", command=self.szoba_foglalas)
        self.foglalas_gomb.pack()

        self.lemondas_gomb = tk.Button(root, text="Lemondás", command=self.szoba_lemondas)
        self.lemondas_gomb.pack()

        self.listazas_gomb = tk.Button(root, text="Foglalások listázása", command=self.foglalasok_listazasa)
        self.listazas_gomb.pack()

        self.add_random_bookings(5)

    def frissit_szobak_listbox(self):
        self.szobak_listbox.delete(0, tk.END)
        for szoba in self.szalloda.szobak:
            self.szobak_listbox.insert(tk.END, str(szoba))

    def szoba_foglalas(self):
        try:
            kivalasztott_index = self.szobak_listbox.curselection()[0]
            szoba = self.szalloda.szobak[kivalasztott_index]
            datum_str = simpledialog.askstring("Foglalás", "Add meg a foglalás dátumát (YYYY-MM-DD):")
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
            if datum < datetime.now().date():
                messagebox.showerror("Hiba", "A foglalás dátuma nem lehet múltbeli dátum.")
                return
            ar = self.szalloda.foglalas(szoba.szobaszam, datum)
            if ar:
                messagebox.showinfo("Siker", f"A foglalás sikeres! Ár: {ar} Ft")
            else:
                messagebox.showerror("Hiba", "A szoba már foglalt erre a dátumra.")
        except IndexError:
            messagebox.showerror("Hiba", "Nincs kiválasztott szoba.")
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen dátum formátum.")

    def szoba_lemondas(self):
        try:
            kivalasztott_index = self.szobak_listbox.curselection()[0]
            kivalasztott_foglalas = self.szobak_listbox.get(kivalasztott_index)
            szobaszam, datum_str = kivalasztott_foglalas.split(", Dátum: ")
            szobaszam = int(szobaszam.split(": ")[1])
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
            siker = self.szalloda.lemondas(szobaszam, datum)
            if siker:
                self.szobak_listbox.delete(kivalasztott_index)
                messagebox.showinfo("Siker", "A lemondás sikeres!")
            else:
                messagebox.showerror("Hiba", "Nem található foglalás erre a dátumra.")
        except IndexError:
            messagebox.showerror("Hiba", "Nincs kiválasztott foglalás.")
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen dátum formátum.")

    def foglalasok_listazasa(self):
        self.szobak_listbox.delete(0, tk.END)
        foglalasok = self.szalloda.foglalasok_listazasa()
        if foglalasok:
            for szobaszam, datum in foglalasok:
                self.szobak_listbox.insert(tk.END, f"Szobaszám: {szobaszam}, Dátum: {datum}")
        else:
            messagebox.showinfo("Foglalások", "Nincs aktív foglalás.")

    def add_random_bookings(self, count):
        today = datetime.now().date()
        for _ in range(count):
            random_room = random.choice(self.szalloda.szobak)
            random_date = today + timedelta(days=random.randint(1, 365))
            self.szalloda.foglalas(random_room.szobaszam, random_date)

if __name__ == "__main__":
    root = tk.Tk()
    app = SzallodaApp(root)
    root.mainloop()