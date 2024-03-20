import random
import tkinter as tk
from tkinter import messagebox

class Gato:
    def __init__(self):
        self.tablero = [' ']*9
        self.jugador = 'O'
        self.computadora = 'X'
        self.turno = self.jugador

    def imprimir_tablero(self):
        print(" " + self.tablero[0] + " | " + self.tablero[1] + " | " + self.tablero[2])
        print("-----------")
        print(" " + self.tablero[3] + " | " + self.tablero[4] + " | " + self.tablero[5])
        print("-----------")
        print(" " + self.tablero[6] + " | " + self.tablero[7] + " | " + self.tablero[8])

    def movimiento_valido(self, movimiento):
        return self.tablero[movimiento] == ' '

    def hacer_movimiento(self, movimiento):
        self.tablero[movimiento] = self.turno
        self.turno = self.computadora if self.turno == self.jugador else self.jugador

    def hay_ganador(self):
        # Comprobación de filas
        for i in range(0, 9, 3):
            if self.tablero[i] == self.tablero[i+1] == self.tablero[i+2] != ' ':
                return True
        # Comprobación de columnas
        for i in range(3):
            if self.tablero[i] == self.tablero[i+3] == self.tablero[i+6] != ' ':
                return True
        # Comprobación de diagonales
        if self.tablero[0] == self.tablero[4] == self.tablero[8] != ' ':
            return True
        if self.tablero[2] == self.tablero[4] == self.tablero[6] != ' ':
            return True
        return False

    def tablero_lleno(self):
        return ' ' not in self.tablero

    def juego_terminado(self):
        return self.hay_ganador() or self.tablero_lleno()

    def resetear_juego(self):
        self.tablero = [' ']*9
        self.turno = self.jugador

    def movimiento_computadora_aleatorio(self):
        movimiento = random.choice([i for i, v in enumerate(self.tablero) if v == ' '])
        return movimiento

    def movimiento_computadora_defensivo(self):
        for i in range(9):
            if self.movimiento_valido(i):
                self.tablero[i] = self.computadora
                if self.hay_ganador():
                    self.tablero[i] = ' '
                    return i
                self.tablero[i] = ' '

        for i in range(9):
            if self.movimiento_valido(i):
                self.tablero[i] = self.jugador
                if self.hay_ganador():
                    self.tablero[i] = ' '
                    return i
                self.tablero[i] = ' '

        movimiento = random.choice([i for i, v in enumerate(self.tablero) if v == ' '])
        return movimiento

    def movimiento_computadora_ofensivo(self):
        for i in range(9):
            if self.movimiento_valido(i):
                self.tablero[i] = self.computadora
                if self.hay_ganador():
                    self.tablero[i] = ' '
                    return i
                self.tablero[i] = ' '

        for i in range(9):
            if self.movimiento_valido(i):
                self.tablero[i] = self.jugador
                if self.hay_ganador():
                    self.tablero[i] = ' '
                    return i
                self.tablero[i] = ' '

        esquinas = [0, 2, 6, 8]
        for i in esquinas:
            if self.movimiento_valido(i):
                return i
        
        if self.movimiento_valido(4):
            return 4
        
        laterales = [1, 3, 5, 7]
        for i in laterales:
            if self.movimiento_valido(i):
                return i

        movimiento = random.choice([i for i, v in enumerate(self.tablero) if v == ' '])
        return movimiento

class InterfazGato:
    def __init__(self, root):
        self.root = root
        self.root.title("Gato")

        self.variante = tk.StringVar(root)
        self.variante.set("Aleatorio")  # Valor predeterminado

        opciones = ["Aleatorio", "Defensivo", "Ofensivo"]
        menu = tk.OptionMenu(root, self.variante, *opciones)
        menu.grid(row=0, column=0)

        self.juego = Gato()
        
        self.botones = []
        for i in range(3):
            for j in range(3):
                boton = tk.Button(root, text='', font=('Helvetica', 20), width=4, height=2,
                                  command=lambda i=i, j=j: self.jugar(i*3 + j))
                boton.grid(row=i+1, column=j, padx=5, pady=5)
                self.botones.append(boton)

        self.actualizar_tablero()

    def jugar(self, movimiento):
        if self.juego.movimiento_valido(movimiento) and not self.juego.juego_terminado():
            self.juego.hacer_movimiento(movimiento)
            self.actualizar_tablero()
            if self.juego.hay_ganador():
                messagebox.showinfo("Fin del juego", "¡Has ganado!")
                self.juego.resetear_juego()
                self.actualizar_tablero()
            elif self.juego.tablero_lleno():
                messagebox.showinfo("Fin del juego", "¡Empate!")
                self.juego.resetear_juego()
                self.actualizar_tablero()
            else:
                variante = self.variante.get()
                if variante == "Aleatorio":
                    movimiento_computadora = self.juego.movimiento_computadora_aleatorio()
                elif variante == "Defensivo":
                    movimiento_computadora = self.juego.movimiento_computadora_defensivo()
                elif variante == "Ofensivo":
                    movimiento_computadora = self.juego.movimiento_computadora_ofensivo()

                self.juego.hacer_movimiento(movimiento_computadora)
                self.actualizar_tablero()
                if self.juego.hay_ganador():
                    messagebox.showinfo("Fin del juego", "¡Has perdido!")
                    self.juego.resetear_juego()
                    self.actualizar_tablero()
                elif self.juego.tablero_lleno():
                    messagebox.showinfo("Fin del juego", "¡Empate!")
                    self.juego.resetear_juego()
                    self.actualizar_tablero()

    def actualizar_tablero(self):
        for i in range(9):
            self.botones[i].config(text=self.juego.tablero[i])

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGato(root)
    root.mainloop()
