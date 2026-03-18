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
        
    def get_all_servers(self):
        return self.session.query(Server).all()

    def get_server_by_id(self, server_id: int):
        return self.session.query(Server).get(server_id)

    def add_server(self, name: str, invite_code: str):
        existing = self.session.query(Server).filter_by(invite_code=invite_code).first()
        if existing:
            raise ValueError(f"Код {invite_code} вже зайнятий!")

        try:
            new_server = Server(
                name=name, 
                invite_code=invite_code, 
                member_count=0
            )
            self.session.add(new_server)
            self.session.commit()
            return new_server
        except Exception as e:
            self.session.rollback()
            raise e

    def update_server(self, server_id: int, name: str, invite_code: str, member_count: int):
        server = self.get_server_by_id(server_id)
        if server:
            server.name = name
            server.invite_code = invite_code
            server.member_count = member_count
            self.session.commit()
        return server

    def delete_server(self, server_id: int):
        server = self.get_server_by_id(server_id)
        if server:
            self.session.delete(server)
            self.session.commit()
            return True
        return False
    
    def get_server_channels(self, server_id: int):
        return self.session.query(TextChannel).filter_by(server_id=server_id).all()

    def add_channel_to_server(self, server_id: int, title: str, slow_mode: int = 0):
        existing = self.session.query(TextChannel).filter_by(
            server_id=server_id, 
            title=title
        ).first()
        
        if existing:
            raise ValueError(f"Канал з назвою '#{title}' вже існує на цьому сервері!")

        try:
            new_channel = TextChannel(
                server_id=server_id, 
                title=title, 
                slow_mode_delay=slow_mode,
                is_locked=False
            )
            self.session.add(new_channel)
            self.session.commit()
            return new_channel
        except Exception as e:
            self.session.rollback() 
            raise e

    def delete_channel(self, channel_id: int):
        channel = self.session.query(TextChannel).get(channel_id)
        if channel:
            self.session.delete(channel)
            self.session.commit()
            return True
        return False

    def get_channel_messages(self, channel_id: int):
        return self.session.query(Message).filter_by(channel_id=channel_id).order_by(Message.timestamp.asc()).all()

    def post_message(self, channel_id: int, author_id: int, content: str):
        if not content.strip(): return None 
        
        new_msg = Message(
            channel_id=channel_id,
            author_id=author_id,
            content=content,
            metadata_json="{}"
        )
        self.session.add(new_msg)
        self.session.commit()
        return new_msg

    def delete_message(self, message_id: int):
        msg = self.session.query(Message).get(message_id)
        if msg:
            self.session.delete(msg)
            self.session.commit()
            return True
        return False
    
    def get_server_members(self, server_id: int):
        return self.session.query(Member).filter_by(server_id=server_id).all()

    def get_member_by_id(self, member_id: int):
        return self.session.query(Member).get(member_id)

    def delete_member(self, member_id: int):
        member = self.get_member_by_id(member_id)
        if member:
            server = member.server
            self.session.delete(member)
            if server.member_count > 0:
                server.member_count -= 1
            self.session.commit()
            return True
        return False

    def update_member_nickname(self, member_id: int, new_nickname: str):
        member = self.get_member_by_id(member_id)
        if member:
            member.nickname = new_nickname
            self.session.commit()
            return member
        return None