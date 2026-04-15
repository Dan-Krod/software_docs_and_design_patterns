from abc import ABC, abstractmethod

class IUserView(ABC):
    """Interface for displaying user data and profile interaction"""
    
    @abstractmethod
    def display_user_profile(self, user_id: int) -> None:
        """Display user profile (name, status, email) based on User class attributes"""
        pass

    @abstractmethod
    def show_system_message(self, message: str) -> None:
        """Output system notification or error message"""
        pass


class IChatView(ABC):
    """Interface for rendering servers, channels, and messages hierarchy"""

    @abstractmethod
    def render_server_list(self, servers: list) -> None:
        """Display list of available Servers as per Server Infrastructure package"""
        pass

    @abstractmethod
    def render_channel_history(self, channel_id: int, messages: list) -> None:
        """Display message history for a specific TextChannel"""
        pass


class IDataImportView(ABC):
    """Interface for monitoring the data migration process (CSV to DB)"""

    @abstractmethod
    def show_import_status(self, current: int, total: int) -> None:
        """Show import progress for the required 1000+ rows"""
        pass

    @abstractmethod
    def on_import_complete(self, success_count: int) -> None:
        """Notify when the import process is finished"""
        pass