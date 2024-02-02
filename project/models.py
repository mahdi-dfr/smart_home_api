from django.db import models
from django.utils import timezone


# Create your models here.

class Project(models.Model):
    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه ها'

    name = models.CharField(max_length=100, verbose_name='تام پروژه', null=False, blank=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='کاربر', related_name='projects',
                             null=False)
    address = models.TextField(null=True, blank=True, verbose_name='آدرس محل سکونت')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    delete_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')

    def __str__(self):
        return f'{self.name}'


class BoardType(models.Model):
    class Meta:
        verbose_name = 'برد'
        verbose_name_plural = 'برد ها'

    BOARD_NAME = [
        ('0', 'برد پیامکی'),
        ('1', 'برد وای فای'),
        ('2', 'برد سنسور'),
        ('3', 'برد رله'),
        ('4', 'برد دیمر'), ]

    name = models.CharField(max_length=1, default='0', verbose_name='نام برد', null=False,
                            blank=False, choices=BOARD_NAME)
    is_input = models.BooleanField(default=False, verbose_name='', )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    delete_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')
    update_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')

    def __str__(self):
        return f'{self.name}'


class NodeType(models.Model):
    class Meta:
        verbose_name = 'نود'
        verbose_name_plural = 'نود ها'

    NODE_NAME = [
        ('0', 'کلید تک تایمر'),
        ('1', 'سنسور دما'),
        ('2', 'سنسور رطوبت'),
        ('3', 'سنسور گاز'),
        ('4', 'سنسور خاک'),
        ('5', 'دیمر'),
        ('6', 'کلید سه تایمر'),
        ('7', 'چشمی ها و سنسور تشخیص حرکت'),
    ]

    name = models.CharField(max_length=1, verbose_name='نام نود', choices=NODE_NAME, null=False, blank=False)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    is_input = models.BooleanField(default=False, verbose_name='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    delete_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')
    update_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')

    def __str__(self):
        return f'{self.name}'


class ProjectBoards(models.Model):
    class Meta:
        verbose_name = 'برد پروژه'
        verbose_name_plural = 'برد های پروژه'

    name = models.CharField(max_length=100, verbose_name='نام برد', null=False, blank=False)
    board_type = models.ForeignKey(BoardType, on_delete=models.CASCADE, verbose_name='برد مربوطه',
                                   related_name='board', null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='پروژه مربوطه',
                                related_name='projects', null=False)
    control_sms_board = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='برد پیامکی مربوطه',
                                          related_name='sms_board', null=True)
    control_wifi_board = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='برد وای فای مربوطه',
                                           related_name='wifi_board', null=True)
    unique_id = models.SmallIntegerField(verbose_name='شناسه ی برد', blank=True, default=1)
    node = models.ManyToManyField(NodeType, verbose_name='نود های برد', related_name='board_node',
                                  through='project.NodeProject')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    delete_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')
    update_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')

    def __str__(self):
        return f'{self.name}'


class NodeProject(models.Model):
    class Meta:
        verbose_name = 'نود پروژه'
        verbose_name_plural = 'نودهای پروژه'

    node_type = models.ForeignKey(NodeType, on_delete=models.CASCADE, verbose_name='نود ها', related_name='node')
    board_project = models.ForeignKey(ProjectBoards, on_delete=models.CASCADE, verbose_name='بردهای انتخابی',
                                      related_name='board_project')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='پروژه', related_name='project_node')
    unique_id = models.SmallIntegerField(verbose_name='شناسه ی نود', blank=True, default=1)
    is_active = models.BooleanField(default=False, verbose_name='فعال بودن نود')


class Room(models.Model):
    class Meta:
        verbose_name = 'اتاق'
        verbose_name_plural = 'اتاق ها'

    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='نام اتاق')
    project = models.ForeignKey(Project, related_name='project_room', on_delete=models.CASCADE, verbose_name='اتاق',
                                null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    delete_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')
    update_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')

    def __str__(self):
        return f'{self.name}'


class Device(models.Model):
    class Meta:
        verbose_name = 'تجهیز'
        verbose_name_plural = 'تجهیزات'

    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='نام تجهیز')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rooms', verbose_name='اتاق', null=False)
    project = models.ForeignKey(Project, related_name='project_device', on_delete=models.CASCADE,
                                verbose_name='پروژه ی تجهیز',
                                default=0,
                                null=False)
    DEVICE_TYPE = [('0', 'کلید تک تایمر'),
                   ('1', 'سنسور دما'),
                   ('2', 'سنسور رطوبت'),
                   ('3', 'سنسور گاز'),
                   ('4', 'سنسور خاک'),
                   ('5', 'دیمر'),
                   ('6', 'کلید سه تایمر'),
                   ('7', 'چشمی ها و سنسور تشخیص حرکت'), ]
    device_type = models.CharField(max_length=1, choices=DEVICE_TYPE, null=False, verbose_name='نوع تجهیز', default='0')
    node_project = models.ForeignKey(NodeProject, on_delete=models.CASCADE, related_name='node_project',
                                     verbose_name='نود',
                                     null=False, blank=False, default=1)
    event_id = models.IntegerField(verbose_name='رویداد', default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    delete_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')
    update_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')

    def __str__(self):
        return f'{self.name} - {self.room}'


class ProjectScenario(models.Model):
    class Meta:
        verbose_name = 'سناریو'
        verbose_name_plural = 'سناریو ها'

    device = models.ForeignKey(Device, null=False, blank=False, verbose_name='تجهیز', on_delete=models.CASCADE,
                               related_name='device_scenario')
    user = models.ForeignKey('user.User', null=False, blank=False, verbose_name='کاربر', on_delete=models.CASCADE,
                             related_name='user_scenario')
    STATUS = [('0', 'خاموش'), ('1', 'روشن')]
    status = models.CharField(max_length=1, default='0', verbose_name='وضعیت سناریو', choices=STATUS)

    def __str__(self):
        return f'{self.device} - {self.status}'
