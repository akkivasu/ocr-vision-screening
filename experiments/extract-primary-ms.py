"""
This code sample shows Prebuilt Layout operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint = "https://document4.cognitiveservices.azure.com/"
key = "97a7d98113b2471c849fa5d2af567cb7"

# Path to your local PDF file
local_pdf_path = "primary-english.pdf"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Open the local PDF file
with open(local_pdf_path, "rb") as f:
    poller = document_analysis_client.begin_analyze_document("prebuilt-layout", document=f)

result = poller.result()


# for idx, style in enumerate(result.styles):
#     print(
#         "Document contains {} content".format(
#          "handwritten" if style.is_handwritten else "no handwritten"
#         )
#     )

with open("result.json", "w") as file:
    # Write the variable to the file
    file.write(str(result))

# for page in result.pages:
#     for line_idx, line in enumerate(page.lines):
#         print(
#          "...Line # {} has text content '{}'".format(
#         line_idx,
#         line.content.encode("utf-8")
#         )
#     )

#     for selection_mark in page.selection_marks:
#         print(
#          "...Selection mark is '{}' and has a confidence of {}".format(
#          selection_mark.state,
#          selection_mark.confidence
#          )
#     )

# for table_idx, table in enumerate(result.tables):
#     print(
#         "Table # {} has {} rows and {} columns".format(
#         table_idx, table.row_count, table.column_count
#         )
#     )
        
#     for cell in table.cells:
#         print(
#             "...Cell[{}][{}] has content '{}'".format(
#             cell.row_index,
#             cell.column_index,
#             cell.content.encode("utf-8"),
#             )
#         )

# print("----------------------------------------")

