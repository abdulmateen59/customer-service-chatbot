from google.cloud import bigquery
from langchain_core.tools import tool
from .settings import configurations


@tool
def get_user_latest_orders(customer_id: str):
    """
    Retrieves the latest orders for a specific customer from BigQuery.

    This tool queries the customer order details database to fetch information
    about a customer's most recent orders. It returns the order numbers, dates,
    and article names for up to 3 of the customer's most recent orders.

    Returns:
    --------
    list of dict
        A list of dictionaries containing order information with the following keys:
        - orderNo: The unique order number
        - articleNames: A list of article names included in the order
        - orderDate: The date when the order was placed (as a date object)

    Example:
    --------
    >>> get_user_latest_orders("3148f986-yhju-1234-1234-4e7ab6cc6a68")
    [
        {
            "orderNo": "92859697",
            "articleNames": ["Nike Shoes", "Adidas T-shirt"],
            "orderDate": datetime.date(2023, 6, 15)
        },
        {
            "orderNo": "92859123",
            "articleNames": ["Puma Jacket"],
            "orderDate": datetime.date(2023, 5, 10)
        }
    ]

    Notes:
    ------
    - The function queries the bigquery table with the customer's order data
    - Orders with eventType "position-storniert" (canceled positions) are excluded
    - Results are limited to the 3 most recent orders, sorted by order time
    - Article names are converted from comma-separated strings to lists
    - The original timestamp (orderTime) is converted to date only (orderDate) and the orderTime column is dropped
    """

    client = bigquery.Client()
    QUERY = (
        f"""
    SELECT
        cod.orderNo,
        cod.orderTime,
        --  Aggregate article names into a single string. Consider using ARRAY_AGG if you need an array.
        STRING_AGG(DISTINCT cod.articleName, ', ' ORDER BY cod.articleName) AS articleNames
    FROM
        `{configurations.order_table}` AS cod
    WHERE cod.customerID = "{customer_id}" AND eventType != "position-storniert"
    GROUP BY cod.orderNo, cod.orderTime  -- Important: Group by non-aggregated columns
    ORDER BY cod.orderTime DESC  -- Order for better presentation (optional)
    LIMIT 3;
    """)
    query_job = client.query(QUERY)
    result = query_job.result()
    if result:
        df = result.to_dataframe()
        df['articleNames'] = df['articleNames'].str.split(',').apply(
            lambda x: [item.strip() for item in x] if isinstance(x, list) else x)
        return str(df.to_dict('records'))
    return "There are no orders for the respective customer"
