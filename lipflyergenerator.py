#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Linux Install Party Flyer Generator for the Liege Linux Team
# (c) Jean-Etienne Poirrier, 2007
# You only need to open the script, edit your own variables and voil�,
# you have a flyer for your LIP.
# This script requires Python, ReportLab (to generate PDF files) and
# the Python Imaging Library
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from time import localtime, strftime

# parameters to change, MANDATORY
NUMBER = "10" # "10" for the 10th LIP, e.g.
DATE = "Samedi 22 septembre 2007"
TIME = "de 10h à 18h"
ADDRESS1 = "Maison de la Fédé"
ADDRESS2 = "Place du XX Août, 24"
COPYRIGHT = "Liege Linux Team (LiLiT) asbl - " + strftime("%d.%m.%Y", localtime())

# parameters to change, if you want
AUTHOR = "lipflyergenerator.py -- J.E. Poirrier"
TITLE = "Linux Install Party"
SUBJECT = "Flyer de Linux Install Party du Liege Linux Team"
KEYWORDS = ['LiLiT', 'Liege', 'Linux', 'Team', 'LIP', 'Install', 'Party', 'flyer']

# Other parameters, should not need any modification
FONT = "Helvetica"
FONTBOLD = "Helvetica-Bold"
FONTSIZE = 35
FONTSIZE2 = 30
SMALLFONTSIZE = 8
width, height = A4
centerh = height/2 # horizontal center, used to center text strings on the page

# create the PDF --- DO NOT EDIT AFTER THIS LINE !!! ---
pdf = Canvas("lipflyer.pdf")
pdf.setPageSize([height, width]) # only trick I found to have a A4 in LANDSCAPE mode 

# Busy with "header"
pdf.setTitle(TITLE)
pdf.setSubject(SUBJECT)
# pdf.setKeywords(KEYWORDS) # not working?
pdf.setAuthor(AUTHOR)

# Putting the 3 images
pdf.drawInlineImage("images/tchantchux.jpg", 40, 240, width=158, height=283)
pdf.drawImage("images/logo-lilit.png", 40, 40, width=None, height=None, mask=[255, 255, 255, 255, 226, 226])
pdf.drawInlineImage("images/penguin.png", 600, 250, width=217, height=260)
# Putting the central text
pdf.setFont(FONT, FONTSIZE) # xème journée d'installation de
pdf.setFillColorRGB(255, 0, 0)
chaine = NUMBER + "       journée d'installation de"
x = pdf.stringWidth(chaine, FONTBOLD, FONTSIZE)
pdf.drawString(centerh - x/2, 530, chaine)
xx = pdf.stringWidth(NUMBER, FONTBOLD, FONTSIZE) # superscript in the previous string
pdf.setFont(FONT, FONTSIZE2)
chaine = "ème"
pdf.drawString(centerh - x/2 + xx, 540, chaine)
pdf.setFont(FONTBOLD, FONTSIZE) # GNU/Linux
pdf.setFillColorRGB(0, 0, 0)
chaine = "GNU/Linux"
x = pdf.stringWidth(chaine, FONTBOLD, FONTSIZE)
pdf.drawString(centerh - x/2, 480, chaine)
pdf.setFont(FONT, FONTSIZE) # sur votre machine
chaine = "sur votre machine" 
x = pdf.stringWidth(chaine, FONT, FONTSIZE)
pdf.drawString(centerh - x/2, 440, chaine)
pdf.setFont(FONTBOLD, FONTSIZE) # date
x = pdf.stringWidth(DATE, FONTBOLD, FONTSIZE)
pdf.drawString(centerh - x/2, 370, DATE)
pdf.setFont(FONT, FONTSIZE) # heure
x = pdf.stringWidth(TIME, FONT, FONTSIZE)
pdf.drawString(centerh - x/2, 325, TIME)
x = pdf.stringWidth(ADDRESS1, FONT, FONTSIZE) # adresse ligne 1
pdf.drawString(centerh - x/2, 280, ADDRESS1)
x = pdf.stringWidth(ADDRESS2, FONT, FONTSIZE) # adresse ligne 2
pdf.drawString(centerh - x/2, 245, ADDRESS2)
pdf.setFont(FONT, FONTSIZE2) # Renseignements et inscription
chaine = "Renseignements et inscription :"
x = pdf.stringWidth(chaine, FONT, FONTSIZE2)
pdf.drawString(centerh + 140 - x/2, 150, chaine)
pdf.setFont(FONTBOLD, FONTSIZE2) # site web LiLiT
chaine = "http://www.lilit.be/lip"
x = pdf.stringWidth(chaine, FONTBOLD, FONTSIZE2)
pdf.drawString(centerh + 140 - x/2, 100, chaine)
pdf.setFont(FONT, FONTSIZE2) # Gratuit et ouvert à tous !
chaine = "Gratuit et ouvert à tous !"
x = pdf.stringWidth(chaine, FONT, FONTSIZE2)
pdf.drawString(centerh + 140 - x/2, 50, chaine)
# Putting the copyright notice
pdf.setFont(FONT, SMALLFONTSIZE)
y = pdf.stringWidth(COPYRIGHT, "Times-Roman", SMALLFONTSIZE)
pdf.rotate(90)
pdf.drawString(5, -height + SMALLFONTSIZE, COPYRIGHT)

# close the page
pdf.showPage()
# save the PDF
pdf.save()
