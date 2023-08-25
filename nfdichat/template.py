# -*- coding: utf-8 -*-
"""
ChatBot prompt template handler
"""
from langchain.prompts import PromptTemplate

template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.

```
{context}
```

Question:
```{question}```

Answer:
"""

CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)
