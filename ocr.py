from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io

def pdfocr(location):
    # global tool, lang
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0]
    req_image = []
    final_text = []

    image_pdf = Image(filename = location, resolution = 300)
    image_jpeg = image_pdf.convert('jpeg')

    for img in image_jpeg.sequence:
        img_page = Image(image = img)
        req_image.append(img_page.make_blob('jpeg'))

    ct = 1
    for img in req_image:
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang = lang,
            builder = pyocr.builders.TextBuilder()
        )
        final_text.append(txt)
        print("%3d / %3d" % (ct, len(req_image)))
        ct += 1

    for frame in image_jpeg.sequence:
        frame.destroy()
    return final_text

# res = pdfocr("Cora_Downloaded/2420/2420.ps.pdf")
# print(len(res))
