from binascii import hexlify


def filenames_from_dir(dirfile):
    with open(dirfile, "rb") as data:
        header = data.read(4)
        text = data.read().decode('utf-16-le')
    # print(hexlify(header))
    # print(text)
    lines = text.split("\n")
    lines = [l.strip() for l in lines]
    lines = [l for l in lines if l.startswith("-a")]
    lines = [" ".join(l.split()[5:]) for l in lines]
    return set(lines)


clean = filenames_from_dir("ppp2.txt")

old = filenames_from_dir("test.txt")

remove = (old - clean)
for l in remove:
    print(f'cp "{l}" ..')
