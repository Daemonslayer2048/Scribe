from Scribe.web import app
from . import db
import os

if __name__ == "__main__":
    app.run()
else:
    if not os.path.exists("./Scribe.db"):
        print(" * Building Database")
        db.build_db()
        print(" * Database built")
    print(" * Database exists")
