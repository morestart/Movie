# 上映电影插件

## 使用方法：

- 将movie.py放于`C:\Users\55334\AppData\Local\Continuum\anaconda3\Lib\site-packages\homeassistant\components`
linux同理，将文件置于HA的components下
- `scheduler.add_job(restart_ha, 'cron', day_of_week='0', hour=2, minute=00)`
在此行更改movie插件显示时间

## 配置内容:

conf下写入此行
```yaml
movie:
```