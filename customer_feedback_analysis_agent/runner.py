from builder import agent
from icecream import ic

if __name__ == "__main__":
    input = {
        "input_text": """Great powerbank. Durable. Huge capacity and is able to charge as fast in as it does out. Powerbank will get a little hot as you do this which is normal, the large size will help dissipate the heat.

Pretty clunky and heavy so it might be pushing it for a 1L belt bag but if you are backpacking / using a laptop bag it is perfect for day trips, weekends where you dont expect to see an outlet.

Capable of charging my steam deck and fast charging my phone with no issues. You can top up your laptops with this too but be aware it will be a little slow to charge if you are also using the laptop at the same time. Will not keep up if at high loads. Great value on sale."""
    }
    app = agent()
    result = app.invoke(input)
    ic(result)
