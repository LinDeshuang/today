from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Todo(models.Model):
    """
    待办事项
    """
    title = models.CharField(max_length=30, null=False, blank=False, verbose_name="标题")
    content = models.TextField(max_length=500, null=False, blank=False, verbose_name="内容")
    level = models.IntegerField(default=5,
                                choices=(
                                    (1, "重要，紧急"),
                                    (2, "重要，不紧急"),
                                    (3, "不重要，紧急"),
                                    (4, "不重要，不紧急"),
                                    (5, "随便")))
    finish_level = models.IntegerField(default=0,
                                       choices=(
                                           (0, "未完成"),
                                           (1, "完美"),
                                           (2, "优秀"),
                                           (3, "良好"),
                                           (4, "及格"),
                                           (5, "不理想")))
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    file = models.FileField(upload_to="todo/images/", null=True, blank=True, verbose_name="上传的文件", help_text="上传的文件")
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.DO_NOTHING)


    class Meta:
        verbose_name = "代办事项"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
