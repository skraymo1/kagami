import azure.durable_functions as df
from langchain_core.documents import Document
import json, os
from kernel_factory import KernelFactory
import semantic_kernel as sk
from typing import List

analyze_sentiment_blueprint = df.Blueprint()


@analyze_sentiment_blueprint.activity_trigger(input_name="chunks")
async def analyze_sentiment(chunks: List[Document]) -> dict:
    kernel = KernelFactory.create_kernel()

    # for larger documents the chunk size maybe too large for the plugin to handle simultaneously
    joined_chunks = f"{os.linesep}".join(chunks)

    skresult = await kernel.invoke(
        kernel.plugins["SummaryPlugin"]["AreStudyFindingsSignificant"],
        sk.KernelArguments(input=joined_chunks),
    )

    # Attempt to parse the JSON string
    try:
        return json.loads(skresult.value[0].content)
    except json.JSONDecodeError:
        return None
