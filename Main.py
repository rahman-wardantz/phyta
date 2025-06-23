import time
from responses import responses

def main():
    # Simpan waktu mulai ketika percakapan dimulai
    start_time = time.time()
    print("Selamat datang di Phyta bot!")
    
    while True:
        user_input = input("Kamu: ").lower()
        if user_input in ['exit', 'quit']:
            print("Phyta: Keluar dari program dalam 3 detik...")
            time.sleep(3)
            # Hitung waktu percakapan hingga titik keluar
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            print(f"Phyta: Total waktu percakapan kamu adalah {elapsed_time} detik.")
            print("Phyta: Sampai jumpa!")
            break

        respon_ditemukan = False
        for keyword, reply in responses.items():
            if keyword in user_input:
                print(f"Phyta: {reply}")
                respon_ditemukan = True
                break
        
        if not respon_ditemukan:
            print(f"Phyta: Kamu mengatakan '{user_input}'")

if __name__ == "__main__":
    main()