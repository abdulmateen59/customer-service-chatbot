from google.cloud import bigquery
from langchain_core.tools import tool
from .settings import configurations


@tool
def get_user_order_return_details(orderNo: str):
    """
    Retrieves return/refund details for a specific customer order from BigQuery.

    This tool queries the customer order return database to fetch information
    about return requests associated with a given order number. It returns details
    such as return event types, return numbers, reasons, and status.

    Parameters:
    -----------
    orderNo : str
        The unique order number to look up return details for.
        Example: "89385937"

    Returns:
    --------
    list of dict
        A list of dictionaries containing return information with the following keys:
        - eventType: The type of return event (e.g., "kundenretoure-wahrscheinlich-abgeschlossen")
        - retourNo: The unique identifier for the return request
        - returnReason: The reason provided for the return (may be None)
        - status: The current status of the return (may be None)
        - eventDate: The date when the return event occurred (as a date object)

    Example:
    --------
    >>> get_user_order_return_details("89385937")
    [
        {
            "eventType": "kundenretoure-wahrscheinlich-abgeschlossen",
            "retourNo": "75afc83f-abc3-47c5-8e9e-ae7104501977",
            "returnReason": None,
            "status": None,
            "eventDate": datetime.date(2024, 12, 24)
        }
    ]

    Notes:
    ------
    - The function queries the bigquery table with the customer's order retour data
    - The original timestamp (eventTime) is converted to date only (eventDate) and the eventTime column is dropped
    - If no returns exist for the order, an empty list will be returned
    """

    client = bigquery.Client()
    QUERY = (
        f"""
        SELECT eventType, eventTime, retourNo, returnReason, status  
        FROM `{configurations.retour_table}`
        Where orderNo = "{orderNo}"
    """)
    query_job = client.query(QUERY)
    result = query_job.result()
    if result:
        df = result.to_dataframe()
        return str(df.to_dict('records'))
    else:
        return "No user returs found."
