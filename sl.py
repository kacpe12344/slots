import tkinter as tk
from tkinter import messagebox
import random

class SlotsGame:
    def __init__(self, root): #konstruktor klasy, inicjalizuje obiekt 
        self.root = root 
        self.root.title("🎰 Slot Machine") #tytuł
        self.root.configure(bg="black") #czarne tło
        
        self.balance = 100 #początkowy balans
        self.bet_amount = 10 #stawka 

        self.symbols = ["🍒", "🍇", "🔔"] #symbole 

        self.create_widgets() #gui, wywołanie metody do tworzenia interfejsu 

    def create_widgets(self): #metoda która tworzy elementy interfejsu usera 
        # Tytuł
        title = tk.Label(self.root, text="SLOT MACHINE", font=("Impact", 32), fg="gold", bg="black") #wielkość czcionki, kolor cz, kolor tła 
        title.pack(pady=10) #umiejscowienie etykiety, px

        # Ramka slotów
        self.slots_frame = tk.Frame(self.root, bg="darkred", bd=10, relief="ridge") #ramka, kolor, grubosc px, styl wypukły
        self.slots_frame.pack(pady=20) #umiejscowienie 

        self.slot_labels = [] #lista 
        for i in range(3): #petla tworząca 3 sloty
            label = tk.Label(self.slots_frame, text="❓", font=("Arial", 60), width=3, bg="black", fg="white", bd=5, relief="sunken") #tworzenie etykiety, czcionka, szerokośc, tło, kolor tekstu, grubośc, styl 
            label.pack(side=tk.LEFT, padx=15)  ##umieszczenie slotów, stylizacja 
            self.slot_labels.append(label) #dodanie etykiety do listy 

        # Pole do ustawiania stawki
        self.bet_label = tk.Label(self.root, text="Stawka:", font=("Arial", 14), fg="white", bg="black") #ekitieta stawka, czcionka, teskt, tło, 
        self.bet_label.pack()
        self.bet_entry = tk.Entry(self.root, font=("Arial", 14), width=10) #szerokosc na 10 znaków 
        self.bet_entry.pack() #umiejscowienie 
        self.bet_entry.insert(0, str(self.bet_amount)) #wstawienie domyslnej stawki 

        # Pole do ustawiania balansu, wprowadzmy liczbe automatycznie zmiania nam sie balans, to samo co w stawce 
        self.balance_label = tk.Label(self.root, text="Balans:", font=("Arial", 14), fg="white", bg="black")
        self.balance_label.pack()
        self.balance_entry = tk.Entry(self.root, font=("Arial", 14), width=10)
        self.balance_entry.pack()
        self.balance_entry.insert(0, str(self.balance)) #umiejscowienie domyslnego balansu 

        # Przycisk SPIN
        spin_button = tk.Button(self.root, text="SPIN", font=("Arial", 20), bg="gold", fg="black", command=self.spin) #tworzymy przycisk, czcionka, tło, tekst, po nasiscięciu wywołujemy metode spin 
        spin_button.pack(pady=20) #umiejscowienie 

    def animate_spin(self, results, index=0, steps=10): #animacja krecenia slotem 
        if steps > 0: #jeśli pozostaly kroki animacji 
            for i in range(3): #dla każdego slotu 
                self.slot_labels[i].config(text=random.choice(self.symbols)) #losowy symbol 
            self.root.after(100, self.animate_spin, results, index, steps - 1) #po 100ms wywołuje funckje jeszcze raz ze zmniejszoną liczbą kroków, czyli 3,2,1 az do 0 
        else: #po zakończonej animacji
            for i in range(3): #dla każdego slotu
                self.slot_labels[i].config(text=results[i]) #przypisanie, ustawienie symbolu 
            self.check_win(results) #wywołuje funkcje, sprawdza czy mamy wygraną 

    def spin(self): # obracania slotem 
        try: #pobranie stawki i balansu z naszych pół 
            self.bet_amount = int(self.bet_entry.get()) #pobranie stawki
            self.balance = int(self.balance_entry.get()) #pobranie balansu 
        except ValueError: #przy złych danych zwraca nam błąd 
            messagebox.showerror("Błąd", "Podaj poprawne wartości dla stawki i balansu!")
            return

        if self.bet_amount > self.balance:
            messagebox.showerror("Błąd", "Niewystarczający balans do ponownego zespinowania")
            return

        self.balance -= self.bet_amount #odjęcie stawki od balansu
        self.balance_entry.delete(0, tk.END) #czyścimy pole balansu
        self.balance_entry.insert(0, str(self.balance)) #wstawienie zaktualizowanmego balansu 

        results = [random.choice(self.symbols) for _ in range(3)] #losowanie 3 symboli
        self.animate_spin(results) #uruchomienie slota 

#wygrana, jeśli wylosujemy 3 takie same symbole nasza stawka mnoży się przez 5 i dodajemy do balansu 
    def check_win(self, results):
        if results[0] == results[1] == results[2]:
            winnings = self.bet_amount * 5
            self.balance += winnings #dodanie wygranej do balansu
            self.balance_entry.delete(0, tk.END) #wyczyszczenie pola balansu  
            self.balance_entry.insert(0, str(self.balance)) #wyświetlenie zaktualizowanego balansu 
            messagebox.showinfo("Wygrana!", f"Gratulacje! Wygrałeś {winnings}!") #komunikat o wygranej 

if __name__ == "__main__":
    root = tk.Tk() #tworzenie okna 
    game = SlotsGame(root) #inicjalizowanie gry
    root.mainloop() #uruchomienie petli 
 