from app import create_app

app = create_app()


@app.route('/status', methods=['GET'])
def status():
    return 'Running!'


@app.route('/')
def home():
    return 'Welcome to AlgorithmicCrypto.com'


if __name__ == '__main__':
    app.run()
