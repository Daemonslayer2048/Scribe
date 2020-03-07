from Scribe.web import app
import os

if __name__ == "__main__":
    app.run()
else:
    if not os.path.exists("./Scribe.db"):
        print(" * Building Database")
        print(" * Database built")
    print(" * Database exists")
