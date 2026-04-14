from retrieveDocuments import retrieveGodotDocumentationFromSource
from chunkDocuments import chunkDocuments
from embedDocuments import embedDocuments

import asyncio

def prepareRAGStore():
    try:
        retrieveGodotDocumentationFromSource()
        chunkDocuments()
        embedDocuments()

    except Exception as e:
        print("prepareRAGStore Error: ", e)
        raise e

prepareRAGStore()