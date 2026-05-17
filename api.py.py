from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# N4-N3级别日语单词数据库
JAPANESE_WORDS = {
    "travel": [
        {
            "word": "切符",
            "romaji": "kippu",
            "example": "電車の<span class='highlight'>切符</span>を買いました。",
            "meaning": "车票",
            "translation": "我买了电车票。",
            "level": "N4"
        },
        {
            "word": "案内所",
            "romaji": "annaijo",
            "example": "<span class='highlight'>案内所</span>で地図をもらいます。",
            "meaning": "问讯处，咨询处",
            "translation": "我在问讯处拿了地图。",
            "level": "N3"
        },
        {
            "word": "観光",
            "romaji": "kankou",
            "example": "京都で<span class='highlight'>観光</span>しました。",
            "meaning": "观光，旅游",
            "translation": "我在京都观光了。",
            "level": "N3"
        },
        {
            "word": "宿泊",
            "romaji": "shukuhaku",
            "example": "ホテルに<span class='highlight'>宿泊</span>します。",
            "meaning": "住宿",
            "translation": "我住在酒店。",
            "level": "N3"
        },
        {
            "word": "搭乗手続き",
            "romaji": "toujou tetsuzuki",
            "example": "<span class='highlight'>搭乗手続き</span>を済ませました。",
            "meaning": "登机手续",
            "translation": "我已经办完了登机手续。",
            "level": "N3"
        }
    ],
    "food": [
        {
            "word": "注文",
            "romaji": "chuumon",
            "example": "料理を<span class='highlight'>注文</span>しましょう。",
            "meaning": "点餐，订购",
            "translation": "我们点餐吧。",
            "level": "N4"
        },
        {
            "word": "お勧め",
            "romaji": "osusume",
            "example": "今日の<span class='highlight'>お勧め</span>料理は何ですか？",
            "meaning": "推荐",
            "translation": "今天的推荐菜是什么？",
            "level": "N3"
        },
        {
            "word": "甘い",
            "romaji": "amai",
            "example": "このケーキは<span class='highlight'>甘い</span>です。",
            "meaning": "甜的",
            "translation": "这个蛋糕很甜。",
            "level": "N4"
        },
        {
            "word": "辛い",
            "romaji": "karai",
            "example": "四川料理は<span class='highlight'>辛い</span>です。",
            "meaning": "辣的",
            "translation": "四川菜很辣。",
            "level": "N4"
        },
        {
            "word": "味",
            "romaji": "aji",
            "example": "この料理の<span class='highlight'>味</span>が大好きです。",
            "meaning": "味道",
            "translation": "我非常喜欢这道菜的味道。",
            "level": "N4"
        }
    ],
    "shopping": [
        {
            "word": "割引",
            "romaji": "waribiki",
            "example": "今日は全品20%<span class='highlight'>割引</span>です。",
            "meaning": "折扣",
            "translation": "今天全部商品打8折。",
            "level": "N3"
        },
        {
            "word": "試着",
            "romaji": "shichaku",
            "example": "この服を<span class='highlight'>試着</span>してもいいですか？",
            "meaning": "试穿",
            "translation": "我可以试穿这件衣服吗？",
            "level": "N3"
        },
        {
            "word": "サイズ",
            "romaji": "saizu",
            "example": "M<span class='highlight'>サイズ</span>はありますか？",
            "meaning": "尺寸",
            "translation": "有M尺寸吗？",
            "level": "N4"
        },
        {
            "word": "レシート",
            "romaji": "reshiito",
            "example": "<span class='highlight'>レシート</span>をください。",
            "meaning": "收据",
            "translation": "请给我收据。",
            "level": "N4"
        },
        {
            "word": "値段",
            "romaji": "nedan",
            "example": "このバッグの<span class='highlight'>値段</span>はいくらですか？",
            "meaning": "价格",
            "translation": "这个包的价格是多少？",
            "level": "N4"
        }
    ],
    "daily_life": [
        {
            "word": "掃除",
            "romaji": "souji",
            "example": "部屋の<span class='highlight'>掃除</span>をします。",
            "meaning": "打扫",
            "translation": "我要打扫房间。",
            "level": "N4"
        },
        {
            "word": "洗濯",
            "romaji": "sentaku",
            "example": "<span class='highlight'>洗濯</span>物を干します。",
            "meaning": "洗衣服",
            "translation": "我要晾衣服。",
            "level": "N4"
        },
        {
            "word": "料理",
            "romaji": "ryouri",
            "example": "母が<span class='highlight'>料理</span>を作っています。",
            "meaning": "烹饪，菜肴",
            "translation": "妈妈正在做饭。",
            "level": "N4"
        },
        {
            "word": "約束",
            "romaji": "yakusoku",
            "example": "友達と<span class='highlight'>約束</span>があります。",
            "meaning": "约定，承诺",
            "translation": "我和朋友有约。",
            "level": "N4"
        },
        {
            "word": "準備",
            "romaji": "junbi",
            "example": "試験の<span class='highlight'>準備</span>をしています。",
            "meaning": "准备",
            "translation": "我正在准备考试。",
            "level": "N4"
        }
    ],
    "business": [
        {
            "word": "会議",
            "romaji": "kaigi",
            "example": "午後2時に<span class='highlight'>会議</span>があります。",
            "meaning": "会议",
            "translation": "下午2点有会议。",
            "level": "N4"
        },
        {
            "word": "報告書",
            "romaji": "houkokusho",
            "example": "<span class='highlight'>報告書</span>を提出します。",
            "meaning": "报告书",
            "translation": "我要提交报告书。",
            "level": "N3"
        },
        {
            "word": "残業",
            "romaji": "zangyou",
            "example": "今日は<span class='highlight'>残業</span>しなければなりません。",
            "meaning": "加班",
            "translation": "今天必须加班。",
            "level": "N3"
        },
        {
            "word": "給料",
            "romaji": "kyuuryou",
            "example": "<span class='highlight'>給料</span>日は25日です。",
            "meaning": "工资",
            "translation": "发薪日是25号。",
            "level": "N3"
        },
        {
            "word": "出張",
            "romaji": "shucchou",
            "example": "来週東京に<span class='highlight'>出張</span>します。",
            "meaning": "出差",
            "translation": "下周要去东京出差。",
            "level": "N3"
        }
    ]
}

