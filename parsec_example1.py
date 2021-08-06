from parsec import *

spaces = regex(r'\s*', re.MULTILINE)
name = regex(r'[_a-zA-Z][_a-zA-Z0-9]*')

tag_start = spaces >> string('<') >> name << string('>') << spaces
tag_stop = spaces >> string('</') >> name << string('>') << spaces


@generate
def header_kv():
    key = yield spaces >> name << spaces
    yield string(':')
    value = yield spaces >> regex('[^\n]+')
    return {key: value}


@generate
def header():
    tag_name = yield tag_start
    values = yield sepBy(header_kv, string('\n'))
    tag_name_end = yield tag_stop
    assert tag_name == tag_name_end
    return {
        'type': 'tag',
        'name': tag_name,
        'values': values
    }


@generate
def body():
    tag_name = yield tag_start
    values = yield sepBy(sepBy1(regex(r'[^\n<,]+'), string(',')), string('\n'))
    tag_name_end = yield tag_stop
    assert tag_name == tag_name_end
    return {
        'type': 'tag',
        'name': tag_name,
        'values': values
    }


def example1_parser() -> Parser:
    return header + body


if __name__ == '__main__':
    result = example1_parser().parse('''
<kv>
  key1: "string"
  key2: 1.00005
  key3: [1,2,3]
</kv>
<csv>
date,windspeed,direction
20190805,22,NNW
20190805,23,NW
20190805,20,NE
</csv>
    ''')
    print(result)
