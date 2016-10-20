# forge-crc64
The script for generating a string with given prefix and CRC64 value.
One of standard CRC-64-ECMA polynomials is used. Table is generated, so you can change the polynomial.

Usage:
```
./forge_crc64.py CRC64-sum [prefix]
```

Example:
```
> python forge_crc64.py 0x3d86b93fd6454496 asd
STR: 61736402abeafa467430a0
CRC: 3d86b93fd6454496
CRC: f80d3ed95322a1c3
```