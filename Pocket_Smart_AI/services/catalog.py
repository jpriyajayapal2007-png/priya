from urllib.parse import quote


PLATFORMS = {

    "Amazon":
        "https://www.amazon.in/s?k={q}",

    "Flipkart":
        "https://www.flipkart.com/search?q={q}",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q={q}",

    "Swiggy":
        "https://www.swiggy.com/search?query={q}",

    "Zomato":
        "https://www.zomato.com/search?q={q}",

    "OYO":
        "https://www.oyorooms.com/search?q={q}"
}


def search_url(
    platform: str,
    query: str
) -> str:

    template = PLATFORMS.get(
        platform
    )

    if not template:
        return "#"

    return template.format(
        q=quote(query)
    )


def demo_products(
    category: str,
    budget: float,
    planner: str
) -> list[dict]:

    if planner == "home":

        rows = [

            (
                "Amazon",
                "LED ceiling light",
                1299,
                "lighting"
            ),

            (
                "IKEA",
                "side table",
                2990,
                "furniture"
            ),

            (
                "Amazon",
                "decorative wall art",
                999,
                "decor"
            ),

            (
                "IKEA",
                "dining chair",
                3490,
                "seating"
            ),

            (
                "Flipkart",
                "ceiling fan",
                2499,
                "appliance"
            )
        ]

    elif planner == "party":

        rows = [

            (
                "Swiggy",
                "party catering search",
                350,
                "food"
            ),

            (
                "Zomato",
                "event catering search",
                450,
                "food"
            ),

            (
                "OYO",
                "event/nearby stay search",
                2500,
                "venue"
            ),

            (
                "Amazon",
                "party decoration set",
                799,
                "decor"
            )
        ]

    else:

        rows = [

            (
                "Amazon",
                "minimal necklace set",
                899,
                "necklace"
            ),

            (
                "Flipkart",
                "stud earrings",
                599,
                "earrings"
            ),

            (
                "Amazon",
                "bracelet set",
                749,
                "bracelet"
            ),

            (
                "Flipkart",
                "statement earrings",
                1199,
                "earrings"
            )
        ]

    results = []

    for platform, name, price, kind in rows:

        results.append({

            "name": name,

            "platform": platform,

            "estimated_price": price,

            "category": kind,

            "search_url": search_url(
                platform,
                name
            ),

            "price_note":
                "Demo estimate; verify current price and availability on the platform."
        })

    return results