# 上映电影插件

## 使用方法：

- 将movie.py放于`homeassistant\components`
- `scheduler.add_job(restart_ha, 'cron', day_of_week='0', hour=2, minute=00)`
在此行更改movie插件显示时间

## 配置内容:

conf下写入此行
```yaml
movie:
```