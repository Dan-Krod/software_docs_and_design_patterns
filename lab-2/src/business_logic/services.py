from src.domain.models import User, ServerOwner, Server, Role, Member, TextChannel, Message
from src.data_access.interfaces import IMessageRepository, IUserRepository

class DataImportService:
    def __init__(self, message_repo: IMessageRepository, user_repo: IUserRepository, session):
        self.message_repo = message_repo
        self.user_repo = user_repo
        self.session = session

    def import_discord_data(self, file_path: str):
        """
        Orchestrates the data import process from CSV to the SQL Database,
        maintaining all architectural relationships defined in the UML diagram.
        """
        raw_data = self.message_repo.load_from_csv(file_path)
        
        for row in raw_data:
            owner = self.user_repo.get_by_email(row['owner_email'])
            if not owner:
                owner = ServerOwner(
                    name=row['owner_name'],
                    email=row['owner_email'],
                    status="Offline"
                )
                self.session.add(owner)

            server = self.session.query(Server).filter_by(name=row['server_name']).first()
            if not server:
                server = Server(
                    name=row['server_name'], 
                    invite_code=row['invite_code'],
                    member_count=0  
                )
                self.session.add(server)
                self.session.flush() 

            role = self.session.query(Role).filter_by(name=row['role_name'], server_id=server.id).first()
            if not role:
                role = Role(name=row['role_name'], server_id=server.id)
                self.session.add(role)
                self.session.flush()

            member_user = self.user_repo.get_by_email(row['member_email'])
            if not member_user:
                member_user = User(
                    name=row['member_nickname'], 
                    email=row['member_email'], 
                    status="Online"
                )
                self.session.add(member_user)
                self.session.flush()

            member = self.session.query(Member).filter_by(
                user_id=member_user.id, 
                server_id=server.id
            ).first()

            if not member:
                member = Member(
                    user_id=member_user.id,
                    server_id=server.id,
                    nickname=row['member_nickname'],
                    is_muted=False
                )
                if role not in member.roles:
                    member.roles.append(role)
                
                self.session.add(member)
                server.member_count += 1
                self.session.flush()

            channel = self.session.query(TextChannel).filter_by(
                title=row['channel_title'], 
                server_id=server.id
            ).first()

            if not channel:
                channel = TextChannel(
                    title=row['channel_title'],
                    is_locked=row['is_locked'] == 'True',
                    slow_mode_delay=int(row['slow_mode']),
                    server_id=server.id
                )
                self.session.add(channel)
                self.session.flush()

            new_msg = Message(
                content=row['message_content'],
                channel_id=channel.id,
                author_id=member.id,
                metadata_json="{}"
            )
            self.session.add(new_msg)

        self.session.commit()
        print(f"Data import from {file_path} completed successfully.")