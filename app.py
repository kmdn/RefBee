# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

from flask import Flask
from flask_cors import CORS, cross_origin
import refbee


app = Flask(__name__)
CORS(app)
@app.route("/<wd_person_id>")
@cross_origin()
def query(wd_person_id):
    # wd_person_id = "Q57231890"

    return refbee.query(wd_person_id)
    """
    Currently: 'title': '<paper1>' may be removed due to title being used as paper key - may change in future ;)
        return format: 
        { '<wd_person_id>': { '<paper1>': {   'title': '<paper1>', 
                                            '<platform1>': 0, 
                                            '<platform2>': 1, ...,
                            '<paper2>': {...} 
                            }
        }
        ...
    """


if __name__ == '__main__':
    app.run()
    """
    Idea: Query Wikidata with a person's identifier (e.g. "Q57231890") and find their publications from other related 
                                                                    platforms via getting their IDs for said platforms
    """
