from flask import Flask, render_template, request, redirect, url_for, flash
import os
from src.business_logic.services import DataImportService
from src.domain.models import TextChannel, Message 

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')
static_dir = os.path.join(current_dir, 'static') 

app = Flask(__name__, 
            template_folder=template_dir, 
            static_folder=static_dir)

app.secret_key = 'super_secret_discord_clone_key_2026'

service: DataImportService = None

@app.route('/')
def index():
    servers = service.get_all_servers()
    return render_template('index.html', servers=servers)

@app.route('/server/add', methods=['GET', 'POST'])
def add_server():
    if request.method == 'POST':
        name = request.form.get('name')
        invite_code = request.form.get('invite_code')
        try:
            service.add_server(name, invite_code)
            flash("Сервер успішно створено!", "success") 
            return redirect(url_for('index'))
        except ValueError as e:
            flash(str(e), "danger") 
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/server/edit/<int:server_id>', methods=['GET', 'POST'])
def edit_server(server_id):
    server = service.get_server_by_id(server_id)
    if request.method == 'POST':
        name = request.form.get('name')
        invite_code = request.form.get('invite_code')
        member_count = int(request.form.get('member_count', 0))
        service.update_server(server_id, name, invite_code, member_count)
        return redirect(url_for('index'))
    return render_template('edit.html', server=server)

@app.route('/server/delete/<int:server_id>')
def delete_server(server_id):
    service.delete_server(server_id)
    return redirect(url_for('index'))

@app.route('/server/<int:server_id>/channels')
def view_channels(server_id):
    """Перегляд усіх каналів конкретного сервера"""
    server = service.get_server_by_id(server_id)
    channels = service.get_server_channels(server_id)
    return render_template('channels.html', server=server, channels=channels)

@app.route('/server/<int:server_id>/channel/add', methods=['POST'])
def add_channel(server_id):
    title = request.form.get('title')
    slow_mode = request.form.get('slow_mode', 0) 
    
    if not title:
        flash("Назва каналу не може бути порожньою!", "danger")
        return redirect(url_for('view_channels', server_id=server_id))
        
    try:
        service.add_channel_to_server(server_id, title, int(slow_mode))
        flash(f"Канал #{title} створено!", "success")
    except ValueError as e:
        flash(str(e), "danger")
    except Exception:
        flash("Сталася непередбачувана помилка при створенні каналу.", "danger")
        
    return redirect(url_for('view_channels', server_id=server_id))

@app.route('/channel/delete/<int:channel_id>')
def delete_channel(channel_id):
    channel = service.session.query(TextChannel).get(channel_id)
    sid = channel.server_id
    service.delete_channel(channel_id)
    return redirect(url_for('view_channels', server_id=sid))

@app.route('/channel/<int:channel_id>/messages', methods=['GET', 'POST'])
def view_messages(channel_id):
    """Стрічка повідомлень каналу (Chat View)"""
    channel = service.session.query(TextChannel).get(channel_id)
    
    if request.method == 'POST':
        content = request.form.get('content')
        author_id = request.form.get('author_id')
        if author_id and content:
            service.post_message(channel_id, int(author_id), content)
        return redirect(url_for('view_messages', channel_id=channel_id))
    
    messages = service.get_channel_messages(channel_id)
    return render_template('messages.html', channel=channel, messages=messages)

@app.route('/message/delete/<int:message_id>')
def delete_message(message_id):
    msg = service.session.query(Message).get(message_id)
    cid = msg.channel_id
    service.delete_message(message_id)
    return redirect(url_for('view_messages', channel_id=cid))

@app.route('/server/<int:server_id>/members')
def view_members(server_id):
    """Сторінка керування учасниками сервера"""
    server = service.get_server_by_id(server_id)
    if not server:
        flash("Сервер не знайдено!", "danger")
        return redirect(url_for('index'))
    
    members = service.get_server_members(server_id)
    return render_template('members.html', server=server, members=members)

@app.route('/member/delete/<int:member_id>')
def delete_member(member_id):
    """Видалення учасника (Kick)"""
    member = service.get_member_by_id(member_id)
    if not member:
        flash("Учасника не знайдено!", "danger")
        return redirect(url_for('index'))
        
    server_id = member.server_id
    service.delete_member(member_id)
    flash(f"Учасника {member.nickname} успішно вилучено.", "warning")
    return redirect(url_for('view_members', server_id=server_id))

@app.route('/member/edit/<int:member_id>', methods=['POST'])
def edit_member(member_id):
    """Оновлення нікнейму учасника"""
    member = service.get_member_by_id(member_id)
    if not member:
        flash("Учасника не знайдено!", "danger")
        return redirect(url_for('index'))
    
    new_nickname = request.form.get('nickname')
    if new_nickname:
        service.update_member_nickname(member_id, new_nickname)
        flash(f"Нікнейм для {member.user.email} змінено на {new_nickname}!", "success")
    else:
        flash("Нікнейм не може бути порожнім!", "warning")
        
    return redirect(url_for('view_members', server_id=member.server_id))

@app.route('/server/<int:server_id>/member/add', methods=['POST'])
def add_member(server_id):
    """Обробка форми додавання нового учасника"""
    email = request.form.get('email')
    nickname = request.form.get('nickname')
    name = request.form.get('name', nickname) 
    
    if not email or not nickname:
        flash("Пошта та нікнейм обов'язкові!", "danger")
        return redirect(url_for('view_members', server_id=server_id))
        
    try:
        service.add_member_to_server(server_id, email, nickname, name)
        flash(f"Учасника {nickname} успішно додано на сервер!", "success")
    except ValueError as e:
        flash(str(e), "danger")
    except Exception:
        flash("Помилка при додаванні учасника.", "danger")
        
    return redirect(url_for('view_members', server_id=server_id))