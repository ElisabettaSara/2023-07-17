from database.DB_connect import DBConnect
from model.product import Product


class DAO():

    @staticmethod
    def getAnno():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(`Date`) as anno
                    from go_daily_sales gds """

        cursor.execute(query,)
        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getColore():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct gp.Product_color as color
                    from go_products gp """

        cursor.execute(query, )
        for row in cursor:
            result.append(row["color"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProdotti(colore):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct gp.Product_number as product
                    from go_products gp
                    where gp.Product_color = %s"""

        cursor.execute(query, (colore,) )
        for row in cursor:
            result.append(row['product'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(colore, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select g1.p as p1, g2.p as p2, count(distinct g1.d1) as peso
                    from(select gds.Product_number as p, gds.`Date` as d1, gds.Retailer_code as r1
                        from go_daily_sales gds , go_products gp 
                        where gp.Product_color =%s 
                        and gds.Product_number = gp.Product_number)  g1,
                        (select gds.Product_number as p, gds.`Date` as d2, gds.Retailer_code as r2
                        from go_daily_sales gds , go_products gp 
                        where gp.Product_color =%s
                        and gds.Product_number = gp.Product_number ) g2
                    where g1.p<g2.p and year(g1.d1)=%s and g1.d1=g2.d2
                    and g1.r1= g2.r2
                    group by g1.p,g2.p"""

        cursor.execute(query, (colore, colore, anno,) )
        for row in cursor:
            result.append((row["p1"],row["p2"],row["peso"]))

        cursor.close()
        conn.close()
        return result





