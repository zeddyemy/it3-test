import sys
from flask import request, jsonify, current_app
from sqlalchemy import desc, func, text
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.task import Task, AdvertTask, EngagementTask, TaskPerformance
from app.utils.helpers.basic_helpers import generate_slug, generate_random_string
from app.utils.helpers.img_helpers import save_image


def get_task_by_ref(task_ref):
    task = EngagementTask.query.filter_by(task_ref=task_ref).first()

    if task is None:
        task = AdvertTask.query.filter_by(task_ref=task_ref).first()

    if task is None:
        task = Task.query.filter_by(task_ref=task_ref).first()
    
    return task


def save_task(data, task_ref=None, task_id=None, payment_status='Pending'):
    try:
        user_id = int(get_jwt_identity())
        task_type = data.get('task_type', '')
        platform = data.get('platform', '')
        fee = data.get('amount', '')
        posts_count = int(data.get('posts_count', ''))
        target_country = data.get('target_country', '')
        target_state = data.get('target_state', '')
        gender = data.get('gender', '')
        caption = data.get('caption', '')
        hashtags = data.get('hashtags', '')
        media =  request.files['media']
        
        goal = data.get('goal','')
        account_link = data.get('account_link', '')
        engagements_count = int(data.get('engagements_count', ''))
        task_ref = task_ref or f"task-{generate_random_string(8)}"
        
        task = None
        if task_id:
            task = Task.query.get(task_id)
        
        if media.filename != '':
            try:
                media_id = save_image(media)
            except Exception as e:
                current_app.logger.error(f"An error occurred while saving image for Task: {str(e)}")
                return None
        elif media.filename == '' and task:
            if task.media_id:
                media_id = task.media_id
            else:
                media_id = None
        else:
            media_id = None
        
        if task_type == 'advert':
            if task:
                task.update(user_id=user_id, type=task_type, platform=platform, fee=fee, media_id=media_id, task_ref=task_ref, payment_status=payment_status, posts_count=posts_count, target_country=target_country, target_state=target_state, gender=gender, caption=caption, hashtags=hashtags)
                
                return task
            else:
                new_task = AdvertTask.create_task(user_id=user_id, type=task_type, platform=platform, fee=fee, media_id=media_id, task_ref=task_ref, payment_status=payment_status, posts_count=posts_count, target_country=target_country, target_state=target_state, gender=gender, caption=caption, hashtags=hashtags)
                
                return new_task
            
        elif task_type == 'engagement':
            if task:
                task.update(user_id=user_id, type=task_type, platform=platform, fee=fee, media_id=media_id, task_ref=task_ref, payment_status=payment_status, goal=goal, account_link=account_link, engagements_count=engagements_count)
                
                return task
            else:
                new_task = EngagementTask.create_task(user_id=user_id, type=task_type, platform=platform, fee=fee, media_id=media_id, task_ref=task_ref, payment_status=payment_status, goal=goal, account_link=account_link, engagements_count=engagements_count)
                
                return new_task
        else:
            return None
    except Exception as e:
        current_app.logger.error(f"An error occurred while saving Task {data.get('task_type')}: {str(e)}")
        db.session.rollback()
        print(f'\n\n{"sys excInfo":-^30}\n', sys.exc_info(), f'\n{"///":-^30}\n\n')
        return None