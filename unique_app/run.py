from market import app


# Run the app 
# use_reloader=True : to reload the server when we make changes to the code (helpful when changing things in DB)
if __name__ == '__main__':
    app.run(debug=True , use_reloader=True)



