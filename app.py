from flask import Flask, request, jsonify
import sqlite3, json
from datetime import datetime

app = Flask(__name__)
DATABASE = 'reviews.db'

# Набор для положительной и отрицательной обратной связи
POSITIVE_KEYWORDS = ['хорошо', 'люблю']
NEGATIVE_KEYWORDS = ['плохо', 'ненавижу']


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def determine_sentiment(text):
    text_lower = text.lower()
    if any(word in text_lower for word in POSITIVE_KEYWORDS):
        return 'positive'
    elif any(word in text_lower for word in NEGATIVE_KEYWORDS):
        return 'negative'
    else:
        return 'neutral'


@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text"'}), 400
    text = json.loads(data)['text']
    sentiment = determine_sentiment(text)
    created_at = datetime.utcnow().isoformat()

    connection = get_db_connection()
    cursor = connection.execute(
        'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
        (text, sentiment, created_at)
    )
    connection.commit()
    review_id = cursor.lastrowid
    connection.close()

    return jsonify({
        'id': review_id,
        'text': text,
        'sentiment': sentiment,
        'created_at': created_at
    })


@app.route('/reviews', methods=['GET'])
def get_reviews():
    sentiment = request.args.get('sentiment')
    conn = get_db_connection()
    if sentiment:
        cursor = conn.execute(
            'SELECT * FROM reviews WHERE sentiment = ?',
            (sentiment,)
        )
    else:
        cursor = conn.execute('SELECT * FROM reviews')
    reviews = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(reviews)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)