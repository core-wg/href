import ciri, itertools, unittest
from ciri import Option


class CiriComponents:
  
  def __init__(self, href):
    self.scheme = [x for x in href if x[0] == Option.SCHEME]
    self.authority = [x for x in href if x[0] in (Option.HOST_NAME, Option.HOST_IP, Option.PORT)]
    self.path = [x for x in href if x[0] in (Option.BASE_PATH, Option.PATH)]
    self.query = [x for x in href if x[0] == Option.QUERY]
    self.fragment = [x for x in href if x[0] == Option.FRAGMENT]

    if len(self.scheme) and self.path == [(Option.PATH, '')]:
      self.path = []
  
  def __iter__(self):
    yield from self.scheme
    yield from self.authority
    yield from self.path
    yield from self.query
    yield from self.fragment


def is_wellformed(href):
  i = 0
  if i < len(href) and href[i][0] == Option.SCHEME:
    i += 1
    if i < len(href) and href[i][0] in (Option.HOST_NAME, Option.HOST_IP):
      i += 1
      if i < len(href) and href[i][0] == Option.PORT:
        i += 1
  elif i < len(href) and href[i][0] in (Option.HOST_NAME, Option.HOST_IP):
    i += 1
    if i < len(href) and href[i][0] == Option.PORT:
      i += 1
  elif i < len(href) and href[i][0] == Option.BASE_PATH:
    i += 1
  while i < len(href) and href[i][0] == Option.PATH:
    i += 1
  while i < len(href) and href[i][0] == Option.QUERY:
    i += 1
  if i < len(href) and href[i][0] == Option.FRAGMENT:
    i += 1
  if i < len(href):
    return False

  return True


def is_absolute(href):
  if not is_wellformed(href):
    return False
  return len(href) and href[0][0] == Option.SCHEME


def is_relative(href):
  if not is_wellformed(href):
    return False
  return not len(href) or href[0][0] != Option.SCHEME


def resolve(base, href):
  if not is_absolute(base) or not is_wellformed(href):
    return None

  Base = CiriComponents(base)
  R = CiriComponents(href)
  T = CiriComponents([])

  if len(R.scheme):
    T.scheme = R.scheme
    T.authority = R.authority
    T.path = R.path
    T.query = R.query
  else:
    if len(R.authority):
      T.authority = R.authority
      T.path = R.path
      T.query = R.query
    else:
      if not len(R.path):
        T.path = Base.path
        if len(R.query):
          T.query = R.query
        else:
          T.query = Base.query
      else:
        if R.path[0][0] != Option.BASE_PATH:
          T.path = R.path
        else:
          T.path = Base.path[:max(0, len(Base.path) - R.path[0][1])] + R.path[1:]
        T.query = R.query
      T.authority = Base.authority
    T.scheme = Base.scheme
  T.fragment = R.fragment
  
  if T.path == [(Option.PATH, '')]:
    T.path = []
  return list(T)


expansions = [
  lambda v: (Option.SCHEME, chr(v)),
  lambda v: (Option.HOST_NAME, chr(v)),
  lambda v: (Option.HOST_IP, bytes([192, 168, 0, v])),
  lambda v: (Option.PORT, v * 0x101),
  lambda v: (Option.BASE_PATH, 0),
  lambda v: (Option.BASE_PATH, 1),
  lambda v: (Option.BASE_PATH, 2),
  lambda v: (Option.BASE_PATH, 3),
  lambda v: (Option.BASE_PATH, 4),
  lambda v: (Option.PATH, ''),
  lambda v: (Option.PATH, chr(v)),
  lambda v: (Option.QUERY, chr(v)),
  lambda v: (Option.FRAGMENT, chr(v)),
]


def expand(n, start=0):
  for i in range(len(n)):
    yield expansions[n[i]](ord(start) + i)


def generate(max_length, start):
  for r in range(max_length + 1):
    for n in itertools.product(range(len(expansions)), repeat=r):
      yield list(expand(n, start))


class TestCiri(unittest.TestCase):

  def test_ciri(self):
    from timeit import default_timer as timer
    import datetime
    i = 0
    s = None
    start = timer()
    for base in generate(6, 'a'):
      for href in generate(2, 'p'):
        self.assertEqual(resolve(base, href), ciri.resolve(base, href), repr((base, href)))
      i += 1
      r = "{0:10.0%}".format(i / 5229043.0)
      if s != r:
        s = r
        elapsed = timer() - start
        print(
          s,
          '   elapsed:',
          str(datetime.timedelta(seconds=elapsed)),
          '   remaining:',
          str(datetime.timedelta(seconds=elapsed * (5229043.0 / i) - elapsed)))
    print(i)


if __name__ == '__main__':
  unittest.main()
