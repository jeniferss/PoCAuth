from app.db_connector import db, app


from app.modules.my_module.views import my_module_blueprint
app.register_blueprint(my_module_blueprint, url_prefix='/api/v1/mymodule')


db.create_all()
