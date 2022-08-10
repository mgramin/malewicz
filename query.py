import sqlparse
from sqlparse import sql


class Query:

    # query_string = ""
    columns = {}

    def __init__(self, query_string):
        self.query_string = query_string
        self.columns = {}
        

    def parse(self):
        parsed = sqlparse.parse(str(self.query_string))[0]
        cmts = [x for x in parsed if isinstance(x, sql.Comment)]

        if cmts:
            cmt = str(cmts[0])
            clear_comments = []
            for line in cmt.splitlines():
                clear_comments.append(line.strip().lstrip("/*").rstrip("*/").lstrip("--").strip())
            self.comments = "\n".join(clear_comments)

        identifier_list = [x for x in parsed if isinstance(x, sql.IdentifierList)]
        
        if identifier_list:
            identifiers = identifier_list[0].get_identifiers()
            for identifier in identifiers:
              comment = [x for x in identifier if isinstance(x, sql.Comment)][0]
              self.columns[identifier.get_name()] = comment.value.strip().lstrip("/*").rstrip("*/").lstrip("--").strip()
