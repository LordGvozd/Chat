import random


def encrypt(text, key):
    return cezar_encrypt(text, symbols, key)


def decrypt(text, key):
    return cezar_decrypt(text, symbols, key)


symbols = r' !#$%&\'()*+",-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~' \
          r'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàá' \
          r'âãäåæçèéêëìíîïð'


def cezar_encrypt(text, abc, key):

    new_abc = cezar_abc_create(abc, key)

    encrypt_message = ""

    count = -1
    for symbol in text:
        index = 0
        count += 1
        for abc_symbol in new_abc:

            if symbol == abc_symbol:

                encrypt_message += str(index)
                if count < len(text) - 1:
                    encrypt_message += ","
                break
            index += 1
    return encrypt_message


def cezar_decrypt(text, abc, key):
    new_abc = cezar_abc_create(abc, key)

    decrypted_message = ""

    for decrypted_symbol in text.split(","):

        decrypted_message += new_abc[int(decrypted_symbol)]
    return decrypted_message


def cezar_abc_create(abc, key):
    new_abc = ""
    for s in range(len(abc)):
        index = s - key
        if index < len(abc):
            new_abc += abc[index]
        else:
            new_abc += abc[index - len(abc)]
    return new_abc


def cezar_generate_key():
    return random.randint(1, 32)


if __name__ == "__main__":
    encr = cezar_encrypt(input(": "), symbols, 2)
    decr = cezar_decrypt(encr, symbols, 2)

    print(encr)
    print(decr)
