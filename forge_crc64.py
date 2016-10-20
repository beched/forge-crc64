import sys

# CRC-64-ECMA polynomial
polynomial = 0xC96C5795D7870F42
table_forward = [0] * 256

def populate_table():
    for i in xrange(256):
        crc = i
        for j in xrange(8):
            if crc & 1:
                crc >>= 1
                crc ^= polynomial
            else:
                crc >>= 1
        table_forward[i] = crc

def crc64(s, crc=0):
    for c in s:
        crc = table_forward[(crc & 0xff) ^ ord(c)] ^ (crc >> 8) & 0xFFFFFFFFFFFFFFFF
    return crc

def help():
    print 'Usage: ./%s CRC64-sum [prefix]' % sys.argv[0]
    quit()

def forge_crc64(to_forge, header):
    # Build reverse table
    table_reverse = [0] * 256

    for i in xrange(256):
        table_reverse[crc64(chr(i)) >> 56] = crc64(chr(i))

    # Reverse CRC
    prev_crc = to_forge
    rev_crc = []

    for i in xrange(8):
        high_bits = prev_crc >> 56
        prev_crc ^= table_reverse[high_bits] # xor with left operand
        prev_crc <<= 8 # adjust right operand
        rev_crc.append(high_bits)

    # Build CRC
    result = ''
    header_crc = crc64(header)
    cur_high_bits = header_crc >> 56

    for rev_byte in rev_crc[::-1]:
        recovered = table_forward.index(table_reverse[rev_byte]) ^ cur_high_bits
        cur_high_bits = crc64(result + chr(recovered), header_crc) & 0xFF
        result += chr(recovered)
    result = header + result

    print 'STR:', result.encode('hex')
    print 'CRC:', hex(crc64(result)).lstrip('0x').rstrip('L')
    print 'CRC:', hex(crc64('\x80')).lstrip('0x').rstrip('L')
    #print 'OLD:', hex(to_forge)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        help()
    populate_table()
    header = ''
    if len(sys.argv) > 2:
        header = sys.argv[2]
    try:
        to_forge = int(sys.argv[1])
    except:
        to_forge = int(sys.argv[1], 16)
    forge_crc64(to_forge, header)