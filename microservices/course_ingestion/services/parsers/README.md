Currently there are two types of Parsers

1 Custom Parsers
These parsers are built based on specific type of documents

Custom PDF Paragraph Parser
This is a more generalised parser which extracts all paragraphs from the given pdf document. This is the default parser for content ingestion

Custom PDF Parser
This parser is built based on a specific set of pdf documents. This will be leveraged where content ingestion is done using parser alone. It extracts different types of headers and corresponding paragraphs and builds course hierarchy. This may not work on a different set of pdf documents
# TODO


Custom HTML Parser
# TODO


2 Openstax Parser

Currently this parser supports only html content and is specifically built to support all openstax courses

Sample Course https://openstax.org/books/concepts-biology/pages/1-1-themes-and-concepts-of-biology
