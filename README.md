 # bozzatesi

Base.html contains data common to all pages

start.html is the starting page, here you can select the painting you want to reproduce(the various paintings are missing)

index.html is the main game here you can create an AI generated image

Final.html will let you see comparison between original & ai generated image

Vote.html will let see other generetad images of the same painting


Views.py: module that manages routes and database

the first time you run the program you will probably need to uncomment the call to the fill() function that happens in @app.route("/") this operation needs to be done only once
