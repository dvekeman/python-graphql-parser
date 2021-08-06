import unittest

from grapql_parser import graphql_parser
from grapql_parser.model import OperationType


class GraphqlParserTest(unittest.TestCase):
    def test_implicit_query(self):
        result = graphql_parser.run('''
        query myquery(
          $participant:uuid!
        ) {
            ''')
        operation = result.operations[0]
        self.assertEqual(operation.operation_type, OperationType.QUERY)

        #     result = graphql_parser().parse('''
        # query myquery(
        #   $participant:uuid!
        # ) {
        #   schema_name(
        #     where:{
        #       participant:{_eq:$participant}
        #     }
        #     limit:1
        #   ){
        #     invoice_number
        #   }
        # }
        #     ''')
        print(result)

    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
