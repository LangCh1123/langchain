from typing import Any, Literal, Sequence

from langchain_core.documents import BaseDocumentTransformer, Document


class ReadabilityTransformer(BaseDocumentTransformer):
    """A transformer that uses the Mozilla Readability library
    to extract the main contentfrom a web page.

    Arguments:
        target: The target format of the extracted content; defaults to "text".
        **readability_options: Additional options to pass to the readability parser.

    Example:
        .. code-block:: python
            from langchain_community.document_transformers import ReadabilityTransformer
            html2text = Html2TextTransformer()
            docs_transform = html2text.transform_documents(docs)
    """

    def __init__(
        self,
        target: Literal["text", "html"] = "text",
        **readability_options: Any,
    ) -> None:
        self.target = target
        self.options = readability_options

    def transform_document(self, document: Document) -> Document:
        try:
            from readability import parse
        except ImportError:
            raise ImportError(
                "readability module not found, "
                "please install it with `pip install python-readability`"
            )

        article = parse(document.page_content, **self.options)

        result = article.text_content if self.target == "html" else article.content

        return Document(page_content=result or "", **document.metadata)

    def transform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        return list(map(self.transform_document, documents))
