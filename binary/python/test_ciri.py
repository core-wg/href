import ciri, unittest, testvectors

class TestCiri(unittest.TestCase):

  def test_is_well_formed(self):
    for i in testvectors. ABSOLUTE:
      with self.subTest(input=i):
        self.assertTrue(ciri.is_well_formed(i))
    for i in testvectors.RELATIVE:
      with self.subTest(input=i):
        self.assertTrue(ciri.is_well_formed(i))
    for (b, i, e) in testvectors.RESOLVED:
      with self.subTest(input=b):
        self.assertTrue(ciri.is_well_formed(b))
      with self.subTest(input=i):
        self.assertTrue(ciri.is_well_formed(i))
      with self.subTest(input=e):
        self.assertTrue(ciri.is_well_formed(e))

  def test_is_absolute(self):
    for i in testvectors.ABSOLUTE:
      with self.subTest(input=i):
        self.assertTrue(ciri.is_absolute(i))
    for i in testvectors.RELATIVE:
      with self.subTest(input=i):
        self.assertFalse(ciri.is_absolute(i))
    for (b, i, e) in testvectors.RESOLVED:
      with self.subTest(input=b):
        self.assertTrue(ciri.is_absolute(b))
      with self.subTest(input=e):
        self.assertTrue(ciri.is_absolute(e))
   
  def test_is_relative(self):
    for i in testvectors.ABSOLUTE:
      with self.subTest(input=i):
        self.assertFalse(ciri.is_relative(i))
    for i in testvectors.RELATIVE:
      with self.subTest(input=i):
        self.assertTrue(ciri.is_relative(i))
    for (b, i, e) in testvectors.RESOLVED:
      with self.subTest(input=b):
        self.assertFalse(ciri.is_relative(b))
      with self.subTest(input=e):
        self.assertFalse(ciri.is_relative(e))
   
  def test_resolve(self):
    for (b, i, e) in testvectors.RESOLVED:
      with self.subTest(base=b, href=i, expected=e):
        self.assertEqual(e, ciri.resolve(b, i, 9000))

  def test_recompose(self):
    for i in testvectors.ABSOLUTE:
      with self.subTest(input=i):
        self.assertIsNotNone(ciri.recompose(i))

  def test_coap(self):
    for i in testvectors.ABSOLUTE:
      with self.subTest(input=i):
        self.assertIsNotNone(ciri.coap(i))

if __name__ == "__main__":
  unittest.main()
