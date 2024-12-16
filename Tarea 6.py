from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId  # Import para manejar ObjectId de MongoDB

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Puerto corregido a 27017
db = client['Tarea5']
recipes_collection = db['recetas']

# Ruta para la página principal
@app.route('/')
def index():
    # Obtener todas las recetas
    recipes = list(recipes_collection.find())
    return render_template('index.html', recipes=recipes)

# Ruta para agregar una nueva receta
@app.route('/create', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        steps = request.form['steps']

        # Guardar la receta en MongoDB
        recipe = {
            'name': name,
            'ingredients': ingredients,
            'steps': steps
        }
        recipes_collection.insert_one(recipe)

        return redirect(url_for('index'))

    return render_template('create.html')

# Ruta para actualizar una receta
@app.route('/update/<string:recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    if request.method == 'POST':
        updated_name = request.form['name']
        updated_ingredients = request.form['ingredients']
        updated_steps = request.form['steps']

        # Actualizar la receta en MongoDB
        recipes_collection.update_one(
            {'_id': ObjectId(recipe_id)},
            {'$set': {
                'name': updated_name,
                'ingredients': updated_ingredients,
                'steps': updated_steps
            }}
        )

        return redirect(url_for('index'))

    # Obtener los datos de la receta a actualizar
    recipe = recipes_collection.find_one({'_id': ObjectId(recipe_id)})

    return render_template('update.html', recipe=recipe)

# Ruta para eliminar una receta
@app.route('/delete/<string:recipe_id>')
def delete_recipe(recipe_id):
    # Eliminar la receta de MongoDB
    recipes_collection.delete_one({'_id': ObjectId(recipe_id)})

    return redirect(url_for('index'))

# Ruta para buscar recetas
@app.route('/search', methods=['GET', 'POST'])
def search_recipes():
    if request.method == 'POST':
        search_term = request.form['search_term']

        # Buscar recetas en MongoDB
        found_recipes = list(recipes_collection.find({'name': {'$regex': search_term, '$options': 'i'}}))

        return render_template('search.html', recipes=found_recipes)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
