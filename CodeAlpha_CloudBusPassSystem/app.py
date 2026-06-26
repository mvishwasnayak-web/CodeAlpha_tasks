from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

ROUTE_PRICES = {
    "Mangalore-Ujire": 80,
    "Mangalore-Dharmasthala": 120,
    "Mangalore-Belthangady": 100
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/routes")
def routes():
    return render_template("routes.html")

@app.route("/booking")
def booking():
    return render_template("booking.html")

@app.route("/book-pass", methods=["POST"])
def book_pass():

    name = request.form["passenger_name"]

    route = request.form["route"]

    price = ROUTE_PRICES[route]

    pass_id = f"PASS{random.randint(1000,9999)}"

    booking = {
        "pass_id": pass_id,
        "name": name,
        "route": route,
        "price": price
    }

    with open("bookings.json", "r") as file:
        data = json.load(file)

    data.append(booking)

    with open("bookings.json", "w") as file:
        json.dump(data, file, indent=4)

    return render_template(
        "success.html",
        pass_id=pass_id,
        name=name,
        route=route,
        price=price
    )
@app.route("/bookings")
def bookings():

    with open("bookings.json", "r") as file:
        data = json.load(file)

    return render_template(
        "bookings.html",
        bookings=data
    )
@app.route("/search", methods=["GET", "POST"])
def search():

    booking = None

    searched = False

    if request.method == "POST":

        pass_id = request.form["pass_id"]

        searched = True

        with open("bookings.json", "r") as file:
            data = json.load(file)

        for item in data:

            if item["pass_id"] == pass_id:

                booking = item

                break

    return render_template(
        "search.html",
        booking=booking,
        searched=searched
    )
if __name__ == "__main__":

    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )