from pypdf import PdfReader
from io import BytesIO

def pdf_to_markdown(pdf_content: bytes) -> str:
    """
    Convert PDF content to markdown format.
    
    Args:
        pdf_content: Raw PDF content as bytes
        
    Returns:
        The PDF content converted to markdown format
    """
    try:
        # Create a BytesIO object from the PDF content
        pdf_stream = BytesIO(pdf_content)
        
        # Read the PDF
        pdf_reader = PdfReader(pdf_stream)
        
        markdown_lines = []
        
        # Process each page
        for page_num, page in enumerate(pdf_reader.pages, 1):
            # Extract text from the page
            text = page.extract_text()
            
            if text.strip():
                # Add page header
                markdown_lines.append(f"## Page {page_num}")
                markdown_lines.append("")
                
                # Process the text line by line
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        # Check if line looks like a heading (all caps, short)
                        if line.isupper() and len(line) < 50:
                            markdown_lines.append(f"### {line}")
                        else:
                            markdown_lines.append(line)
                        markdown_lines.append("")
        
        return '\n'.join(markdown_lines)
        
    except Exception as e:
        # Return a simple error message in markdown format
        return f"# Error converting PDF to markdown\n\nUnable to process PDF content: {str(e)}" 