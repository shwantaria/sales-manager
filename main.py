import psycopg2
from flask import Flask, request, render_template, redirect
from werkzeug.utils import redirect
app = Flask(__name__)


# con = psycopg2.connect(user="postgres", password="12345",
#                        host="localhost", port="5432", database="myduka")

con = psycopg2.connect(user="xzwcjyaweniagb", password="7ce28f98e33edaa731ab2d67132849d19e33fa14c317e64266f6cd51829333e4",
                       host="ec2-52-30-81-192.eu-west-1.compute.amazonaws.com", port="5432", database="dfsf4q0tk84onh")

cur = con.cursor()
cur.execute("select * from product2")
cur.execute("CREATE TABLE IF NOT EXISTS product2 (id serial PRIMARY KEY,name VARCHAR(100),buying_price INT,selling_price INT,stock_quantity INT) ;")
cur.execute("CREATE TABLE IF NOT EXISTS sales3 (sales_id serial PRIMARY KEY,pid INT,quantity INT,created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()) ;")
con.commit()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('basic.html')


@app.route('/contact')
def contact_us():
    cur = con.cursor()
    cur.execute("""SELECT SUM(product2.selling_price-product2.buying_price) as profit,product2.name from sales3
    join product2 on product2.id=sales3.pid
    GROUP BY product2.name""")

    d = (cur.fetchall())
    # print("d",d)
    e = []
    z = []
    for i in d:
        e.append(i[0])
        z.append(i[1])
    print("e", e)
    print("z", z)


    

    return render_template('index.html', d=d, e=e, z=z)


@app.route('/sales')
def sales():
    cur = con.cursor()
    cur.execute("""SELECT sales3.sales_id,sales3.quantity,product2.name,product2.buying_price,product2.selling_price,(product2.selling_price-product2.buying_price)*sales3.quantity AS profit FROM sales3 join product2
    on product2.id=sales3.pid;""")

    sales = (cur.fetchall())
    p3 = sales
    return render_template('sales.html', p3=p3,)


@app.route('/sale', methods=["POST", "GET"])
def sale():
    if request.method == "POST":
        cur = con.cursor()
        pid = request.form["Item-id"]
        sales_quantity = request.form["item-quantity"]
        cur.execute("""INSERT INTO sales3 (pid,quantity) VALUES (%(pid)s,%(sales_quantity)s)""", {
                    "pid": pid, "sales_quantity": sales_quantity})
        con.commit()
        return redirect('/sales')


@app.route('/products', methods=["POST", "GET"])
def product():
    if request.method == "POST":
        cur = con.cursor()
        n = request.form["name"]
        b = request.form["buying_price"]
        s = request.form["selling_price"]
        q = request.form["stock_quantity"]
        cur.execute("""INSERT INTO product2 (name,buying_price,selling_price,stock_quantity) VALUES (%(n)s,%(b)s,%(s)s,%(q)s)""", {
                    "n": n, "b": b, "s": s, "q": q})
        return redirect('/products')

    else:
        cur = con.cursor()
        cur.execute("select * from product2")
        products = cur.fetchall()
        f1 = products
        return render_template('table2.html', f1=f1)


@app.route('/form')
def form():
    cur = con.cursor()
    cur.execute("select * from product2")
    products = (cur.fetchall())
    f2 = products

    return render_template('table.html', f2=f2)


@app.route('/sales')
def sal():
    cur = con.cursor()
    cur.execute("""select sales.sales_id,products.name,products.stock_quantity,(products.selling_price-products.buying_price)*sales.quantity as profit from products
    join sales on sales.pid=products.id""")
    sales = (cur.fetchall())
    p3 = sales
    return render_template('sales.html', p3=p3,)


if __name__ == "__main__":
    app.run(debug=True)
