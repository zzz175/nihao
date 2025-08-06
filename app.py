from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 配置静态文件
app.static_folder = 'static'
app.static_url_path = '/static'


@app.route('/')
def index():
    """主页路由"""
    return render_template('daohang.html')


@app.route('/api/time')
def get_time():
    """获取当前时间的API"""
    now = datetime.now()
    return jsonify({
        'time': now.strftime('%H:%M:%S'),
        'date': now.strftime('%Y年%m月%d日'),
        'weekday': now.strftime('%A'),
        'timestamp': now.timestamp()
    })


@app.route('/api/search')
def search():
    """搜索重定向API"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': '搜索关键词不能为空'}), 400
    
    # 判断是否为网址
    if query.startswith(('http://', 'https://')):
        return redirect(query)
    elif '.' in query and ' ' not in query:
        return redirect(f'http://{query}')
    else:
        # 使用百度搜索
        return redirect(f'https://www.baidu.com/s?wd={query}')


@app.route('/api/bookmarks')
def get_bookmarks():
    """获取书签列表"""
    bookmarks = [
        {'name': '百度', 'url': 'https://www.baidu.com', 'icon': '🔍'},
        {'name': 'DeepSeek', 'url': 'https://www.deepseek.com', 'icon': '🤖'},
        {'name': '哔哩哔哩', 'url': 'https://www.bilibili.com', 'icon': '📺'},
        {'name': '网易云音乐', 'url': 'https://music.163.com', 'icon': '🎵'}
    ]
    return jsonify(bookmarks)


@app.route('/api/bookmarks', methods=['POST'])
def add_bookmark():
    """添加书签"""
    data = request.get_json()
    if not data or 'name' not in data or 'url' not in data:
        return jsonify({'error': '缺少必要参数'}), 400
    
    # 这里可以添加保存到数据库的逻辑
    return jsonify({'message': '书签添加成功', 'bookmark': data})


@app.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({'error': '服务器内部错误'}), 500


@app.before_request
def before_request():
    """请求前处理"""
    # 记录请求日志
    print(f'[{datetime.now()}] {request.method} {request.url}')


@app.after_request
def after_request(response):
    """请求后处理"""
    # 添加CORS头
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


if __name__ == '__main__':
    # 确保模板和静态文件目录存在
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print('启动导航页面服务...')
    print('访问地址: http://127.0.0.1:5000')
    print('API文档:')
    print('  GET  /api/time      - 获取当前时间')
    print('  GET  /api/search    - 搜索重定向')
    print('  GET  /api/bookmarks - 获取书签列表')
    print('  POST /api/bookmarks - 添加书签')
    print('  GET  /health        - 健康检查')
    
    app.run(debug=True, host='127.0.0.1', port=5000)