# DeepSeek API模拟（实际使用时替换为真实API）
def call_deepseek_api(topic):
    """模拟调用DeepSeek API生成单词"""
    # 这里模拟根据主题选择相关单词
    topic_lower = topic.lower()
    
    # 根据关键词匹配主题
    if any(word in topic_lower for word in ['旅行', '旅行', '観光', 'trip', 'travel']):
        category = 'travel'
    elif any(word in topic_lower for word in ['食べ', '料理', '食事', 'food', 'restaurant']):
        category = 'food'
    elif any(word in topic_lower for word in ['買い物', 'ショッピング', 'shopping', '购物']):
        category = 'shopping'
    elif any(word in topic_lower for word in ['仕事', 'ビジネス', 'business', '公司']):
        category = 'business'
    else:
        category = 'daily_life'
    
    # 从对应类别中随机选择3-6个单词
    words = JAPANESE_WORDS.get(category, JAPANESE_WORDS['daily_life'])
    selected_words = random.sample(words, min(len(words), random.randint(3, 6)))
    
    return {
        "topic": topic,
        "category": category,
        "words": selected_words,
        "generated_at": datetime.now().isoformat()
    }

@app.route('/')
def home():
    return jsonify({
        "message": "日语单词Flashcard API",
        "version": "1.0.0",
        "endpoints": {
            "/api/generate": "生成单词卡 (POST)",
            "/api/topics": "获取可用主题 (GET)",
            "/api/words/<category>": "获取特定类别单词 (GET)"
        }
    })

@app.route('/api/generate', methods=['POST'])
def generate_flashcards():
    """生成单词卡API端点"""
    data = request.json
    if not data or 'topic' not in data:
        return jsonify({"error": "请提供主题参数"}), 400
    
    topic = data['topic']
    count = data.get('count', 5)  # 默认生成5个单词
    
    try:
        # 调用模拟的DeepSeek API
        result = call_deepseek_api(topic)
        
        # 限制返回单词数量
        if len(result['words']) > count:
            result['words'] = result['words'][:count]
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """获取可用主题列表"""
    topics = list(JAPANESE_WORDS.keys())
    return jsonify({
        "topics": topics,
        "count": len(topics)
    })

@app.route('/api/words/<category>', methods=['GET'])
def get_words_by_category(category):
    """获取特定类别的单词"""
    if category not in JAPANESE_WORDS:
        return jsonify({"error": "类别不存在"}), 404
    
    words = JAPANESE_WORDS[category]
    count = request.args.get('count', len(words))
    
    try:
        count = int(count)
        if count < 1:
            count = len(words)
    except:
        count = len(words)
    
    # 随机选择指定数量的单词
    selected_words = random.sample(words, min(count, len(words)))
    
    return jsonify({
        "category": category,
        "words": selected_words,
        "total_available": len(words)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

# 为Vercel部署准备
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)