import sys
import os
import argparse
import markdown2
from weasyprint import HTML, CSS


def md_to_pdf_weasy(input_md, output_pdf, css_path=None):
    # Paths to assets
    main_logo = '99_visual_assets/main_logo_transparent_background.png'
    small_logo = '99_visual_assets/small_logo_transparent_background.png'

    # Read markdown file
    with open(input_md, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown2.markdown(md_content, extras=["tables", "fenced-code-blocks"])

    # Extract document title (first heading or filename)
    import re
    match = re.search(r'# (.+)', md_content)
    doc_title = match.group(1) if match else os.path.splitext(os.path.basename(input_md))[0]

    # Cover page HTML
    cover_html = f'''
    <section class="cover" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 90vh; background: linear-gradient(135deg, #4A64FF 0%, #B23EFF 100%); color: #fff; padding: 0 3em; box-sizing: border-box; max-width: 900px; margin: 0 auto;">
        <img src="{main_logo}" alt="Galaxium Logo" style="max-width: 320px; margin-bottom: 2em;">
        <h1 style="font-size: 2.8em; font-family: 'Orbitron', 'Exo 2', Arial, sans-serif; font-weight: 700; margin-bottom: 0.5em; color: #fff; text-shadow: 0 2px 12px #0B0C1D55;">{doc_title}</h1>
        <div style="font-size: 1.2em; font-family: 'Inter', Arial, sans-serif; opacity: 0.85;">Galaxium Travels</div>
    </section>
    <div style="page-break-after: always;"></div>
    '''

    # Footer HTML (WeasyPrint running element)
    footer_html = f'''
    <div class="footer" id="footer">
        <img src="{small_logo}" alt="Footer Logo">
        Galaxium Travels
    </div>
    '''

    # Full HTML document
    html_doc = f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='utf-8'>
        <title>{doc_title}</title>
        <link rel='stylesheet' href='{css_path or 'md_pdf_style.css'}'>
        <style>
            .footer {{
                display: block;
            }}
        </style>
    </head>
    <body>
    {cover_html}
    {footer_html}
    <div class="content">
    {html_content}
    </div>
    </body>
    </html>
    """

    # Write HTML to a temporary file
    import tempfile
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as tmp_html:
        tmp_html.write(html_doc)
        tmp_html_path = tmp_html.name

    # Use WeasyPrint to generate PDF
    HTML(tmp_html_path, base_url=os.getcwd()).write_pdf(output_pdf, stylesheets=[CSS(css_path or '98_utils/md_pdf_style.css')])
    print(f"PDF created: {output_pdf}")
    os.remove(tmp_html_path)


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown file to a pretty PDF using WeasyPrint.')
    parser.add_argument('input_md', help='Path to the input Markdown file')
    parser.add_argument('output_pdf', help='Path to the output PDF file')
    parser.add_argument('--css', help='Path to a custom CSS file', default='98_utils/md_pdf_style.css')
    args = parser.parse_args()

    if not os.path.isfile(args.input_md):
        print(f"Input file {args.input_md} does not exist.")
        sys.exit(1)

    if not os.path.isfile(args.css):
        print(f"CSS file {args.css} does not exist. Using default styling.")
        css_path = None
    else:
        css_path = args.css

    md_to_pdf_weasy(args.input_md, args.output_pdf, css_path)

if __name__ == '__main__':
    main() 