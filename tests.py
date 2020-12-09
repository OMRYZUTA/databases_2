import ex2

tests = [
    {
        "query": "SELECT * FROM Customers, Orders WHERE ((Customers.Name='Mike') AND Orders.Price>1000) OR 3=1;",
        "expected": "Valid",
    },
    {
        "query": "SELECT Customers.Name FROM Customers WHERE Customers.Age=25;",
        "expected": "Valid",
    },
    {
        "query": "   SELECT Customers.Name FROM Customers WHERE    Customers.Name='Mike'      ;",
        "expected": "Valid",
    },
    {
        "query": "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE Customers.Name=Orders.CustomerName;",
        "expected": "Valid",
    },
    {
        "query": "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE Customers.Name=Orders.CustomerName AND Orders.Price>1000;",
        "expected": "Valid",
    },
    {
        "query": "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName) AND Orders.Price>1000;",
        "expected": "Valid",
    },
    {
        "query": "SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName) OR (Orders.Price>59);",
        "expected": "Valid",
    },

    {
        "query": "SELECT DISTINCT * FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName) OR (Orders.Price>1000);",
        "expected": "Valid",
    },
    {
        "query": "SELECT DISTINCT * FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName)OR (Orders.Price>1000);",
        "expected": "Valid",
    },
    {
        "query": "SELECT DISTINCT * FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName)AND(Orders.Price>1000);",
        "expected": "Valid",
    },
]


def main():
   pass


if __name__ == "__main__":
    main()
