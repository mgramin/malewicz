import uuid

class Page:
    def __init__(self, rows, total_pages, current_page):
        self.rows = rows
        self.total_pages = total_pages 
        self.current_page = current_page
        # self.next_page = false
        # self.prev_page = false
