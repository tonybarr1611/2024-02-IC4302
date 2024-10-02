from init import createFlask

app = createFlask()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)