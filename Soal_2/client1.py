import socket
import threading

# configurasi ke server
HOST = '127.0.0.1'
PORT = 55555

# Input nickname agar chat lebih seru 
nickname = input("Masukan Nickname Anda : ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    """
    Tugasnya terus menerus dan mendengarkan pesan dari server
    """

    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                # jika server minta nickname. kirimkan
                client.send(nickname.encode('ascii'))
            else:
                # jika pesan biasa, tampilkan 
                print(message)
        except:
            print("Terjadi kesalahan! koneksi ditutup.")
            client.close()
            break

def write():
    """
    Tugas : Terus menerus menunggu input user untuk dikirim
    """
    while True:
        # Format pesan: "Budi: Halo semua"
        text = input("")
        message = f'{nickname}: {text}'
        client.send(message.encode('ascii'))

# Menjalankan Thread Mendengar
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Menjalankan Thread Menulis
write_thread = threading.Thread(target=write)
write_thread.start()