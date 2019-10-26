import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\Gabija\\Desktop\\Hack\\handwriting-8e91fd0b8d13.json"
from random_word import RandomWords
from PIL import Image

def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    #image1 = Image.open('C:\\Users\\Gabija\\Documents\\BGN_hackathon\\Handwriting\\p.jpg').convert('1')
    #image1.save('C:\\Users\\Gabija\\Documents\\BGN_hackathon\\Handwriting\\p2.jpg')
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    if len(response.full_text_annotation.pages) is 0:
        print("null*************************")
        response = client.text_detection(image=image)
        texts = response.text_annotations

        print('Texts:')
        print(texts)
        for text in texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

    else:
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                print('\nBlock confidence: {}\n'.format(block.confidence))

                for paragraph in block.paragraphs:
                    print('Paragraph confidence: {}'.format(
                        paragraph.confidence))

                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        print('Word text: {} (confidence: {})'.format(
                            word_text, word.confidence))

                        for symbol in word.symbols:
                            print('\tSymbol: {} (confidence: {})'.format(
                                symbol.text, symbol.confidence))



if __name__ == '__main__':
    #r = RandomWords()
    #print(r.get_random_word())
    detect_document('C:\\Users\\Gabija\\Documents\\BGN_hackathon\\Handwriting\\p.jpg')


