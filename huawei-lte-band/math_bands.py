meaning_bands_list = [
    ('b1', 'FDD 2100 Mhz'),
    ('b2', 'FDD 1900 Mhz'),
    ('b3', 'FDD 1800 Mhz'),
    ('b4', 'FDD 1700 Mhz'),
    ('b5', 'FDD 850 Mhz'),
    ('b6', 'FDD 800 Mhz'),
    ('b7', 'FDD 2600 Mhz'),
    ('b8', 'FDD 900 Mhz'),
    ('b19', 'FDD 850 Mhz'),
    ('b20', 'FDD 800 Mhz'),
    ('b26', 'FDD 850 Mhz'),
    ('b28', 'FDD 700 Mhz'),
    ('b32', 'FDD 1500 Mhz'),
    ('b38', 'TDD 2600 Mhz'),
    ('b40', 'TDD 2300 Mhz'),
    ('b41', 'TDD 2500 Mhz'),
]

bands_list = [band for band, meaning in meaning_bands_list]
meaning_bands_dict = {band: meaning for band, meaning in meaning_bands_list}
bands_ui_dict = {band: f'{band.upper()}: {meaning_bands_dict[band]}' for band in bands_list}

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
