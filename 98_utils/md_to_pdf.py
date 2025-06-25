import sys
import os
import argparse
import markdown2
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor


def md_to_pdf(input_md, output_pdf):
    # Read markdown file
    with open(input_md, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown2.markdown(md_content)

    # Extract lines for simple conversion (no images/tables)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Set up PDF document
    doc = SimpleDocTemplate(output_pdf, pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    styles.add(ParagraphStyle(name='MyTitle', fontSize=22, leading=28, alignment=TA_CENTER, spaceAfter=18, textColor=HexColor('#2E4053')))
    styles.add(ParagraphStyle(name='MyHeading1', fontSize=18, leading=22, spaceAfter=12, textColor=HexColor('#2874A6')))
    styles.add(ParagraphStyle(name='MyHeading2', fontSize=15, leading=19, spaceAfter=10, textColor=HexColor('#1ABC9C')))
    styles.add(ParagraphStyle(name='MyNormal', fontSize=11, leading=15, spaceAfter=8))

    for elem in soup.recursiveChildGenerator():
        if elem.name == 'h1':
            story.append(Paragraph(elem.get_text(), styles['MyTitle']))
            story.append(Spacer(1, 0.2*inch))
        elif elem.name == 'h2':
            story.append(Paragraph(elem.get_text(), styles['MyHeading1']))
        elif elem.name == 'h3':
            story.append(Paragraph(elem.get_text(), styles['MyHeading2']))
        elif elem.name == 'p':
            story.append(Paragraph(elem.get_text(), styles['MyNormal']))
        elif elem.name == 'ul':
            for li in elem.find_all('li'):
                story.append(Paragraph('• ' + li.get_text(), styles['MyNormal']))
        elif elem.name == 'ol':
            for idx, li in enumerate(elem.find_all('li'), 1):
                story.append(Paragraph(f'{idx}. ' + li.get_text(), styles['MyNormal']))

    doc.build(story)
    print(f"PDF created: {output_pdf}")


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown file to a pretty PDF.')
    parser.add_argument('input_md', help='Path to the input Markdown file')
    parser.add_argument('output_pdf', help='Path to the output PDF file')
    args = parser.parse_args()

    if not os.path.isfile(args.input_md):
        print(f"Input file {args.input_md} does not exist.")
        sys.exit(1)

    md_to_pdf(args.input_md, args.output_pdf)

if __name__ == '__main__':
    main() 