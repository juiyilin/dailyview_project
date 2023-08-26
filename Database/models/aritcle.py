from django.db import models


def get_upload_path(instance, filename):
    """
    Profile name 為資料夾名字放入圖片。
    :param instance: Django models 物件。
    :param filename: Django models 物件。
    :return: str ->　檔案路徑。
    """
    return f'register/{instance.owner.id_card}/{filename}'


class CategoryTag(models.Model):
    tag = models.CharField(max_length=16)

    class Meta:
        db_table = 'CategoryTag'


class Article(models.Model):
    class Meta:
        db_table = 'Article'


class UserRegister(models.Model):
    owner = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)

    class Meta:
        """
        改資料庫名字。
        """
        db_table = 'UserRegister'

    def to_dict(self):
        """
        給計算歐式距離用的。
        會透過 read_image_and_register 傳送到 BackgroundProgram.py
        """
        return {'id': self.id, 'name': self.owner.name, 'feature': self.feature,
                'project_name': self.owner.project_name, 'identify_number': self.owner.identify_number,
                'date_of_issue': self.owner.date_of_issue, 'id_card': self.owner.id_card}
