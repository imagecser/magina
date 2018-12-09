from magina import create_app, app

create_app('ctx')
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', port=80, use_reloader=False)
