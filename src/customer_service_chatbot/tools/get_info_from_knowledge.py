from google.api_core.client_options import ClientOptions
from langchain_core.tools import tool
from google.cloud import discoveryengine_v1
from .settings import configurations


@tool
def get_info_from_knowledge(query: str) -> str:
    """
    Retrieves an answer from the company's FAQs.

    This tool queries the company's FAQs to fetch relevant information
    based on the provided query. It searches the specified Discovery Engine data store
    and extracts the answer from the structured data of the first search result.

    Parameters:
    -----------
    query : str
        The search query for retrieving information from the knowledge base.

    Returns:
    --------
    str
        The extracted answer from the knowledge base.

    Example:
    --------
    >>> knowledge_base("What is the return policy?")
    "You can return items within 30 days of purchase with a valid receipt."
    """

    api_endpoint = f"{configurations.location}-discoveryengine.googleapis.com"
    client_options = ClientOptions(api_endpoint=api_endpoint)
    client = discoveryengine_v1.SearchServiceClient(client_options=client_options)
    serving_config = f"projects/{configurations.project}/locations/{configurations.location}/dataStores/{configurations.datastore}/servingConfigs/default_search"
    request = discoveryengine_v1.SearchRequest(
        serving_config=serving_config,
        query=query,
        page_size=1,
    )
    response = client.search(request=request)
    document = response.results[0].document
    struct_data = document.struct_data
    return str(dict(struct_data._pb).get("answer"))[14:]
