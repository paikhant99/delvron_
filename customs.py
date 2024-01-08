from tkinter import ttk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import *
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os
from constants import resource_path

DO_RV_COMPANY_NAME = "DELVRON MYANMAR COMPANY LIMITED"
DO_RV_ADDRESS_DETAIL = "No.181-D, Aloun Phayar Road, North Okkalapa Industrial Zone,"
DO_RV_ADDRESS_TOWNSHIP = "North Okkalapa Township, Yangon, Myanmar."
DO_RV_CONTACT_NUMBER = "Telephone Number : 09-262 389 197, 09-897 793 466"
DO_RV_WEBSITE = "Website : www.delvron-myanmar.com"

DO_RV_C_NAME_LABEL = "COMPANY NAME"
DO_RV_C_ADDRESS_LABEL = "ADDRESS"
DO_RV_C_CONTACT_LABEL = "CUSTOMER CONTACT"
DO_RV_C_SERIAL_LABEL = "MACHINE SERIAL NO"


class CustomPDF(canvas.Canvas):

    def __init__(self, name, _expected_sale_id, _sale_date, _items, _company, _approved_by, _sell_by, size=A4,
                 image_paths=["images/logo_black.png", "images/singa_water_logo_black.jpg"]):
        self._filename = name
        canvas.Canvas.__init__(self, filename=name, pagesize=size)
        print(A4)

        self._layout_cash_receipt_form(size[0], size[1], _expected_sale_id, _sale_date, _items, _company,
                                       image_paths)
        # self._draw_dotted_line(0, size[1]/2, size[0], size[1]/2, dot_space=5)
        self._layout_delivery_order_form(size[0], size[1] / 2, _expected_sale_id, _sale_date, _items, _company,
                                         _approved_by.name if _approved_by else '', _sell_by.name if _sell_by else '',
                                         image_paths)

    def _layout_delivery_order_form(self, _page_width, _page_height, _expected_sale_id, _sale_date, _order_products,
                                    _company, _approved_by_name, _sell_by_name, image_paths):
        """Show Delivery Order Form"""

        canvas.Canvas.drawImage(self, image=resource_path(image_paths[0]), x=0+(_page_width * 0.05),
                                y=_page_height * 0.881, width=_page_width * 0.134, height=_page_height * 0.118)
        canvas.Canvas.setFont(self, "Helvetica-Bold", (_page_width*_page_height)*0.00006)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.952,
                                 DO_RV_COMPANY_NAME)
        canvas.Canvas.setFont(self, "Helvetica", (_page_width*_page_height)*0.000035)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.928,
                                 DO_RV_ADDRESS_DETAIL)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.904,
                                 DO_RV_ADDRESS_TOWNSHIP)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.881,
                                 DO_RV_CONTACT_NUMBER)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.857,
                                 DO_RV_WEBSITE)
        canvas.Canvas.line(self, 0+(_page_width * 0.05), _page_height * 0.833, _page_width-(_page_width * 0.05),
                           _page_height * 0.833)

        canvas.Canvas.setFont(self, "Helvetica-Bold", (_page_width*_page_height)*0.00006)
        canvas.Canvas.drawString(self, (_page_width * 0.748) + (_page_width * 0.05), _page_height * 0.928,
                                 f"{_expected_sale_id}")

        canvas.Canvas.setFont(self, "Helvetica", (_page_width*_page_height)*0.000035)
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height * 0.786, DO_RV_C_NAME_LABEL)
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height * 0.738, DO_RV_C_ADDRESS_LABEL)
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height * 0.691, DO_RV_C_CONTACT_LABEL)
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height * 0.643, DO_RV_C_SERIAL_LABEL)
        canvas.Canvas.drawString(self, (_page_width * 0.201)+(_page_width * 0.05), _page_height * 0.786,
                                 f":   {_company.name}")
        canvas.Canvas.drawString(self, (_page_width * 0.201)+(_page_width * 0.05), _page_height * 0.738,
                                 f":   {_company.address}")
        canvas.Canvas.drawString(self, (_page_width * 0.201)+(_page_width * 0.05), _page_height * 0.691,
                                 f":   {_company.phno}")
        canvas.Canvas.drawString(self, (_page_width * 0.201)+(_page_width * 0.05), _page_height * 0.643,
                                 f":   {_company.serial_no}")

        canvas.Canvas.setFont(self, "Helvetica-Bold", (_page_width * _page_height) * 0.00004)
        canvas.Canvas.drawString(self, (_page_width * 0.764)-(_page_width * 0.05), _page_height * 0.786,
                                 "DELIVERY ORDER")
        canvas.Canvas.setFont(self, "Helvetica", (_page_width*_page_height)*0.000035)
        canvas.Canvas.line(self, (_page_width * 0.764)-(_page_width * 0.05), _page_height * 0.774, (_page_width * 0.932)
                           - (_page_width * 0.05), _page_height * 0.774)
        canvas.Canvas.drawString(self, (_page_width * 0.764)-(_page_width * 0.05), _page_height * 0.738, "DATE")
        canvas.Canvas.drawString(self, (_page_width * 0.764)-(_page_width * 0.05), _page_height * 0.691, "REF")
        canvas.Canvas.drawString(self, (_page_width * 0.815) - (_page_width * 0.05), _page_height * 0.738,
                                 f":   {_sale_date}")
        canvas.Canvas.drawString(self, (_page_width * 0.815)-(_page_width * 0.05), _page_height * 0.691, f":")
        canvas.Canvas.drawString(self, (_page_width * 0.832)-(_page_width * 0.05), _page_height * 0.691, "DM- ")
        canvas.Canvas.drawString(self, (_page_width * 0.899)-(_page_width * 0.05), _page_height * 0.691, "DO- ")

        items = [['No', 'DESCRIPTION', 'COUNT', 'QUANTITY', 'REMARK']]
        print(_order_products)

        items += [[idx+1, order_product.item.name, order_product.item.measurement, order_product.qty,
                   order_product.remark] for idx, order_product in enumerate(_order_products)]

        if len(_order_products) < 5:
            for index in range(5 - len(_order_products)):
                items += [['', '', '', '', '']]

        items += [['TOTAL', '', '', '', '']]

        table = Table(items, [_page_width * 0.058, (_page_width * 0.319)-(_page_width * 0.033),
                              (_page_width * 0.125)-(_page_width * 0.016), (_page_width * 0.159)-(_page_width * 0.016),
                              (_page_width * 0.335)-(_page_width * 0.033)], _page_height * 0.035, style=TableStyle([
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTNAME', (0, -1), (2, -1), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, -1), (_page_width*_page_height)*0.000035),
                                ('FONTSIZE', (0, 0), (-1, 0), (_page_width*_page_height)*0.000039),
                                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                                ('SPAN', (0, -1), (2, -1)),
                                ('COLWIDTHS', (0, 0), (0, -1), 30),
                                ('COLHEIGHTS', (0, 0), (-1, 0), 25)
                                ]))
        table.wrapOn(self, 200, 200)
        table.drawOn(self, 0+(_page_width * 0.05), _page_height - ((_page_height * 0.38) + table._height))

        if len(_order_products) < 5:
            canvas.Canvas.setStrokeColor(self, aColor=colors.Color(0, 0, 0, alpha=0.5))
            canvas.Canvas.line(self, _page_width * 0.605, _page_height - ((_page_height * 0.38) + table._height) +
                               (((5 - len(_order_products)) + 1) * (_page_height * 0.035)) - 7,
                               _page_width * 0.546, _page_height - ((_page_height * 0.38) + table._height) +
                               (((5 - len(_order_products)) + 1) * (_page_height * 0.035)) - 7)
            canvas.Canvas.line(self, _page_width * 0.605, _page_height - ((_page_height * 0.38) + table._height) +
                               (((5 - len(_order_products)) + 1) * (_page_height * 0.035)) - 7,
                               _page_width * 0.546, _page_height - ((_page_height * 0.38) + table._height) +
                               (1 * (_page_height*0.035)) + 7)
            canvas.Canvas.line(self, _page_width*0.605, _page_height - ((_page_height * 0.38) + table._height) +
                               (1 * (_page_height*0.035))+7, _page_width*0.546, _page_height -
                               ((_page_height * 0.38) + table._height) + (1 * (_page_height*0.035))+7)
            canvas.Canvas.setStrokeColor(self, aColor=colors.Color(0, 0, 0, alpha=1))

        canvas.Canvas.setFont(self, "Helvetica", (_page_width*_page_height)*0.000027)

        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height - ((_page_height * 0.475) + table._height),
                                 "Approved By")
        canvas.Canvas.drawString(self, (_page_width * 0.083)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.475) + table._height), f":    {'.' * 30}")

        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height - ((_page_height * 0.522) + table._height),
                                 "Name")
        canvas.Canvas.drawString(self, (_page_width * 0.083)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.522) + table._height), f":    {_approved_by_name}")

        canvas.Canvas.drawString(self, (_page_width * 0.251)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.475) + table._height), "Sell By")
        canvas.Canvas.drawString(self, (_page_width * 0.285)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.475) + table._height), f":    {'.' * 30}")

        canvas.Canvas.drawString(self, (_page_width * 0.251)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.522) + table._height), "Name")
        canvas.Canvas.drawString(self, (_page_width * 0.285)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.522) + table._height), f":    {_sell_by_name}")

        canvas.Canvas.drawString(self, (_page_width * 0.453)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.475) + table._height), "Received By")
        canvas.Canvas.drawString(self, (_page_width * 0.52)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.475) + table._height), f":    {'.' * 30}")

        canvas.Canvas.drawString(self, (_page_width * 0.453)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.522) + table._height), "Name")
        canvas.Canvas.drawString(self, (_page_width * 0.52)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.522) + table._height), f":    {'.' * 30}")

        canvas.Canvas.drawImage(self, image=resource_path(image_paths[1]), x=(_page_width * 0.89)-(_page_width * 0.05),
                                y=_page_height - ((_page_height * 0.51) + table._height), width=_page_width * 0.083,
                                height=_page_height * 0.118)

        canvas.Canvas.showPage(self)

    def _layout_cash_receipt_form(self, _page_width, _page_height, _expected_order_id, _expected_order_date,
                                  _order_products, _company, image_paths):
        """Show Cash Receipt Form"""

        canvas.Canvas.drawImage(self, image=resource_path(image_paths[0]), x=0+(_page_width * 0.05),
                                y=_page_height * 0.94, width=_page_width * 0.134, height=_page_height * 0.059)
        canvas.Canvas.setFont(self, "Helvetica-Bold", (_page_width*_page_height)*0.000031)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.976,
                                 DO_RV_COMPANY_NAME)
        canvas.Canvas.setFont(self, "Helvetica", (_page_width*_page_height)*0.000017)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.964,
                                 DO_RV_ADDRESS_DETAIL)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.952,
                                 DO_RV_ADDRESS_TOWNSHIP)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.94,
                                 DO_RV_CONTACT_NUMBER)
        canvas.Canvas.drawString(self, (_page_width * 0.151)+(_page_width * 0.05), _page_height * 0.928, DO_RV_WEBSITE)
        canvas.Canvas.line(self, 0+(_page_width * 0.05), _page_height * 0.916, _page_width-(_page_width * 0.05),
                           _page_height * 0.916)

        canvas.Canvas.setFont(self, "Helvetica-Bold", (_page_width*_page_height)*0.000031)
        canvas.Canvas.drawString(self, (_page_width * 0.748) + (_page_width * 0.05), _page_height * 0.964,
                                 f"{_expected_order_id}")

        canvas.Canvas.setFont(self, "Helvetica", (_page_width*_page_height)*0.000017)
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height * 0.893, DO_RV_C_NAME_LABEL)
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height * 0.869, DO_RV_C_ADDRESS_LABEL)
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height * 0.845, DO_RV_C_CONTACT_LABEL)
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height * 0.821, DO_RV_C_SERIAL_LABEL)
        canvas.Canvas.drawString(self, (_page_width * 0.201)+(_page_width * 0.05), _page_height * 0.893,
                                 f":   {_company.name}")
        canvas.Canvas.drawString(self, (_page_width * 0.201)+(_page_width * 0.05), _page_height * 0.869,
                                 f":   {_company.address}")
        canvas.Canvas.drawString(self, (_page_width * 0.201)+(_page_width * 0.05), _page_height * 0.845,
                                 f":   {_company.phno}")
        canvas.Canvas.drawString(self, (_page_width * 0.201)+(_page_width * 0.05), _page_height * 0.821,
                                 f":   {_company.serial_no}")

        canvas.Canvas.setFont(self, "Helvetica-Bold", (_page_width*_page_height)*0.000021)
        canvas.Canvas.drawString(self, (_page_width * 0.764)-(_page_width * 0.05), _page_height * 0.893,
                                 "OFFICIAL CASH RECEIPT")
        canvas.Canvas.setFont(self, "Helvetica", (_page_width*_page_height)*0.000017)
        canvas.Canvas.line(self, (_page_width * 0.764)-(_page_width * 0.05), _page_height * 0.887,
                           _page_width-(_page_width * 0.05), _page_height * 0.887)
        canvas.Canvas.drawString(self, (_page_width * 0.764)-(_page_width * 0.05), _page_height * 0.869, "DATE")
        canvas.Canvas.drawString(self, (_page_width * 0.764)-(_page_width * 0.05), _page_height * 0.845, "REF")
        canvas.Canvas.drawString(self, (_page_width * 0.815)-(_page_width * 0.05), _page_height * 0.869,
                                 f":   {_expected_order_date}")
        canvas.Canvas.drawString(self, (_page_width * 0.815)-(_page_width * 0.05), _page_height * 0.845, f":")

        items = [['No', 'DESCRIPTION', 'QUANTITY', 'UNIT PRICE (MMK)', 'TOTAL PRICE (MMK)']]
        total = 0
        for idx, order_product in enumerate(_order_products):
            items += [[idx+1, order_product.item.name, order_product.qty, order_product.unit_price,
                       int(order_product.qty) * int(order_product.unit_price)]]
            total += int(order_product.qty) * int(order_product.unit_price)

        if len(_order_products) < 5:
            for index in range(5 - len(_order_products)):
                items += [['', '', '', '', '']]

        items += [["BANK INFORMATION (MMK)", "", "TOTAL", "", total]]
        items += [["Account Name : DELVRON MYANMAR CO.,LTD ", "", "PAYMENT AMOUNT", "", ""]]
        items += [["Account Number (MMK) : 070 103 070 034 289 01", "", "BALANCE", "", ""]]

        table1 = Table(items, [(_page_width*0.058), (_page_width*0.319)-(_page_width*0.033),
                               (_page_width*0.125)-(_page_width*0.016), (_page_width*0.209)-(_page_width*0.016),
                               (_page_width*0.285)-(_page_width*0.033)], _page_height * 0.017, style=TableStyle([
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('ALIGN', (0, -3), (3, -1), 'LEFT'),
                                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('FONTNAME', (0, -3), (3, -1), 'Helvetica-Bold'),
                                    ('FONTSIZE', (0, 0), (-1, -1), (_page_width*_page_height)*0.000017),
                                    ('FONTSIZE', (0, 0), (-1, 0), (_page_width*_page_height)*0.000019),
                                    ('FONTSIZE', (0, -3), (1, -3), (_page_width*_page_height)*0.000019),
                                    ('FONTSIZE', (0, -2), (1, -1), (_page_width*_page_height)*0.000015),
                                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                                    ('SPAN', (0, -3), (1, -3)),
                                    ('SPAN', (0, -2), (1, -2)),
                                    ('SPAN', (0, -1), (1, -1)),
                                    ('SPAN', (2, -3), (3, -3)),
                                    ('SPAN', (2, -2), (3, -2)),
                                    ('SPAN', (2, -1), (3, -1)),
                                    ('COLWIDTHS', (0, 0), (0, -1), 30),
                                    ('COLHEIGHTS', (0, 0), (-1, 0), 30),
                                    ('INNERGRID', (0, -3), (1, -1), 0, colors.white),
                                ]))
        print(_page_width)
        print(_page_height)

        table1.wrapOn(self, 200, 200)
        table1.drawOn(self, 0+(_page_width * 0.05), _page_height - ((_page_height * 0.19) + table1._height))

        items = [["INLET TDS", "OUTLET TDS", "BALANCE METER", "TOP-UP VALUE"]]
        items += [["", "", "", ""]]
        table2 = Table(items, [(_page_width*0.188)-(_page_width*0.0167),
                               (_page_width*0.188)-(_page_width*0.0167), (_page_width*0.335)-(_page_width*0.033),
                               (_page_width*0.285)-(_page_width*0.033)], 15, style=TableStyle([
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                                ]))
        table2.wrapOn(self, 200, 200)
        table2.drawOn(self, 0+(_page_width * 0.05), _page_height - ((_page_height * 0.231) + table1._height))

        if len(_order_products) < 5:
            canvas.Canvas.setStrokeColor(self, aColor=colors.Color(0, 0, 0, alpha=0.5))
            canvas.Canvas.line(self, _page_width * 0.874, _page_height - ((_page_height * 0.19)+table1._height) +
                               (((5 - len(_order_products)) + 3) * (_page_height * 0.017)) - 7, _page_width * 0.773,
                               _page_height - ((_page_height * 0.19) + table1._height) +
                               (((5 - len(_order_products)) + 3) * (_page_height * 0.017)) - 7)
            canvas.Canvas.line(self, _page_width * 0.874, _page_height - ((_page_height * 0.19)+table1._height) +
                               (((5 - len(_order_products)) + 3) * (_page_height * 0.017)) - 7,
                               _page_width * 0.773, _page_height - ((_page_height * 0.19) + table1._height) +
                               (3 * (_page_height*0.017)) + 7)
            canvas.Canvas.line(self, _page_width*0.874, _page_height - ((_page_height * 0.19) + table1._height) +
                               (3 * (_page_height*0.017))+7, _page_width*0.773, _page_height -
                               ((_page_height * 0.19) + table1._height) + (3 * (_page_height*0.017))+7)
            canvas.Canvas.setStrokeColor(self, aColor=colors.Color(0, 0, 0, alpha=1))

        canvas.Canvas.setFont(self, "Helvetica", (_page_width*_page_height)*0.000017)

        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height - ((_page_height * 0.261) + table1._height),
                                 f"{'.' * 55}")
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height - ((_page_height * 0.279) + table1._height),
                                 "AUTHORIZED SIGNATURE")
        canvas.Canvas.drawString(self, 0+(_page_width * 0.05), _page_height - ((_page_height * 0.296) + table1._height),
                                 "DELVRON MYANMAR CO.,LTD")

        canvas.Canvas.drawString(self, (_page_width * 0.285)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.261) + table1._height), f"{'.' * 55}")
        canvas.Canvas.drawString(self, (_page_width * 0.285)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.279) + table1._height), "CUSTOMER SIGNATURE")
        canvas.Canvas.drawString(self, (_page_width * 0.285)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.296) + table1._height), "NAME")
        canvas.Canvas.drawString(self, (_page_width * 0.352)+(_page_width * 0.05), _page_height -
                                 ((_page_height * 0.296) + table1._height), f"  : {'.' * 40}")

        canvas.Canvas.drawImage(self, image=resource_path(image_paths[1]), x=(_page_width * 0.89)-(_page_width * 0.05),
                                y=_page_height - ((_page_height * 0.296) + table1._height), width=_page_width * 0.083,
                                height=_page_height * 0.059)

        # if ((250 + table2._height) * 2) + 10 > A4[1]:
        #     canvas.Canvas.showPage(self)

        return 250 + table2._height

    def generate(self):
        canvas.Canvas.save(self)

    def delete_pdf(self):
        os.remove(self._filename)

    def getpdfdata(self):
        return canvas.Canvas.getpdfdata(self)

    def canvas(self):
        return canvas.Canvas

    def _draw_dotted_line(self, x1, y1, x2, y2, dot_space=3, dot_size=1):
        dx = x2 - x1
        dy = y2 - y1
        length = max(abs(dx), abs(dy))
        dot_x = dx / length * dot_space
        dot_y = dy / length * dot_space

        for i in range(int(length / dot_space)):
            x = x1 + dot_x * i
            y = y1 + dot_y * i
            self.circle(x, y, dot_size, fill=1)


class CustomComboBox(ttk.Combobox):

    def __init__(self, master, state: str, values: dict, *args, **kwargs):
        ttk.Combobox.__init__(self, master, values=list(values.keys()), *args, **kwargs, state=state)
        self.dictionary = values

    def set_values(self, values):
        self.dictionary = values
        self['values'] = list(values.keys())

    def get(self):
        if ttk.Combobox.get(self) == '':
            return ''
        if ttk.Combobox.get(self) in self['values']:
            return self.dictionary[ttk.Combobox.get(self)]
        return ttk.Combobox.get(self)
