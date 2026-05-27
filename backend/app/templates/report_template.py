from reportlab.platypus import Spacer


class ReportTemplate:

    def __init__(self, pdf):
        self.pdf = pdf

    def add_spacing(self, height=12):
        self.pdf.elements.append(Spacer(1, height))