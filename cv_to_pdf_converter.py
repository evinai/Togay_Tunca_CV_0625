#!/usr/bin/env python3
"""
CV to PDF Converter - WeasyPrint only
--------------------------------------
This script converts your HTML CV to PDF using WeasyPrint.

Requirements:
- WeasyPrint: pip install weasyprint
"""

import os
import sys
from pathlib import Path


def check_requirements():
    """Check if required libraries are installed"""
    try:
        import weasyprint  # noqa: F401

        return True
    except ImportError:
        print("Missing required library: WeasyPrint")
        print("Please install it: pip install weasyprint")
        return False


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
        
        /* Hide images in PDF generation */
        img { display: none !important; }
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


def main():
    """Main function to handle command-line usage"""
    if not check_requirements():
        return

    # Paths
    base_dir = "/home/evinai/Desktop/Togay_Tunca_CV_0625"

    # Check for Turkish version argument or specific file
    if len(sys.argv) > 1:
        if sys.argv[1] == "--turkish":
            html_file = os.path.join(base_dir, "cv_word_turkish_v3.html")
            output_file = os.path.join(
                base_dir, "Togay_Tunca_CV_Turkish_WeasyPrint_v3.pdf"
            )
        elif sys.argv[1].endswith(".html"):
            # Direct file path provided
            html_file = (
                sys.argv[1]
                if os.path.isabs(sys.argv[1])
                else os.path.join(base_dir, sys.argv[1])
            )
            # Determine output name based on input file
            if "turkish" in os.path.basename(html_file).lower():
                output_file = os.path.join(
                    base_dir, "Togay_Tunca_CV_Turkish_WeasyPrint_v3.pdf"
                )
            else:
                output_file = os.path.join(base_dir, "Togay_Tunca_CV_WeasyPrint_v3.pdf")
        else:
            print("Usage: python cv_to_pdf_converter.py [--turkish | filename.html]")
            return
    else:
        # Default to English
        html_file = os.path.join(base_dir, "cv_word_english_v3.html")
        output_file = os.path.join(base_dir, "Togay_Tunca_CV_WeasyPrint_v3.pdf")

    css_file = os.path.join(base_dir, "pdf_styles.css")

    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"Error: Could not find HTML file: {html_file}")
        return

    # Convert to PDF
    convert_with_weasyprint(html_file, output_file, css_file)

    print("\n✅ PDF conversion complete!")
    print(f"Output: {os.path.basename(output_file)}")


if __name__ == "__main__":
    main()
