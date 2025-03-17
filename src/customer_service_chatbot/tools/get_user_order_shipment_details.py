from google.cloud import bigquery
from langchain_core.tools import tool
from .settings import configurations


@tool
def get_user_order_shipment_details(orderNo: str):
    """
    Retrieves shipment tracking details for a specific customer order from BigQuery.

    This tool queries the customer order shipment tracking database to fetch
    information about shipment status and events. It returns shipment numbers,
    event types, and dates associated with a given order number.

    Returns:
    --------
    list of dict
        A list of dictionaries containing shipment tracking information with the following keys:
        - shipmentNo: The shipment tracking number
        - eventType: The type of shipment event (e.g., "SHIPPED", "DELIVERED", "IN_TRANSIT")
        - eventDate: The date when the event occurred (as a date object)

    Example:
    --------
    >>> get_user_order_shipment_details("92859697")
    [
        {"shipmentNo": "TRK123456", "eventType": "SHIPPED", "eventDate": datetime.date(2023, 5, 15)},
        {"shipmentNo": "TRK123456", "eventType": "DELIVERED", "eventDate": datetime.date(2023, 5, 18)}
    ]

    Notes:
    ------
    - The function queries the bigquery table with the customer's order sjipment tracking data
    - The original timestamp (eventTime) is converted to date only (eventDate) and the eventTime column is dropped
    """

    client = bigquery.Client()
    QUERY = (
        f"""
        SELECT shipmentNo, eventTime, eventType 
        FROM `{configurations.shipment_table}`
        Where orderNo = "{orderNo}"
    """)
    query_job = client.query(QUERY)
    result = query_job.result()
    if result:
        df = result.to_dataframe()
        return "Following are user orders:" + str(df.to_dict('records'))
    return "No user orders found!"

