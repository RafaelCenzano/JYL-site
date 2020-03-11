from jyl import app

# Run Flask app
app.run(
    host='0.0.0.0', # host to view from outside the network
    port=8080 # assign to port 8080
)