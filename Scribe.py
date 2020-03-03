from web import app
import db
import os

if __name__ == "__main__":
    if not os.path.exists("./Scribe.db"):
        print("Building Database")
        db.build_db()
    app.run()
