from app.extensions import db
from sqlalchemy.orm import backref
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models import Media
from app.utils.helpers.basic_helpers import generate_random_string

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False) # advert task, or engagement task
    platform = db.Column(db.String(80), nullable=False)
    fee = db.Column(db.Float, nullable=False)
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    task_key = db.Column(db.String(120), unique=True, nullable=False)
    payment_status = db.Column(db.String(80), nullable=False) # complete, pending, failed
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trendit3_user_id = db.Column(db.Integer, db.ForeignKey('trendit3_user.id'), nullable=False)
    trendit3_user = db.relationship('Trendit3User', backref=db.backref('tasks', lazy='dynamic'))
    
    @classmethod
    def create_task(cls, trendit3_user_id, type, platform, fee, payment_status, media_id=None, **kwargs):
        the_task_ref = generate_random_string(8)
        counter = 1
        max_attempts = 6  # maximum number of attempts to create a unique task_key
        
        while cls.query.filter_by(task_key=the_task_ref).first() is not None:
            if counter > max_attempts:
                raise ValueError(f"Unable to create a unique task after {max_attempts} attempts.")
            the_task_ref = f"{generate_random_string(8)}-{generate_random_string(2)}-{counter}"
            counter += 1
        
        task = cls(trendit3_user_id=trendit3_user_id, type=type, platform=platform, fee=fee, task_key=the_task_ref, payment_status=payment_status, media_id=media_id, **kwargs)
        
        # Set additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(task, key, value)
        
        db.session.add(task)
        db.session.commit()
        
        return task
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_task_media(self):
        if self.media_id:
            theMedia = Media.query.get(self.media_id)
            if theMedia:
                return theMedia.get_path()
            else:
                return None
        else:
            return None
    
    def to_dict(self):
        advert_task_dict = {}
        advert_task = AdvertTask.query.get(self.id)
        if advert_task:
            advert_task_dict.update({
                'posts_count': advert_task.posts_count,
                'target_country': advert_task.target_country,
                'target_state': advert_task.target_state,
                'gender': advert_task.gender,
                'caption': advert_task.caption,
                'hashtags': advert_task.hashtags,
            })
        
        engagement_task_dict = {}
        engagement_task = EngagementTask.query.get(self.id)
        if engagement_task:
            engagement_task_dict.update({
                'goal': engagement_task.goal,
                'account_link': engagement_task.account_link,
                'engagements_count': engagement_task.engagements_count,
            })
            
        return {
            'id': self.id,
            'type': self.type,
            'platform': self.platform,
            'media_path': self.get_task_media(),
            'task_key': self.task_key,
            'payment_status': self.payment_status,
            'creator': {
                'id': self.trendit3_user_id,
                'username': self.trendit3_user.username,
                'email': self.trendit3_user.email
            },
            **advert_task_dict,
            **engagement_task_dict 
        }


class AdvertTask(Task):
    id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    posts_count = db.Column(db.Integer, nullable=False)
    target_country = db.Column(db.String(120), nullable=False)
    target_state = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    hashtags = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<ID: {self.id}, User ID: {self.trendit3_user_id}, Platform: {self.platform}, Posts Count: {self.posts_count}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'platform': self.platform,
            'media_path': self.get_task_media(),
            'task_key': self.task_key,
            'payment_status': self.payment_status,
            'posts_count': self.posts_count,
            'target_country': self.target_country,
            'target_state': self.target_state,
            'gender': self.gender,
            'caption': self.caption,
            'hashtags': self.hashtags,
            'creator': {
                'id': self.trendit3_user_id,
                'username': self.trendit3_user.username,
                'email': self.trendit3_user.email
            }
        }


class EngagementTask(Task):
    id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    goal = db.Column(db.String(80), nullable=False)
    account_link = db.Column(db.String(120), nullable=False)
    engagements_count = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<ID: {self.id}, User ID: {self.trendit3_user_id}, Goal: {self.goal}, Platform: {self.platform}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'platform': self.platform,
            'media_path': self.get_task_media(),
            'task_key': self.task_key,
            'payment_status': self.payment_status,
            'goal': self.goal,
            'account_link': self.account_link,
            'engagements_count': self.engagements_count,
            'creator': {
                'id': self.trendit3_user_id,
                'username': self.trendit3_user.username,
                'email': self.trendit3_user.email
            }
        }


class TaskPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), unique=True, nullable=False, default=generate_random_string(8))
    task_id = db.Column(db.Integer, nullable=False)  # either an AdvertTask id or an EngagementTask id
    task_type = db.Column(db.String(80), nullable=False)  # either 'advert' or 'engagement'
    reward_money = db.Column(db.Float(), default=00.00, nullable=False)
    proof_screenshot_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
    status = db.Column(db.String(80), default='Pending')
    date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('trendit3_user.id'), nullable=False)
    trendit3_user = db.relationship('Trendit3User', backref=db.backref('performed_tasks', lazy='dynamic'))
    
    def __repr__(self):
        return f'<ID: {self.id}, User ID: {self.user_id}, Task ID: {self.task_id}, Task Type: {self.task_type}, Status: {self.status}>'
    
    @classmethod
    def create_task_performance(cls, user_id, task_id, task_type, reward_money, proof_screenshot_id, status):
        task = cls(user_id=user_id, task_id=task_id, task_type=task_type, reward_money=reward_money, proof_screenshot_id=proof_screenshot_id, status=status)
        
        db.session.add(task)
        db.session.commit()
        
        return task
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    def get_proof_screenshot(self):
        if self.proof_screenshot_id:
            theImage = Media.query.get(self.proof_screenshot_id)
            if theImage:
                return theImage.get_path()
            else:
                return None
        else:
            return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'task_id': self.task_id,
            'task_type': self.task_type,
            'reward_money': self.reward_money,
            'proof_screenshot_path': self.get_proof_screenshot(),
            'status': self.status,
            'date_completed': self.date_completed,
            'user': {
                'id': self.user_id,
                'username': self.trendit3_user.username,
                'email': self.trendit3_user.email
            },
        }
