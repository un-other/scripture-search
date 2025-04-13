"""Run Scripture Search."""

from scripture_search.search.simple_search import SimpleSearch


def main():
    """Run Scripture Search."""
    search = SimpleSearch()
    while True:
        query = input("Enter a query to search for scriptures or type 'q' to quit: ")
        if query.lower() == "q":
            break
        results = search.run(query)
        print(results)

if __name__ == "__main__":
    main()
