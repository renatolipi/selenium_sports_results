# TODO:
"""
Create a centralized file which offers some options about:
 - which sports results to scrap
 - output (e.g. JSON file)
"""

from scrappers.motorsports import formula1


if __name__ == "__main__":
    formula1.run_it_all()  # So far it's just printing the output