# from docarray import DocumentArray, Document
# import json
# from jina import Client

# # Load and preprocess data
# da = DocumentArray()

# with open('icecat-products-w_price-19k-20201127.json') as f:
#     jdocs = json.load(f)
# for doc in jdocs:
#     d = Document(
#         text=" ".join(
#             [
#                 doc[item]
#                 for item in doc
#                 if item.startswith("title")
#                 or item.startswith("attr_t")
#                 or item.startswith("short_description")
#                 or item.startswith("name")
#                 or item.startswith("supplier")
#             ]
#         ),
#         tags=doc,
#     )
#     da.append(d)

# # Define the Flow connection (client-side)
# client = Client(host='http://localhost:8080')

# # Index data
# with client.post('/index', inputs=da) as response:
#     # Handle potential errors during indexing (optional)
#     try:
#         # If there's an error, it'll raise an exception
#         response.data.head()  # Trigger any errors early
#     except Exception as e:
#         print(f"Error during indexing: {e}")
#         # Handle the error appropriately (e.g., retry, log, etc.)

# # Query examples
# query1 = Document(text='laptop case')
# with client.post('/search', inputs=query1, return_type=DocumentArray) as response:
#     results = response.data
#     print(f"Query: '{query1.text}' - Top match tags: {results[0].matches[0].tags}")
# from docarray import DocumentArray, Document
import json
from jina import Client
from typing import List, Optional
from docarray import DocList, BaseDoc
from docarray.typing import NdArray


class MyDoc(BaseDoc):
    text: str
    embedding: Optional[NdArray] = None


class MyDocWithMatches(MyDoc):
    matches: DocList[MyDoc] = []
    scores: List[float] = []


# Load and preprocess data
docs = DocList()

with open('icecat-products-w_price-19k-20201127.json') as f:
    jdocs = json.load(f)
for doc in jdocs:
    d = MyDoc(
        text=" ".join(
            [
                doc[item]
                for item in doc
                if item.startswith("title")
                or item.startswith("attr_t")
                or item.startswith("short_description")
                or item.startswith("name")
                or item.startswith("supplier")
            ]
        ),
        tags=doc,
    )
    docs.append(d)

# Define the Flow connection (client-side)
client = Client(host='http://localhost:8080')

# Prepare documents for indexing (converted to MyDoc format)
docs_to_index = DocList[MyDoc]()
for doc in docs:
    new_doc = MyDoc(text=doc.text)  # Convert to MyDoc format
    docs_to_index.append(new_doc)

# Index data (with request_size for chunking)
indexed_docs = client.post(
    '/index',
    inputs=docs_to_index,
    return_type=DocList[MyDoc],
    request_size=10,  # Consider adjusting based on data size and server resources
)

print(f'Indexed documents: {len(indexed_docs)}')

# Prepare query documents
query_docs = DocList[MyDoc]()
for i in range(10):
    query_doc = MyDoc(text=f'bag')
    query_docs.append(query_doc)

# Search with request_size for chunking and expected MyDocWithMatches response type
search_results = client.post(
    '/search',
    inputs=query_docs,
    # return_type=DocList[MyDocWithMatches],
    # return_type=List[MyDoc],
    # return_type=MyDocWithMatches, 
    return_type=DocList[MyDoc],
    request_size=10,  # Consider adjusting based on data size and server resources
)

for doc in search_results:
    # print(f'Query {doc.text} has {len(doc.matches)} matches')
    print(f'Query {doc.text} has {len(getattr(doc, "matches", []))} matches')