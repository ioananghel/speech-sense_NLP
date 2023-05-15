# __init__.py makes the website dir a python package
from website import create_app

app = create_app()

# you want it to run the server only if it's being run from this file
if __name__ == '__main__':
    # reruns the server on every change
    app.run(debug=True)
