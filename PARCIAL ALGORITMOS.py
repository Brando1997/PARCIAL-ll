import threading
import time
import random
import queue

BARBEROS = 1
CLIENTES = 20
ASIENTOS = 4
ESPERAS = 1

def espera():
    time.sleep(ESPERAS * random.random())

class Barbero(threading.Thread):
    condicion = threading.Condition()
    alto_completo = threading.Event()

    def __init__(self, ID):
        super().__init__()
        self.ID = ID

    def run(self):
        while True:
            try:
                cliente_actual = sala_espera.get(block=False)
            except queue.Empty:
                if self.alto_completo.is_set():
                    return

                print(f"El barbero {self.ID} esta dormido... Zzz... Zzz... ")
                with self.condicion:
                    self.condicion.wait()
            else:
                cliente_actual.cortar(self.ID)

class Cliente(threading.Thread):
    DURACION_CORTE = 4

    def __init__(self, ID):
        super().__init__()
        self.ID = ID

    def corte(self):
        time.sleep(self.DURACION_CORTE * random.random())
    
    def cortar(self, id_barbero):
        print(f"El barbero {id_barbero} le esta cortando el pelo al cliente {self.ID}")
        self.corte()
        print(f"El Barbero {id_barbero} termino de cortarle el pelo al cliente {self.ID}")
        self.atendido.set()

    def run(self):
        self.atendido = threading.Event()

        try:
            sala_espera.put(self, block=False)
        except queue.Full:
            print(f"Todos los asientos estan llenos, {self.ID} el cliente se fue...")
            return

        print(f"El cliente {self.ID} se sento en una silla.")
        with Barbero.condicion:
            Barbero.condicion.notify(1)

        self.atendido.wait()


if __name__== "__main__":
    TODOS_CLIENTES = []
    sala_espera = queue.Queue(ASIENTOS)
    
    for i in range(BARBEROS):
        hilo_barbero = Barbero(i)
        hilo_barbero.start()

    for i in range(CLIENTES):
        espera()
        cliente = Cliente(i)
        TODOS_CLIENTES.append(cliente)
        cliente.start()

    for cliente in TODOS_CLIENTES:
        cliente.join()

    time.sleep(0.1)
    Barbero.alto_completo.set()
    with Barbero.condicion:
        Barbero.condicion.notify_all()

    print("La Barberia a cerrado gracias por venir.")

    














                
