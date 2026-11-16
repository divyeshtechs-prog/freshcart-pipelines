
from stream.driver import DRIVERS


def topic_matches(pattern, routing_key):
    """Match RabbitMQ topic patterns: * matches one word, # matches zero or more."""
    pattern_parts = pattern.split(".")
    key_parts = routing_key.split(".")

    def match(p, k):
        if p == len(pattern_parts):
            return k == len(key_parts)

        token = pattern_parts[p]

        if token == "#":
            return any(
                match(p + 1, next_k)
                for next_k in range(k, len(key_parts) + 1)
            )

        if k == len(key_parts):
            return False

        if token == "*" or token == key_parts[k]:
            return match(p + 1, k + 1)

        return False

    return match(0, 0)


def recipients(routing_key):
    return {
        queue
        for queue, pattern in DRIVERS.items()
        if topic_matches(pattern, routing_key)
    }


def test_rapido_routing_rules():
    assert recipients("bangalore.koramangala.food") == {
        "ravi", "meena", "control"
    }

    assert recipients("bangalore.indiranagar.ride") == {
        "priya", "arjun", "control"
    }

    assert recipients("bangalore.whitefield.ride") == {
        "arjun", "control"
    }

    assert recipients("chennai.tnagar.food") == {
        "karthik"
    }

    assert recipients("chennai.whitefield.ride") == set()

    assert recipients("bangalore.koramangala") == {
        "control"
    }
