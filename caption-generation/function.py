import requests
import vertexai
from google.cloud import firestore
from vertexai.vision_models import ImageTextModel, Image

PROJECT_ID = 'REPLACE ME'
LOCATION = 'us-central1'

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = ImageTextModel.from_pretrained("imagetext@001")

def download_file(url, filename):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open the file in binary write mode
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded file: {filename}")
    else:
        print(f"Failed to download file: status code {response.status_code}")


def entrypoint(event, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    # Firestore client creation
    db = firestore.Client()

    # Get the document path
    resource_string = context.resource
    document_path = resource_string.split('/documents/')[1]

    # Get the image path for the document, and download the image
    image_path = event['value']['fields']['image']['stringValue']
    download_file(image_path, "/tmp/image.jpg")
    source_image = Image.load_from_file(location='/tmp/image.jpg')

    captions = model.get_captions(
        image=source_image,
        number_of_results=1,
        language="en",
    )

    # Updating the caption field
    document_reference = db.document(document_path)
    document_reference.update({'caption': captions[0].capitalize()})