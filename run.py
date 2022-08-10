from project.config import config
from project.models import Genres, Movies, Directors, Users
from project.server import create_app, db

app = create_app(config)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genres": Genres,
        "Movies": Movies,
        "Directors": Directors,
        "Users": Users
    }

if __name__ == "__main__":
    app.run(port=1080, debug=True)
