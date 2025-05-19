import random
from math import gcd


def is_prime(n, k=5):
    """Kiểm tra số nguyên tố bằng Miller-Rabin"""
    if n <= 1: return False
    elif n <= 3: return True
    elif n % 2 == 0: return False
    
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def generate_prime(bit_length=512):
    """Sinh số nguyên tố lớn"""
    while True:
        p = random.getrandbits(bit_length)
        if p % 2 != 0 and is_prime(p): return p

def extended_gcd(a, b):
    """Thuật toán Euclid mở rộng"""
    if a == 0: return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Tính nghịch đảo modulo"""
    g, x, y = extended_gcd(a, m)
    if g != 1: raise ValueError("Không tồn tại nghịch đảo")
    else: return x % m


def text_to_blocks(text, max_bits):
    """Chia văn bản UTF-8 thành các block nhị phân"""
    max_bytes = (max_bits // 8) - 1 
    encoded = text.encode('utf-8')
    return [encoded[i:i+max_bytes] for i in range(0, len(encoded), max_bytes)]

def blocks_to_text(blocks):
    """Ghép các block nhị phân thành văn bản gốc"""
    return b''.join(blocks).decode('utf-8', errors='strict')

def generate_keys(bit_length=512):
    """Sinh khóa công khai (p, g, y) và khóa bí mật x"""
    p = generate_prime(bit_length)
    g = random.randint(2, p-2)
    x = random.randint(2, p-2)
    y = pow(g, x, p)
    return (p, g, y), x

def encrypt_block(block, public_key):
    """Mã hóa 1 block binary"""
    p, g, y = public_key
    m = int.from_bytes(block, 'big')
    
    if m >= p:
        raise ValueError("Block quá lớn so với p")
    
    k = random.randint(2, p-2)
    while gcd(k, p-1) != 1:
        k = random.randint(2, p-2)
    
    c1 = pow(g, k, p)
    c2 = (m * pow(y, k, p)) % p
    return (c1, c2)

def decrypt_block(cipher, private_key, p):
    """Giải mã 1 block"""
    c1, c2 = cipher
    x = private_key
    s = pow(c1, x, p)
    m = (c2 * modinv(s, p)) % p
    return m.to_bytes((m.bit_length() + 7) // 8, 'big')

def main():
    
    
    # Sinh khóa
    bit_length = int(input("\nNhập độ dài khóa (bit, tối thiểu 512): ") or "512")
    public_key, private_key = generate_keys(bit_length)
    p, g, y = public_key
    
    print(f"\n[KHÓA CÔNG KHAI]\np = {p}\ng = {g}\ny = {y}")
    print(f"\n[KHÓA BÍ MẬT]\nx = {private_key}")
    
    
    text = input("\nNhập văn bản cần mã hóa: ")
    
    # Mã hóa
    try:
        encrypted = encrypt_text(text, public_key)
        print("\n[BẢN MÃ]")
        for i, (c1, c2) in enumerate(encrypted):
            print(f"Khối {i+1}: c1={c1}\nc2={c2}\n")
        
        # Giải mã
        decrypted = decrypt_text(encrypted, private_key, p)
        print(f"\n[VĂN BẢN GIẢI MÃ]\n{decrypted}")
        
        # Kiểm tra
        if text == decrypted:
            print("\n Kết quả: Giải mã chính xác!")
        else:
            print("\n Lỗi: Giải mã không khớp!")
    except ValueError as e:
        print(f"\n Lỗi: {str(e)}")
        print("Gợi ý: Giảm độ dài văn bản hoặc tăng kích thước khóa")

def encrypt_text(text, public_key):
    """Mã hóa toàn bộ văn bản"""
    p, _, _ = public_key
    blocks = text_to_blocks(text, p.bit_length())
    return [encrypt_block(block, public_key) for block in blocks]

def decrypt_text(encrypted_blocks, private_key, p):
    """Giải mã toàn bộ văn bản"""
    decrypted_blocks = [decrypt_block(cipher, private_key, p) for cipher in encrypted_blocks]
    return blocks_to_text(decrypted_blocks)

if __name__ == "__main__":
    while True:
        main()
       
  