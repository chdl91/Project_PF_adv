from typing import List, Optional
from data_access.subject_dao import SubjectDAO


class SubjectService:
    """Business logic for subjects and topics."""

    def __init__(self, subject_dao: SubjectDAO):
        self.subject_dao = subject_dao

    def get_all_subjects(self) -> List[str]:
        return [s.subject_name for s in self.subject_dao.get_all()]

    def get_subject_id_by_name(self, name: str) -> Optional[int]:
        subject = self.subject_dao.get_by_name(name)
        return subject.subject_id if subject else None

    def get_topics_by_subject(self, subject_name: str) -> List[str]:
        subject = self.subject_dao.get_by_name(subject_name)
        if not subject:
            raise Exception(f"Subject '{subject_name}' not found.")
        return [t.topic_name for t in self.subject_dao.get_topics(subject.subject_id)]

    def get_topics_with_ids_by_subject(self, subject_name: str) -> List[dict]:
        subject = self.subject_dao.get_by_name(subject_name)
        if not subject:
            raise Exception(f"Subject '{subject_name}' not found.")
        topics = self.subject_dao.get_topics(subject.subject_id)
        return [{"topic_id": t.topic_id, "topic_name": t.topic_name} for t in topics]

    def add_subject(self, name: str) -> bool:
        result = self.subject_dao.add_subject(name)
        if result is None:
            print(f" Subject '{name}' already exists.")
            return False
        print(f" Subject '{name}' added (ID: {result.subject_id})")
        return True

    def add_topic(self, topic_name: str, subject_id: int) -> bool:
        result = self.subject_dao.add_topic(topic_name, subject_id)
        if result is None:
            print(f" Topic '{topic_name}' already exists.")
            return False
        print(f" Topic '{topic_name}' added (ID: {result.topic_id})")
        return True

    def delete_topic(self, topic_id: int) -> bool:
        return self.subject_dao.delete_topic(topic_id)

    def delete_subject(self, subject_id: int) -> bool:
        return self.subject_dao.delete_subject(subject_id)
