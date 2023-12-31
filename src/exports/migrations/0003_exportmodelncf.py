# Generated by Django 4.2.7 on 2024-01-02 17:23

from django.db import migrations, models
import exports.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('exports', '0002_rename_created_at_export_timestamp_export_latest_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportModelNCF',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(blank=True, null=True, upload_to=exports.models.export_file_handler)),
                ('name', models.CharField(default='model', max_length=100)),
                ('n_epochs', models.IntegerField(default=10)),
                ('batch_size', models.IntegerField(default=200)),
                ('learning_rate', models.FloatField(default=0.005)),
                ('embedding_size', models.IntegerField(default=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
