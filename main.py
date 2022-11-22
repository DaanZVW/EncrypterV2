from core.driver.exporter import exporter
from core.driver.encrypter import encrypter

from core.helpers.ascii_scope import ascii_scope, asciiSetting
from core.helpers.scrambler import scrambler, scrambleSetting

from core.models.enigma import enigma, enigmaRotor
from core.models.swap import swap, swapSetting
from core.models.shift import shift


if __name__ == '__main__':
    encrypt = encrypter()

    ascii_setting = ascii_scope(asciiSetting.printable)
    encrypt.addModel(
        enigma(
            ascii_setting,
            [enigmaRotor(len(ascii_setting), scrambler=scrambler()),
             enigmaRotor(len(ascii_setting), scrambler=scrambler()),
             enigmaRotor(len(ascii_setting), scrambler=scrambler())]
        )
    )
    encrypt.addModel(
        shift(5, ascii_scope(asciiSetting.printable), scrambler())
    )
    encrypt.addModel(
        swap(swapSetting.random, scrambler=scrambler())
    )
    encrypt.addModel(
        swap(swapSetting.reverse, 5)
    )

    msg = 'This is a test message which should be encrypted and decrypted correctly'
    a = encrypt.encrypt(msg)
    print(a.encode('utf-8'))

    export = exporter()
    export.exportEncrypter(encrypt, 'test', overwrite=True)
    n_encrypt = export.importEncrypter('test')

    a = n_encrypt.decrypt(a)
    print(a)


