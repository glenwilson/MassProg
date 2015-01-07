class StackObj(object):
    def __init__(self, monomial, queue, output):
        self.monomial = monomial
        self.queue = queue
        self.output = output

    def get_monomial(self):
        return self.monomial

    def get_queue(self):
        return self.queue

    def get_output(self):
        return self.output
