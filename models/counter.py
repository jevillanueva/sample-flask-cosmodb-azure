from utils.database import db
def addVisitorRoot():
    db.counter.update({"visitor":"root"}, { "$inc": { "value": 1 } } , upsert=True)

def viewVisitorRoot():
    views = db.counter.find_one({"visitor":"root"})
    return views["value"]

    
