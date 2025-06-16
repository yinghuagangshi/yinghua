"""
@User:  slg
@Time: 2022/8/27
@Remark: GmSSL支持SM2/SM3/SM4等国密算法
pip install gmssl
"""

#import base64
#import binascii
from gmssl import sm2, func, sm3
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT



# SM2算法
class crypt_sm2:
    """
    国密SM2算法的Python实现， 提供了 encrypt、 decrypt等函数用于加密解密
    """
    def __init__(self, private_key ="", public_key = ""):
        """
        private_key: 16进制的私钥
        public_key: 16进制的公钥
        """
        if len(private_key) > 0:
            self._private_key = private_key
        else:
            self._private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'

        if len(public_key) > 0:
            self._private_key = public_key
        else:
            self._public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

        # 初始化CryptSM2，生成或传入密钥对
        self.sm2_crypt = sm2.CryptSM2(public_key=self._public_key, private_key=self._private_key)


    # encrypt
    def encrypt(self, data):
        """
        返回byes类型加密后的数据
        data: bytes类型的数据        
        """       
        enc_data = self.sm2_crypt.encrypt(data)
        return enc_data


    # decrypt
    def decrypt(self, data):
        """
        返回byes类型解密后的数据
        data: bytes类型的数据,        
        """
        dec_data = self.sm2_crypt.decrypt(data)
        return dec_data


    # random_hex
    def random_hex(self):
        random_hex_str = func.random_hex(self.sm2_crypt.para_len)
        return random_hex_str

    
    # sign 签名函数
    def sign(self, data, random_hex_str):
        """
        返回签名的数据
        data: bytes类型的数据
        random_hex_str:16进制的字符串
        """
        signData = self.sm2_crypt.sign(data, random_hex_str) #  16进制
        return signData


    # verify 验签函数
    def verify(self, sign, data):
        """
        sign: 签名,bytes类型的数据
        data: bytes类型的数据
        """
        return self.sm2_crypt.verify(sign, data)


    # sign_with_sm3
    def sign_with_sm3(self, data):
        """
        返回16进制字符串
        data: bytes类型的数据
        """
        # sign = self.sm2_crypt.sign_with_sm3(data)
        random = self.random_hex()
        hash_data = sm3_hash(data)
        str_b = bytes(hash_data, encoding='utf-8')    
        return self.sign(str_b, random)
    

    # verify_with_sm3
    def verify_with_sm3(self, sign, data):            
        """
        sign: bytes类型的数据
        data: bytes类型的数据
        """
        hash_data = sm3_hash(data)
        str_b = bytes(hash_data, encoding='utf-8')
        
        return self.verify(sign, str_b)

    
# SM3算法，SM3 是中国国家密码管理局发布的 密码哈希算法，输出固定为 256 位（32 字节），通常以 64 位 16 进制字符串 表示
def sm3_hash(msg):
    """
    返回16进制字符串
    msg:字符串
    """
    str_b = bytes(msg, encoding='utf-8')    
    return sm3.sm3_hash( func.bytes_to_list(str_b) )

# 基于 SM3 的密钥派生函数，从密码生成密钥
def sm3_kdf(msg, klen):
    """
    返回16进制字符串
    msg:字符串
    klen为密钥长度（单位byte）,如：16，32, 64等
    """
    str_b = bytes(msg, encoding='utf-8')
    return sm3.sm3_kdf(str_b, klen)


# SM4算法
class crypt_sm4:
    def __init__(self):
        self._key = b'3l5butlj26hvv313'
        self._iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' # bytes类型
        self.sm4 = CryptSM4()

        
    def set_key(self, key):
        """ key:bytes类型的数据 """
        self._key = key

    # ECB 模式
    def encrypt_ecb(self, data):
        """
        SM4-ECB encryption
        :param data: bytes类型的数据 
        """ 
        self.sm4.set_key(self._key, SM4_ENCRYPT)
        return self.sm4.crypt_ecb(data)


    def decrypt_ecb(self, data):
        """
        SM4-ECB decryption
        :param data: bytes类型的数据 
        
        """ 
        self.sm4.set_key(self._key, SM4_DECRYPT)
        return self.sm4.crypt_ecb(data)
        
    # CBC 模式
    def encrypt_cbc(self, data, iv = []):
        """
        SM4-CBC encryption
        :param data: bytes类型的数据        
        :param iv: 长度为16偏移量
        """
        self.sm4.set_key(self._key, SM4_ENCRYPT)
        if len(iv) < 1:
            return self.sm4.crypt_cbc(self._iv, data)
        else:
            return self.sm4.crypt_cbc(iv, data)


    def decrypt_cbc(self, data, iv = []):
        """
        SM4-CBC decryption
        :param data: bytes类型的数据        
        :param iv: 长度为16偏移量
        """
        self.sm4.set_key(self._key, SM4_DECRYPT)
        if len(iv) < 1:
            return self.sm4.crypt_cbc(self._iv, data)
        else:
            return self.sm4.crypt_cbc(iv, data)



# SM4 加密前对数据进行填充（16进制字符串）：如果text不足16位的倍数，就用"00"补足，即采用NoPadding方式补齐
def PKCS_zero(text):
    newbytes = '00'
    if len(text) % 32:
        add = 32 - (len(text) % 32)
        add = add >> 1
    else:
        add = 0
    text = text + newbytes * add
    return text
