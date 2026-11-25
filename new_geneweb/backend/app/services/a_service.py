from app.persistence.DBConnector import DBConnector


class AService:
    """
    Service layer responsible for managing genealogical bases.
    Handles logic for creating, listing, and deleting bases.
    """

    session: DBConnector

    def __init__(self, session: DBConnector) -> None:
        self.session = session
