import random
from math import gcd

def generate_small_primes():
    """Danh sách số nguyên tố"""
    return [p for p in range(11, 1000) if all(p % i != 0 for i in range(2, int(p**0.5) + 1))]

def find_primitive_root(p):
    """Tìm phần tử nguyên thủy"""
    for g in range(2, p):
        if all(pow(g, (p-1)//f, p) != 1 for f in {2, (p-1)//2} if (p-1) % f == 0):
            return g
    return None

def generate_small_keys():
    """Sinh khóa công khai (p, g, y) và khóa bí mật x v"""
    small_primes = generate_small_primes()
    while True:
        p = random.choice(small_primes)
        g = find_primitive_root(p)
        if g is not None:
            break
    
    x = random.randint(2, p-2)
    y = pow(g, x, p)
    return (p, g, y), x

def encrypt_small(m, public_key):
    """Mã hóa số m < p"""
    p, g, y = public_key
    while True:
        k = random.randint(2, p-2)
        if gcd(k, p-1) == 1:
            break
    c1 = pow(g, k, p)
    c2 = (m * pow(y, k, p)) % p
    return (c1, c2)

def decrypt_small(cipher, private_key, p):
    """Giải mã """
    c1, c2 = cipher
    x = private_key
    s = pow(c1, x, p)
    return (c2 * pow(s, p-2, p)) % p

def text_to_blocks(text, block_size):
    """Chia văn bản thành các block ký tự"""
    return [text[i:i+block_size] for i in range(0, len(text), block_size)]

def block_to_number(block, max_value):
    """Chuyển block ký tự thành số < max_value"""
    num = 0
    for c in block:
        num = num * 256 + ord(c)
        if num >= max_value:
            raise ValueError("Block quá lớn so với p")
    return num

def number_to_block(num, length):
    """Chuyển số về block ký tự"""
    block = []
    for _ in range(length):
        block.insert(0, chr(num % 256))
        num = num // 256
    return ''.join(block)


def encrypt_text(text, public_key):
    """Mã hóa văn bản dài"""
    p, _, _ = public_key
    max_block_size = (p.bit_length() // 8) 
    blocks = text_to_blocks(text, max_block_size)
    
    encrypted_blocks = []
    for block in blocks:
        m = block_to_number(block, p)
        c1, c2 = encrypt_small(m, public_key)
        encrypted_blocks.append((c1, c2, len(block)))
    return encrypted_blocks

def decrypt_text(encrypted_blocks, private_key, p):
    """Giải mã văn bản dài"""
    decrypted_blocks = []
    for c1, c2, length in encrypted_blocks:
        m = decrypt_small((c1, c2), private_key, p)
        decrypted_blocks.append(number_to_block(m, length))
    return ''.join(decrypted_blocks)


if __name__ == "__main__":

    
    # Sinh khóa
    public_key, private_key = generate_small_keys()
    p, g, y = public_key
    print(f"\n[KHÓA CÔNG KHAI]")
    print(f"p = {p} ")
    print(f"g = {g} (phần tử nguyên thủy)")
    print(f"y = {y}")
    print(f"\n[KHÓA BÍ MẬT]\nx = {private_key}")

    text = input("\nNhập văn bản cần mã hóa: ")
    
    # Mã hóa
    try:
        encrypted = encrypt_text(text, public_key)
        print("\n[BẢN MÃ]")
        for i, (c1, c2, length) in enumerate(encrypted):
            print(f"Khối {i+1}: c1={c1}, c2={c2}, độ dài={length}")
        
        # Giải mã
        decrypted = decrypt_text(encrypted, private_key, p)
        print(f"\n[VĂN BẢN GIẢI MÃ]\n{decrypted}")
        
        # Kiểm tra
        if text == decrypted:
            print("\n Giải mã thành công!")
        else:
            print("\n Giải mã không khớp!")
    except ValueError as e:
        print(f"\nLỗi: {str(e)}")
        print("Hãy thử với văn bản ngắn hơn hoặc chọn khóa lớn hơn")