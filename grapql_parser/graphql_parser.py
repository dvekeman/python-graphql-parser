from __future__ import annotations

from parsec import *

from grapql_parser import model

whitespace = regex(r'\s*', re.MULTILINE)

lexeme = lambda p: p << whitespace
lparen = lexeme(string('('))
rparen = lexeme(string(')'))
lbrace = lexeme(string('{'))
rbrace = lexeme(string('}'))
lbrack = lexeme(string('['))
rbrack = lexeme(string(']'))
colon = lexeme(string(':'))
comma = lexeme(string(','))
dollar = lexeme(string('$'))
equal_sign = lexeme(string('='))
exclamation_mark = lexeme(string('!'))
true = lexeme(string('true')).result(True)
false = lexeme(string('false')).result(False)
null = lexeme(string('null')).result(None)
name = lexeme(
    regex(r'[_A-Za-z][_0-9A-Za-z]*')
).parsecmap(str)


def number():
    return lexeme(
        regex(r'-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][+-]?[0-9]+)?')
    ).parsecmap(float)


def charseq():
    """Parse string. (normal string and escaped string)"""

    def string_part():
        """Parse normal string."""
        return regex(r'[^"\\]+')

    def string_esc():
        """Parse escaped string."""
        return string('\\') >> (
                string('\\')
                | string('/')
                | string('"')
                | string('b').result('\b')
                | string('f').result('\f')
                | string('n').result('\n')
                | string('r').result('\r')
                | string('t').result('\t')
                | regex(r'u[0-9a-fA-F]{4}').parsecmap(lambda s: chr(int(s[1:], 16)))
        )

    return string_part() | string_esc()


@lexeme
@generate
def quoted():
    yield string('"')
    body = yield many(charseq())
    yield string('"')
    return ''.join(body)


@generate
def object_pair():
    key = yield quoted
    yield colon
    val = yield value
    return (key, val)


@generate
def array():
    yield lbrack
    elements = yield sepBy(value, comma)
    yield rbrack
    return elements


@generate
def dict_object():
    yield lbrace
    pairs = yield sepBy(object_pair, comma)
    yield rbrace
    return dict(pairs)


value = number() | dict_object | array | true | false | null


@generate('graphql mutation')
def mutation():
    yield string('mutation')


@generate
def implicit_query():
    yield lbrace
    query_name = yield name
    yield rbrace
    return model.Operation(
        operation_type=model.OperationType.QUERY,
        name=query_name,
        variables=[]
    )


@generate
def named_type():
    variable_name_type = yield name
    non_nullable = yield optional(exclamation_mark)

    named_type = model.NamedType(
        type_name=variable_name_type
    )
    if non_nullable:
        return model.NonNullType(
            type=named_type
        )
    else:
        return named_type


@generate
def list_type():
    yield lbrack
    variable_list_type = yield type
    yield rbrack
    non_nullable = yield optional(exclamation_mark)
    list_type = model.ListType(
        type=variable_list_type
    )
    if non_nullable:
        return model.NonNullType(
            type=list_type
        )
    else:
        return list_type


type = named_type | list_type


@generate
def default_value():
    yield equal_sign
    default_value = yield value
    return default_value


@generate
def variable_definition():
    yield dollar
    variable_name = yield name
    yield colon
    variable_type = yield type
    variable_default_value = yield optional(default_value)
    return model.Variable(
        name=variable_name,
        type=variable_type,
        default_value=variable_default_value
    )


@generate
def variable_definitions():
    yield lparen
    definitions = yield sepBy(variable_definition, comma)
    yield rparen
    return definitions


@lexeme
@generate
def explicit_query():
    yield lexeme(string('query'))
    query_name = yield name
    query_variable_definitions = yield optional(variable_definitions)
    yield lbrace
    # yield rbrace
    return model.Operation(
        operation_type=model.OperationType.QUERY,
        name=query_name,
        variables=query_variable_definitions
    )


query = implicit_query | explicit_query


@lexeme
@generate
def graphql_document():
    operations = yield many(query | mutation)
    return model.GraphqlDocument(
        fragments=[],  # TODO
        operations=operations
    )


def graphql_parser() -> Parser:
    return whitespace >> graphql_document


def run(input: str) -> model.GraphqlDocument:
    return graphql_parser().parse(input)
