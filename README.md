# Get Started
Create environment and install dependencies
```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
``` 
Configure MONGO_DB:
```
docker_compose up
export MONGODB_URL="mongodb://[user]:[password]@localhost:27017/?retryWrites=true&w=majority"
```

Populate DB:
```
mongosh
use RECIPES
db.RECIPES.insert( [ { _id: '63fdc21d62ea66fcaf6a35db', label: 'Chicken Vesuvio', source: 'Serious Eats', url: 'http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html' }, { _id: '63fdc26962ea66fcaf6a35df', label: 'Cauliflower and Tofu Curry Recipe', source: 'Serious Eats', url: 'http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html' }, { _id: '63fdc24062ea66fcaf6a35dd', label: 'Chicken Paprikash', source: 'No Recipes', url: 'http://norecipes.com/recipe/chicken-paprikash/' } ] )
exit
```
Run the server:
```
uvicorn app.main:app --reload
```
