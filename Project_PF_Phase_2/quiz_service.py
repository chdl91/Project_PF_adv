import os
from typing import List, Optional
from sqlmodel import SQLModel, create_engine, Session, select
from DB_classes import Topic, Question, Answer, User

# Set up database connection (works even if Folder is moved, as it uses relative path)
script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(script_dir, "DB", "quiz.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}")

def get_all_topics() -> List[str]:
    """
    Retrieves all topic names from the database.
    
    Returns:
        List[str]: A list of topic names.
        
    Raises:
        Exception: If there is an error during database access.
    """
    try:
        with Session(ENGINE) as session:
            statement = select(Topic)
            results = session.exec(statement).all()
            return [topic.topic_name for topic in results]
    except Exception as e:
        raise Exception(f"Error occurred while fetching topics: {e}")
    
   
# Test the function
if __name__ == "__main__":
    print("Starting test...")
    try:
        topics = get_all_topics()
        print(f"Topics found: {topics}")
        print(f"Number of topics: {len(topics)}")
    except Exception as e:
        print(f"Error: {e}")