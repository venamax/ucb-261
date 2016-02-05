from mrjob.job import MRJob
import csv

def csv_readline(line):
    for row in csv.reader([line]):
        return row

class TopPages(MRJob):

    def mapper(self, line_no, line):
        record = csv_readline(line)
        page_visitor = ((record[1],record[4]))
        yield page_visitor, 1
                  
    def reducer(self, page_visitor, visit_counts):
        total = sum(i for i in visit_counts)
        yield page_visitor, total
                  
        
if __name__ == '__main__':
    TopPages.run()