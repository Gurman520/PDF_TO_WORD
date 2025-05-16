import pdfplumber
from pdf2docx import Converter
from docx import Document
from docx.shared import Pt


def enhance_document(pdf_path, docx_path, logger):
    """Улучшение форматирования документа"""
    try:
        doc = Document(docx_path)
        
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                # Извлечение точных координат текста
                words = page.extract_words(
                    x_tolerance=1,
                    y_tolerance=1,
                    keep_blank_chars=False,
                    use_text_flow=True
                )
                
                # Настройка стилей документа
                for paragraph in doc.paragraphs:
                    paragraph.style.font.size = Pt(11)
                    paragraph.style.font.name = 'Arial'
                
                # Сохранение изображений (если есть)
                if page.images:
                    for img in page.images:
                        # Здесь можно добавить обработку изображений
                        pass
        
        doc.save(docx_path)
        return True
    except Exception as e:
        logger.error(f"Document enhancement failed: {str(e)}")
        return False

def convert_pdf_to_docx_advanced(pdf_path, docx_path, logger):
    """Улучшенная конвертация с сохранением форматирования"""
    try:
        # Основная конвертация через pdf2docx
        cv = Converter(pdf_path)
        cv.convert(docx_path, multi_processing=True)
        cv.close()
        
        # Дополнительная обработка для улучшения качества
        if not enhance_document(pdf_path, docx_path, logger):
            logger.warning("Document enhancement skipped due to errors")
        
        return True
    except Exception as e:
        logger.error(f"Advanced conversion failed: {str(e)}")
        return False