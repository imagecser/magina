from magina import create_app, app

if __name__ == '__main__':
    create_app('dev')
    app.run(host='0.0.0.0', port=80)
