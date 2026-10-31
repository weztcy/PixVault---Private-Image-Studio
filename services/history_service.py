from history.manager import HistoryManager


class HistoryService:
    def __init__(self):

        self.manager = HistoryManager()

    def get_history(self):

        return self.manager.get_all()

    def delete_history(self, record_id):

        return self.manager.delete(record_id)

    def clear_history(self):

        return self.manager.clear()
