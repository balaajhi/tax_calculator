from app.controller import app


@app.route('/health')
def hello_world():  # test health of endpoint
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, port=8080)
