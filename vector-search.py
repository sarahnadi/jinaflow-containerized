# import json
# from jina import Client
# from typing import List, Optional
# from docarray import DocList, BaseDoc
# from docarray.typing import NdArray


# class MyDoc(BaseDoc):
#     text: str
#     embedding: Optional[NdArray] = None


# class MyDocWithMatches(MyDoc):
#     matches: DocList[MyDoc] = []
#     scores: List[float] = []


# # Load and preprocess data
# docs = DocList()

# with open('icecat-products-w_price-19k-20201127.json') as f:
#     jdocs = json.load(f)
# for doc in jdocs:
#     d = MyDoc(
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
#     docs.append(d)

# # Define the Flow connection (client-side)
# client = Client(host='http://localhost:8080')

# # Prepare documents for indexing (converted to MyDoc format)
# docs_to_index = DocList[MyDoc]()
# for doc in docs:
#     new_doc = MyDoc(text=doc.text)  # Convert to MyDoc format
#     docs_to_index.append(new_doc)

# # Index data (with request_size for chunking)
# indexed_docs = client.post(
#     '/index',
#     inputs=docs_to_index,
#     return_type=DocList[MyDoc],
#     request_size=10,  # Consider adjusting based on data size and server resources
# )

# print(f'Indexed documents: {len(indexed_docs)}')

# # Prepare query documents
# query_docs = DocList[MyDoc]()
# for i in range(10):
#     query_doc = MyDoc(text=f'bag')
#     query_docs.append(query_doc)

# # Search with request_size for chunking and expected MyDocWithMatches response type
# search_results = client.post(
#     '/search',
#     inputs=query_docs,
#     # return_type=DocList[MyDocWithMatches],
#     # return_type=List[MyDoc],
#     # return_type=MyDocWithMatches, 
#     return_type=DocList[MyDoc],
#     request_size=10,  # Consider adjusting based on data size and server resources
# )

# for doc in search_results:
#     # print(f'Query {doc.text} has {len(doc.matches)} matches')
#     print(f'Query {doc.text} has {len(getattr(doc, "matches", []))} matches')

import json
from jina import Client
from typing import List, Optional
from docarray import DocList, BaseDoc
from docarray.typing import NdArray

class MyDoc(BaseDoc):
    text: str
    embedding: Optional[NdArray] = None

# Load and preprocess data (directly using DocList)
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

# Directly index the original DocList
indexed_docs = client.post(
    '/index',
    inputs=docs,
    return_type=DocList,
    request_size=10,  # Adjust if needed
)

print(f'Indexed documents: {len(indexed_docs)}')

# Prepare query documents
query_docs = DocList(MyDoc(text=f'bag') for _ in range(10))

# Search with correct return type
search_results = client.post(
    '/search',
    inputs=query_docs,
    return_type=DocList,  # Response already includes matches
    request_size=10,  # Adjust if needed
)

for doc in search_results:
    print(doc)
    print(f'Query {doc.text} has {len(doc.matches)} matches')
    for match in doc.matches:
        print(match.tags)  # Access full product details
