from flask import Flask, render_template
import pandas as pd
import json
from datetime import datetime

app = Flask(__name__)


def load_weibo_data(csv_file='weibo_data.csv'):
    """加载微博数据CSV文件"""
    df = pd.read_csv(csv_file)

    # 转换发布时间为datetime对象
    df['发布时间'] = pd.to_datetime(df['发布时间'])
    df['发布时间_str'] = df['发布时间'].dt.strftime('%Y-%m-%d %H:%M')

    # 按时间排序
    df = df.sort_values('发布时间', ascending=False)

    # 准备可视化数据
    df['hour'] = df['发布时间'].dt.hour
    activity_by_hour = df.groupby('hour').size().reset_index(name='count')

    # 准备互动数据
    interaction_data = df[['发布时间_str', '转发数', '评论数', '点赞数']].to_dict('records')

    stats = {
        'total_posts': len(df),
        'total_reposts': int(df['转发数'].sum()),
        'total_comments': int(df['评论数'].sum()),
        'total_likes': int(df['点赞数'].sum()),
        'most_popular': df.loc[df['点赞数'].idxmax()].to_dict(),
        'activity_by_hour': json.loads(activity_by_hour.to_json(orient='records')),
        'interaction_data': interaction_data
    }

    return df.to_dict('records'), stats


@app.route('/')
def index():
    weibo_data, stats = load_weibo_data()
    return render_template('index.html',
                           weibo_data=weibo_data,
                           stats=stats)


if __name__ == '__main__':
    app.run(debug=True)