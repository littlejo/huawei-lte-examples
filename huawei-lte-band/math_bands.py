bands_list = [
    'b1',
    'b2',
    'b3',
    'b4',
    'b5',
    'b6',
    'b7',
    'b8',
    'b19',
    'b20',
    'b26',
    'b28',
    'b32',
    'b38',
    'b40',
    'b41',
]

hex_band_list = [hex(2 ** (int(band.replace('b', '')) - 1)) for band in bands_list][::-1]

def convert_hex_band(num_hex):
    band_num = str(bin(int(num_hex, 0))[2:]).count('0') + 1
    return 'b%s' %band_num

def convert_bands_hex2list(num_hex):
    res_list = []
    num_int = int(num_hex, 16)
    for hex_band in hex_band_list:
        int_band = int(hex_band, 0)
        if num_int >= int_band:
            res_list.append(convert_hex_band(hex_band))
            num_int -= int_band
    return res_list

def convert_bands_list2hex(bands_list):
    res_int = 0
    for band in bands_list:
        power = int(band.replace('b', '')) - 1
        res_int += 2 ** power
    return str(hex(res_int)).replace('0x', '')
