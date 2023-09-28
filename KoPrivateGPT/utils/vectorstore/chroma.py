from typing import List

from langchain.vectorstores import Chroma

from KoPrivateGPT.schema import Passage
from KoPrivateGPT.utils.vectorstore.base import SlimVectorStore


class ChromaSlim(Chroma, SlimVectorStore):
    def add_passages(self, passages: List[Passage]):
        embeddings = None
        if self._embedding_function is not None:
            contents = [passage.content for passage in passages]
            embeddings = self._embedding_function.embed_documents(contents)
        metadatas = [{"passage_id": passage.id} for passage in passages]
        self._collection.upsert(
            embeddings=embeddings,
            metadatas=metadatas,
            ids=[str(passage.id) for passage in passages],
            documents=["" for _ in range(len(passages))]
        )
