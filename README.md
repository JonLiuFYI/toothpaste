# toothpaste 0.1
A simple Python 3 API for managing store inventories. Developed in a test-driven approach.

Requires Flask 1.0.2 and Connexion 2.2.0 (Swagger should be included with Connexion). Unit testing requires Pytest.

## Using toothpaste
To launch the server, in your terminal, go to the toothpaste directory and execute `server.py` or run `python server.py` (if Python 3 isn't default on your system, use `python3 server.py` instead).

See API documentation and test run it: http://localhost:5000/api/ui

Run unit tests: run `pytest` in this directory.

## Assorted musings
* Adding an item to the cart is vulnerable to abuse by sending an item with a valid title but wrong inventory_count
* Shop should really be a singleton
* In its current state, Cart is basically a crappy singleton. This would prepare for an eventual extension to have multiple carts for different users.
* There should have been a CartListing class that contains Item and purchase quantity data. This way, Cart would just maintain a list of CartListings instead of clumsily juggling dicts.
* There's no real reason why this is called toothpaste
