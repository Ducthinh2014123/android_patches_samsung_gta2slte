from pathlib import Path
from struct import unpack_from, pack_into
from elftools.elf.elffile import ELFFile
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB

src = Path(
    "vendor/samsung/gta2slte/proprietary/vendor/"
    "lib/libperipheral_client.so"
)

dst = Path("/tmp/parcel-audit/libperipheral_client-patched.so")
data = bytearray(src.read_bytes())
ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)

with src.open("rb") as f:
    elf = ELFFile(f)
    text = elf.get_section_by_name(".text")
    exidx = elf.get_section_by_name(".ARM.exidx")

    text_addr = text["sh_addr"]
    text_off = text["sh_offset"]

    exidx_addr = exidx["sh_addr"]
    exidx_off = exidx["sh_offset"]
    exidx_size = exidx["sh_size"]

count = 0

def patch(addr, expected, instruction):
    global count

    off = text_off + addr - text_addr
    old = bytes.fromhex(expected)

    if data[off:off + len(old)] != old:
        raise RuntimeError(
            f"Unexpected bytes at {addr:#x}"
        )

    encoded, _ = ks.asm(instruction, addr)
    new = bytes(encoded)

    if len(new) != len(old):
        raise RuntimeError(
            f"Instruction size mismatch at {addr:#x}"
        )

    data[off:off + len(new)] = new
    count += 1

    print(
        f"{addr:#08x}: {old.hex()} -> "
        f"{new.hex()} | {instruction}"
    )

# Callback
patch(0x76e4, "9cb0", "sub sp, #0x80")
patch(0x76f6, "1b90", "str r0, [sp, #0x7c]")
patch(0x76f8, "0eac", "add r4, sp, #0x40")
patch(0x7746, "1b99", "ldr r1, [sp, #0x7c]")
patch(0x774c, "1cb0", "add sp, #0x80")

# Register
patch(0x78a0, "9eb0", "sub sp, #0x88")
patch(0x78b6, "1d90", "str r0, [sp, #0x84]")
patch(0x78b8, "10ac", "add r4, sp, #0x48")
patch(0x7926, "269a", "ldr r2, [sp, #0xa8]")
patch(0x7932, "279a", "ldr r2, [sp, #0xac]")
patch(0x7952, "1d99", "ldr r1, [sp, #0x84]")
patch(0x795a, "1eb0", "add sp, #0x88")

# Unregister, connect, disconnect, acknowledge
for base in (0x796c, 0x79f4, 0x7a7c, 0x7b04):
    extra = 8 if base == 0x7b04 else 0

    patch(base + 4, "9db0", "sub sp, #0x84")
    patch(base + 0x18, "1c90",
          "str r0, [sp, #0x80]")
    patch(base + 0x1a, "0fac",
          "add r4, sp, #0x44")
    patch(base + 0x6e + extra, "1c99",
          "ldr r1, [sp, #0x80]")
    patch(base + 0x76 + extra, "1db0",
          "add sp, #0x84")

# Acknowledge incoming argument
patch(0x7b44, "2499", "ldr r1, [sp, #0xa0]")

# Shutdown
patch(0x7b96, "9db0", "sub sp, #0x84")
patch(0x7ba2, "1c90", "str r0, [sp, #0x80]")
patch(0x7ba4, "0fac", "add r4, sp, #0x44")
patch(0x7bea, "1c99", "ldr r1, [sp, #0x80]")
patch(0x7bf2, "1db0", "add sp, #0x84")

print("\n===== ARM UNWIND =====")

def prel31(word):
    value = word & 0x7fffffff
    if value & 0x40000000:
        value -= 0x80000000
    return value

frames = {
    0x76e0: 112,
    0x789c: 120,
    0x796c: 116,
    0x79f4: 116,
    0x7a7c: 116,
    0x7b04: 116,
    0x7b94: 116,
}

entries = []

for i in range(0, exidx_size, 8):
    off = exidx_off + i
    fn, unwind = unpack_from("<II", data, off)
    addr = exidx_addr + i + prel31(fn)
    entries.append((addr, off, unwind))

covered = set()

for i, (addr, off, unwind) in enumerate(entries):
    end = (
        entries[i + 1][0]
        if i + 1 < len(entries)
        else 0xffffffff
    )

    affected = [
        fn for fn in frames
        if addr <= fn < end
    ]

    if not affected:
        continue

    if addr not in frames:
        raise RuntimeError(
            f"Unexpected shared unwind at {addr:#x}"
        )

    if unwind >> 24 != 0x80:
        raise RuntimeError(
            f"Unsupported unwind format at {addr:#x}"
        )

    opcode = (unwind >> 16) & 0xff
    expected = frames[addr] // 4 - 1

    if opcode != expected:
        raise RuntimeError(
            f"Unexpected unwind opcode at {addr:#x}: "
            f"{opcode:#x}, expected {expected:#x}"
        )

    if any(frames[fn] != frames[addr] for fn in affected):
        raise RuntimeError("Mixed stack sizes")

    new = (
        (unwind & 0xff00ffff)
        | ((opcode + 4) << 16)
    )

    pack_into("<I", data, off + 4, new)
    covered.update(affected)

    print(
        f"{addr:#08x}: {unwind:#010x} "
        f"-> {new:#010x}"
    )

if covered != set(frames):
    raise RuntimeError("Incomplete unwind coverage")

dst.write_bytes(data)

print("\n===== SUCCESS =====")
print("Instructions patched:", count)
print("Output:", dst)
print("Original file unchanged")
