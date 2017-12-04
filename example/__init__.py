from flask import Blueprint

example = Blueprint(
    'example',
    __name__,
    # 指定模板文件路径
    template_folder='temlates/example',
    # 指定静态文件路径
    static_folder='static/example',
    # 指定URL访问前缀
    url_prefix='/example'
)
