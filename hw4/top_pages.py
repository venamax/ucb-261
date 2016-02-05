from mrjob.job import MRJob
import csv

def csv_readline(line):
    """Given a sting CSV line, return a list of strings."""
    for row in csv.reader([line]):
        return row

class TopPages(MRJob):

    def mapper(self, line_no, line):
        """Extracts the Vroot that was visited"""
        record = csv_readline(line)
        yield record[1], 1
                  
    def reducer(self, page, visit_counts):
        """Sumarizes the visit counts by adding them together.  If total visits
        is more than 400, yield the results"""
        total = sum(i for i in visit_counts)
        yield page, total
                  
        
if __name__ == '__main__':
    TopPages.run()