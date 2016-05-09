import io
from flask import Flask, request, send_file
from PIL import Image
from PIL.ImagePalette import ImagePalette
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

PAGE = """
<h1>Quantize to 4 colors</h1>
<span>Upload an image <8 MB!</span>
<form action="submit" method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
"""

@app.route('/')
def hello_world():
    return PAGE

@app.route('/submit', methods=['POST'])
def upload_image():
    image = Image.open(request.files['file']).convert('RGB')
    quantized = image.quantize(colors=4, method=1, kmeans=8)
    asbytes = io.BytesIO()
    quantized.save(asbytes, format='png')
    asbytes.seek(0)
    return send_file(asbytes, attachment_filename="quantized.png", as_attachment=True)    

if __name__ == '__main__':
    app.run()

