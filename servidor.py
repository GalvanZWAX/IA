import socket
import threading

class Servidor:
    def __init__(self, host='localhost', port=65432):
        self.HOST = host
        self.PORT = port
        self.condiciones_iniciales()

    def condiciones_iniciales(self):
        # Definir las condiciones iniciales del juego
        self.juego_terminado = False
        self.mensaje_inicial = "No siento nada"  # Mensaje inicial para el cliente
        self.mensajes = {
            "inicial": self.mensaje_inicial,
            "perdiste": "Perdiste",
            "ganaste": "¡Has ganado!"
        }

    def manejar_cliente(self, conexion, direccion):
        print(f"Conectado a {direccion}")
        conexion.sendall(self.mensajes["inicial"].encode('utf-8'))

        while not self.juego_terminado:
            datos = conexion.recv(1024).decode('utf-8')
            if not datos:
                break
            print(f"Recibido de {direccion}: {datos}")
            
            # Procesar la acción recibida
            if datos.startswith("Avanzar"):
                # Lógica de procesamiento de la acción
                if "ganar" in datos:
                    self.juego_terminado = True
                    conexion.sendall(self.mensajes["ganaste"].encode('utf-8'))
                else:
                    conexion.sendall(self.mensaje_inicial.encode('utf-8'))
            else:
                self.juego_terminado = True
                conexion.sendall(self.mensajes["perdiste"].encode('utf-8'))
                
        conexion.close()
        print(f"Conexión con {direccion} cerrada")

    def iniciar(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            print(f"Servidor escuchando en {self.HOST}:{self.PORT}")

            while True:
                conexion, direccion = s.accept()
                threading.Thread(target=self.manejar_cliente, args=(conexion, direccion)).start()

if __name__ == '__main__':
    servidor = Servidor()
    servidor.iniciar()
