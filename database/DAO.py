from database.DB_connect import DBConnect
from model.product import Product


class DAO():

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct(extract(year from `Date`)) as years
                    from go_daily_sales
                    """

        cursor.execute(query,)
        for row in cursor:
            result.append(row['years'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getColors():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct(Product_color)
                    from go_products gp """

        cursor.execute(query, )
        for row in cursor:
            result.append(row['Product_color'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select Product_number, Product, Product_color, Unit_cost, Unit_price
                    from go_products gp 
                    where gp.Product_color = 'white'"""

        cursor.execute(query, )
        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnection(idMap, colore, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t1.p1, t2.p2, count(distinct(t1.d1)) as peso
                    from (select Retailer_code as r1, gds.Product_number as p1, `Date` as d1
                            from go_daily_sales gds, go_products gp 
                            where gp.Product_color = %s and extract(year from `Date`) = %s and gds.Product_number = gp.Product_number) t1,
                        (select Retailer_code as r2, gds.Product_number as p2, `Date` as d2
                            from go_daily_sales gds, go_products gp 
                            where gp.Product_color = %s and extract(year from `Date`) = %s and gds.Product_number = gp.Product_number) t2
                    where t1.r1 = t2.r2 and t1.d1 = t2.d2 and t1.p1 < t2.p2
                    group by t1.p1, t2.p2"""

        cursor.execute(query, (colore, anno, colore, anno,))
        for row in cursor:
            result.append((idMap[row['p1']],
                           idMap[row['p2']],
                           row['peso']))

        cursor.close()
        conn.close()
        return result