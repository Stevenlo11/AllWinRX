import mysql.connector
from mysql.connector import Error

# Function to fetch total purchase cost
def fetch_totals(connection, is_generic=False):
    try:
        cursor = connection.cursor()
        if is_generic:
            # Calculate total for generics
            query = "SELECT SUM(PricePerUnit * QTY) FROM Customer_Data WHERE If_generic = 'Yes'"
        else:
            # Calculate total for all items
            query = "SELECT SUM(PricePerUnit * QTY) FROM Customer_Data"
        cursor.execute(query)
        result = cursor.fetchone()
        total_purchase_cost = result[0] if result else 0  # Ensure we got a result
        cursor.close()
        return total_purchase_cost
    except Error as e:
        print(f"Error: {e}")
        return 0

# Function to calculate generic percentage
def calculate_generic_percentage(generic_total, overall_total):
    if overall_total > 0:
        return (generic_total / overall_total) * 100
    return 0

# Function to fetch discount percentage
def fetch_discount(connection, total_cost, generic_percentage):
    try:
        cursor = connection.cursor()
        query = """
        SELECT Discount_pct_brand FROM Rebate_1_brand 
        WHERE %s >= Monthly_sale_low AND %s <= Monthly_sale_high 
        AND %s >= Generic_Low_pct AND %s <= Generic_High_pct
        """
        cursor.execute(query, (total_cost, total_cost, generic_percentage, generic_percentage))
        result = cursor.fetchone()
        discount = result[0] if result else 0  # Ensure we got a result
        cursor.close()
        return discount
    except Error as e:
        print(f"Error: {e}")
        return 0

# Main script execution
if __name__ == '__main__':
    connection = mysql.connector.connect(
        host='msam.lmu.build',
        database='msamlmub_CapitolDrugs',
        user='msamlmub_cd',
        password='Capit01_D2023'
    )

    if connection.is_connected():
        # Fetch total purchase cost for all items
        total_cost = fetch_totals(connection)
        
        # Fetch total purchase cost for generic items
        generic_cost = fetch_totals(connection, is_generic=True)
        
        # Calculate the generic percentage of total purchase cost
        generic_percentage = calculate_generic_percentage(generic_cost, total_cost)

                # Fetch discount based on total cost and generic percentage
        discount_percentage = fetch_discount(connection, total_cost, generic_percentage)

        # Output the results
        print(f"Total Purchase Cost: ${total_cost:.2f}")
        print(f"Generic Purchase Cost: ${generic_cost:.2f}")
        print(f"Generic Percentage of Total Purchase Cost: {generic_percentage:.2f}%")
        print(f"Applicable Discount Percentage: {discount_percentage:.2f}%")





        connection.close()
