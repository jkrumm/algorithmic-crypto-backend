from app import create_app

app = create_app()


@app.route('/status', methods=['GET'])
def status():
    return 'Running!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
