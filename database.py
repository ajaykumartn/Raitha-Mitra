import sqlite3
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseManager:
    def __init__(self, db_path='raitha_mitra.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                mobile TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                verified BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                image_path TEXT,
                disease_name TEXT NOT NULL,
                confidence REAL,
                yield_impact TEXT,
                symptoms TEXT,
                organic_treatment TEXT,
                chemical_treatment TEXT,
                prevention_tips TEXT,
                market_prices TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Chat conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT DEFAULT 'New Chat',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Chat messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                response TEXT,
                message_type TEXT DEFAULT 'text',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES chat_conversations (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        
        conn.commit()
        conn.close()
        
        # Create demo user
        self.create_demo_user()
    
    def create_demo_user(self):
        """Create a demo user for testing"""
        try:
            demo_user = {
                'name': 'Demo User',
                'email': 'demo@raithamitra.com',
                'mobile': '9876543210',
                'password': '123456',
                'location': 'Bengaluru, Karnataka'
            }
            self.create_user(**demo_user)
            print("✅ Demo user created: demo@raithamitra.com / 9876543210 / 123456")
        except Exception as e:
            # User might already exist
            pass
    
    def create_user(self, name, email, mobile, password, location):
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = generate_password_hash(password)
        
        cursor.execute('''
            INSERT INTO users (name, email, mobile, password_hash, location, verified)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, mobile, password_hash, location, True))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id
    
    def get_user_by_email_or_mobile(self, email_or_mobile):
        """Get user by email or mobile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE email = ? OR mobile = ?
        ''', (email_or_mobile, email_or_mobile))
        
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    def verify_password(self, user, password):
        """Verify user password"""
        if user['password_hash'].startswith(('pbkdf2:', 'scrypt:', 'argon2:')):
            return check_password_hash(user['password_hash'], password)
        else:
            # Fallback for plain text passwords (demo mode)
            return user['password_hash'] == password
    
    def update_user_password(self, email, new_password_hash):
        """Update user password"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            print(f"🔄 Updating password for email: {email}")
            
            cursor.execute('''
                UPDATE users 
                SET password_hash = ?
                WHERE email = ?
            ''', (new_password_hash, email))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            
            print(f"✅ Password update success: {success}, rows affected: {cursor.rowcount}")
            return success
        except Exception as e:
            print(f"❌ Error updating password: {e}")
            return False
    

    
    def save_prediction(self, user_id, disease_name, confidence, yield_impact, 
                       symptoms, organic_treatment, chemical_treatment, 
                       prevention_tips, market_prices, image_path=None):
        """Save prediction result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (
                user_id, image_path, disease_name, confidence, yield_impact,
                symptoms, organic_treatment, chemical_treatment, 
                prevention_tips, market_prices
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, image_path, disease_name, confidence, yield_impact,
              symptoms, organic_treatment, chemical_treatment, 
              prevention_tips, market_prices))
        
        prediction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return prediction_id
    
    def get_user_predictions(self, user_id, limit=10):
        """Get user's prediction history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM predictions 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        predictions = cursor.fetchall()
        conn.close()
        
        return [dict(pred) for pred in predictions]
    
    def get_all_predictions(self, limit=50):
        """Get all predictions for analytics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, u.name as user_name, u.email as user_email
            FROM predictions p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
            LIMIT ?
        ''', (limit,))
        
        predictions = cursor.fetchall()
        conn.close()
        
        return [dict(pred) for pred in predictions]
    
    def create_chat_conversation(self, user_id, title="New Chat"):
        """Create a new chat conversation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_conversations (user_id, title)
            VALUES (?, ?)
        ''', (user_id, title))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversation_id
    
    def get_user_conversations(self, user_id, limit=20):
        """Get user's chat conversations"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.*, 
                   (SELECT COUNT(*) FROM chat_messages WHERE conversation_id = c.id) as message_count,
                   (SELECT message FROM chat_messages WHERE conversation_id = c.id ORDER BY created_at DESC LIMIT 1) as last_message
            FROM chat_conversations c
            WHERE c.user_id = ?
            ORDER BY c.updated_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        conversations = cursor.fetchall()
        conn.close()
        
        return [dict(conv) for conv in conversations]
    
    def save_chat_message(self, conversation_id, user_id, message, response=None, message_type='text'):
        """Save a chat message and response"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_messages (conversation_id, user_id, message, response, message_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (conversation_id, user_id, message, response, message_type))
        
        message_id = cursor.lastrowid
        
        # Update conversation timestamp
        cursor.execute('''
            UPDATE chat_conversations 
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (conversation_id,))
        
        conn.commit()
        conn.close()
        
        return message_id
    
    def get_conversation_messages(self, conversation_id, limit=50):
        """Get messages from a conversation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM chat_messages
            WHERE conversation_id = ?
            ORDER BY created_at ASC
            LIMIT ?
        ''', (conversation_id, limit))
        
        messages = cursor.fetchall()
        conn.close()
        
        return [dict(msg) for msg in messages]
    
    def update_conversation_title(self, conversation_id, title):
        """Update conversation title"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE chat_conversations 
            SET title = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, conversation_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_conversation(self, conversation_id, user_id):
        """Delete a conversation and its messages"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Delete messages first
        cursor.execute('''
            DELETE FROM chat_messages 
            WHERE conversation_id = ?
        ''', (conversation_id,))
        
        # Delete conversation
        cursor.execute('''
            DELETE FROM chat_conversations 
            WHERE id = ? AND user_id = ?
        ''', (conversation_id, user_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
