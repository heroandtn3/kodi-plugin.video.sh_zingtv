import unittest
import zing_tv
import zing_api


class TestCipher(unittest.TestCase):

    def setUp(self):
        self.a = "0IWOUZ6789ABCDEF"
        self.b = "0123456789abcdef"
        self.c = "GHmn|LZk|DFbv|BVd|ASlz|QWp|ghXC|Nas|Jcx|ERui|Tty|rIU|POwq|efK|Mjo".split('|')

    def test_replace_encrypt(self):
        for ia, ib in zip(self.a, self.b):
            self.assertEqual(zing_tv.replace_encrypt(ib), ia)


    def test_replace_decrypt(self):
        for ia, ib in zip(self.a, self.b):
            self.assertEqual(zing_tv.replace_decrypt(ia), ib)
        
    def test_replace_c(self):
        for i in range(len(self.c)):
            self.assertIn(zing_tv.replace_c(i), self.c[i])

    def test_replace_enum(self):
        for i, ci in enumerate(self.c):
            for cci in ci:
                self.assertEqual(zing_tv.replace_enum(cci), i)

        self.assertEqual(zing_tv.replace_enum('0'), -1)

    def test_cipher(self):
        pass
        #self.assertEqual(zing_tv.get_cipher('ZW6W8OOU', [10, 2, 0, 1, 0]), 'ZnJmtkmszBAAXvcTFmkH')

    def test_encrypt(self):
        self.assertEqual(zing_tv.encrypt(1382187828), "ZW6W8OOU")
        self.assertEqual(zing_tv.encrypt(307861704), "IWZ998C8")

    def test_decrypt(self):
        self.assertEqual(zing_tv.decrypt('ZW6W8OOU'), 1382187828)

    def test_decode_encoded_key(self):
        encoded_key = zing_tv.encoded_key('ZW6W8OOU')
        decoded_key = zing_tv.decode_key(encoded_key)
        self.assertEqual(decoded_key, 'ZW6W8OOU')

    def test_decoded_key(self):
        pass
        #self.assertEqual(zing_tv.decode_encoded_key('kHxmyLnaAsnHsLEtBXGybmkn'), 'ZW67FWWF')

    def test_encoded_key(self):
        pass


    def test_get_direct_link_id(self):
        pass
        #self.assertEqual(zing_tv.get_direct_link_id('IWZA0O0O'), 'LmcntlQhEitDHLn')

class TestAes(unittest.TestCase):

    def test_encrypt_aes(self):
        text = 'The answer is no'
        key = 'This is a key123'
        iv = 'This is an IV456'
        cipher_text = '\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'
        self.assertEqual(
            zing_tv.encrypt_aes(text=text, key=key, iv=iv), 
            cipher_text)

    def test_decrypt_aes(self):
        text = 'The answer is no'
        cipher_text = '\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'
        key = 'This is a key123'
        iv = 'This is an IV456'
        self.assertEqual(
            zing_tv.decrypt_aes(cipher=cipher_text, key=key, iv=iv), 
            text)


class ZingApiTests(unittest.TestCase):

    def test_genre_child_return_root_genre(self):
        res = zing_api.genre_child()
        self.assertEqual(res['total'], 1)

    def test_genre_child_78(self):
        res = zing_api.genre_child(78)
        self.assertIsNotNone(res.get('total'))

    def test_program_list_78(self):
        res = zing_api.program_list(78)
        self.assertIsNotNone(res.get('total'))

    def test_program_list_has_next_page(self):
        res = zing_api.program_list(78)
        self.assertIsNotNone(res.get('next'))

    def test_program_list_does_not_has_next_page(self):
        res = zing_api.program_list(78, page=200)
        self.assertIsNone(res.get('next'))

    def test_program_info_2573(self):
        res = zing_api.program_info(2573)
        self.assertEqual(res['response']['id'], 2573)

    def test_program_info_628(self):
        res = zing_api.program_info(628)
        self.assertEqual(res['response']['id'], 628)

    def test_series_medias_802(self):
        res = zing_api.series_medias(802)
        self.assertIsNotNone(res.get('total'))

if __name__ == '__main__':
    unittest.main()