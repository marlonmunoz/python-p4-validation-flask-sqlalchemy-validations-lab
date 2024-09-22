from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    # Requires each record to have a name
    @validates('name', 'phone_number')                                    
    def validate_name(self, key, value):                   
        if key == 'name':
            if not value:
                raise ValueError('Name is required')
            if Author.query.filter(Author.name == value).first():
                raise ValueError('Name is already in use')
        elif key == 'phone_number':
            if not value.isdigit() or len(value) != 10:
                raise ValueError('Phone number must be 10 digits long')
        return value

    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title', 'content', 'category', 'summary')
    def validate_title(self, key, value):
        if key == 'title':
            if not value:
                raise ValueError('Title is required')
            clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
            if not any(phrase in value for phrase in clickbait_phrases):
                raise ValueError('Title must contain one of the following phrases: "Won\'t Believe", "Secret", "Top", "Guess"')
    
        elif key == 'content':
            if len(value) < 250:
                raise ValueError('Content must be at least 250 characters long')
        elif key == 'summary':
            if len(value) > 250:
                raise ValueError('Summary must be less than 250 characters long')
        elif key == 'category':
            if value not in ['Fiction', 'Non-Fiction']:
                raise ValueError('Category must be either "Fiction" or "Non-Fiction"')
   
   
        return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
