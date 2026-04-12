## Pydantic + Redis Vector Database as RAG


## Resources

- https://pydantic.dev/docs/ai/examples/data-analytics/rag/
- https://pydantic.dev/docs/ai/guides/embeddings/#_top

<hr>

## Retrieval Augmented Generation (RAG) Steps:
1. Prepare raw documents (Ex. Text, Files, Images, etc)
    - Collect , clean, normalise data/ documents and add metadata, etc
2. Chunking you raw documents (Optional for Small Documents)
    - Chunking is the process of partitioning large documents into smaller chunks, which would be then be vector embedded
    - Chunking allows for higher precision matches/ retrieval when vector embedded, allowing for better partial matching within documents
3. Select Embedding Model
    - Choose Embedding Model depending on your use case (Ex. Text, Files, Images, etc)
4. Create Vector Embedding Database
5. Populate the Vector Embedding Database with Vector Embedding Entries
    - This database will contain vector embeddings of chunks/ raw documents
6. In order to query the Vector Embedding Database, you will need to vector embed your Text Query
    - You will then be returned the closest documents/ chunks to the vector embedded Text Query in the vector space
    - You can also build a Vector Index (ANN Data Structures) to speed up Vector Embed Queries