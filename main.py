from flask import Flask, request, send_file, jsonify, Response, render_template
from flask_cors import CORS
import tempfile
import os
import traceback
import logging
import shutil
import converted as cn
from waitress import serve


app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('PDF-Converter')

@app.route('/', methods=['GET'])
def home():
    # server_ip = request.host
    return render_template("index.html", title="Home Page", server_ip="10.1.2.58:5000")


@app.route('/convert', methods=['POST'])
def convert():
    tmp_dir = None
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'Empty file'}), 400

        tmp_dir = tempfile.mkdtemp()
        pdf_path = os.path.join(tmp_dir, 'input.pdf')
        app.logger.info(f'{file.filename[:-4]}.docx')
        name = file.filename[:-4]
        docx_path = os.path.join(tmp_dir, f'{name}.docx')
        
        file.save(pdf_path)

        if not cn.convert_pdf_to_docx_advanced(pdf_path, docx_path, logger):
            return jsonify({'error': 'Conversion failed'}), 500

        return send_file(
            docx_path,
            as_attachment=True,
            download_name=f'{name}.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        logger.error(f"Error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500
    finally:
        if tmp_dir and os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)

if __name__ == '__main__':
    serve(app, host='10.1.2.58', port=5000)