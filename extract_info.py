import zipfile
import xml.etree.ElementTree as ET

def get_docx_text(path):
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    
    # Parse XML
    tree = ET.XML(xml_content)
    
    # Namespace dictionary
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    paragraphs = []
    
    # Iterate through all w:p (paragraphs)
    for paragraph in tree.iter('{%s}p' % ns['w']):
        texts = []
        for node in paragraph.iter('{%s}t' % ns['w']):
            if node.text:
                texts.append(node.text)
        if texts:
            paragraphs.append(''.join(texts))
            
    return '\n'.join(paragraphs)

if __name__ == '__main__':
    text = get_docx_text('information.docx')
    with open('info_content.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Extraction done.")
