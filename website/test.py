from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time


canvas = canvas.Canvas("form.pdf", pagesize=(250,450))
canvas.setLineWidth(.3)
canvas.setFont('Helvetica', 14)

canvas.drawString(45,430,'Butterfly Garden : Ticket')
canvas.line(10,416,240,416)
canvas.drawInlineImage("../qrcodes/0CA3K4.png", 53, 271, width=140,height=140)
canvas.line(10,266,240,266)
canvas.setFont('Helvetica', 12)
canvas.drawString(20,250,'Name : Viral Sangani')
canvas.drawString(20,233,'Adult : 3')
canvas.drawString(120,233,'Children : 3')
canvas.drawString(20,215,'Time : '+time.asctime( time.localtime(time.time()) ))
canvas.line(10,192,240,192)
canvas.line(10,191,240,191)
canvas.drawInlineImage("../qrcodes/0CA3K4.png", 53, 30, width=140,height=140)
canvas.save()
