import random

def enrich(sender_email: str) -> dict:
    companies = ["Acme Corp", "Globex", "Initech", "Umbrella"]
    industries = ["Software", "Finance", "Healthcare", "Retail"]
    roles = ["Manager", "Director", "Engineer", "VP"]
    return {
        "company": random.choice(companies),
        "industry": random.choice(industries),
        "size": random.choice(["1-10", "11-50", "51-200", "500-1000"]),
        "contact_role": random.choice(roles)
    }
