import vertexai

from google.cloud import firestore
from vertexai.language_models import TextGenerationModel

vertexai.init(project="REPLACE ME", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison")

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

    # Get the value of the "name" field
    name_value = event['value']['fields']['name']['stringValue']
    response = model.predict(
        f"""Write a description for {name_value} which can be used in a travel app""",
        **parameters
    )

    # Updating the description field
    document_reference = db.document(document_path)
    document_reference.update({'description': response.text})