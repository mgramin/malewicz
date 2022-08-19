import sqlparse
from sqlparse import sql


class Query:

    # query_string = ""
    columns = {}
    comments = ""
    title = ""
    description = ""

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

            comment_lines = self.comments.splitlines()
            
            if len(comment_lines) == 1:
                self.title = self.comments.splitlines()[0]
            if len(comment_lines) >= 2:
                self.title = self.comments.splitlines()[0]
                self.description = self.comments.splitlines()[1]

        identifier_list = [x for x in parsed if isinstance(x, sql.IdentifierList)]
        
        if identifier_list:
            identifiers = identifier_list[0].get_identifiers()
            for identifier in identifiers:
              comment = [x for x in identifier if isinstance(x, sql.Comment)][0]
              self.columns[identifier.get_name()] = comment.value.strip().lstrip("/*").rstrip("*/").lstrip("--").strip()
