#!/usr/bin/env python3
"""
CV to PDF Converter - Compare WeasyPrint and pdfkit outputs
---------------------------------------------------------
This script converts your HTML CV to PDF using both WeasyPrint and pdfkit,
allowing you to compare which one produces better results.

Requirements:
- WeasyPrint: pip install weasyprint
- pdfkit: pip install pdfkit
- wkhtmltopdf: system installation required (e.g., apt-get install wkhtmltopdf)
"""

import os
import sys
from pathlib import Path


def check_requirements():
    """Check if required libraries are installed"""
    missing = []

    try:
        import weasyprint
    except ImportError:
        missing.append("WeasyPrint (pip install weasyprint)")

    try:
        import pdfkit
    except ImportError:
        missing.append("pdfkit (pip install pdfkit)")

    if missing:
        print("Missing required libraries:")
        for lib in missing:
            print(f"- {lib}")
        print("\nPlease install them and try again.")
        return False

    return True


def convert_with_weasyprint(html_file, output_file, css_file=None):
    """Convert HTML to PDF using WeasyPrint with options for page fitting"""
    from weasyprint import HTML, CSS

    print(f"Converting with WeasyPrint: {output_file}")

    # Create base URL for handling relative paths
    base_url = Path(html_file).parent.as_uri()

    # Load HTML
    html = HTML(filename=html_file, base_url=base_url)

    stylesheets = []

    # Add custom CSS if provided
    if css_file and os.path.exists(css_file):
        stylesheets.append(CSS(filename=css_file))

    # Add minimal CSS for optimization only (no margins or scaling)
    fit_css = CSS(
        string="""
        /* Space optimizations only - margins and scaling controlled by HTML */
        .section-title { margin-top: 15px !important; }
        .job-section { margin-bottom: 10px !important; }
        ul { 
            margin-top: 0px !important; 
            margin-bottom: 3px !important;
            padding-left: 15px !important;
        }
        li { margin-bottom: 2px !important; }
        """
    )

    stylesheets.append(fit_css)

    # Generate PDF
    html.write_pdf(
        output_file,
        stylesheets=stylesheets,
        presentational_hints=True,
        optimize_size=("fonts", "images"),
    )

    print(f"✅ WeasyPrint PDF created: {output_file}")


def convert_with_pdfkit(html_file, output_file):
    """Convert HTML to PDF using pdfkit with optimized options for page fit"""
    import pdfkit

    print(f"Converting with pdfkit: {output_file}")

    # Configuration options for better page fitting
    options = {
        # Page settings
        "page-size": "A4",
        "margin-top": "0.6in",
        "margin-right": "0.5in",
        "margin-bottom": "0.6in",
        "margin-left": "0.5in",
        # Note: Page numbering requires the patched version of wkhtmltopdf
        # Install from: https://wkhtmltopdf.org/downloads.html
        # "footer-right": "Page [page] of [topage]",
        # "footer-font-size": "9",
        # "footer-font-name": "Calibri",
        # "footer-spacing": "5",
        # Content adjustments
        "dpi": 400,
        "zoom": 0.45,  # Reduced from 0.50
        # Other settings
        "encoding": "UTF-8",
        "print-media-type": True,
    }

    # Convert to PDF
    pdfkit.from_file(html_file, output_file, options=options)

    print(f"✅ pdfkit PDF created: {output_file}")


def main():
    """Main function to handle command-line usage"""
    if not check_requirements():
        return

    # Paths
    base_dir = "/home/evinai/Desktop/Togay_Tunca_CV_0625"

    # Check for Turkish version argument
    if len(sys.argv) > 1 and sys.argv[1] == "--turkish":
        html_file = os.path.join(base_dir, "cv_word_turkish_v3.html")
        weasyprint_output = os.path.join(
            base_dir, "Togay_Tunca_CV_Turkish_WeasyPrint_v3.pdf"
        )
        pdfkit_output = os.path.join(base_dir, "Togay_Tunca_CV_Turkish_pdfkit_v3.pdf")
    else:
        html_file = os.path.join(base_dir, "cv_word_english_v3.html")
        weasyprint_output = os.path.join(base_dir, "Togay_Tunca_CV_WeasyPrint_v3.pdf")
        pdfkit_output = os.path.join(base_dir, "Togay_Tunca_CV_pdfkit_v3.pdf")

    css_file = os.path.join(base_dir, "pdf_styles.css")

    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"Error: Could not find HTML file: {html_file}")
        return

    # Process command-line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--pdfkit-only":
        convert_with_pdfkit(html_file, pdfkit_output)
    elif len(sys.argv) > 1 and sys.argv[1] == "--weasyprint-only":
        convert_with_weasyprint(html_file, weasyprint_output, css_file)
    else:
        # Generate both by default
        convert_with_weasyprint(html_file, weasyprint_output, css_file)
        try:
            convert_with_pdfkit(html_file, pdfkit_output)
        except Exception as e:
            print(f"⚠️ Error with pdfkit: {e}")
            print(
                "If wkhtmltopdf is not installed, run: sudo apt-get install wkhtmltopdf"
            )

    print("\nDone! Compare the outputs to see which looks better.")
    print(f"WeasyPrint: {os.path.basename(weasyprint_output)}")
    print(f"pdfkit:     {os.path.basename(pdfkit_output)}")


if __name__ == "__main__":
    main()
