import tabula
import csv

def pdf_to_csv(pdf_path, csv_path):
    # Extract tabular data from the PDF
    df = tabula.read_pdf(pdf_path, pages='all')
    
    # Write the extracted data to a CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for index, page in enumerate(df):
            # Write each page's data into the CSV file
            page.to_csv(csv_file, index=False, header=(index == 0))

# Example usage
pdf_to_csv('barimt1.pdf', 'example.csv')
