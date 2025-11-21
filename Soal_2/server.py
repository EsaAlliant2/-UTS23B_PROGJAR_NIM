import socket
import threading

# konfigurasi server
HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# List untuk menampung semua koneksi client yang aktif
clients = [] 
nicknames = []

def broadcast(message, pengirim_socket=None):
    """
    Mengirim pesan ke SEMUA client kecuali pengirimnya sendiri.
    """
    for client in clients:
        # Jika tidak ingin pesan balik ke pengirim, uncoment baris if
        # client != pengirim_socket:

        try:
            client.send(message)
        except:
            # jika gagal mengirim ( misal client putus tiba tiba ),  lewati
            client.close()
            # Penghapusan client akan ditangani fungsi handle()

def handle(client):
    """
    Fungsi ini berjalan dalam thread terpisah untuk SETIAP clien.
    Tugasnya hanya mendengarkan pesan dari client tersebut
    """
    while True:
        try:
            # 1. terima pesan dari client
            message = client.recv(1024)
        
            # sebarkan ke semua orang(broadcast)
            broadcast(message, client)

        except:
            # Jika ada error (client disconet ), hapus dari list dan tutup thread
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                print(f"[SERVER] {nickname} terputus.")
                broadcast(f"{nickname} telah meninggalkan chat ".encode('ascii')) 
                nickname.remove(nickname)
                break

def receive():
    """
    Fungsi utama untuk menerima koneksi baru 
    """

    print(f"[SERVER] Chat server berjalan di {HOST}:{PORT}...")
    
    while True:
        # menerima koneksi baru 
        client, address = server.accept()
        print(f"[SERVER] Terhubung dengan {str(address)}")

        # Meminta nickname (protokol sederhana: client kirim nickname terlebih dahulu)
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)

        print(f"[ SERVER ] Nickname client ini adalah {nickname}")
        broadcast(f"{nickname} bergabung dalam chat!.".encode('ascii'))
        client.send('Terhubung ke server!'.encode('ascii'))

        # Membuat thread nbaru untuk client ini
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()