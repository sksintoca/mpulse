from mpulse import create_app

# main python code to creat and run app/server
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
