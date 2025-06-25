import sqlite3
import random
import string
from datetime import datetime, timedelta

db = sqlite3.connect(
    "db.sqlite3", isolation_level=None,
)
cursor = db.cursor()

# ================================================================
# カテゴリー

def insert_categories():
    categories = [
        ('新入社員研修', '新入社員を対象とした基礎的なビジネスマナーや業務研修'),
        ('採用力強化研修', '人事・採用担当者向けのスキルアップ研修'),
        ('内定者研修', '内定者を早期に育成・意識付けするための研修'),
        ('MOST', 'マイナビオリジナルの研修パッケージ（例）'),
        ('e-learning', 'オンラインで受講できる研修教材・プログラム')
    ]

    cursor.execute('DELETE FROM training_categories')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="training_categories"')

    cursor.executemany('''
    INSERT INTO training_categories (name, description)
    VALUES (?, ?)
    ''', categories)

# ================================================================
# programs

def insert_training_programs():
    cursor.execute('DELETE FROM training_programs')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="training_programs"')

    programs = [
        (1, 'ビジネスマナー基礎研修', '名刺交換や敬語など社会人としての基本を学ぶ'),
        (1, '電話応対トレーニング', '顧客との電話対応に自信をつける研修'),
        (1, '新入社員向けタイムマネジメント', '時間管理スキルを高めるための基礎講座'),
        (1, '報告・連絡・相談の基本', 'ホウレンソウを徹底習得する実践型研修'),
        (1, 'チームワーク強化演習', '協働スキルを高めるアクティブラーニング形式'),
        
        (2, '採用面接官トレーニング', '採用面接での評価基準と質問スキルを向上'),
        (2, 'オンライン採用スキル講座', 'リモート採用時代のコミュニケーション術'),
        (2, 'インターン企画実践研修', '魅力的なインターン設計法と運営ノウハウ'),
        (2, '評価シート設計講座', '選考フローで活きる評価指標の構築'),
        (2, 'ダイバーシティ採用研修', '多様な人材の採用と活用に向けた実践学習'),

        (3, '内定者向け社会人準備講座', '内定者に対して基本的なビジネス知識を提供'),
        (3, '内定者マインドセット研修', '入社前の意識と行動変化を促進'),
        (3, 'eラーニングで学ぶ企業文化', '企業理解を深めるオンライン研修'),
        (3, '内定者リーダーシップ体験', 'チーム活動を通じて潜在リーダーを育てる'),
        (3, '内定者フォローオンラインサロン', '継続的な関係性維持を目的とした月次交流'),

        (4, 'MOSTコミュニケーション編', '対話スキル・傾聴力を高める'),
        (4, 'MOSTリーダー育成講座', '新任リーダーに必要なマインドとスキルを習得'),
        (4, 'MOST課題発見ワークショップ', '現場の課題発見力を鍛えるアクティブラーニング'),
        (4, 'MOSTロジカルシンキング研修', '論理的思考力の習得と演習'),
        (4, 'MOST新卒フォローアップ', '入社半年後の振り返りと自己成長計画'),

        (5, '動画で学ぶ営業基礎', 'いつでも見られる営業入門講座'),
        (5, 'Excelデータ分析入門（e-learning）', '基礎から学ぶデータ活用講座'),
        (5, 'ハラスメント防止研修（e-learning）', '社員全体に向けた予防と理解の促進'),
        (5, 'タイムマネジメント実践編（e-learning）', '自己管理力を養うeラーニング教材'),
        (5, '新任管理職向けマネジメント研修', '初めて部下を持つ方向けのeラーニング'),

        (5, 'プロジェクト思考入門', '課題解決のための基本フレームを学ぶ'),
        (5, '自己分析×キャリア設計ワーク', '長期的視点でキャリアを考えるeラーニング'),
        (2, 'Z世代向け採用戦略セミナー', '若年層の志向を踏まえた採用手法の構築'),
        (3, '内定者チームビルディング研修', '仲間意識を育むワークショップ'),
        (1, '新人営業職向けOJTサポート研修', '現場に入る前のOJT準備研修')
    ]
    cursor.executemany('''
    INSERT INTO training_programs (category_id, name, description)
    VALUES (?, ?, ?)
    ''', programs)

# ================================================================
# ユーザー
def generate_username():
    return 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def generate_email():
    user = ''.join(random.choices(string.ascii_lowercase, k=5))
    domain = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f'{user}@{domain}.jp'

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=12))

# 初期データ生成
def insert_users():
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="users"')
    users = []
    for _ in range(200):
        username = generate_username()
        email = generate_email()
        password = generate_password()
        industory_id = random.randint(1, 18)
        users.append((username, email, industory_id, password))

    cursor.executemany('''
    INSERT INTO users (username, email, industory_id, password)
    VALUES (?, ?, ?, ?)
    ''', users)

# ================================================================
# レビュー

# ランダム評価を生成
def random_rating():
    return random.randint(1, 5)

# 任意の過去日を生成
def random_timestamp():
    days_ago = random.randint(0, 365)
    dt = datetime.now() - timedelta(days=days_ago)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# レビュー200件を生成（training_program_id: 1–30, user_account_id: 1–30）
def insert_reviews():
    cursor.execute('DELETE FROM reviews')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="reviews"')
    reviews = []
    for i in range(200):
        review = (
            random.randint(1, 30),  # training_program_id
            random.randint(1, 80),  # user_account_id

            random_rating(),  # overall_rating
            random_rating(),  # contents_rating
            random_rating(),  # lecturer_rating
            random_rating(),  # cost_performance_rating
            random_rating(),  # practicality_rating
            random_rating(),  # ease_of_understanding_rating

            '満足できた',         # comment_summary
            '良かった',           # pros
            '悪かった',           # cons

            random_timestamp(),     # created_at
            random.choice([True, False])  # is_visible
        )
        reviews.append(review)

    cursor.executemany('''
    INSERT INTO reviews (
        training_program_id, user_account_id,
        overall_rating, contents_rating, lecturer_rating,
        cost_performance_rating, practicality_rating, ease_of_understanding_rating,
        comment_summary, pros, cons,
        created_at, is_visible
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', reviews)

def insert_industories():
    industries = [
        '農業，林業',
        '漁業',
        '鉱業，採石業，砂利採取業',
        '建設業',
        '製造業',
        '電気・ガス・熱供給・水道業',
        '情報通信業',
        '運輸業，郵便業',
        '卸売業，小売業',
        '金融業，保険業',
        '不動産業，物品賃貸業',
        '学術研究，専門・技術サービス業',
        '宿泊業，飲食サービス業',
        '生活関連サービス業，娯楽業',
        '教育，学習支援業',
        '医療，福祉',
        '複合サービス事業',
        'サービス業（他に分類されないもの）'
    ]

    # 既存データ削除（必要に応じて）
    cursor.execute('DELETE FROM industories')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="industories"')  # IDリセット

    # 挿入
    cursor.executemany(
        'INSERT INTO industories (name) VALUES (?)',
        [(name,) for name in industries]
    )

insert_reviews()
insert_users()
# insert_industories()

db.commit()
db.close()