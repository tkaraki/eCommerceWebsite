from app import app, db
from app.models import Item, User, Sellerorder, Buyerorder, Review, Report

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Item': Item, 'User': User, 'Sellerorder': Sellerorder, 'Buyerorder': Buyerorder, 'Review': Review, 'Report': Report}
