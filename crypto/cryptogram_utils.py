from Crypto.Cipher import AES
import base64
import random
import hashlib

BLOCK_SIZE = 16  # Bytes

unpad = lambda date: date[0:-ord(date[len(date) - 1:])]


def pad(text):
    """
    #填充函数，使被加密数据的字节码长度是block_size的整数倍
    """
    count = len(text.encode('utf-8'))
    add = BLOCK_SIZE - (count % BLOCK_SIZE)
    entext = text + (chr(add) * add)
    return entext


def aes_encrypt(key, data):
    '''
    AES的ECB模式加密方法
    :param key: 密钥
    :param data:被加密字符串（明文）
    :return:密文
    '''
    key = key.encode('utf8')
    # 字符串补位
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf8')
    #    print(enctext) #打印输出密文
    return enctext


def aes_decrypt(key, data):
    '''
    :param key: 密钥
    :param data: 加密后的数据（密文）
    :return:明文
    '''
    key = key.encode('utf8')
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)

    # 去补位
    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode('utf8')
    print(text_decrypted)
    return text_decrypted


def gen_secret_key(key_len):
    # 1、先指定字符集，字符集中包括数字、大小写字母、特殊符号：
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # 2、从指定的字符集中随机取，分别取8位，组合成新字符串
    str1 = []
    for i in range(key_len):
        str1.append(random.choice(seed))
    secret_key = ''.join(str1)
    # print(secret_key)
    return secret_key


def sha512(value):
    """
    https://docs.python.org/zh-cn/3/library/hashlib.html
    信息摘要 用于身份验证
    :param value:  信息
    :return:  hash之后的寄过
    """
    m = hashlib.sha256()
    m.update(value.encode('utf-8'))
    return m.hexdigest()


if __name__ == '__main__':
    key = gen_secret_key(16)
    data = 'cGdVHMqI/lw6Nj7gahM5gH4xlpaQ33bzUeQEcWbA3j3ZC02Ek92HAnwtgWUSTzibrUOurAMD9BY17k+x3PDwOA=='
    endata = aes_encrypt(key, data)
    print(endata)
