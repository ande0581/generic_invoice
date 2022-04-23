import datetime
from django.contrib import messages
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.six import BytesIO
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm, inch, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from .models import PDFImage


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(115 * mm, 25 * mm + (0.2 * inch),
                             "Page {} of {}".format(self._pageNumber, page_count))


def generate_pdf(request, obj, invoice_item_dict, save_to_disk=False):
    buff = BytesIO()

    # The page width totals 18.6cm
    doc = SimpleDocTemplate(buff, rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=1.5 * cm, bottomMargin=3.75 * cm)

    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('Thank You For Your Business', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()

    story = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Data', alignment=TA_LEFT, fontSize=8, leading=7))
    styles.add(ParagraphStyle(name='Line_Data_Small', alignment=TA_LEFT, fontSize=7, leading=8))
    styles.add(ParagraphStyle(name='Line_Data_Medium', alignment=TA_LEFT, fontSize=10, leading=8))
    styles.add(ParagraphStyle(name='Line_Data_Large', alignment=TA_LEFT, fontSize=12, leading=12))
    styles.add(ParagraphStyle(name='Line_Data_Large_Right', alignment=TA_RIGHT, fontSize=12, leading=12))
    styles.add(ParagraphStyle(name='Line_Data_Large_Center', alignment=TA_CENTER, fontSize=12, leading=12))
    styles.add(ParagraphStyle(name='Invoice_Date', alignment=TA_LEFT, fontSize=12, leading=12))
    styles.add(ParagraphStyle(name='Line_Data_Largest', fontName='Times-BoldItalic', alignment=TA_CENTER, fontSize=22, leading=15))
    styles.add(ParagraphStyle(name='Line_Label', fontSize=10, leading=12, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Label_Center', fontSize=7, alignment=TA_CENTER))

    # Add Invoicing Party, Invoice ID and Date
    telephone = obj.invoicing_party.telephone
    telephone = "({}) {}-{}".format(telephone[:3], telephone[3:6], telephone[6:])

    invoicing_party_paragraph = """
        {first} {last}<br />
        {street}<br />
        {city}, {state} {zip}<br />
        {telephone}<br />
        {email}""".format(first=obj.invoicing_party.first_name, last=obj.invoicing_party.last_name,
                          street=obj.invoicing_party.street, city=obj.invoicing_party.city,
                          state=obj.invoicing_party.state, zip=obj.invoicing_party.zip,
                          telephone=telephone, email=obj.invoicing_party.email)

    header = ""

    invoice_number = """
        Invoice: {id:04d}<br />
        Date: {date}
        """.format(id=obj.id, date=datetime.date.today().strftime('%x'))

    data1 = [[Paragraph(invoicing_party_paragraph, styles['Line_Data_Large']),
             Paragraph(header, styles['Line_Data_Large']),
             Paragraph(invoice_number, styles['Line_Data_Large'])]]

    t1 = Table(data1, colWidths=(6.7 * cm, 8 * cm, 4.6 * cm))
    t1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story.append(t1)

    # Add Title to PDF
    title = 'Invoice'
    data1 = [[Paragraph(title, styles["Line_Data_Largest"])]]

    t1 = Table(data1, colWidths=(18.6 * cm))
    t1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))

    story.append(t1)
    story.append(Spacer(2, 32))

    # Add Invoiced Party to Invoice
    telephone = obj.invoiced_party.telephone
    telephone = "({}) {}-{}".format(telephone[:3], telephone[3:6], telephone[6:])

    invoiced_party_paragraph = """
        {first} {last}<br />
        {street}<br />
        {city}, {state} {zip}<br />
        {telephone}<br />
        {email}""".format(first=obj.invoiced_party.first_name, last=obj.invoiced_party.last_name,
                          street=obj.invoiced_party.street, city=obj.invoiced_party.city,
                          state=obj.invoiced_party.state, zip=obj.invoiced_party.zip, telephone=telephone,
                          email=obj.invoiced_party.email)

    data1 = [[Paragraph('Bill To', styles["Line_Data_Large"]),
              Paragraph('Description', styles["Line_Data_Large"])],
             [Paragraph(invoiced_party_paragraph, styles["Line_Data_Large"]),
             Paragraph(obj.description, styles["Line_Data_Large"])]]

    t1 = Table(data1, colWidths=(9.3 * cm, 9.3 * cm))
    t1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (1, 0), colors.gainsboro)
    ]))

    story.append(t1)

    # Add Title to Invoicing Party Items Section - Tom's Section
    if invoice_item_dict['invoicing_items_obj']:
        # Add a space between tables
        story.append(Spacer(4, 32))

        title = [[Paragraph(f"{obj.invoicing_party.first_name}'s Items", styles["Line_Data_Large"]),
                  Paragraph('Split %', styles["Line_Data_Large_Center"]),
                  Paragraph(f'{obj.invoicing_party.first_name }', styles["Line_Data_Large_Right"]),
                  Paragraph(f'{obj.invoiced_party.first_name} Owes', styles["Line_Data_Large_Right"]),
                  Paragraph('Total', styles["Line_Data_Large_Right"]),
                 ]]

        t1 = Table(title, colWidths=(7.6 * cm, 2 * cm, 3 * cm, 3 * cm, 3 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), .25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.gainsboro)
        ]))

        story.append(t1)

        # Add Invoicing Items
        data1 = [[Paragraph(str(item.description), styles["Line_Data_Large"]),
                  Paragraph(str(item.split_percentage), styles["Line_Data_Large_Center"]),
                  Paragraph(str("{0:.2f}".format(round(item.invoicing_party_cost, 2))), styles["Line_Data_Large_Right"]),
                  Paragraph(str("{0:.2f}".format(round(item.invoiced_party_cost, 2))), styles["Line_Data_Large_Right"]),
                  Paragraph(str("{0:.2f}".format(round(item.cost, 2))), styles["Line_Data_Large_Right"])] for item
                 in
                 invoice_item_dict['invoicing_items_obj']]

        t1 = Table(data1, colWidths=(7.6 * cm, 2 * cm, 3 * cm, 3 * cm, 3 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        story.append(t1)

        # Add Total for Invoicing Items
        invoicing_items_summary = [[Paragraph(f"Total", styles["Line_Data_Large"]),
                                    Paragraph('', styles["Line_Data_Large"]),
                                    Paragraph(str("{0:.2f}".format(round(invoice_item_dict['tom_paid_total'], 2))), styles["Line_Data_Large_Right"]),
                                    Paragraph(str("{0:.2f}".format(round(invoice_item_dict['what_sara_owes'], 2))), styles["Line_Data_Large_Right"]),
                                    Paragraph(str("{0:.2f}".format(round(invoice_item_dict['invoicing_items_total'], 2))), styles["Line_Data_Large_Right"])]]

        t1 = Table(invoicing_items_summary, colWidths=(7.6 * cm, 2 * cm, 3 * cm, 3 * cm, 3 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke)
        ]))

        story.append(t1)

    # Add Title to Invoiced Party Items Section - Sara's Section
    if invoice_item_dict['invoiced_items_obj']:
        # Add a space between tables
        story.append(Spacer(4, 32))

        title = [[Paragraph(f"{obj.invoiced_party.first_name}'s Items", styles["Line_Data_Large"]),
                  Paragraph('Split %', styles["Line_Data_Large_Center"]),
                  Paragraph(f'{obj.invoiced_party.first_name }', styles["Line_Data_Large_Right"]),
                  Paragraph(f'{obj.invoicing_party.first_name} Owes', styles["Line_Data_Large_Right"]),
                  Paragraph('Total', styles["Line_Data_Large_Right"]),
                 ]]

        t1 = Table(title, colWidths=(7.6 * cm, 2 * cm, 3 * cm, 3 * cm, 3 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), .25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.gainsboro)
        ]))

        story.append(t1)

        # Add Invoiced Items
        data1 = [[Paragraph(str(item.description), styles["Line_Data_Large"]),
                  Paragraph(str(item.split_percentage), styles["Line_Data_Large_Center"]),
                  Paragraph(str("{0:.2f}".format(round(item.invoiced_party_cost, 2))), styles["Line_Data_Large_Right"]),
                  Paragraph(str("{0:.2f}".format(round(item.invoicing_party_cost, 2))), styles["Line_Data_Large_Right"]),
                  Paragraph(str("{0:.2f}".format(round(item.cost, 2))), styles["Line_Data_Large_Right"])] for item
                 in
                 invoice_item_dict['invoiced_items_obj']]

        t1 = Table(data1, colWidths=(7.6 * cm, 2 * cm, 3 * cm, 3 * cm, 3 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        story.append(t1)

        # Add Total for Invoiced Items
        invoicing_items_summary = [[Paragraph(f"Total", styles["Line_Data_Large"]),
                                    Paragraph('', styles["Line_Data_Large"]),
                                    Paragraph(str("{0:.2f}".format(round(invoice_item_dict['sara_paid_total'], 2))), styles["Line_Data_Large_Right"]),
                                    Paragraph(str("{0:.2f}".format(round(invoice_item_dict['what_tom_owes'], 2))), styles["Line_Data_Large_Right"]),
                                    Paragraph(str("{0:.2f}".format(round(invoice_item_dict['invoiced_items_total'], 2))), styles["Line_Data_Large_Right"])]]

        t1 = Table(invoicing_items_summary, colWidths=(7.6 * cm, 2 * cm, 3 * cm, 3 * cm, 3 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke)
        ]))

        story.append(t1)

    # Add a space between tables
    story.append(Spacer(4, 32))

    # Add Summary of Who Owes to Invoice
    title = [[Paragraph(f"Summary", styles["Line_Data_Large"]),
              Paragraph(f'{obj.invoicing_party.first_name} Owes', styles["Line_Data_Large_Right"]),
              Paragraph(f'{obj.invoiced_party.first_name} Owes', styles["Line_Data_Large_Right"]),
              Paragraph('Difference', styles["Line_Data_Large_Right"]),
              ]]

    t1 = Table(title, colWidths=(9.6 * cm, 3 * cm, 3 * cm, 3 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), .25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.gainsboro)
    ]))

    story.append(t1)

    # Add Summary Values
    invoicing_items_summary = [[Paragraph(f"{invoice_item_dict['the_owing_party']}", styles["Line_Data_Large"]),
                                Paragraph(str("{0:.2f}".format(round(invoice_item_dict['what_tom_owes'], 2))),
                                          styles["Line_Data_Large_Right"]),
                                Paragraph(str("{0:.2f}".format(round(invoice_item_dict['what_sara_owes'], 2))),
                                          styles["Line_Data_Large_Right"]),
                                Paragraph(str("{0:.2f}".format(round(invoice_item_dict['the_owing_total'], 2))),
                                          styles["Line_Data_Large_Right"])]]

    t1 = Table(invoicing_items_summary, colWidths=(9.6 * cm, 3 * cm, 3 * cm, 3 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke)
    ]))

    story.append(t1)

    doc.build(story, canvasmaker=NumberedCanvas)

    pdf = buff.getvalue()
    buff.close()

    if save_to_disk:
        myfile = ContentFile(pdf)
        db_model = PDFImage()
        db_model.invoice = obj
        filename_temp = 'invoice'

        db_model.filename.save(filename_temp, myfile)
        messages.success(request, "PDF was saved successfully!")
        return redirect('invoice_app:invoice_detail', pk=obj.id)

    filename = "{}_invoice_{}".format(obj.invoiced_party.__str__().replace(' ', '_').replace(',', '').lower(), datetime.date.today())
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename={}.pdf'.format(filename)
    response.write(pdf)

    return response
