from init import createFlask

app = createFlask()
    
if __name__ == '__main__':
    app.run(host='localhost', port=5000)