from DAL.Repositories.GroupRepository import GroupRepository
from DAL.Repositories.UserRepository import UserRepository
from DAL.Repositories.LinkRepository import LinkRepository


class UnitOfWork:

    def __init__(self, db_session):
        self.session = db_session
